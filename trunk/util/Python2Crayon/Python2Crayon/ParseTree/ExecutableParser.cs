using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	class ExecutableParser
	{
		private static readonly HashSet<string> ASSIGNMENT_OPS = new HashSet<string>(
			"= += -= *= /= //= %= &= |= ^= **= <<= >>=".Split(' '));

		public Executable Parse(TokenStream tokens, bool nestedIndentAllowed, int indention)
		{
			string next = tokens.PeekValue();

			if (nestedIndentAllowed)
			{
				switch (next)
				{
					case "def": return ParseDef(tokens, indention);
					case "class": return ParseClass(tokens, indention);
					case "if": return ParseIfLikeThing(tokens, indention);
					case "elif": return ParseIfLikeThing(tokens, indention);
					case "else": return ParseIfLikeThing(tokens, indention);
					case "for": return ParseIfLikeThing(tokens, indention);
					case "while": return ParseIfLikeThing(tokens, indention);
					default: break;
				}
			}
			switch (next)
			{
				case "break": return ParseAtomicItem(tokens, indention);
				case "continue": return ParseAtomicItem(tokens, indention);
				case "pass": return ParseAtomicItem(tokens, indention);
				case "return": return ParseReturn(tokens, indention);
				case "import": return ParseImport(tokens, indention);
				case "from": return ParseImport(tokens, indention);
				default: break;
			}


			Expression expression = ExpressionParser.Parse(tokens);

			next = tokens.PeekValue();
			if (ASSIGNMENT_OPS.Contains(next))
			{
				Token assignmentToken = tokens.Pop();
				Expression assignmentValue = ExpressionParser.Parse(tokens);
				return new Assignment(expression, assignmentToken, assignmentValue);
			}

			return new ExpressionAsExecutable(expression);
		}

		private Executable ParseImport(TokenStream tokens, int indention)
		{
			tokens.SkipWhitespace();

			List<Token> fromChain = null;
			List<Token> importChain = null;
			List<Token> asChain = null;
			Token firstToken = null;

			if (tokens.PeekValue() == "from")
			{
				firstToken = tokens.Pop();
				fromChain = ParseDotChainForImport(tokens);
			}

			firstToken = firstToken ?? tokens.PopExpected("import");
			importChain = ParseDotChainForImport(tokens);

			if (tokens.PopIfPresent("as"))
			{
				asChain = ParseDotChainForImport(tokens);
				if (asChain.Count > 1) throw new ParserException(asChain[0], "Expected: variable");
			}

			return new ImportStatement(firstToken, importChain, fromChain, asChain == null ? null : asChain[0]);
		}

		private List<Token> ParseDotChainForImport(TokenStream tokens)
		{
			List<Token> output = new List<Token>() {tokens.Pop()};
			if (output[0].Value != "*" && !Util.IsIdentifier(output[0]))
			{
				throw new ParserException(output[0], "Invalid import statement.");
			}

			while (tokens.PopIfPresent("."))
			{
				Token next = tokens.Pop();
				if (next.Value != "*" && !Util.IsIdentifier(next))
				{
					throw new ParserException(next, "Invalid import statement.");
				}
				output.Add(next);
			}

			return output;
		}

		private Executable ParseAtomicItem(TokenStream tokens, int indention)
		{
			tokens.SkipWhitespace();
			Token token = tokens.Pop();
			if (token.Value == "break") return new BreakStatement(token);
			if (token.Value == "continue") return new ContinueStatement(token);
			if (token.Value == "pass") return new PassStatement(token);
			throw new Exception("wat?");
		}

		private Executable ParseReturn(TokenStream tokens, int indention)
		{
			tokens.SkipWhitespace();
			Token token = tokens.PopExpected("return");
			Expression value = null;
			if (tokens.HasMore && tokens.PeekType() != TokenType.NEWLINE)
			{
				value = ExpressionParser.Parse(tokens);
			}
			return new ReturnStatement(token, value);
		}

		private Executable ParseIfLikeThing(TokenStream tokens, int currentIndention)
		{
			// This is used for if, elif, else, while, and for, because they are all similar.
			Token token = tokens.Pop();
			string tokenValue = token.Value;
			Expression condition = null;
			Token forIterator = null;
			if (tokenValue == "for")
			{
				forIterator = tokens.Pop();
				if (!Util.IsIdentifier(forIterator)) throw new ParserException(forIterator, "Expected variable name.");
				tokens.PopExpected("in");
			}
			if (tokenValue != "else")
			{
				condition = ExpressionParser.Parse(tokens);
			}
			tokens.PopExpected(":");
			IList<Executable> body = this.ParseBlock(tokens, currentIndention, false);

			if (tokenValue == "for") return new ForEachLoop(token, forIterator, condition, body);
			if (tokenValue == "while") return new WhileLoop(token, condition, body);

			return new IfRawComponent(token, condition, body);
		}

		private Executable ParseClass(TokenStream tokens, int currentIndention)
		{
			Token classToken = tokens.PopExpected("class");
			Token nameToken = tokens.Pop();
			if (!Util.IsIdentifier(nameToken)) throw new ParserException(nameToken, "Invalid class name.");
			Token baseClassName = null;
			if (tokens.PopIfPresent("("))
			{
				baseClassName = tokens.Pop();
				if (!Util.IsIdentifier(baseClassName)) throw new ParserException(baseClassName, "Invalid base class name.");
				tokens.PopExpected(")");
			}
			tokens.PopExpected(":");
			IList<Executable> members = this.ParseBlock(tokens, currentIndention, false);
			List<Executable> membersFiltered = new List<Executable>();
			foreach (Executable member in members)
			{
				if (member is PassStatement)
				{
					// this is fine.
				}
				else if (!(member is FunctionDefinition))
				{
					throw new ParserException(member.FirstToken, "Non function members of classes are not supported yet.");
				}
				else
				{
					membersFiltered.Add(member);
				}
			}

			return new ClassDefinition(classToken, nameToken, baseClassName, membersFiltered);
		}

		private Executable ParseDef(TokenStream tokens, int currentIndent)
		{
			Token defToken = tokens.PopExpected("def");
			Token nameToken = tokens.Pop();
			if (!Util.IsIdentifier(nameToken))
			{
				throw new ParserException(nameToken, "Invalid function name.");
			}

			tokens.PopExpected("(");
			List<Token> args = new List<Token>();
			List<Expression> argValues = new List<Expression>();
			while (!tokens.PopIfPresent(")"))
			{
				if (args.Count > 0)
				{
					tokens.PopExpected(",");
				}
				Token argToken = tokens.Pop();
				if (!Util.IsIdentifier(argToken)) throw new ParserException(argToken, "Invalid argument name.");
				Expression argValue = null;
				if (tokens.PopIfPresent("="))
				{
					argValue = ExpressionParser.Parse(tokens);
				}
				args.Add(argToken);
				argValues.Add(argValue);
			}
			tokens.PopExpected(":");

			IList<Executable> body = this.ParseBlock(tokens, currentIndent, false);
			return new FunctionDefinition(defToken, nameToken, args, argValues, body);
		}

		public Executable[] ParseCode(TokenStream tokens)
		{
			return ParseBlock(tokens, 0, true).ToArray();
		}

		// YOU LEFT OFF HERE
		// You were about to go through and document exactly what each indention variable meant more clearly.
		private IList<Executable> ParseBlock(TokenStream tokens, int ownerIndention, bool start)
		{
			int blockIndention = tokens.PeekIndention();
			if (start)
			{
				if (blockIndention != 0)
				{
					throw new ParserException(tokens.Peek(), "Unexpected indention");
				}
			}
			else
			{
				if (blockIndention == -1)
				{
					// This indicates the code is on the same line. Parse one line.
					// def foo(): return 42
					Executable exec = this.Parse(tokens, false, -1);
					return new List<Executable>() { exec };
				}

				if (blockIndention <= ownerIndention)
				{
					// No indention was found. But it is required.
					throw new ParserException(tokens.Peek(), "Expected: indention");
				}
			}

			int requiredIndention = blockIndention;
			
			List<Executable> code = new List<Executable>();
			while (tokens.HasMore)
			{
				int currentIndention = tokens.PeekIndention();

				// any new indention should be handled by a recursive call
				if (currentIndention > requiredIndention) throw new ParserException(tokens.Peek(), "Unexpected indention");

				// if it's indented less than the required but more than the previous, then that's not right
				// e.g.
				// def foo()
				//     x = 1
				//   return x # this is wrong
				if (currentIndention < requiredIndention && currentIndention > ownerIndention) throw new ParserException(tokens.Peek(), "Unexpected indention");

				// def foo()
				//     x = 42
				// y = 3.14 # this is no longer part of foo()
				// start is excluded because when start is true, the owner indention and current indention are the same.
				if (!start && currentIndention <= ownerIndention) return code;

				tokens.SkipWhitespace();
				if (tokens.HasMore)
				{
					code.Add(this.Parse(tokens, true, currentIndention));
				}
				else
				{
					return code;
				}
			}
			return code;
		}

		// all tabs have been canonicalized to 8 spaces in the tokenizer before this point.
		private static int DELETE_ME_GetIndention(string maybeWhitespace)
		{
			for (int i = 0; i < maybeWhitespace.Length; ++i)
			{
				if (maybeWhitespace[i] != ' ') return -1;
			}
			return maybeWhitespace.Length;
		}
	}
}
