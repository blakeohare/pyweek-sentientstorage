using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class IfStatement : Executable
	{
		public Token IfToken { get; private set; }
		public Expression Condition { get; private set; }
		public Executable[] TrueCode { get; private set; }
		public Executable[] FalseCode { get; private set; }

		public IfStatement(Token ifToken, Expression condition, IList<Executable> trueCode)
			: base(ifToken)
		{
			this.IfToken = ifToken;
			this.Condition = condition;
			this.TrueCode = trueCode.ToArray();
			this.FalseCode = EMPTY_LIST;
		}

		public void SetFalseCode(IList<Executable> falseCode)
		{
			this.FalseCode = falseCode.ToArray();
		}

		public override IList<Executable> Resolve()
		{
			this.Condition = this.Condition.Resolve();
			this.TrueCode = ResolveBlock(this.TrueCode);
			this.FalseCode = ResolveBlock(this.FalseCode);

			if (this.Condition is BooleanConstant)
			{
				return ((BooleanConstant)this.Condition).Value
					? this.TrueCode
					: this.FalseCode;
			}

			return Listify(this);
		}
	}
}
