using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class ComparisonChain : Expression
	{
		public Expression[] Expressions { get; private set; }
		public Token[] OpTokens { get; private set; }

		public ComparisonChain(IList<Expression> expressions, IList<Token> ops)
			: base(expressions[0].FirstToken)
		{
			this.Expressions = expressions.ToArray();
			this.OpTokens = ops.ToArray();
		}

		public override Expression Resolve()
		{
			for (int i = 0; i < this.Expressions.Length; ++i)
			{
				this.Expressions[i] = this.Expressions[i].Resolve();
			}

			for (int i = 1; i < this.Expressions.Length - 1; ++i)
			{
				if (!this.IsSimpleEnough(this.Expressions[i]))
				{
					throw new ParserException(this.Expressions[i].FirstToken,
						"Complex expressions are not allowed as the inner elements of comparison chains. " +
						"This is because this expression must be expanded from e.g. a < b < c to a < b && b < c, " +
						"thus causing inner elements to be invoked multiple times.");
				}
			}

			List<Expression> output = new List<Expression>();

			for (int i = 0; i < this.Expressions.Length - 1; ++i)
			{
				Expression left = this.Expressions[i];
				Expression right = this.Expressions[i + 1];
				Expression single = new BinaryOpChain(new Expression[] { left, right }, new Token[] { this.OpTokens[i] });
				output.Add(single);
			}

			if (output.Count == 1) return output[0];
			List<Token> andTokens = new List<Token>();
			while (andTokens.Count < output.Count - 1)
			{
				andTokens.Add(new Token("and", null, 0, 0, TokenType.ALPHANUM));
			}
			return new BinaryOpChain(output, andTokens);
		}

		private bool IsSimpleEnough(Expression exp)
		{
			if (exp is NullConstant ||
				exp is BooleanConstant ||
				exp is IntegerConstant ||
				exp is FloatConstant ||
				exp is StringConstant ||
				exp is Variable)
			{
				return true;
			}

			if (exp is DotField)
			{
				return IsSimpleEnough(((DotField)exp).Root);
			}

			if (exp is IndexExpression)
			{
				return
					IsSimpleEnough(((IndexExpression)exp).Root) &&
					IsSimpleEnough(((IndexExpression)exp).Index);
			}

			return false;
		}
	}
}
