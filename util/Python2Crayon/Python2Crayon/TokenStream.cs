using System.Collections.Generic;
using System.Linq;

namespace Python2Crayon
{
	internal class TokenStream
	{
		private Token[] tokens;
		private int index;
		private int length;

		public TokenStream(IList<Token> tokens)
		{
			tokens = ScrubEmptyLines(tokens);
			tokens = ConsolidateIsNot(tokens);
			this.tokens = tokens.ToArray();

			this.index = 0;
			this.length = tokens.Count;
		}

		// convert "is not" and "not in" into single tokens as this greatly simplifies parsing.
		private static IList<Token> ConsolidateIsNot(IList<Token> tokens)
		{
			List<Token> output = new List<Token>();
			string value;
			Token token;
			for (int i = 0; i < tokens.Count; ++i)
			{
				token = tokens[i];
				value = token.Value;
				if (value == "is")
				{
					if (i + 1 < tokens.Count && tokens[i + 1].Value == "not")
					{
						token.Value += " not";
						i++;
					}
				}
				else if (value == "not")
				{
					if (i + 1 < tokens.Count && tokens[i + 1].Value == "in")
					{
						token.Value += " in";
						i++;
					}

				}
				output.Add(token);
			}
			return output;
		}

		private static IList<Token> ScrubEmptyLines(IList<Token> tokens)
		{
			List<Token> output = new List<Token>();
			int length = tokens.Count;
			bool skip ;
			for (int i = 0; i < length; ++i)
			{
				skip = false;
				if (i + 1 < length)
				{
					Token a = tokens[i];
					Token b = tokens[i + 1];
					if (b.Type == TokenType.NEWLINE)
					{
						if (a.Type == TokenType.INDENT)
						{
							skip = true;
							i++;
						}
						else if (a.Type == TokenType.NEWLINE)
						{
							skip = true;
						}
					}
				}

				if (!skip)
				{
					output.Add(tokens[i]);
				}
			}
			return output;
		}

		public Token Peek() { return this.HasMore ? this.tokens[this.index] : null; }
		public Token Pop() { return this.HasMore ? this.tokens[this.index++] : null; }
		public TokenType PeekType() { return this.HasMore ? this.Peek().Type : TokenType.NEWLINE; }
		public string PeekValue() { return this.HasMore ? this.tokens[this.index].Value : null; }
		public string PopValue() { return this.HasMore ? this.tokens[this.index++].Value : null; }
		public bool IsNext(string value) { return this.PeekValue() == value; }
		public bool HasMore { get { return this.index < this.length; } }

		public bool PopIfPresent(string value)
		{
			if (this.IsNext(value))
			{
				this.index++;
				return true;
			}
			return false;
		}

		public Token PopExpected(string value)
		{
			Token output = this.Pop();
			if (output == null)
			{
				throw new ParserException(null, "Unexpected EOF");
			}
			else if (output.Value != value)
			{
				throw new ParserException(output, "Unexpected token. Expected: '" + value + "', Actual: '" + output.Value + "'");
			}
			return output;
		}

		public int PeekIndention()
		{
			if (this.index >= this.length) return -1;
			Token next = this.tokens[this.index];
			if (next.Type == TokenType.INDENT) return next.Value.Length;
			if (next.Type == TokenType.NEWLINE)
			{
				if (this.index + 1 < this.length)
				{
					next = this.tokens[this.index + 1];
					if (next.Type == TokenType.INDENT)
					{
						return next.Value.Length;
					}
				}
			}

			return -1;
		}

		public void SkipWhitespace()
		{
			while (true)
			{
				Token next = this.Peek();
				if (next == null) return;
				if (next.Type != TokenType.INDENT && next.Type != TokenType.NEWLINE) return;
				++this.index;
			}
		}
	}
}
