using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	class FunctionDefinition : Executable
	{
		public Token NameToken { get; private set; }
		public string Name { get; private set; }
		public Token[] ArgNameTokens { get; private set; }
		public Expression[] ArgDefaultValues { get; private set; }
		public Executable[] Body { get; private set; }

		public FunctionDefinition(Token defToken, Token nameToken, IList<Token> argNames, IList<Expression> argValues, IList<Executable> body)
			: base(defToken)
		{
			this.NameToken = NameToken;
			this.Name = nameToken.Value;
			this.ArgNameTokens = argNames.ToArray();
			this.ArgDefaultValues = argValues.ToArray();
			this.Body = body.ToArray();
		}

		public override IList<Executable> Resolve()
		{
			for (int i = 0; i < this.ArgDefaultValues.Length; ++i)
			{
				Expression arg = this.ArgDefaultValues[i];
				if (arg != null)
				{
					this.ArgDefaultValues[i] = arg.Resolve();
				}
			}

			this.Body = ResolveBlock(this.Body);
			return Listify(this);
		}
	}
}
