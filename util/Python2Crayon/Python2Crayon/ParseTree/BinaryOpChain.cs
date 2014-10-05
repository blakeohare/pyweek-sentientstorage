using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class BinaryOpChain : Expression
	{
		public Expression[] Expressions { get; private set; }
		public Token[] OpTokens { get; private set; }

		public BinaryOpChain(IList<Expression> expressions, IList<Token> ops)
			: base(expressions[0].FirstToken)
		{
			this.Expressions = expressions.ToArray();
			this.OpTokens = ops.ToArray();
		}

		public override Expression Resolve()
		{
			for (int i = 0; i < this.Expressions.Length; ++i)
			{
				this.Expressions[i] = this.Expressions[i].Resolve();
			}

			return this;
		}
	}
}
