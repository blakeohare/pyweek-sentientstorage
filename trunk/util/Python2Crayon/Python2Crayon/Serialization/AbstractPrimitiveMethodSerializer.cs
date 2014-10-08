using System;
using System.Collections.Generic;
using System.Linq;
using Python2Crayon.ParseTree;

namespace Python2Crayon.Serialization
{
	internal abstract class AbstractPrimitiveMethodSerializer
	{
		private Serializer serializer;
		public AbstractPrimitiveMethodSerializer(Serializer serializer)
		{
			this.serializer = serializer;
			this.methodLookup = new Dictionary<string, System.Reflection.MethodInfo>();
			this.argCount = new Dictionary<string, int>();
			Type t = this.GetType();
			System.Reflection.MethodInfo[] methods = t.GetMethods( System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.NonPublic);
			foreach (System.Reflection.MethodInfo method in methods)
			{
				if (method.Name.StartsWith("X_"))
				{
					List<string> name = new List<string>();
					for (int i = 2; i < method.Name.Length; ++i)
					{
						char c = method.Name[i];
						if (c >= 'A' && c <= 'Z')
						{
							name.Add("_" + (char)(c - 'A' + 'a'));
						}
						else
						{
							name.Add("" + c);
						}
					}

					string id = string.Join("", name).Substring(1);
					this.methodLookup[id] = method;
					this.argCount[id] = method.GetParameters().Length - 1;
				}
			}
		}

		private Dictionary<string, System.Reflection.MethodInfo> methodLookup;
		private Dictionary<string, int> argCount;

		protected void SerializeExpression(List<string> output, Expression expression)
		{
			this.serializer.SerializeExpression(output, expression);
		}

		public void Convert(List<string> output, SystemFunctionInvocation sysFunction)
		{
			Expression[] args = sysFunction.Args;
			System.Reflection.MethodInfo method;
			if (this.methodLookup.TryGetValue(sysFunction.Name, out method))
			{
				if (this.argCount[sysFunction.Name] != args.Length)
				{
					throw new ParserException(sysFunction.FirstToken, "Invalid number of args for $" + sysFunction.Name + ". Expected " + this.argCount[sysFunction.Name] + " but found " + sysFunction.Args.Length + ".");
				}
				List<object> methodArgs = new List<object>() { output };
				methodArgs.AddRange(args);
				method.Invoke(this, methodArgs.ToArray());
			}
			else
			{
				throw new ParserException(sysFunction.FirstToken, "Unknown primitive function:" + sysFunction.Name);
			}
		}

		protected abstract void X_DictionaryGetWithDefault(List<string> output, Expression dict, Expression key, Expression defaultValue);
		protected abstract void X_DictionaryKeys(List<string> output, Expression dict);
		protected abstract void X_DictionarySize(List<string> output, Expression dict);

		protected abstract void X_DrawEllipse(List<string> output, ParseTree.Expression screen, ParseTree.Expression left, ParseTree.Expression top, ParseTree.Expression width, ParseTree.Expression height, ParseTree.Expression red, ParseTree.Expression green, ParseTree.Expression blue);
		protected abstract void X_DrawRectangle(List<string> output, Expression screen, Expression left, Expression top, Expression width, Expression height, Expression red, Expression green, Expression blue);
		protected abstract void X_DrawTriangle(List<string> output, Expression screen, Expression x1, Expression y1, Expression x2, Expression y2, Expression x3, Expression y3, Expression red, Expression green, Expression blue);
		
		protected abstract void X_ImageBlit(List<string> output, Expression screen, Expression image, Expression x, Expression y);
		protected abstract void X_ImageHeight(List<string> output, Expression image);
		protected abstract void X_ImageWidth(List<string> output, Expression image);

		protected abstract void X_Int(List<string> output, Expression num);

		protected abstract void X_ListAdd(List<string> output, Expression list, Expression value);
		protected abstract void X_ListJoin(List<string> output, Expression list, Expression sep);
		protected abstract void X_ListLength(List<string> output, Expression list);
		protected abstract void X_ListRemove(List<string> output, Expression list, Expression index);
		protected abstract void X_ListShuffle(List<string> output, Expression list);

		protected abstract void X_MathAbs(List<string> output, Expression num);
		protected abstract void X_MathSin(List<string> output, Expression theta);

		protected abstract void X_ParseInt(List<string> output, Expression value);

		protected abstract void X_Print(List<string> output, Expression value);

		protected abstract void X_ScreenFill(List<string> output, Expression screen, Expression red, Expression green, Expression blue);

		protected abstract void X_Str(List<string> output, Expression value);

		protected abstract void X_StringLength(List<string> output, Expression str);
		protected abstract void X_StringLower(List<string> output, Expression str);
		protected abstract void X_StringSplit(List<string> output, Expression str, Expression sep);
		protected abstract void X_StringTrim(List<string> output, Expression str);
		protected abstract void X_StringUpper(List<string> output, Expression str);
	}
}
