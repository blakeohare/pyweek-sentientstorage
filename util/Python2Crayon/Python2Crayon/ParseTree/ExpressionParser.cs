using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal static class ExpressionParser 
	{
		public static Expression Parse(TokenStream tokens)
		{
			return ParseLambda(tokens);
		}

		public static Expression ParseLambda(TokenStream tokens)
		{
			tokens.SkipWhitespace();
			if (tokens.IsNext("lambda"))
			{
				Token lambdaToken = tokens.PopExpected("lambda");
				List<Token> argNames = new List<Token>();
				List<Expression> argValues = new List<Expression>();

				if (!tokens.PopIfPresent(":"))
				{
					bool nextAllowed = true;
					while (!tokens.PopIfPresent(":"))
					{
						if (!nextAllowed) tokens.PopExpected(":"); // throws
						Token argName = tokens.Pop();
						if (!Util.IsIdentifier(argName)) throw new ParserException(argName, "Invalid lambda arg name.");
						Expression argValue = null;
						if (tokens.PopIfPresent("="))
						{
							argValue = ExpressionParser.Parse(tokens);
						}

						argNames.Add(argName);
						argValues.Add(argValue);

						nextAllowed = tokens.PopIfPresent(",");
					}
				}
			}

			return ParseTernary(tokens);
		}

		public static Expression ParseTernary(TokenStream tokens)
		{
			Expression left = ParseBooleanOr(tokens);
			if (tokens.PopIfPresent("if"))
			{
				Expression condition = ParseBooleanOr(tokens);
				tokens.PopExpected("else");
				Expression right = ParseTernary(tokens);
				return new Ternary(condition, left, right);
			}
			return left;
		}

		public static Expression ParseBooleanOr(TokenStream tokens)
		{
			Expression left = ParseBooleanAnd(tokens);
			if (tokens.PopIfPresent("or"))
			{
				Expression right = ParseBooleanOr(tokens);
				return new BooleanCombinator(left, right, "or");
			}
			return left;
		}

		public static Expression ParseBooleanAnd(TokenStream tokens)
		{
			tokens.SkipWhitespace();
			Expression left = ParseBooleanNot(tokens);
			if (tokens.PopIfPresent("and"))
			{
				Expression right = ParseBooleanAnd(tokens);
				return new BooleanCombinator(left, right, "and");
			}
			return left;
		}

		public static Expression ParseBooleanNot(TokenStream tokens)
		{
			tokens.SkipWhitespace();
			if (tokens.IsNext("not"))
			{
				Token notToken = tokens.Pop();
				Expression expression = ParseComparisons(tokens);
				return new Negation(notToken, expression, Negation.PrefixType.BOOLEAN_NOT);
			}

			return ParseComparisons(tokens);
		}

		private static readonly HashSet<string> COMPARISON_TOKENS = new HashSet<string>("in|not in|is|is not|<|<=|>|>=|<>|!=|==".Split('|'));
		public static Expression ParseComparisons(TokenStream tokens)
		{
			Expression left = ParseBitwiseOr(tokens);
			string next = tokens.PeekValue();
			if (COMPARISON_TOKENS.Contains(next))
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> comparisons = new List<Token>();
				while (COMPARISON_TOKENS.Contains(next))
				{
					comparisons.Add(tokens.Pop());
					expressions.Add(ParseBitwiseOr(tokens));
					next = tokens.PeekValue();
				}
				return new ComparisonChain(expressions, comparisons);
			}
			return left;
		}

		public static Expression ParseBitwiseOr(TokenStream tokens)
		{
			Expression left = ParseBitwiseXor(tokens);
			string next = tokens.PeekValue();
			if (next == "|")
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> ops = new List<Token>();
				while (next == "|")
				{
					ops.Add(tokens.Pop());
					expressions.Add(ParseBitwiseXor(tokens));
					next = tokens.PeekValue();
				}
				return new BinaryOpChain(expressions, ops);
			}
			return left;
		}

		public static Expression ParseBitwiseXor(TokenStream tokens)
		{
			Expression left = ParseBitwiseAnd(tokens);
			string next = tokens.PeekValue();
			if (next == "^")
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> ops = new List<Token>();
				while (next == "^")
				{
					ops.Add(tokens.Pop());
					expressions.Add(ParseBitwiseAnd(tokens));
					next = tokens.PeekValue();
				}
				return new BinaryOpChain(expressions, ops);
			}
			return left;
		}

		public static Expression ParseBitwiseAnd(TokenStream tokens)
		{
			Expression left = ParseBitshift(tokens);
			string next = tokens.PeekValue();
			if (next == "^")
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> ops = new List<Token>();
				while (next == "^")
				{
					ops.Add(tokens.Pop());
					expressions.Add(ParseBitshift(tokens));
					next = tokens.PeekValue();
				}
				return new BinaryOpChain(expressions, ops);
			}
			return left;
		}

		private static readonly HashSet<string> BITSHIFT_OPERATORS = new HashSet<string>("<< >>".Split(' '));
		public static Expression ParseBitshift(TokenStream tokens)
		{
			Expression left = ParseAddition(tokens);
			string next = tokens.PeekValue();
			if (BITSHIFT_OPERATORS.Contains(next))
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> ops = new List<Token>();
				while (BITSHIFT_OPERATORS.Contains(next))
				{
					ops.Add(tokens.Pop());
					expressions.Add(ParseAddition(tokens));
					next = tokens.PeekValue();
				}
				return new BinaryOpChain(expressions, ops);
			}
			return left;
		}

		private static readonly HashSet<string> ADDITION_OPERATORS = new HashSet<string>("+ -".Split(' '));
		public static Expression ParseAddition(TokenStream tokens)
		{
			Expression left = ParseMultiplication(tokens);
			string next = tokens.PeekValue();
			if (ADDITION_OPERATORS.Contains(next))
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> ops = new List<Token>();
				while (ADDITION_OPERATORS.Contains(next))
				{
					ops.Add(tokens.Pop());
					expressions.Add(ParseMultiplication(tokens));
					next = tokens.PeekValue();
				}
				return new BinaryOpChain(expressions, ops);
			}
			return left;
		}

		private static readonly HashSet<string> MULTIPLICATION_OPERATORS = new HashSet<string>("* / // %".Split(' '));
		public static Expression ParseMultiplication(TokenStream tokens)
		{
			Expression left = ParseNot(tokens);
			string next = tokens.PeekValue();
			if (MULTIPLICATION_OPERATORS.Contains(next))
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> ops = new List<Token>();
				while (MULTIPLICATION_OPERATORS.Contains(next))
				{
					ops.Add(tokens.Pop());
					expressions.Add(ParseNot(tokens));
					next = tokens.PeekValue();
				}
				return new BinaryOpChain(expressions, ops);
			}
			return left;
		}

		private static Expression ParseNot(TokenStream tokens)
		{
			tokens.SkipWhitespace();
			string next = tokens.PeekValue();
			if (next == "+" || next == "-" || next == "~")
			{
				Token token = tokens.Pop();
				Expression root = ParseExponents(tokens);
				return new Negation(token, root, 
					token.Value == "+"
						? Negation.PrefixType.POSITIVE
						: token.Value == "-"
							? Negation.PrefixType.NEGATIVE
							: Negation.PrefixType.BITWISE_NOT);
			}

			return ParseExponents(tokens);
		}

		private static Expression ParseExponents(TokenStream tokens)
		{
			Expression left = ParseEntityWithSuffix(tokens);
			string next = tokens.PeekValue();
			if (next == "**")
			{
				List<Expression> expressions = new List<Expression>() { left };
				List<Token> ops = new List<Token>();
				while (next == "**")
				{
					ops.Add(tokens.Pop());
					expressions.Add(ParseEntityWithSuffix(tokens));
					next = tokens.PeekValue();
				}
				return new BinaryOpChain(expressions, ops);
			}
			return left;
		}

		private static Expression ParseEntityWithSuffix(TokenStream tokens)
		{
			Expression expression = ParseRootEntity(tokens);
			bool nextAllowed;
			bool keepGoing = true;
			string next = tokens.PeekValue();

			while (keepGoing)
			{
				switch (next)
				{
					case "[":
						// indexing or slicing
						Token bracketToken = tokens.Pop();
						List<Expression> sliceComponents = new List<Expression>();
						nextAllowed = true;
						while (!tokens.PopIfPresent("]"))
						{
							if (!nextAllowed) tokens.PopExpected("]"); // throws

							if (tokens.IsNext(":"))
							{
								sliceComponents.Add(null);
							}
							else
							{
								sliceComponents.Add(Parse(tokens));
							}
							nextAllowed = tokens.PopIfPresent(":");
						}
						if (nextAllowed)
						{
							sliceComponents.Add(null);
						}
						if (sliceComponents.Count == 0)
						{
							throw new ParserException(bracketToken, "Unexpected token.");
						}
						else if (sliceComponents.Count == 1)
						{
							expression = new IndexExpression(expression, bracketToken, sliceComponents[0]);
						}
						else if (sliceComponents.Count <= 3)
						{
							expression = new SliceExpression(expression, bracketToken, sliceComponents);
						}
						else
						{
							throw new ParserException(bracketToken, "Slice expression has too many components.");
						}
						break;
					case "(":
						// function call
						Token openParen = tokens.Pop();
						nextAllowed = true;
						List<Expression> args = new List<Expression>();
						while (!tokens.PopIfPresent(")"))
						{
							if (!nextAllowed) tokens.PopExpected(")"); // throws
							args.Add(Parse(tokens));
							nextAllowed = tokens.PopIfPresent(",");
						}

						expression = new FunctionInvocation(expression, args);
						break;
					case ".":
						// dot field
						Token dotToken = tokens.Pop();
						Token fieldToken = tokens.Pop();
						if (!Util.IsIdentifier(fieldToken))
						{
							throw new ParserException(fieldToken, "Invalid field.");
						}
						expression = new DotField(expression, dotToken, fieldToken, fieldToken.Value);
						break;
					default:
						keepGoing = false;
						break;
				}
				next = tokens.PeekValue();
			}

			return expression;
		}

		private static Expression ParseRootEntity(TokenStream tokens)
		{
			tokens.SkipWhitespace();
			string next = tokens.PeekValue();
			if (next == "True" || next == "False")
			{
				Token token = tokens.Pop();
				return new BooleanConstant(token, next == "True");
			}
			else if (next == "None")
			{
				Token token = tokens.Pop();
				return new NullConstant(token);
			}
			else if (next.StartsWith("'") || next.StartsWith("\""))
			{
				Token token = tokens.Pop();
				int quoteSize = next.StartsWith("'''") || next.StartsWith("\"\"\"") ? 3 : 1;
				return new StringConstant(token, Util.RemoveEscapeSequences(token, next.Substring(quoteSize, next.Length - quoteSize * 2)));
			}
			else if (next.StartsWith("r'") || next.StartsWith("r\""))
			{
				Token token = tokens.Pop();
				int quoteSize = next.StartsWith("r'''") || next.StartsWith("r\"\"\"") ? 3 : 1;
				
				return new StringConstant(token, next.Substring(quoteSize + 1, next.Length - quoteSize * 2 - 1));
			}
			else if (next == "(")
			{
				// Tuples or parentehsis
				Token parenthesisToken = tokens.Pop();
				List<Expression> parenthesisExpressions = new List<Expression>();
				bool nextAllowed = true;
				while (!tokens.PopIfPresent(")"))
				{
					if (!nextAllowed) tokens.PopExpected(")"); // throws
					parenthesisExpressions.Add(Parse(tokens));
					nextAllowed = tokens.PopIfPresent(",");
					tokens.SkipWhitespace();
				}

				if (parenthesisExpressions.Count > 1 || nextAllowed)
				{
					return new InlineTuple(parenthesisToken, parenthesisExpressions);
				}
				else
				{
					return new ParenthesisGroup(parenthesisToken, parenthesisExpressions[0]);
				}
			}
			else if (next == "[")
			{
				Token bracketToken = tokens.Pop();
				List<Expression> listItems = new List<Expression>();
				bool nextAllowed = true;
				while (!tokens.PopIfPresent("]"))
				{
					if (!nextAllowed) tokens.PopExpected("]"); // throws
					listItems.Add(Parse(tokens));
					nextAllowed = tokens.PopIfPresent(",");
					tokens.SkipWhitespace();
				}
				return new InlineList(bracketToken, listItems);
			}
			else if (next == "{")
			{
				Token braceToken = tokens.Pop();
				List<Expression> dictionaryKeys = new List<Expression>();
				List<Expression> dictionaryValues = new List<Expression>();
				bool nextAllowed = true;
				while (!tokens.PopIfPresent("}"))
				{
					if (!nextAllowed) tokens.PopExpected("}"); // throws
					dictionaryKeys.Add(Parse(tokens));
					tokens.PopExpected(":");
					dictionaryValues.Add(Parse(tokens));
					nextAllowed = tokens.PopIfPresent(",");
					tokens.SkipWhitespace();
				}
				return new InlineDictionary(braceToken, dictionaryKeys, dictionaryValues);
			}
			else if (next.StartsWith("0x") || next.StartsWith("0o") || next.StartsWith("0X") || next.StartsWith("0O"))
			{
				Token integerToken = tokens.Pop();
				int radix = next.ToLowerInvariant().StartsWith("0x") ? 16 : 8;
				string stringValue = next.Substring(2);
				if (stringValue.Length == 0)
				{
					throw new ParserException(integerToken, "Invalid base " + radix + " constant.");
				}
				int value = Util.ParseNumber(integerToken, stringValue, radix);
				return new IntegerConstant(integerToken, value);
			}
			else if (next[0] >= '0' && next[0] <= '9')
			{
				Token numberToken = tokens.Pop();
				if (next.Contains('.') || next.Contains('e') || next.Contains('E'))
				{
					double value = Util.ParseDouble(numberToken);
					return new FloatConstant(numberToken, value);
				}
				else
				{
					int value = Util.ParseNumber(numberToken, next, 10);
					return new IntegerConstant(numberToken, value);
				}
			}
			else if (next[0] == '.')
			{
				Token numberToken = tokens.Pop();
				double value = Util.ParseDouble(numberToken);
				return new FloatConstant(numberToken, value);
			}
			else if (next[0] == '$')
			{
				// Because system functions can't be used as pointers, the invocation and arguments
				// are parsed here. Any standalone occurence of a system function is an error.
				Token dollarToken = tokens.Pop();
				Token nameToken = tokens.Pop();
				if (!Util.IsIdentifier(nameToken)) throw new ParserException(nameToken, "Invalid system function name.");
				tokens.PopExpected("(");
				bool nextAllowed = true;
				List<Expression> args = new List<Expression>();
				while (!tokens.PopIfPresent(")"))
				{
					args.Add(Parse(tokens));
					nextAllowed = tokens.PopIfPresent(",");
				}

				return new SystemFunctionInvocation(dollarToken, nameToken, args);
			}
			else if (
				(next[0] >= 'a' && next[0] <= 'z') ||
				(next[0] >= 'A' && next[0] <= 'Z') ||
				next[0] == '_')
			{
				Token token = tokens.Pop();
				if (token.Value == "squeedly_spooch")
				{
				}
				return new Variable(token, token.Value);
			}
			else
			{
				throw new ParserException(tokens.Peek(), "Unrecognized token.");
			}
		}
	}
}
