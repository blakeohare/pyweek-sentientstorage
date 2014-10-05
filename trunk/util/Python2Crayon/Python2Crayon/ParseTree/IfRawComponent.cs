using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class IfRawComponent : Executable
	{
		public enum ComponentType
		{
			IF,
			ELIF,
			ELSE
		}

		public ComponentType Type { get; private set; }
		public Expression NullableExpression { get; private set; }
		public Executable[] Body { get; private set; }

		public IfRawComponent(Token token, Expression nullableCondition, IList<Executable> body)
			: base(token)
		{
			// I find the following 3 lines mildly humorous.
			if (token.Value == "if") this.Type = ComponentType.IF;
			else if (token.Value == "elif") this.Type = ComponentType.ELIF;
			else this.Type = ComponentType.ELSE;

			this.NullableExpression = nullableCondition;
			this.Body = body.ToArray();
		}

		public override IList<Executable> Resolve()
		{
			throw new InvalidOperationException("If raw components must be resolved out of the parse tree.");
		}
	}
}
