using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class StringConstant : Expression
	{
		public string Value { get; private set; }

		public StringConstant(Token token, string value)
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
