using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class BooleanCombinator : Expression
	{
		public Expression Left { get; private set; }
		public Expression Right { get; private set; }
		public bool IsAnd { get; private set; }
		public BooleanCombinator(Expression left, Expression right, string type)
			: base(left.FirstToken)
		{
			this.IsAnd = type == "and";
			this.Left = left;
			this.Right = right;
		}

		public override Expression Resolve()
		{
			this.Left = this.Left.Resolve();
			this.Right = this.Right.Resolve();
			// TODO: resolve boolean constants
			return this;
		}
	}
}
