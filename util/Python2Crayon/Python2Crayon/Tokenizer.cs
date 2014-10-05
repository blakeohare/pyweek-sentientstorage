using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon
{
	class Tokenizer
	{
		private enum State
		{
			PRE_WHITESPACE,
			COMMENT,
			ENTITY,
			STRING,
			RAW_STRING,
			NONE
		}

		private HashSet<string> TWO_CHAR_TOKENS = new HashSet<string>("+= -= *= -= << >> >= <= != == /= &= |= ^= ** // <>".Split(' '));
		private HashSet<string> THREE_CHAR_TOKENS = new HashSet<string>("<<= >>= //= **= ...".Split(' '));
		public TokenStream Tokenize(string filename, string code)
		{
			code = code.Replace("\r\n", "\n").Replace('\r', '\n') + "\n\0";
			int length = code.Length - 1;
			int[] lines = new int[code.Length];
			int[] cols = new int[code.Length];
			int line = 0;
			int col = 0;
			char c;
			for (int i = 0; i < length; ++i)
			{
				lines[i] = line;
				cols[i] = col;
				c = code[i];
				if (c == '\n')
				{
					line++;
					col = 0;
				}
				else
				{
					col++;
				}
			}

			List<Token> tokens = new List<Token>();
			string c1, c2, c3;
			State state = State.PRE_WHITESPACE;
			int indentCount = 0;
			int tokenStart = 0;
			string stringType = null;
			StringBuilder currentToken = new StringBuilder();
			for (int i = 0; i < length; ++i)
			{
				c = code[i];
				c1 = "" + c;
				c2 = i < length - 1 ? code.Substring(i, 2) :null;
				c3 = i < length - 2 ? code.Substring(i, 3) : null;
				if (state == State.PRE_WHITESPACE)
				{
					if (c == ' ') indentCount++;
					else if (c == '\t') indentCount += 8;
					else
					{
						--i;
						state = State.NONE;
						tokens.Add(new Token(Token.GetSpaces(indentCount), filename, lines[tokenStart], cols[tokenStart], TokenType.INDENT));
						indentCount = 0;
					}
				}
				else if (state == State.COMMENT)
				{
					if (c == '\n')
					{
						--i;
						state = State.NONE;
					}
				}
				else if (state == State.STRING || state == State.RAW_STRING)
				{
					if (c1 == stringType || c3 == stringType)
					{
						currentToken.Append(stringType);
						i += stringType.Length - 1;
						state = State.NONE;
						tokens.Add(new Token(currentToken.ToString(), filename, lines[tokenStart], cols[tokenStart], TokenType.STRING));
						currentToken.Clear();
					}
					else
					{
						currentToken.Append(c);
					}
				}
				else if (state == State.ENTITY)
				{
					if ((c >= 'a' && c <= 'z') ||
						(c >= 'A' && c <= 'Z') ||
						(c >= '0' && c <= '9') ||
						c == '_')
					{
						currentToken.Append(c);
					}
					else if (c == '.' && Util.IsNumbers(currentToken.ToString()))
					{
						currentToken.Append(c);
					}
					else
					{
						state = State.NONE;
						tokens.Add(new Token(currentToken.ToString(), filename, lines[tokenStart], cols[tokenStart], TokenType.ALPHANUM));
						currentToken.Clear();
						state = State.NONE;
						--i;
					}
				}
				else if (c == '\n')
				{
					tokens.Add(new Token("\n", filename, lines[i], cols[i], TokenType.NEWLINE));
					state = State.PRE_WHITESPACE;
					tokenStart = i + 1;
				}
				else if (c == '#')
				{
					state = State.COMMENT;
				}
				else if (c == '\'' || c == '"' || 
					(c == 'r' && (c2 == "r'" || c2 == "r\"")))
				{
					state = State.STRING;
					bool raw = c == 'r';
					if (raw)
					{
						string c4 = code.Substring(i, 4);
						if (c4 == "r'''" || c4 == "r\"\"\"")
						{
							stringType = c4.Substring(1);
						}
						else
						{
							stringType = c2.Substring(1);
						}
					}
					else
					{
						if (c3 == "'''" || c3 == "\"\"\"")
						{
							stringType = c3;
						}
						else
						{
							stringType = c1;
						}
					}
					tokenStart = i;
					currentToken.Append(stringType);
					i += stringType.Length - 1;
					if (raw) ++i;
				}
				else if (c == ' ' || c == '\t')
				{
					// do nothing
				}
				else if (c == 'r' && (c2 == "r'" || c2 == "r\""))
				{
					state = State.STRING;
					string c4 = code.Substring(i, 4);
					if (c4 == "r'''" || c4 == "r\"\"\"")
					{
						stringType = c4.Substring(1);
					}
					else
					{
						stringType = c2.Substring(1);
					}
					tokenStart = i;
					currentToken.Append(stringType);
					i += stringType.Length - 1;
				}
				else if (
					(c >= 'a' && c <= 'z') ||
					(c >= 'A' && c <= 'Z') ||
					(c >= '0' && c <= '9') ||
					c == '_')
				{
					state = State.ENTITY;
					tokenStart = i;
					--i;
				}
				else if (TWO_CHAR_TOKENS.Contains(c2))
				{
					tokens.Add(new Token(c2, filename, lines[i], cols[i], TokenType.OTHER));
					++i;
				}
				else if (THREE_CHAR_TOKENS.Contains(c3))
				{
					tokens.Add(new Token(c3, filename, lines[i], cols[i], TokenType.OTHER));
					i += 2;
				}
				else if (c == '.' && c2 != null && Util.IsNumbers(c2.Substring(1)))
				{
					state = State.ENTITY;
					tokenStart = i;
					currentToken.Clear();
					currentToken.Append(".");
				}
				else
				{
					tokens.Add(new Token(c1, filename, lines[i], cols[i], TokenType.OTHER));
				}
			}

			tokens.RemoveAt(tokens.Count - 1);

			return new TokenStream(tokens);
		}
	}
}
