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
if(OperatingSystem.IsWindows()) {
 Assert(GamePaths.Normalize(@"d:/games/steam\steamapps\common\The Rhapsody of Zephyr Remastered")==@"D:\games\steam\steamapps\common\The Rhapsody of Zephyr Remastered");
 Assert(GamePaths.Normalize("  \"D:/Games/游戏/\"  ")==@"D:\Games\游戏");
 Assert(GamePaths.Normalize(@"\\server\share\game\")==@"\\server\share\game");
 Console.WriteLine("PASS: mixed separators, quoted Unicode path, UNC path");
}
