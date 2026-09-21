using System.IO;
using System.Text.RegularExpressions;
namespace ZephyrPatcher;

// The URI only requests verification; completion must be inferred from fresh
// local resource checks, never from Process.Start or Steam's window closing.
public sealed class SteamVerificationWatch(string gamePath, DateTimeOffset started)
{
 public string GamePath { get; } = gamePath;
 bool observedSteamBusy;
 public string Evaluate(string resourceState, uint? steamFlags, DateTimeOffset now)
 {
  bool steamBusy=steamFlags.HasValue && steamFlags.Value!=4;
  observedSteamBusy|=steamBusy;
  if(!steamBusy && resourceState=="original")return "original";
  if(!steamBusy && steamFlags==4 && observedSteamBusy)return "finished";
  if(now-started>=TimeSpan.FromMinutes(15))return "timeout";
  return "waiting";
 }
 public static uint? ReadFlags(string gamePath)
 {
  try
  {
   var game=new DirectoryInfo(gamePath);
   if(!string.Equals(game.Parent?.Name,"common",StringComparison.OrdinalIgnoreCase))return null;
   var path=Path.Combine(game.Parent!.Parent!.FullName,"appmanifest_5099430.acf");
   // Steam can replace/write this file during validation; sharing is intentional.
   using var stream=new FileStream(path,FileMode.Open,FileAccess.Read,FileShare.ReadWrite|FileShare.Delete);
   using var reader=new StreamReader(stream);string text=reader.ReadToEnd();
   string Field(string key)=>Regex.Match(text,"\""+key+"\"\\s+\"([^\"]+)\"").Groups[1].Value;
   if(Field("appid")!="5099430"||!string.Equals(Field("installdir"),game.Name,StringComparison.OrdinalIgnoreCase))return null;
   return uint.TryParse(Field("StateFlags"),out var flags)?flags:null;
  }
  catch(IOException){return null;}
  catch(UnauthorizedAccessException){return null;}
  catch(ArgumentException){return null;}
 }
}
