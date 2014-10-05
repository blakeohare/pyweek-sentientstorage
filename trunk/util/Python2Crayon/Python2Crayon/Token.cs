using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon
{
	internal enum TokenType {
		NEWLINE,
		INDENT,
		STRING,
		ALPHANUM,
		OTHER
	}

	internal class Token
	{
		private static string sillyCache = " ";
		private static Dictionary<int, string> indentCache = new Dictionary<int, string>();
		public static string GetSpaces(int length)
		{
			string output;
			if (!indentCache.TryGetValue(length, out output))
			{
				while (sillyCache.Length < length)
				{
					sillyCache += sillyCache;
				}
				output = sillyCache.Substring(0, length);
				indentCache[length] = output;
			}
			return output;
		}

		public int Line { get; private set; }
		public int Col { get; private set; }
		public string Value { get; set; }
		public string File { get; private set; }
		public TokenType Type { get; private set; }

		public Token(string value, string file, int line, int col, TokenType type)
		{
			this.File = file;
			this.Value = value;
			this.Line = line;
			this.Col = col;
			this.Type = type;
		}

		public override string ToString()
		{
			string value = this.Value;
			if (this.Type == TokenType.NEWLINE) value = "\\n";
			else if (this.Type == TokenType.INDENT) value = "INDENT x " + this.Value.Length;

			return value + " : Line " + (this.Line + 1) + ", Col " + (this.Col + 1);
		}
	}
}
