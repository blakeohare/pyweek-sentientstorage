using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Python2Crayon.ParseTree;

namespace Python2Crayon.Serialization
{
	internal class CrayonPrimitiveMethods : AbstractPrimitiveMethodSerializer
	{
		public CrayonPrimitiveMethods(CrayonSerializer serializer) : base(serializer) { }

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

		protected override void X_DictionarySize(List<string> output, ParseTree.Expression dict)
		{
			throw new NotImplementedException();
		}

		protected override void X_DrawEllipse(List<string> output, ParseTree.Expression screen, ParseTree.Expression left, ParseTree.Expression top, ParseTree.Expression width, ParseTree.Expression height, ParseTree.Expression red, ParseTree.Expression green, ParseTree.Expression blue)
		{
			output.Add("$gfx_draw_ellipse(");
			SerializeExpression(output, left);
			output.Add(", ");
			SerializeExpression(output, top);
			output.Add(", ");
			SerializeExpression(output, width);
			output.Add(", ");
			SerializeExpression(output, height);
			output.Add(", ");
			SerializeExpression(output, red);
			output.Add(", ");
			SerializeExpression(output, green);
			output.Add(", ");
			SerializeExpression(output, blue);
			output.Add(", 255)");
			
		}

		protected override void X_DrawRectangle(List<string> output, ParseTree.Expression screen, ParseTree.Expression left, ParseTree.Expression top, ParseTree.Expression width, ParseTree.Expression height, ParseTree.Expression red, ParseTree.Expression green, ParseTree.Expression blue)
		{
			output.Add("$gfx_draw_rectangle(");
			SerializeExpression(output, left);
			output.Add(", ");
			SerializeExpression(output, top);
			output.Add(", ");
			SerializeExpression(output, width);
			output.Add(", ");
			SerializeExpression(output, height);
			output.Add(", ");
			SerializeExpression(output, red);
			output.Add(", ");
			SerializeExpression(output, green);
			output.Add(", ");
			SerializeExpression(output, blue);
			output.Add(", 255)");
		}

		protected override void X_DrawTriangle(List<string> output, Expression screen, Expression x1, Expression y1, Expression x2, Expression y2, Expression x3, Expression y3, Expression red, Expression green, Expression blue)
		{
			output.Add("CRAYON_BUG_WORKAROUND_BLARG = 12345");
		}

		protected override void X_ImageBlit(List<string> output, ParseTree.Expression screen, ParseTree.Expression image, ParseTree.Expression x, ParseTree.Expression y)
		{
			output.Add("$gfx_blit_image(");
			SerializeExpression(output, image);
			output.Add(", $floor(");
			SerializeExpression(output, x);
			output.Add("), $floor(");
			SerializeExpression(output, y);
			output.Add("))");
		}

		protected override void X_ImageHeight(List<string> output, ParseTree.Expression image)
		{
			SerializeExpression(output, image);
			output.Add(".height");
		}

		protected override void X_ImageWidth(List<string> output, ParseTree.Expression image)
		{
			SerializeExpression(output, image);
			output.Add(".width");
		}

		protected override void X_Int(List<string> output, ParseTree.Expression num)
		{
			// Blarg blarg blarg blarg. Just remember that this is round down floor() and not decimal truncation int().
			output.Add("$floor(");
			SerializeExpression(output, num);
			output.Add(")");
		}

		protected override void X_ListAdd(List<string> output, ParseTree.Expression list, ParseTree.Expression value)
		{
			SerializeExpression(output, list);
			output.Add(".add(");
			SerializeExpression(output, value);
			output.Add(")");
		}

		protected override void X_ListJoin(List<string> output, ParseTree.Expression list, ParseTree.Expression sep)
		{
			SerializeExpression(output, list);
			output.Add(".join(");
			SerializeExpression(output, sep);
			output.Add(")");
		}

		protected override void X_ListLength(List<string> output, ParseTree.Expression list)
		{
			SerializeExpression(output, list);
			output.Add(".length");
		}

		protected override void X_ListRemove(List<string> output, Expression list, Expression index)
		{
			SerializeExpression(output, list);
			output.Add(".remove(");
			SerializeExpression(output, index);
			output.Add(")");
		}

		protected override void X_ListShuffle(List<string> output, ParseTree.Expression list)
		{
			SerializeExpression(output, list);
			output.Add(".shuffle()");
		}

		protected override void X_MathAbs(List<string> output, ParseTree.Expression num)
		{
			output.Add("$abs(");
			SerializeExpression(output, num);
			output.Add(")");
		}

		protected override void X_MathSin(List<string> output, ParseTree.Expression theta)
		{
			output.Add("$sin(");
			SerializeExpression(output, theta);
			output.Add(")");
		}

		protected override void X_MusicPlay(List<string> output, Expression song)
		{
			output.Add("$abs(0)"); // TODO: music in Crayon
		}

		protected override void X_ParseInt(List<string> output, ParseTree.Expression value)
		{
			output.Add("$parse_int(");
			SerializeExpression(output, value);
			output.Add(")");
		}

		protected override void X_Print(List<string> output, ParseTree.Expression value)
		{
			output.Add("$print(");
			SerializeExpression(output, value);
			output.Add(")");
		}

		protected override void X_ScreenFill(List<string> output, ParseTree.Expression screen, ParseTree.Expression red, ParseTree.Expression green, ParseTree.Expression blue)
		{
			output.Add("$gfx_fill_screen(");
			SerializeExpression(output, red);
			output.Add(", ");
			SerializeExpression(output, green);
			output.Add(", ");
			SerializeExpression(output, blue);
			output.Add(")");
		}

		protected override void X_Str(List<string> output, Expression value)
		{
			output.Add("('' + (");
			SerializeExpression(output, value);
			output.Add("))");
		}

		protected override void X_StringLength(List<string> output, ParseTree.Expression str)
		{
			SerializeExpression(output, str);
			output.Add(".length");
		}

		protected override void X_StringLower(List<string> output, ParseTree.Expression str)
		{
			SerializeExpression(output, str);
			output.Add(".lower()");
		}

		protected override void X_StringSplit(List<string> output, ParseTree.Expression str, ParseTree.Expression sep)
		{
			SerializeExpression(output, str);
			output.Add(".split(");
			SerializeExpression(output, sep);
			output.Add(")");
		}

		protected override void X_StringTrim(List<string> output, ParseTree.Expression str)
		{
			SerializeExpression(output, str);
			output.Add(".trim()");
		}

		protected override void X_StringUpper(List<string> output, ParseTree.Expression str)
		{
			SerializeExpression(output, str);
			output.Add(".upper()");
		}
	}
}
