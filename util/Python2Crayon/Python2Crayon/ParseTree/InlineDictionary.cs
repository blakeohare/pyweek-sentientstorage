using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class InlineDictionary : Expression
	{
		public Expression[] Keys { get; private set; }
		public Expression[] Values { get; private set; }
		public InlineDictionary(Token braceToken, IList<Expression> keys, IList<Expression> values)
			: base(braceToken)
		{
			this.Keys = keys.ToArray();
			this.Values = values.ToArray();
		}

		public override Expression Resolve()
		{
			int size = this.Keys.Length;

			for (int i = 0; i < size; ++i)
			{
				this.Keys[i] = this.Keys[i].Resolve();
				this.Values[i] = this.Values[i].Resolve();
			}

			return this;
		}
	}
}
