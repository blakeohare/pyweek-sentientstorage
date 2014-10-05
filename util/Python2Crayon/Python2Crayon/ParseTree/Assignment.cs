using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class Assignment : Executable
	{
		public Token AssignmentToken { get; private set; }
		public Expression Target { get; private set; }
		public Expression Value { get; private set; }

		public Assignment(Expression target, Token assignmentToken, Expression value)
			: base(target.FirstToken)
		{
			this.AssignmentToken = assignmentToken;
			this.Target = target;
			this.Value = value;
		}

		public override IList<Executable> Resolve()
		{
			this.Value = this.Value.Resolve();
			Expression t = this.Target;
			bool targetValid = true;
			if (t is Variable)
			{
				// nothing to do
			}
			else if (t is DotField)
			{
				DotField dotField = (DotField)t;
				this.Target = dotField.Resolve();
				if (!(this.Target is DotField))
				{
					targetValid = false;
				}
			}
			else if (t is IndexExpression)
			{
				IndexExpression index = (IndexExpression)t;
				this.Target = index.Resolve();
				if (!(this.Target is IndexExpression))
				{
					targetValid = false;
				}
			}
			else
			{
				targetValid = false;
			}

			if (!targetValid)
			{
				throw new ParserException(this.FirstToken, "Invalid target for assignment.");
			}

			return Listify(this);
		}
	}
}
