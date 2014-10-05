using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class NullConstant : Expression
	{
		public NullConstant(Token token)
			: base(token)
		{ }

		public override Expression Resolve()
		{
			return this;
		}
	}
}
