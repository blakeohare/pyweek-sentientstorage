using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class ForLoop : Executable
	{
		public Executable[] Init { get; private set; }
		public Expression Condition { get; private set; }
		public Executable[] Step { get; private set; }
		public Executable[] Body { get; private set; }
		public ForEachLoop OriginalForEachLoop { get; private set; }

		public ForLoop(Token forToken, ForEachLoop originalForEachLoop, IList<Executable> init, Expression condition, IList<Executable> step, IList<Executable> body)
			: base(forToken)
		{
			this.Init = init.ToArray();
			this.Condition = condition;
			this.Step = step.ToArray();
			this.Body = body.ToArray();
			this.OriginalForEachLoop = originalForEachLoop;
		}

		public override IList<Executable> Resolve()
		{
			this.Init = ResolveBlock(this.Init);
			this.Condition = this.Condition.Resolve();
			this.Step = ResolveBlock(this.Step);
			this.Body = ResolveBlock(this.Body);
			return Listify(this);
		}
	}
}
