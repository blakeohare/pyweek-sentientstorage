using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Python2Crayon.ParseTree;

namespace Python2Crayon.Serialization
{
	internal abstract class Serializer
	{
		public abstract void SerializeExpression(List<string> output, Expression expression);
	}

	internal class CrayonSerializer : Serializer
	{
		private readonly CrayonPrimitiveMethods PRIMITIVE_METHODS;
		public CrayonSerializer()
		{
			this.PRIMITIVE_METHODS = new CrayonPrimitiveMethods(this);
		}

		public string Serialize(IList<Executable> code)
		{
			List<string> output = new List<string>();
			
			foreach (Executable line in code)
			{
				this.Serialize(output, line, "");
			}

			return string.Join("", output);
		}

		public void Serialize(List<string> output, Executable exec, string indention)
		{
			if (exec == null) throw new NullReferenceException();

			if (exec is Assignment) SerializeAssignment(output, (Assignment)exec, indention);
			else if (exec is ExpressionAsExecutable) SerializeExpressionAsExecutable(output, (ExpressionAsExecutable)exec, indention);
			else if (exec is ForEachLoop) SerializeForEachLoop(output, (ForEachLoop)exec, indention);
			else if (exec is ForLoop) SerializeForLoop(output, (ForLoop)exec, indention);
			else if (exec is IfStatement) SerializeIfStatement(output, (IfStatement)exec, indention, true);
			else if (exec is ClassDefinition) SerializeClassDefinition(output, (ClassDefinition)exec, indention);
			else if (exec is BreakStatement) SerializeBreakStatement(output, (BreakStatement)exec, indention);
			else if (exec is FunctionDefinition) SerializeFunctionDefinition(output, (FunctionDefinition)exec, indention);
			else if (exec is ReturnStatement) SerializeReturnStatement(output, (ReturnStatement)exec, indention);
			else if (exec is WhileLoop) SerializeWhileLoop(output, (WhileLoop)exec, indention);
			else throw new NotImplementedException(exec.GetType().ToString());
		}

		private void SerializeWhileLoop(List<string> output, WhileLoop whileLoop, string indention)
		{
			output.Add(indention);
			output.Add("while (");
			SerializeExpression(output, whileLoop.Condition);
			output.Add(") {\n");
			SerializeBlock(output, whileLoop.Body, indention + "\t");
			output.Add(indention);
			output.Add("}\n");
		}

		private void SerializeReturnStatement(List<string> output, ReturnStatement returnStatement, string indention)
		{
			output.Add(indention);
			output.Add("return");
			if (returnStatement.Value != null)
			{
				output.Add(" ");
				SerializeExpression(output, returnStatement.Value);
			}
			output.Add(";\n");
		}

		private void SerializeFunctionDefinition(List<string> output, FunctionDefinition funDef, string indention)
		{
			output.Add(indention);
			output.Add("function ");
			output.Add(funDef.Name);
			output.Add("(");
			for (int i = 0; i < funDef.ArgNameTokens.Length; ++i)
			{
				if (i > 0) output.Add(", ");
				output.Add(funDef.ArgNameTokens[i].Value);
				if (funDef.ArgDefaultValues[i] != null) {
					output.Add("=");
					SerializeExpression(output, funDef.ArgDefaultValues[i]);
				}
			}
			output.Add(") {\n");
			SerializeBlock(output, funDef.Body, indention + "\t");
			output.Add(indention);
			output.Add("}\n\n");

		}

		private void SerializeBreakStatement(List<string> output, BreakStatement breakStatement, string indention)
		{
			output.Add(indention);
			output.Add("break;\n");
		}

		private void SerializeClassDefinition(List<string> output, ClassDefinition classDef, string indention)
		{
			output.Add(indention);
			output.Add("class ");
			output.Add(classDef.NameToken.Value);

			if (classDef.BaseClassToken != null)
			{
				output.Add(" : ");
				output.Add(classDef.BaseClassToken.Value);
				output.Add(" {\n");
			}
			else
			{
				output.Add(" {\n");
			}

			for (int i = 0; i < classDef.Members.Length; ++i)
			{
				if (i > 0)
				{
					output.Add("\n");
				}

				FunctionDefinition funDef = classDef.Members[i];

				SerializeFunctionDefinition(output, funDef, indention + "\t", funDef.Name == "__init__");
			}

			output.Add(indention);
			output.Add("}\n\n");
		}

		private void SerializeFunctionDefinition(List<string> output, FunctionDefinition funDef, string indention, bool isConstructor)
		{
			output.Add(indention);
			if (isConstructor)
			{
				output.Add("constructor");
			}
			else
			{
				output.Add("function ");
				output.Add(funDef.Name);
			}

			output.Add("(");
			bool first = true;
			for (int i = 0; i < funDef.ArgNameTokens.Length; ++i)
			{
				string argName = funDef.ArgNameTokens[i].Value;
				if (argName == "self") continue;
				if (first) first = false;
				else output.Add(", ");
				output.Add(argName);
				if (funDef.ArgDefaultValues[i] != null)
				{
					output.Add("=");
					SerializeExpression(output, funDef.ArgDefaultValues[i]);
				}
			}
			output.Add(") {");
			if (funDef.Body.Length > 0)
			{
				output.Add("\n");
				SerializeBlock(output, funDef.Body, indention + "\t");

				output.Add(indention);
				output.Add("}\n");
			}
			else
			{
				output.Add(" }\n");
			}
		}

		private void SerializeBlock(List<string> output, IList<Executable> block, string indention)
		{
				for (int i = 0; i < block.Count; ++i)
				{
					Serialize(output, block[i], indention);
				}
		}

		private void SerializeForLoop(List<string> output, ForLoop forLoop, string indention)
		{
			List<string> temporaryBuffer = new List<string>();
			string temp;
			output.Add(indention);
			output.Add("for (");
			for (int i = 0; i < forLoop.Init.Length; ++i)
			{
				if (i > 0)
				{
					output.Add(", ");
				}
				Serialize(temporaryBuffer, forLoop.Init[i], null);
				temp = string.Join("", temporaryBuffer);
				while (temp.EndsWith(";") || temp.EndsWith("\n")) temp = temp.Substring(0, temp.Length - 1);
				temporaryBuffer.Clear();
				output.Add(temp);
			}
			output.Add("; ");
			SerializeExpression(output, forLoop.Condition);
			output.Add("; ");
			for (int i = 0; i < forLoop.Step.Length; ++i)
			{
				if (i > 0)
				{
					output.Add(",");
				}
				Serialize(temporaryBuffer, forLoop.Step[i], null);
				temp = string.Join("", temporaryBuffer);
				while (temp.EndsWith(";") || temp.EndsWith("\n")) temp = temp.Substring(0, temp.Length - 1);
				temporaryBuffer.Clear();
				output.Add(temp);
			}
			output.Add(") {\n");
			SerializeBlock(output, forLoop.Body, indention + "\t");
			output.Add(indention);
			output.Add("}\n");
		}

		private void SerializeIfStatement(List<string> output, IfStatement ifStatement, string indention, bool useFirstIndention)
		{
			if (useFirstIndention)
			{
				output.Add(indention);
			}
			output.Add("if (");
			SerializeExpression(output, ifStatement.Condition);
			output.Add(") {\n");
			SerializeExecList(output, ifStatement.TrueCode, indention + "\t");
			output.Add(indention);
			output.Add("}");
			if (ifStatement.FalseCode.Length == 0)
			{
				output.Add("\n");
			}
			else
			{
				output.Add(" else ");
				if (ifStatement.FalseCode.Length == 1 && ifStatement.FalseCode[0] is IfStatement)
				{
					SerializeIfStatement(output, (IfStatement)ifStatement.FalseCode[0], indention, false);
				}
				else
				{
					output.Add("{\n");
					SerializeExecList(output, ifStatement.FalseCode, indention + "\t");
					output.Add(indention);
					output.Add("}\n");
				}
			}
			
		}

		private void SerializeExecList(List<string> output, IList<Executable> execs, string indention)
		{
			foreach (Executable exec in execs)
			{
				Serialize(output, exec, indention);
			}
		}

		private void SerializeForEachLoop(List<string> output, ForEachLoop forLoop, string indention)
		{
			output.Add(indention);
			output.Add("for (");
			output.Add(forLoop.IteratorVariable.Value);
			output.Add(" : ");
			SerializeExpression(output, forLoop.IterableExpression);
			output.Add(") {\n");
			string innerIndention = indention + "\t";
			for (int i = 0; i < forLoop.Body.Length; ++i)
			{
				Serialize(output, forLoop.Body[i], innerIndention);
			}
			output.Add(indention);
			output.Add("}\n");
		}

		private void SerializeExpressionAsExecutable(List<string> output, ExpressionAsExecutable expr, string indention)
		{
			output.Add(indention);
			SerializeExpression(output, expr.Expression);
			output.Add(";\n");
		}

		private void SerializeAssignment(List<string> output, Assignment assignment, string indention)
		{
			output.Add(indention);
			SerializeExpression(output, assignment.Target);
			output.Add(" ");
			output.Add(assignment.AssignmentToken.Value);
			output.Add(" ");
			SerializeExpression(output, assignment.Value);
			output.Add(";\n");
		}

		public override void SerializeExpression(List<string> output, Expression expr)
		{
			if (expr is FunctionInvocation) SerializeFunctionInvocation(output, (FunctionInvocation)expr);
			else if (expr is Variable) SerializeVariable(output, (Variable)expr);
			else if (expr is StringConstant) SerializeStringConstant(output, (StringConstant)expr);
			else if (expr is IntegerConstant) SerializeIntegerConstant(output, (IntegerConstant)expr);
			else if (expr is DotField) SerializeDotField(output, (DotField)expr);
			else if (expr is BinaryOpChain) SerializeBinaryOpChain(output, (BinaryOpChain)expr);
			else if (expr is ParenthesisGroup) SerializeParenthesisGroup(output, (ParenthesisGroup)expr);
			else if (expr is InlineList) SerializeInlineList(output, (InlineList)expr);
			else if (expr is InlineTuple) SerializeInlineTuple(output, (InlineTuple)expr);
			else if (expr is BooleanConstant) SerializeBooleanConstant(output, (BooleanConstant)expr);
			else if (expr is NullConstant) output.Add("null");
			else if (expr is SystemFunctionInvocation) SerializeSystemFunctionInvocation(output, (SystemFunctionInvocation)expr);
			else if (expr is BooleanCombinator) SerializeBooleanCombinator(output, (BooleanCombinator)expr);
			else if (expr is FloatConstant) SerializeFloatConstant(output, (FloatConstant)expr);
			else if (expr is Negation) SerializeNegation(output, (Negation)expr);
			else if (expr is InlineDictionary) SerializeInlineDictionary(output, (InlineDictionary)expr);
			else if (expr is IndexExpression) SerializeIndex(output, (IndexExpression)expr);
			else if (expr is SliceExpression) SerializeSlice(output, (SliceExpression)expr);
			else if (expr is Ternary) SerializeTernary(output, (Ternary)expr);
			else throw new NotImplementedException(expr.GetType().ToString());
		}

		private void SerializeFloatConstant(List<string> output, FloatConstant floatConst)
		{
			string value = floatConst.Value.ToString();
			if (!value.Contains('.'))
			{
				value += ".0";
			}

			output.Add(value);
		}

		private void SerializeTernary(List<string> output, Ternary ternary)
		{
			SerializeExpression(output, ternary.Condition);
			output.Add(" ? (");
			SerializeExpression(output, ternary.TrueExpression);
			output.Add(") : (");
			SerializeExpression(output, ternary.FalseExpression);
			output.Add(")");
		}

		private void SerializeSlice(List<string> output, SliceExpression slice)
		{
			SerializeExpression(output, slice.Root);
			output.Add("[");
			for (int i = 0; i < slice.Components.Length; ++i)
			{
				if (i > 0) output.Add(":");
				if (slice.Components[i] != null)
				{
					SerializeExpression(output, slice.Components[i]);
				}
			}
			output.Add("]");
		}

		private void SerializeIndex(List<string> output, IndexExpression index)
		{
			SerializeExpression(output, index.Root);
			output.Add("[");
			SerializeExpression(output, index.Index);
			output.Add("]");
		}

		private void SerializeInlineDictionary(List<string> output, InlineDictionary dictionary)
		{
			output.Add("{");
			for (int i = 0; i < dictionary.Keys.Length; ++i)
			{
				if (i > 0) output.Add(", ");
				SerializeExpression(output, dictionary.Keys[i]);
				output.Add(": ");
				SerializeExpression(output, dictionary.Values[i]);
			}
			output.Add("}");
		}

		private void SerializeNegation(List<string> output, Negation negation)
		{
			if (negation.Type == Negation.PrefixType.BITWISE_NOT)
			{
				output.Add("~");
			}
			else if (negation.Type == Negation.PrefixType.BOOLEAN_NOT)
			{
				output.Add("!");
			}
			else if (negation.Type == Negation.PrefixType.NEGATIVE)
			{
				output.Add("-");
			}

			SerializeExpression(output, negation.Root);
		}

		private void SerializeBooleanCombinator(List<string> output, BooleanCombinator booleanCombinator)
		{
			output.Add("(");
			SerializeExpression(output, booleanCombinator.Left);
			output.Add(booleanCombinator.IsAnd ? " && " : " || ");
			SerializeExpression(output, booleanCombinator.Right);
			output.Add(")");
		}

		private void SerializeInlineTuple(List<string> output, InlineTuple inlineTuple)
		{
			output.Add("[");
			for (int i = 0; i < inlineTuple.Items.Length; ++i)
			{
				if (i > 0)
				{
					output.Add(", ");
				}
				SerializeExpression(output, inlineTuple.Items[i]);
			}
			output.Add("]");
		}

		private void SerializeBooleanConstant(List<string> output, BooleanConstant boolConst)
		{
			output.Add(boolConst.Value ? "true" : "false");
		}

		private void SerializeSystemFunctionInvocation(List<string> output, SystemFunctionInvocation sysfun)
		{
			PRIMITIVE_METHODS.Convert(output, sysfun);
		}

		private void SerializeInlineList(List<string> output, InlineList list)
		{
			output.Add("[");
			for (int i = 0; i < list.Items.Length; ++i)
			{
				if (i > 0) output.Add(", ");
				SerializeExpression(output, list.Items[i]);
			}
			output.Add("]");
		}

		private void SerializeParenthesisGroup(List<string> output, ParenthesisGroup parenGroup)
		{
			output.Add("(");
			SerializeExpression(output, parenGroup.InnerExpression);
			output.Add(")");
		}

		private void SerializeDotField(List<string> output, DotField dotField)
		{
			SerializeExpression(output, dotField.Root);
			output.Add(".");
			output.Add(dotField.FieldName);
		}

		private void SerializeBinaryOpChain(List<string> output, BinaryOpChain opChain)
		{
			for (int i = 0; i < opChain.Expressions.Length; ++i)
			{
				if (i > 0)
				{
					output.Add(" ");
					output.Add(opChain.OpTokens[i - 1].Value);
					output.Add(" ");
				}
				SerializeExpression(output, opChain.Expressions[i]);
			}
		}

		private void SerializeIntegerConstant(List<string> output, IntegerConstant intValue)
		{
			int value = intValue.Value;
			output.Add("" + value);
		}

		private void SerializeStringConstant(List<string> output, StringConstant str)
		{
			output.Add("\"");
			output.Add(Util.InsertEscapeSequences(str.Value));
			output.Add("\"");
		}

		private void SerializeVariable(List<string> output, Variable variable)
		{
			if (variable.Value == "self")
			{
				output.Add("this");
			}
			else
			{
				output.Add(variable.Value);
			}
		}

		private void SerializeFunctionInvocation(List<string> output, FunctionInvocation function)
		{
			if (function.Root is Variable)
			{
				// If it's uppercase, then it's a constructor invocation.
				string varName = ((Variable)function.Root).Value;
				if (varName[0] == varName.ToUpperInvariant()[0])
				{
					output.Add("new ");
				}
			}

			this.SerializeExpression(output, function.Root);
			output.Add("(");
			for (int i = 0; i < function.Args.Length; ++i)
			{
				if (i > 0) output.Add(", ");
				this.SerializeExpression(output, function.Args[i]);
			}
			output.Add(")");
		}
	}
}
