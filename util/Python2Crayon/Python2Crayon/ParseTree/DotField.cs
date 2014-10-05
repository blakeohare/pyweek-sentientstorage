using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class DotField : Expression
	{
		public Expression Root { get; private set; }
		public Token DotToken { get; private set; }
		public Token FieldToken { get; private set; }
		public string FieldName { get; private set; }

		public DotField(Expression root, Token dotToken, Token fieldToken, string fieldName)
			: base(root.FirstToken)
		{
			this.Root = root;
			this.DotToken = dotToken;
			this.FieldToken = fieldToken;
			this.FieldName = fieldName;
		}

		public override Expression Resolve()
		{
			this.Root = this.Root.Resolve();
			return this;
		}
	}
}
