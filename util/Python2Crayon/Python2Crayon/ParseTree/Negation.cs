using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class Negation : Expression
	{
		public Expression Root { get; private set; }
		public Token Op { get; private set; }
		public PrefixType Type { get; private set; }
		
		public enum PrefixType 
		{
			POSITIVE,
			NEGATIVE,
			BITWISE_NOT,
			BOOLEAN_NOT
		}

		public Negation(Token token, Expression root, PrefixType type)
			: base(token)
		{
			this.Op = token;
			this.Root = root;
			this.Type = type;
		}

		public override Expression Resolve()
		{
			this.Root = this.Root.Resolve();

			if (this.Type == PrefixType.POSITIVE) return this.Root; // technically this should throw on non number types, but this operator is useless so I'm trimming it, thus letting things like +"string" through.
			else if (this.Type == PrefixType.NEGATIVE)
			{
				if (this.Root is IntegerConstant)
				{
					IntegerConstant root = (IntegerConstant)this.Root;
					return new IntegerConstant(root.FirstToken, -root.Value);
				}
				else if (this.Root is FloatConstant)
				{
					FloatConstant root = (FloatConstant)this.Root;
					return new FloatConstant(root.FirstToken, -root.Value);
				}
			}
			else if (this.Type == PrefixType.BOOLEAN_NOT)
			{
				if (this.Root is BooleanConstant)
				{
					return new BooleanConstant(this.FirstToken, !((BooleanConstant)this.Root).Value);
				}
			}

			return this;
		}
	}
}
