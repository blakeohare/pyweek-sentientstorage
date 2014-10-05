using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class WhileLoop : Executable
	{
		public Expression Condition { get; private set; }
		public Executable[] Body { get; private set; }

		public WhileLoop(Token whileToken, Expression condition, IList<Executable> body)
			: base(whileToken)
		{
			this.Condition = condition;
			this.Body = body.ToArray();
		}

		public override IList<Executable> Resolve()
		{
			this.Condition = this.Condition.Resolve();
			this.Body = ResolveBlock(this.Body);
			return Listify(this);
		}
	}
}
