using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class ExpressionAsExecutable : Executable
	{
		public Expression Expression { get; private set; }

		public ExpressionAsExecutable(Expression expression)
			: base(expression.FirstToken)
		{
			this.Expression = expression;
		}

		public override IList<Executable> Resolve()
		{
			this.Expression = this.Expression.Resolve();
			return Listify(this);
		}
	}
}
