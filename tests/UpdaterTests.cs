using System.Security.Cryptography;
using System.Text;
using ZephyrPatcher;
static void Assert(bool condition){if(!condition)throw new Exception("Test failed");}
Assert(Updates.Compare("0.1.0","0.1.0-beta.1")>0);
Assert(Updates.Compare("v0.1.0-beta.10","0.1.0-beta.2")>0);
Assert(Updates.Compare("1.0.0","0.9.9")>0);
Assert(Updates.Compare("0.1.0-beta.1","v0.1.0-beta.1")==0);
using var key=RSA.Create(3072);
byte[] metadata=Encoding.UTF8.GetBytes("{\"version\":\"0.1.0-beta.2\"}");
byte[] signature=key.SignData(metadata,HashAlgorithmName.SHA256,RSASignaturePadding.Pss);
Updates.VerifyMetadata(metadata,signature,"v0.1.0-beta.2",key.ExportSubjectPublicKeyInfoPem());
bool rejected=false;
try{Updates.VerifyMetadata(metadata,signature,"v0.1.0-beta.3",key.ExportSubjectPublicKeyInfoPem());}catch(InvalidDataException){rejected=true;}
Assert(rejected);metadata[2]^=1;rejected=false;
try{Updates.VerifyMetadata(metadata,signature,"v0.1.0-beta.2",key.ExportSubjectPublicKeyInfoPem());}catch(CryptographicException){rejected=true;}
Assert(rejected);
Console.WriteLine("PASS: semantic versions, valid signature, tag mismatch, tampered metadata");
var now=DateTimeOffset.UtcNow;
var watch=new SteamVerificationWatch("fixture",now);
Assert(watch.Evaluate("installed",4,now)=="waiting");
Assert(watch.Evaluate("original",260,now.AddSeconds(15))=="waiting");
Assert(watch.Evaluate("original",4,now.AddSeconds(30))=="original");
watch=new("fixture",now);
Assert(watch.Evaluate("unsupported_or_modified",260,now)=="waiting");
Assert(watch.Evaluate("unsupported_or_modified",4,now.AddSeconds(15))=="finished");
watch=new("fixture",now);
Assert(watch.Evaluate("installed",4,now.AddMinutes(15))=="timeout");
Assert(watch.Evaluate("original",null,now)=="original");
Assert(SteamVerificationWatch.ReadFlags(Path.Combine(Path.GetTempPath(),"not-a-steam-library"))==null);
var fixture=Path.Combine(Path.GetTempPath(),"zephyr-watch-"+Guid.NewGuid().ToString("N"),"steamapps");
Directory.CreateDirectory(Path.Combine(fixture,"common","TestGame"));
var manifest=Path.Combine(fixture,"appmanifest_5099430.acf");
File.WriteAllText(manifest,"\"appid\" \"5099430\" \"installdir\" \"TestGame\" \"StateFlags\" \"260\"");
Assert(SteamVerificationWatch.ReadFlags(Path.Combine(fixture,"common","TestGame"))==260);
File.WriteAllText(manifest,"\"appid\" \"5099430\" \"installdir\" \"TestGame\" \"StateFlags\" \"4\"");
Assert(SteamVerificationWatch.ReadFlags(Path.Combine(fixture,"common","TestGame"))==4);
File.WriteAllText(manifest,"\"appid\" \"5099430\" \"installdir\" \"OtherGame\" \"StateFlags\" \"4\"");
Assert(SteamVerificationWatch.ReadFlags(Path.Combine(fixture,"common","TestGame"))==null);
Console.WriteLine("PASS: Steam wait -> original, busy original guarded, updated build finished, timeout, absent/wrong manifest, live manifest change");
if(OperatingSystem.IsWindows()) {
 Assert(GamePaths.Normalize(@"d:/games/steam\steamapps\common\The Rhapsody of Zephyr Remastered")==@"D:\games\steam\steamapps\common\The Rhapsody of Zephyr Remastered");
 Assert(GamePaths.Normalize("  \"D:/Games/游戏/\"  ")==@"D:\Games\游戏");
 Assert(GamePaths.Normalize(@"\\server\share\game\")==@"\\server\share\game");
 Console.WriteLine("PASS: mixed separators, quoted Unicode path, UNC path");
}
