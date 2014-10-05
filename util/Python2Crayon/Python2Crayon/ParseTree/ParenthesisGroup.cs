using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class ParenthesisGroup : Expression
	{
		public Expression InnerExpression { get; private set; }

		public ParenthesisGroup(Token openParen, Expression expr)
			: base(openParen)
		{
			this.InnerExpression = expr;
		}

		public override Expression Resolve()
		{
			this.InnerExpression = this.InnerExpression.Resolve();
			return this;
		}
	}
}
