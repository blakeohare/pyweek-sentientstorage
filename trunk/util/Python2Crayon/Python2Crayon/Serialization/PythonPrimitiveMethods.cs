using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Python2Crayon	.ParseTree;

namespace Python2Crayon.Serialization
{
	internal class PythonPrimitiveMethods : AbstractPrimitiveMethodSerializer
	{
		public PythonPrimitiveMethods(PythonSerializer serializer) : base(serializer) { }

		protected override void X_DictionaryGetWithDefault(List<string> output, Expression dictionary, Expression key, Expression defaultValue)
		{
			SerializeExpression(output, dictionary);
			output.Add(".get(");
			SerializeExpression(output, key);
			output.Add(", ");
			SerializeExpression(output, defaultValue);
			output.Add(")");
		}

		protected override void X_DictionaryKeys(List<string> output, Expression dict)
		{
			SerializeExpression(output, dict);
			output.Add(".keys()");
		}

		protected override void X_DictionarySize(List<string> output, Expression dict)
		{
			throw new NotImplementedException();
		}

		protected override void X_DrawEllipse(List<string> output, Expression screen, Expression left, Expression top, Expression width, Expression height, Expression red, Expression green, Expression blue)
		{
			output.Add("pygame.draw.ellipse(");
			SerializeExpression(output, screen);
			output.Add(", (");
			SerializeExpression(output, red);
			output.Add(", ");
			SerializeExpression(output, green);
			output.Add(", ");
			SerializeExpression(output, blue);
			output.Add("), pygame.Rect(");
			SerializeExpression(output, left);
			output.Add(", ");
			SerializeExpression(output, top);
			output.Add(", ");
			SerializeExpression(output, width);
			output.Add(", ");
			SerializeExpression(output, height);
			output.Add("))");
		}

		protected override void X_DrawRectangle(List<string> output, ParseTree.Expression screen, ParseTree.Expression left, ParseTree.Expression top, ParseTree.Expression width, ParseTree.Expression height, ParseTree.Expression red, ParseTree.Expression green, ParseTree.Expression blue)
		{
			// TODO: need to run this through a helper function to avoid 1-height bugs
			output.Add("pygame.draw.rect(");
			SerializeExpression(output, screen);
			output.Add(", (");
			SerializeExpression(output, red);
			output.Add(", ");
			SerializeExpression(output, green);
			output.Add(", ");
			SerializeExpression(output, blue);
			output.Add("), pygame.Rect(");
			SerializeExpression(output, left);
			output.Add(", ");
			SerializeExpression(output, top);
			output.Add(", ");
			SerializeExpression(output, width);
			output.Add(", ");
			SerializeExpression(output, height);
			output.Add("))");
		}

		protected override void X_DrawTriangle(List<string> output, Expression screen, Expression x1, Expression y1, Expression x2, Expression y2, Expression x3, Expression y3, Expression red, Expression green, Expression blue)
		{
			output.Add("pygame.draw.polygon(");
			SerializeExpression(output, screen);
			output.Add(", (");
			SerializeExpression(output, red);
			output.Add(", ");
			SerializeExpression(output, green);
			output.Add(", ");
			SerializeExpression(output, blue);
			output.Add("), ((");
			SerializeExpression(output, x1);
			output.Add(", ");
			SerializeExpression(output, y1);
			output.Add("), (");
			SerializeExpression(output, x2);
			output.Add(", ");
			SerializeExpression(output, y2);
			output.Add("), (");
			SerializeExpression(output, x3);
			output.Add(", ");
			SerializeExpression(output, y3);
			output.Add(")))");

		}

		protected override void X_ImageBlit(List<string> output, Expression screen, Expression image, Expression x, Expression y)
		{
			SerializeExpression(output, screen);
			output.Add(".blit(");
			SerializeExpression(output, image);
			output.Add(", (");
			SerializeExpression(output, x);
			output.Add(", ");
			SerializeExpression(output, y);
			output.Add("))");
		}

		protected override void X_ImageHeight(List<string> output, ParseTree.Expression image)
		{
			SerializeExpression(output, image);
			output.Add(".get_height()");
		}

		protected override void X_ImageWidth(List<string> output, ParseTree.Expression image)
		{
			SerializeExpression(output, image);
			output.Add(".get_width()");
		}

		protected override void X_Int(List<string> output, Expression num)
		{
			output.Add("int(");
			SerializeExpression(output, num);
			output.Add(")");
		}

		protected override void X_ListAdd(List<string> output, Expression list, Expression value)
		{
			SerializeExpression(output, list);
			output.Add(".append(");
			SerializeExpression(output, value);
			output.Add(")");
		}

		protected override void X_ListJoin(List<string> output, Expression list, Expression sep)
		{
			SerializeExpression(output, sep);
			output.Add(".join(");
			SerializeExpression(output, list);
			output.Add(")");
		}

		protected override void X_ListRemove(List<string> output, Expression list, Expression index)
		{
			SerializeExpression(output, list);
			output.Add(".pop(");
			SerializeExpression(output, index);
			output.Add(")");
		}

		protected override void X_ListLength(List<string> output, Expression list)
		{
			output.Add("len(");
			SerializeExpression(output, list);
			output.Add(")");
		}

		protected override void X_ListShuffle(List<string> output, Expression list)
		{
			output.Add("random.shuffle(");
			SerializeExpression(output, list);
			output.Add(")");
		}

		protected override void X_MathAbs(List<string> output, ParseTree.Expression num)
		{
			output.Add("abs(");
			SerializeExpression(output, num);
			output.Add(")");
		}

		protected override void X_MathSin(List<string> output, ParseTree.Expression theta)
		{
			output.Add("math.sin(");
			SerializeExpression(output, theta);
			output.Add(")");
		}

		protected override void X_MusicPlay(List<string> output, Expression song)
		{
			output.Add("play_music(");
			SerializeExpression(output, song);
			output.Add(")");
		}

		protected override void X_ParseInt(List<string> output, Expression value)
		{
			output.Add("int(");
			SerializeExpression(output, value);
			output.Add(")");
		}

		protected override void X_Print(List<string> output, Expression value)
		{
			output.Add("print(");
			SerializeExpression(output, value);
			output.Add(")");
		}

		protected override void X_ScreenFill(List<string> output, Expression screen, Expression red, Expression green, Expression blue)
		{
			SerializeExpression(output, screen);
			output.Add(".fill((");
			SerializeExpression(output, red);
			output.Add(", ");
			SerializeExpression(output, green);
			output.Add(", ");
			SerializeExpression(output, blue);
			output.Add("))");
		}

		protected override void X_Str(List<string> output, Expression value)
		{
			output.Add("str(");
			SerializeExpression(output, value);
			output.Add(")");
		}

		protected override void X_StringLength(List<string> output, Expression str)
		{
			output.Add("len(");
			SerializeExpression(output, str);
			output.Add(")");
		}

		protected override void X_StringLower(List<string> output, Expression str)
		{
			SerializeExpression(output, str);
			output.Add(".lower()");
		}

		protected override void X_StringSplit(List<string> output, Expression str, Expression sep)
		{
			SerializeExpression(output, str);
			output.Add(".split(");
			SerializeExpression(output, sep);
			output.Add(")"); 
		}

		protected override void X_StringTrim(List<string> output, Expression str)
		{
			SerializeExpression(output, str);
			output.Add(".strip()");
		}

		protected override void X_StringUpper(List<string> output, Expression str)
		{
			SerializeExpression(output, str);
			output.Add(".upper()");
		}
	}
}
