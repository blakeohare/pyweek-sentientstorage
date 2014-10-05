using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	class PassStatement : Executable
	{
		public PassStatement(Token token) : base(token) { }

		public override IList<Executable> Resolve()
		{
			return EMPTY_LIST;
		}
	}
}
