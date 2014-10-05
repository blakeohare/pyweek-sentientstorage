using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal class ForEachLoop : Executable
	{
		public Token IteratorVariable { get; private set; }
		public Expression IterableExpression { get; private set; }
		public Executable[] Body { get; private set; }
		
		public ForEachLoop(Token forToken, Token iteratorVariable, Expression iterableExpression, IList<Executable> body)
			: base(forToken)
		{
			this.IteratorVariable = iteratorVariable;
			this.IterableExpression = iterableExpression;
			this.Body = body.ToArray();
		}

		// TODO: get rid of this and add support for foreach loops in Crayon
		public override IList<Executable> Resolve()
		{
			this.IterableExpression = this.IterableExpression.Resolve();
			this.Body = ResolveBlock(this.Body);
			FunctionInvocation fi = this.IterableExpression as FunctionInvocation;

			if (fi != null && fi.Root is Variable)
			{
				string functionName = ((Variable)fi.Root).Value;
				if (functionName == "range" || functionName == "xrange")
				{
					if (fi.Args.Length > 0 && fi.Args.Length <= 3)
					{
						return Listify(ResolveWithRange(fi.Args));
					}
				}
			}

			return Listify(this);
		}

		private static int VARIABLE_ALLOCATION_COUNTER = 1;

		private ForLoop ResolveWithRange(Expression[] rangeArgs)
		{
			List<Executable> init = new List<Executable>();

			Expression increment = new IntegerConstant(null, 1);
			if (rangeArgs.Length == 3)
			{
				if (rangeArgs[2] is IntegerConstant || rangeArgs[2] is Variable)
				{
					increment = rangeArgs[2];
				}
				string variableName = "crayon_conversion_step_" + VARIABLE_ALLOCATION_COUNTER++;
				init.Add(new Assignment(new Variable(null, variableName), new Token("=", null, 0, 0, TokenType.OTHER), rangeArgs[2]));
				increment = new Variable(null, variableName);
			}

			Expression start = new IntegerConstant(null, 0);
			// if 2 or 3 are present, then an explicit start is given
			if (rangeArgs.Length > 1)
			{
				start = rangeArgs[0];
			}

			Expression end = null;
			if (rangeArgs.Length == 1)
			{
				end = rangeArgs[0];
			}
			else
			{
				end = rangeArgs[1];
			}

			if (end is IntegerConstant || end is Variable)
			{
				// this is fine
			}
			else
			{
				string variableName = "crayon_conversion_length_" + VARIABLE_ALLOCATION_COUNTER++;
				init.Add(new Assignment(new Variable(null, variableName), new Token("=", null, 0, 0, TokenType.OTHER), end));
				end = new Variable(null, variableName);
			}

			init.Add(new Assignment(new Variable(this.IteratorVariable, this.IteratorVariable.Value), new Token("=", null, 0, 0, TokenType.OTHER), start));
			Expression condition = new BinaryOpChain(
				new Expression[] { 
					new Variable(this.IteratorVariable, this.IteratorVariable.Value), 
					end },
				new Token[] { new Token("<", null, 0, 0, TokenType.OTHER) });

			List<Executable> step = new List<Executable>()
			{
				new Assignment(
					new Variable(this.IteratorVariable, this.IteratorVariable.Value),
					new Token("+=", null, 0, 0, TokenType.OTHER),
					increment)
			};

			return new ForLoop(this.FirstToken, this, init, condition, step, this.Body);
		}
	}
}
