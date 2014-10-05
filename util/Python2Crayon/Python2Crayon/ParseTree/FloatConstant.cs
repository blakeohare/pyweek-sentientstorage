using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class FloatConstant : Expression
	{
		public double Value { get; private set; }

		public FloatConstant(Token token, double value)
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
