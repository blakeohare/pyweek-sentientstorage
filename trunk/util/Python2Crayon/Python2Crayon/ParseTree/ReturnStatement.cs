using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	class ReturnStatement : Executable
	{
		public Expression Value { get; private set; }

		public ReturnStatement(Token token, Expression value)
			: base(token)
		{
			this.Value = value;
		}

		public override IList<Executable> Resolve()
		{
			if (this.Value == null)
			{
				this.Value = new NullConstant(null);
			}

			this.Value = this.Value.Resolve();

			return Listify(this);
		}
	}
}
