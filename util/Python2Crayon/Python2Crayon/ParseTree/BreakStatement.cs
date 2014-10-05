using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class BreakStatement : Executable
	{
		public BreakStatement(Token token) : base(token) { }

		public override IList<Executable> Resolve() { return Listify(this); }
	}
}
