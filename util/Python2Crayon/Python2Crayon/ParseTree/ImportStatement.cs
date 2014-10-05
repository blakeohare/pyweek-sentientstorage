using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class ImportStatement : Executable
	{
		public Token Target { get; private set; }

		public Token[] ImportChain { get; private set; }
		public Token[] FromChain { get; private set; }
		public Token AsValue { get; private set; }

		public ImportStatement(Token importToken, IList<Token> importChain, IList<Token> fromChain, Token asValue)
			: base(importToken)
		{
			this.ImportChain = importChain.ToArray();
			this.FromChain = fromChain == null ? null : fromChain.ToArray();
			this.AsValue = asValue;
		}

		public override IList<Executable> Resolve()
		{
			// imports are all done in the header.
			return EMPTY_LIST;
		}
	}
}
