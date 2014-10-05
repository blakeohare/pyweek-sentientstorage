using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class SystemFunctionInvocation : Expression 
	{
		public Token Root { get; private set; }
		public string Name { get; private set; }
		public Expression[] Args { get; private set; }

		public SystemFunctionInvocation(Token prefix, Token root, IList<Expression> args)
			: base(prefix)
		{
			this.Root = root;
			this.Name = root.Value;
			this.Args = args.ToArray();
		}

		public override Expression Resolve()
		{
			for (int i = 0; i < this.Args.Length; ++i)
			{
				this.Args[i] = this.Args[i].Resolve();
			}
			return this;
		}
	}
}
