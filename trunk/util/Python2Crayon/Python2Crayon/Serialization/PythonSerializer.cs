using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Python2Crayon.ParseTree;

namespace Python2Crayon.Serialization
{
	internal class PythonSerializer : Serializer
	{
		private readonly AbstractPrimitiveMethodSerializer PRIMITIVE_METHODS;

		public PythonSerializer()
		{
			PRIMITIVE_METHODS = new PythonPrimitiveMethods(this);
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
			if (exec is Assignment) SerializeAssignment(output, (Assignment)exec, indention);
			else if (exec is ClassDefinition) SerializeClassDefinition(output, (ClassDefinition)exec, indention);
			else if (exec is FunctionDefinition) SerializeFunctionInvocation(output, (FunctionDefinition)exec, indention);
			else if (exec is IfStatement) SerializeIfStatement(output, (IfStatement)exec, indention, false);
			else if (exec is ExpressionAsExecutable) SerializeExpressionAsExecutable(output, (ExpressionAsExecutable)exec, indention);
			else if (exec is ForEachLoop) SerializeForEachLoop(output, (ForEachLoop)exec, indention);
			else if (exec is BreakStatement) SerializeBreakStatement(output, (BreakStatement)exec, indention);
			else if (exec is ReturnStatement) SerializeReturnStatement(output, (ReturnStatement)exec, indention);
			else if (exec is ForLoop) Serialize(output, ((ForLoop)exec).OriginalForEachLoop, indention);
			else if (exec is WhileLoop) SerializeWhileLoop(output, (WhileLoop)exec, indention);
			else throw new NotImplementedException();
		}

		private void SerializeWhileLoop(List<string> output, WhileLoop whileLoop, string indention)
		{
			output.Add(indention);
			output.Add("while ");
			SerializeExpression(output, whileLoop.Condition);
			output.Add(":\n");
			SerializeBlock(output, whileLoop.Body, indention + "\t");
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
			output.Add("\n");
		}

		private void SerializeBreakStatement(List<string> output, BreakStatement breakStatement, string indention)
		{
			output.Add(indention);
			output.Add("break\n");
		}

		private void SerializeForEachLoop(List<string> output, ForEachLoop forEachLoop, string indention)
		{
			output.Add(indention);
			output.Add("for ");
			output.Add(forEachLoop.IteratorVariable.Value);
			output.Add(" in ");
			SerializeExpression(output, forEachLoop.IterableExpression);
			output.Add(":\n");
			SerializeBlock(output, forEachLoop.Body, indention + "\t");
		}

		private void SerializeExpressionAsExecutable(List<string> output, ExpressionAsExecutable expr, string indention)
		{
			output.Add(indention);
			SerializeExpression(output, expr.Expression);
			output.Add("\n");
		}

		private void SerializeIfStatement(List<string> output, IfStatement ifStatement, string indention, bool skipIndention)
		{
			if (!skipIndention) {
				output.Add(indention);
			}
			output.Add("if ");
			SerializeExpression(output, ifStatement.Condition);
			output.Add(":\n");
			SerializeBlock(output, ifStatement.TrueCode, indention + "\t");
			if (ifStatement.FalseCode.Length > 0)
			{
				if (ifStatement.FalseCode.Length == 1 && ifStatement.FalseCode[0] is IfStatement)
				{
					output.Add(indention);
					output.Add("el");
					SerializeIfStatement(output, (IfStatement)ifStatement.FalseCode[0], indention, true);
				}
				else
				{
					output.Add(indention);
					output.Add("else:\n");
					SerializeBlock(output, ifStatement.FalseCode, indention + "\t");
				}
			}
		}

		private void SerializeBlock(List<string> output, IList<Executable> block, string indention)
		{
			if (block.Count == 0)
			{
				output.Add(indention);
				output.Add("pass\n");
			}
			else
			{
				for (int i = 0; i < block.Count; ++i)
				{
					Serialize(output, block[i], indention);
				}
			}
		}

		private void SerializeFunctionInvocation(List<string> output, FunctionDefinition funDef, string indention)
		{
			output.Add(indention);
			output.Add("def ");
			output.Add(funDef.Name);
			output.Add("(");
			for (int i = 0; i < funDef.ArgNameTokens.Length; ++i)
			{
				if (i > 0) output.Add(", ");
				output.Add(funDef.ArgNameTokens[i].Value);
				Expression defaultValue = funDef.ArgDefaultValues[i];
				if (defaultValue != null)
				{
					SerializeExpression(output, defaultValue);
				}
			}
			output.Add("):\n");
			SerializeBlock(output, funDef.Body, indention + "\t");
		}

		private void SerializeClassDefinition(List<string> output, ClassDefinition classDef, string indention)
		{
			output.Add(indention);
			output.Add("class ");
			output.Add(classDef.NameToken.Value);
			if (classDef.BaseClassToken != null)
			{
				output.Add("(");
				output.Add(classDef.BaseClassToken.Value);
				output.Add("):\n");
			}
			else
			{
				output.Add(":\n");
			}

			foreach (FunctionDefinition fd in classDef.Members)
			{
				this.Serialize(output, fd, indention + "\t");
				output.Add("\n");
			}

			if (classDef.Members.Length == 0)
			{
				output.Add(indention);
				output.Add("\tpass\n");
			}
		}

		private void SerializeAssignment(List<string> output, Assignment assignment, string indention)
		{
			output.Add(indention);
			SerializeExpression(output, assignment.Target);
			output.Add(" ");
			output.Add(assignment.AssignmentToken.Value);
			output.Add(" ");
			SerializeExpression(output, assignment.Value);
			output.Add("\n");
		}

		public override void SerializeExpression(List<string> output, Expression expr)
		{
			if (expr is FunctionInvocation) SerializeFunctionInvocation(output, (FunctionInvocation)expr);
			else if (expr is DotField) SerializeDotField(output, (DotField)expr);
			else if (expr is Variable) SerializeVariable(output, (Variable)expr);
			else if (expr is IntegerConstant) SerializeIntegerConstant(output, (IntegerConstant)expr);
			else if (expr is ParenthesisGroup) SerializeParenthesisGroup(output, (ParenthesisGroup)expr);
			else if (expr is BinaryOpChain) SerializeBinaryOpChain(output, (BinaryOpChain)expr);
			else if (expr is BooleanConstant) SerializeBooleanConstant(output, (BooleanConstant)expr);
			else if (expr is InlineList) SerializeInlineList(output, (InlineList)expr);
			else if (expr is InlineTuple) SerializeInlineTuple(output, (InlineTuple)expr);
			else if (expr is SystemFunctionInvocation) SerializeSystemFunctionInvocation(output, (SystemFunctionInvocation)expr);
			else if (expr is NullConstant) output.Add("None");
			else if (expr is StringConstant) SerializeStringConstant(output, (StringConstant)expr);
			else if (expr is BooleanCombinator) SerializeBooleanCombinator(output, (BooleanCombinator)expr);
			else if (expr is FloatConstant) SerializeFloatConstant(output, (FloatConstant)expr);
			else if (expr is Negation) SerializeNegation(output, (Negation)expr);
			else if (expr is InlineDictionary) SerializeInlineDictionary(output, (InlineDictionary)expr);
			else if (expr is IndexExpression) SerializeIndex(output, (IndexExpression)expr);
			else if (expr is SliceExpression) SerializeSlice(output, (SliceExpression)expr);
			else if (expr is Ternary) SerializeTernary(output, (Ternary)expr);
			else throw new NotImplementedException();
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
			SerializeExpression(output, ternary.TrueExpression);
			output.Add(" if ");
			SerializeExpression(output, ternary.Condition);
			output.Add(" else ");
			SerializeExpression(output, ternary.FalseExpression);
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

		private void SerializeIndex(List<string> output, IndexExpression index)
		{
			SerializeExpression(output, index.Root);
			output.Add("[");
			SerializeExpression(output, index.Index);
			output.Add("]");
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
			SerializeExpression(output, booleanCombinator.Left);
			output.Add(booleanCombinator.IsAnd ? " and " : " or ");
			SerializeExpression(output, booleanCombinator.Right);
		}

		private void SerializeInlineTuple(List<string> output, InlineTuple inlineTuple)
		{
			output.Add("(");
			for (int i = 0; i < inlineTuple.Items.Length; ++i)
			{
				if (i > 0)
				{
					output.Add(", ");
				}
				SerializeExpression(output, inlineTuple.Items[i]);
			}
			if (inlineTuple.Items.Length == 1) output.Add(",");
			output.Add(")");
		}

		private void SerializeBooleanConstant(List<string> output, BooleanConstant boolConst)
		{
			output.Add(boolConst.Value ? "True" : "False");
		}

		private void SerializeStringConstant(List<string> output, StringConstant stringConst)
		{
			output.Add("\"");
			output.Add(Util.InsertEscapeSequences(stringConst.Value));
			output.Add("\"");
		}

		private void SerializeBinaryOpChain(List<string> output, BinaryOpChain binaryOpChain)
		{
			for (int i = 0; i < binaryOpChain.Expressions.Length; ++i)
			{
				if (i > 0)
				{
					output.Add(" ");
					output.Add(binaryOpChain.OpTokens[i - 1].Value);
					output.Add(" ");
				}
				SerializeExpression(output, binaryOpChain.Expressions[i]);
			}
		}

		private void SerializeParenthesisGroup(List<string> output, ParenthesisGroup parenGroup)
		{
			output.Add("(");
			SerializeExpression(output, parenGroup.InnerExpression);
			output.Add(")");
		}

		private void SerializeIntegerConstant(List<string> output, IntegerConstant intConst)
		{
			output.Add(intConst.Value.ToString());
		}

		private void SerializeVariable(List<string> output, Variable variable)
		{
			output.Add(variable.Value);
		}

		private void SerializeDotField(List<string> output, DotField dotField)
		{
			SerializeExpression(output, dotField.Root);
			output.Add(".");
			output.Add(dotField.FieldName);
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

		private void SerializeFunctionInvocation(List<string> output, FunctionInvocation functionInvocation)
		{
			SerializeExpression(output, functionInvocation.Root);
			output.Add("(");
			for (int i = 0; i < functionInvocation.Args.Length; ++i)
			{
				if (i > 0) output.Add(", ");
				SerializeExpression(output, functionInvocation.Args[i]);
			}
			output.Add(")");
		}
	}
}
