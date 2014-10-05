using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Reflection;

namespace Python2Crayon
{
	internal static class Util
	{
		private static readonly HashSet<char> IDENTIFIER_CHARS = new HashSet<char>(
			"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_".ToCharArray());

		public static bool IsIdentifier(Token token)
		{
			string value = token.Value;
			for (int i = value.Length - 1; i >= 0; --i)
			{
				char c = value[i];
				if (i == 0)
				{
					if (c >= '0' && c <= '9') return false;
				}
				if (!IDENTIFIER_CHARS.Contains(c))
				{
					return false;
				}
			}
			return true;
		}

		public static bool IsNumbers(string value)
		{
			char c;
			for (int i = value.Length - 1; i >= 0; --i)
			{
				c = value[i];
				if (c < '0' || c > '9') return false;
			}
			return true;
		}

		private static readonly string NUMBER_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz";
		public static int ParseNumber(Token token, string value, int radix)
		{
			value = value.ToLowerInvariant();
			int output = 0;
			for (int i = 0; i < value.Length; ++i)
			{
				int digitValue = NUMBER_DIGITS.IndexOf(value[i]);
				if (digitValue == -1)
				{
					throw new ParserException(token, "Invalid base " + radix + " constant.");
				}
				output = output * radix + digitValue;
			}
			return output;
		}

		public static double ParseDouble(Token token)
		{
			string[] parts = token.Value.ToLowerInvariant().Split('e');
			if (parts.Length > 2) throw new ParserException(token, "Invalid float constant.");
			string value = parts[0];
			string exponent = parts.Length == 1 ? "1" : parts[1];

			double rootValue;
			if (!double.TryParse(value, out rootValue)) throw new ParserException(token, "Invalid float constant.");
			int exponentValue;
			if (!int.TryParse(exponent, out exponentValue)) throw new ParserException(token, "Invalid float constant.");

			if (rootValue == 0 && exponentValue == 0) return 0.0;

			return System.Math.Pow(rootValue, exponentValue);
		}

		public static string InsertEscapeSequences(string rawValue)
		{
			StringBuilder sb = new StringBuilder();
			char c;
			for (int i = 0; i < rawValue.Length; ++i)
			{
				c = rawValue[i];
				switch (c)
				{
					case '\n': sb.Append("\\n"); break;
					case '\t': sb.Append("\\t"); break;
					case '\\': sb.Append("\\\\"); break;
					case '"': sb.Append("\\\""); break;
					case '\r': sb.Append("\\r"); break;
					case '\0': sb.Append("\\0"); break;
					default: sb.Append(c); break;
				}
			}
			return sb.ToString();
		}

		public static string RemoveEscapeSequences(Token token, string value)
		{
			StringBuilder sb = new StringBuilder();
			char c;
			for (int i = 0; i < value.Length; ++i)
			{
				c = value[i];
				if (c == '\\')
				{
					if (i + 1 < value.Length)
					{
						switch (value[i + 1])
						{
							case 'n': c = '\n'; break;
							case 'r': c = '\r'; break;
							case 't': c = '\t'; break;
							case '\\': c = '\\'; break;
							case '0': c = '\0'; break;
							case '"': c = '"'; break;
							case '\'': c = '\''; break;
							default: throw new ParserException(token, "Invalid escape sequence in string.");
						}
						++i;
					}
					else
					{
						throw new ParserException(token, "Backslash at the end.");
					}
				}

				sb.Append(c);
			}
			return sb.ToString();
		}

		private static string root= null;
		public static string Root
		{
			get
			{
				if (root == null)
				{
					root = System.Environment.GetEnvironmentVariable("PYWEEK19_ROOT");
					if (root == null)
					{
						System.Console.Error.WriteLine("You must set the PYWEEK19_ROOT to the folder of where your SVN is");
						throw new Exception();
					}
				}

				return root;
			}
		}

		public static string ReadFileFromDisk(string path)
		{
			string text = System.IO.File.ReadAllText(System.IO.Path.Combine(Util.Root, path));
			if (text.Length >= 3 && text[0] == 239 && text[1] == 191 && text[2] == 187)
			{
				text = text.Substring(3);
			}
			return text;
		}

		public static void WriteFile(string path, string contents)
		{
			path = System.IO.Path.Combine(Util.Root, path);
			System.IO.File.WriteAllText(path, contents);
		}

		public static string ReadFileFromAssembly(string path)
		{
			Assembly assembly = typeof(Util).Assembly;
			string prefix = assembly.FullName.Split(',')[0];
			string[] foo = assembly.GetManifestResourceNames();
			path = prefix + "." + path.Replace('/', '.');
			System.IO.Stream stream = assembly.GetManifestResourceStream(path);
			StringBuilder sb = new StringBuilder();
			int readValue = 0;
			do
			{
				readValue = stream.ReadByte();
				if (readValue != -1 && readValue != 65535)
				{
					sb.Append((char)readValue);
				}
			} while (readValue != -1 && readValue != 65535);

			string output = sb.ToString();
			if (output.Length >= 3 && output[0] == 239 && output[1] == 187 && output[2] == 191)
			{
				output = output.Substring(3);
			}
			return output;
		}

		public static void SyncDirectories(string fromRoot, string toRoot, ICollection<string> files)
		{
			fromRoot = System.IO.Path.Combine(Util.Root, fromRoot);
			toRoot = System.IO.Path.Combine(Util.Root, toRoot);

			if (System.IO.Directory.Exists(toRoot))
			{
				System.IO.Directory.Delete(toRoot, true);
			}
			System.IO.Directory.CreateDirectory(toRoot);
			foreach (string file in files)
			{
				EnsureFolderExists(System.IO.Path.GetDirectoryName(System.IO.Path.Combine(toRoot, file)));
				System.IO.File.Copy(System.IO.Path.Combine(fromRoot, file), System.IO.Path.Combine(toRoot, file));
			}
		}

		public static void EnsureFolderExists(string path)
		{
			if (!System.IO.Directory.Exists(path))
			{
				string parent = System.IO.Path.GetDirectoryName(path);
				EnsureFolderExists(parent);
				System.IO.Directory.CreateDirectory(path);
			}
		}
	}
}
