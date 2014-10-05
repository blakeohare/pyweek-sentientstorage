using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class Ternary :Expression
	{
		public Expression Condition { get; private set; }
		public Expression TrueExpression { get; private set; }
		public Expression FalseExpression { get; private set; }

		public Ternary(Expression condition, Expression trueCode, Expression falseCode)
			: base(trueCode.FirstToken)
		{
			this.TrueExpression = trueCode;
			this.FalseExpression = falseCode;
			this.Condition = condition;
		}

		public override Expression Resolve()
		{
			this.Condition = this.Condition.Resolve();
			this.TrueExpression = this.TrueExpression.Resolve();
			this.FalseExpression = this.FalseExpression.Resolve();
			return this;
		}
	}
}
