using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class ClassDefinition : Executable
	{
		public Token NameToken { get; private set; }
		public Token BaseClassToken { get; private set; }
		public FunctionDefinition[] Members { get; private set; }

		public ClassDefinition(Token classToken, Token nameToken, Token baseClassToken, IList<Executable> members)
			: base(classToken)
		{
			this.NameToken = nameToken;
			this.BaseClassToken = baseClassToken;
			this.Members = members.OfType<FunctionDefinition>().ToArray();
		}

		public override IList<Executable> Resolve()
		{
			foreach (FunctionDefinition fd in this.Members)
			{
				// because the function definition instance will not change, no need to save a new list.
				fd.Resolve();
			}
			return Listify(this);
		}
	}
}
