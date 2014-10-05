using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class IntegerConstant : Expression
	{
		public int Value { get; private set; }

		public IntegerConstant(Token token, int value)
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
