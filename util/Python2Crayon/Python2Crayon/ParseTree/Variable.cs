using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class Variable : Expression
	{
		public string Value { get; private set; }

		public Variable(Token token, string value)
			: base(token)
		{
			this.Value = value;
		}

		public override Expression Resolve()
		{
			return this;
		}
	}
}
