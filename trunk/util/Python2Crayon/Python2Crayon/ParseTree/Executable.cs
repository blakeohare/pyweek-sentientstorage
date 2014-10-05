using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Python2Crayon.ParseTree
{
	internal abstract class Executable
	{
		public Token FirstToken { get; private set; }

		public Executable(Token firstToken)
		{
			this.FirstToken = firstToken;
		}

		public abstract IList<Executable> Resolve();

		protected static IList<Executable> Listify(Executable executable)
		{
			return new List<Executable>() { executable };
		}

		protected Executable[] EMPTY_LIST = new Executable[0];

		public static Executable[] ResolveBlock(IList<Executable> code)
		{
			List<Executable> output = new List<Executable>();
			for (int i = 0; i < code.Count; ++i)
			{
				Executable line = code[i];
				if (line is IfRawComponent && ((IfRawComponent)line).Type == IfRawComponent.ComponentType.IF)
				{
					IfRawComponent rawIf = (IfRawComponent)line;
					IfStatement head = null;
					IfStatement tail = null;
					if (rawIf.Type != IfRawComponent.ComponentType.IF)
					{
						throw new ParserException(rawIf.FirstToken, "Unexpected token.");
					}

					head = new IfStatement(rawIf.FirstToken, rawIf.NullableExpression, rawIf.Body);
					tail = head;
					bool keepGoing = true;
					while (keepGoing)
					{
						if (i + 1 < code.Count && code[i + 1] is IfRawComponent)
						{
							++i;
							IfRawComponent consecutiveIfComponent = (IfRawComponent)code[i];
							if (consecutiveIfComponent.Type == IfRawComponent.ComponentType.ELIF)
							{
								IfStatement elifPiece = new IfStatement(consecutiveIfComponent.FirstToken, consecutiveIfComponent.NullableExpression, consecutiveIfComponent.Body);
								tail.SetFalseCode(Listify(elifPiece));
								tail = elifPiece;
							}
							else if (consecutiveIfComponent.Type == IfRawComponent.ComponentType.ELSE)
							{
								tail.SetFalseCode(consecutiveIfComponent.Body);
								keepGoing = false;
								break;
							}
							else
							{
								--i;
								break;
							}
						}
						else
						{
							break;
						}
					}
					line = head;
				}

				output.AddRange(line.Resolve());
			}
			return output.ToArray();
		}
	}
}
