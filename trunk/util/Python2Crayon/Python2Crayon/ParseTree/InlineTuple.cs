using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class InlineTuple : Expression 
	{
		public Expression[] Items { get; private set; }
		public InlineTuple(Token openParen, IList<Expression> items)
			: base(openParen)
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
