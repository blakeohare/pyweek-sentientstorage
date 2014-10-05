using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon
{
	internal class ParserException : Exception
	{
		private static string GetTokenInfo(Token token)
		{
			if (token == null) return "[No token info] ";
			return token.File + ", Line " + (token.Line + 1) + ", Col " + (token.Col + 1) + " ";
		}

		public ParserException(Token token, string message) : base(GetTokenInfo(token) + message)
		{

		}
	}
}
