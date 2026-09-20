using System.IO;
namespace ZephyrPatcher;
public static class GamePaths
{
 public static string Normalize(string input)
 {
  var path=Path.TrimEndingDirectorySeparator(Path.GetFullPath(input.Trim().Trim('"').Replace('/', '\\')));
  if(path.Length>=2 && path[1]==':')path=char.ToUpperInvariant(path[0])+path[1..];
  return path;
 }
}
