using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Python2Crayon.ParseTree;
using Python2Crayon.Serialization;

namespace Python2Crayon
{
	internal class Program
	{
		private static Dictionary<string, string> ParseSettingsMeow()
		{
			string[] lines = Util.ReadFileFromDisk("settings.meow").Split('\n');
			Dictionary<string, string> output = new Dictionary<string, string>();
			foreach (string line in lines)
			{
				string[] parts= line.Trim().Split(':');
				if (parts.Length > 1)
				{
					string key = parts[0].Trim();
					string value = parts[1];
					for (int i = 2; i < parts.Length; ++i)
					{
						value += ":" + parts[i];
					}
					output[key] = value.Trim();
				}
			}
			return output;
		}

		static void Main(string[] args)
		{
			Dictionary<string, string> settings = ParseSettingsMeow();

			int fps = int.Parse(settings["FPS"]);
			int gameWidth = int.Parse(settings["GAME_WIDTH"]);
			int gameHeight = int.Parse(settings["GAME_HEIGHT"]) ;
			int screenWidth = int.Parse(settings["SCREEN_WIDTH"]);
			int screenHeight = int.Parse(settings["SCREEN_HEIGHT"]);

			string gameRoot = settings["GAME_ROOT"];
			string codeFolder = System.IO.Path.Combine(gameRoot, settings["CODE_FOLDER"]);
			string imagesFolder = System.IO.Path.Combine(gameRoot, settings["IMAGES_FOLDER"]);
			string audioFolder = System.IO.Path.Combine(gameRoot, settings["AUDIO_FOLDER"]);
			string dataFolder = System.IO.Path.Combine(gameRoot, settings["DATA_FOLDER"]);
			string outputFolder = settings["OUTPUT_FOLDER"];
			
			string startSceneClassName = settings["START_SCENE"];
			
			string[] imageFiles = FileCrawler.Crawl(imagesFolder, ".png", ".jpg");
			string imageFilesString = string.Join("|", imageFiles).Replace('\\', '/');

			string[] audioFiles = FileCrawler.Crawl(audioFolder, ".ogg");

			string[] textFiles = FileCrawler.Crawl(dataFolder, ".txt", ".dat", ".json", ".xml");
			StringBuilder textFileStoreBuilder = new StringBuilder();
			textFileStoreBuilder.Append("{\n");
			foreach (string textFile in textFiles)
			{
				string content = Util.ReadFileFromDisk(System.IO.Path.Combine(dataFolder, textFile));
				string escapedContent = Util.InsertEscapeSequences(content);
				string key = "\"" + textFile.Replace('\\', '/') + "\"";
				textFileStoreBuilder.Append("\t");
				textFileStoreBuilder.Append(key);
				textFileStoreBuilder.Append(": \"");
				textFileStoreBuilder.Append(escapedContent);
				textFileStoreBuilder.Append("\",\n");
			}
			textFileStoreBuilder.Append("}\n");
			string textFileStore = textFileStoreBuilder.ToString();

			Dictionary<string, object> replacements = new Dictionary<string, object>()
			{
				{ "FPS", fps },
				{ "GAME_WIDTH", gameWidth },
				{ "GAME_HEIGHT", gameHeight },
				{ "SCREEN_WIDTH", screenWidth },
				{ "SCREEN_HEIGHT", screenHeight },
				{ "IMAGE_FILES", imageFilesString },
				{ "IMAGES_ROOT", "'" + settings["IMAGES_FOLDER"] + "'"},
				{ "START_SCENE", startSceneClassName },
				{ "TEXT_FILES", textFileStore },
			};

			Tokenizer tokenizer = new Tokenizer();
			ExecutableParser parser = new ExecutableParser();
			List<Executable> parseTree = new List<Executable>();
			foreach (string file in FileCrawler.Crawl(codeFolder, ".py"))
			{
				string code = Util.ReadFileFromDisk(System.IO.Path.Combine(codeFolder, file));
				code = ApplyReplacements(code, replacements);

				TokenStream tokens = tokenizer.Tokenize(file, code);
				parseTree.AddRange(parser.ParseCode(tokens));
			}
			
			Executable[] resolvedParseTree = Executable.ResolveBlock(parseTree);
			
			CrayonSerializer crayonSerializer = new CrayonSerializer();
			string crayonOutput = crayonSerializer.Serialize(resolvedParseTree);
			string crayonHeader = GetTemplateFile("header.cry", replacements);
			string crayonFooter = GetTemplateFile("footer.cry", replacements);
			crayonOutput = crayonHeader + "\n" + crayonOutput + "\n" + crayonFooter;

			PythonSerializer pythonSerializer = new PythonSerializer();
			string pythonOutput = pythonSerializer.Serialize(resolvedParseTree);
			string pythonHeader = GetTemplateFile("header.py", replacements);
			string pythonFooter = GetTemplateFile("footer.py", replacements);
			pythonOutput = pythonHeader + "\n" + pythonOutput + "\n" + pythonFooter;

			Util.WriteFile(System.IO.Path.Combine(outputFolder, "run.py"), pythonOutput);
			Util.WriteFile(System.IO.Path.Combine(outputFolder, "start.cry"), crayonOutput);

			Util.SyncDirectories(imagesFolder, System.IO.Path.Combine(outputFolder, settings["IMAGES_FOLDER"]), imageFiles);
			Util.SyncDirectories(audioFolder, System.IO.Path.Combine(outputFolder, settings["AUDIO_FOLDER"]), audioFiles);
		}

		private static string GetTemplateFile(string path, Dictionary<string, object> replacements)
		{
			string output = Util.ReadFileFromAssembly("Serialization/Templates/" + path);
			return ApplyReplacements(output, replacements);
		}

		private static string ApplyReplacements(string code, Dictionary<string, object> replacements)
		{
			foreach (string key in replacements.Keys)
			{
				code = code.Replace("%%%" + key + "%%%", replacements[key].ToString());
			}
			return code;
		}
	}
}
