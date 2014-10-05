using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class SliceExpression : Expression
	{
		public Expression Root { get; private set; }
		public Token BracketToken { get; private set; }
		public Expression[] Components { get; private set; }

		public SliceExpression(Expression root, Token bracketToken, IList<Expression> components)
			: base(root.FirstToken)
		{
			this.Root = root;
			this.BracketToken = bracketToken;
			this.Components = components.ToArray();
		}

		public override Expression Resolve()
		{
			this.Root = this.Root.Resolve();
			for (int i = 0; i < this.Components.Length; ++i)
			{
				if (this.Components[i] != null)
				{
					this.Components[i] = this.Components[i].Resolve();
				}
			}
			return this;
		}
	}
}
