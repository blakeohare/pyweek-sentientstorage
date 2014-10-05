using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class IndexExpression : Expression
	{
		public Expression Root { get; private set; }
		public Token BracketToken { get; private set; }
		public Expression Index { get; private set; }

		public IndexExpression(Expression root, Token bracketToken, Expression index)
			: base(root.FirstToken)
		{
			this.Root = root;
			this.BracketToken = bracketToken;
			this.Index = index;
		}

		public override Expression Resolve()
		{
			this.Root = this.Root.Resolve();
			this.Index = this.Index.Resolve();
			return this;
		}
	}
}
