using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class FunctionInvocation : Expression 
	{
		public Expression Root { get; private set; }
		public Expression[] Args { get; private set; }

		public FunctionInvocation(Expression root, IList<Expression> args)
			: base(root.FirstToken)
		{
			this.Root = root;
			this.Args = args.ToArray();
		}

		public override Expression Resolve()
		{
			this.Root = this.Root.Resolve();
			for (int i = 0; i < this.Args.Length; ++i)
			{
				this.Args[i] = this.Args[i].Resolve();
			}
			return this;
		}
	}
}
