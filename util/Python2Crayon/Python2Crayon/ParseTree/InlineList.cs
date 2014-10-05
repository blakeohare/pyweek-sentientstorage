using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class InlineList : Expression
	{
		public Expression[] Items { get; private set; }

		public InlineList(Token bracketToken, IList<Expression> items)
			: base(bracketToken)
		{
			this.Items = items.ToArray();
		}

		public override Expression Resolve()
		{
			for (int i = 0; i < this.Items.Length; ++i)
			{
				this.Items[i] = this.Items[i].Resolve();
			}
			return this;
		}
	}
}
