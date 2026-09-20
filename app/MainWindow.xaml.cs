using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Windows;
using Microsoft.Win32;
namespace ZephyrPatcher;
public partial class MainWindow : Window
{
 bool busy,initialized,preview;int generation;string? updatePage;
 public MainWindow(){InitializeComponent();Closing+=OnClosing;}
 public void PreparePreview(){preview=true;GamePath.Text=@"D:\SteamLibrary\steamapps\common\The Rhapsody of Zephyr Remastered";StateTitle.Text="原版游戏 · 可以安装汉化";StateDetail.Text="已识别受支持版本。安装前会自动备份，之后可随时恢复原版。";InstallButton.IsEnabled=true;}
 public async void Initialize(){initialized=true;GamePath.Text=FindGame()??"";await Refresh();await CheckUpdates(false);}
 static string? FindGame()
 {
  var steam=Registry.GetValue(@"HKEY_CURRENT_USER\Software\Valve\Steam","SteamPath",null) as string;
  if(steam==null)return null;var roots=new List<string>{steam};var file=Path.Combine(steam,"steamapps","libraryfolders.vdf");
  if(File.Exists(file))foreach(Match m in Regex.Matches(File.ReadAllText(file),"\"path\"\\s+\"([^\"]+)\""))roots.Add(m.Groups[1].Value.Replace(@"\\",@"\"));
  return roots.Select(r=>Path.Combine(r,"steamapps","common","The Rhapsody of Zephyr Remastered")).FirstOrDefault(p=>File.Exists(Path.Combine(p,"ZephyrRemastered.exe")));
 }
 void OnClosing(object? sender,CancelEventArgs e){if(busy){e.Cancel=true;MessageBox.Show(this,"正在处理游戏文件，请等待完成后再关闭。","请稍候");}}
 void SetBusy(bool value){busy=value;GamePath.IsEnabled=!value;InstallButton.IsEnabled=false;RestoreButton.IsEnabled=false;RecoverButton.IsEnabled=!value;Progress.Visibility=value?Visibility.Visible:Visibility.Collapsed;}
 async Task<JsonElement> RunEngine(string action)
 {
  var start=new ProcessStartInfo(Path.Combine(AppContext.BaseDirectory,"tools","ZephyrPatchEngine","ZephyrPatchEngine.exe")){UseShellExecute=false,CreateNoWindow=true,RedirectStandardOutput=true,RedirectStandardError=true,StandardOutputEncoding=System.Text.Encoding.UTF8,StandardErrorEncoding=System.Text.Encoding.UTF8};
  start.ArgumentList.Add(action);start.ArgumentList.Add("--game");start.ArgumentList.Add(GamePath.Text.Trim());start.ArgumentList.Add("--payload");start.ArgumentList.Add(Path.Combine(AppContext.BaseDirectory,"payload"));
  using var process=new Process{StartInfo=start};process.ErrorDataReceived+=(_,e)=>{if(!string.IsNullOrWhiteSpace(e.Data))Dispatcher.BeginInvoke(()=>ProgressText.Text=e.Data);};
  process.Start();process.BeginErrorReadLine();string output=await process.StandardOutput.ReadToEndAsync();await process.WaitForExitAsync();
  JsonElement result;
  try{result=JsonDocument.Parse(output.Trim()).RootElement.Clone();}catch{throw new InvalidOperationException("无法读取处理结果。请检查下载包是否完整，或尝试以管理员身份运行。");}
  if(!result.GetProperty("ok").GetBoolean())throw new InvalidOperationException(result.GetProperty("error").GetString());return result;
 }
 async Task Refresh()
 {
  if(preview||busy||string.IsNullOrWhiteSpace(GamePath.Text))return;int ticket=++generation;SetBusy(true);StateTitle.Text="正在检查游戏文件…";
  try
  {
   var r=await RunEngine("status");if(ticket!=generation)return;ShowState(r);
  }catch(Exception ex){StateTitle.Text="暂时不能操作";StateDetail.Text=ex.Message;}
  finally{busy=false;GamePath.IsEnabled=true;Progress.Visibility=Visibility.Collapsed;}
 }
 void ShowState(JsonElement r)
 {
  string state=r.GetProperty("status").GetString()??"";
  (StateTitle.Text,StateDetail.Text)=state switch{
   "original"=>("原版游戏 · 可以安装汉化","安装前自动备份。恢复原版会还原安装前的韩语游戏文件，不改动存档。"),
   "installed"=>("已安装最新汉化","直接启动游戏即可。朱雀仿宋已启用，原版花体菜单保留；视频字幕暂未汉化。"),
   "update_available"=>("已有汉化 · 可以更新","将基于已保存的原版备份更新，保留存档。"),
   "recovery_required"=>("上次操作未完成","请关闭游戏，点击“恢复上次操作”后再继续。"),
   "unmanaged_localization"=>("检测到已有汉化","当前版本正确，但本工具没有原版备份。请先用原备份恢复或通过 Steam 验证文件，再使用本工具安装。"),
   _=>("版本不支持，或文件已被修改","为保护游戏，未写入文件。请检查兼容版本；第三方补丁需先恢复原版。")};
  InstallButton.IsEnabled=r.GetProperty("can_install").GetBoolean()&&state!="installed";InstallButton.Content=state=="update_available"?"更新汉化":"安装汉化";RestoreButton.IsEnabled=r.GetProperty("can_restore").GetBoolean();RecoverButton.IsEnabled=true;RecoverButton.Visibility=state=="recovery_required"?Visibility.Visible:Visibility.Collapsed;
 }
 async Task Operate(string action)
 {
  if(busy)return;SetBusy(true);ProgressText.Text="正在准备，请保持游戏关闭…";
  try{var r=await RunEngine(action);ShowState(r);ProgressText.Text=action=="install"?"汉化已完成，校验通过。现在可以进入游戏。":"已完成，文件校验通过。";}
  catch(Exception ex){StateTitle.Text="操作未完成";StateDetail.Text=ex.Message;MessageBox.Show(this,ex.Message,"操作提示");}
  finally{busy=false;GamePath.IsEnabled=true;Progress.Visibility=Visibility.Collapsed;await Refresh();}
 }
 async void BrowseClick(object sender,RoutedEventArgs e){if(busy)return;var dialog=new OpenFolderDialog{Title="选择包含 ZephyrRemastered.exe 的游戏文件夹"};if(dialog.ShowDialog(this)==true){GamePath.Text=dialog.FolderName;await Refresh();}}
 async void PathChanged(object sender,System.Windows.Controls.TextChangedEventArgs e){if(!initialized||busy)return;int ticket=++generation;await Task.Delay(600);if(ticket==generation)await Refresh();}
 async void InstallClick(object sender,RoutedEventArgs e)=>await Operate("install");
 async void RestoreClick(object sender,RoutedEventArgs e){if(MessageBox.Show(this,"恢复原版游戏文件？存档不会改动。","恢复原版",MessageBoxButton.YesNo)==MessageBoxResult.Yes)await Operate("restore");}
 async void RecoverClick(object sender,RoutedEventArgs e)=>await Operate("recover");
 static void Open(string url)=>Process.Start(new ProcessStartInfo(url){UseShellExecute=true});
 void StoreClick(object sender,RoutedEventArgs e)=>Open("https://store.steampowered.com/app/5099430/");
 void FeedbackClick(object sender,RoutedEventArgs e)=>Open("https://github.com/wanjizheng/zephyr-remastered-zh-cn/issues/new/choose");
 async Task CheckUpdates(bool manual)
 {
  try{var update=await Updates.Check();if(update!=null){updatePage=update;UpdateStatus.Text="有新版本可下载";if(manual&&MessageBox.Show(this,"发现已验证的新版本。打开下载页面？下载并解压后，运行新版程序即可更新汉化。","检查更新",MessageBoxButton.YesNo)==MessageBoxResult.Yes)Open(update);}else{UpdateStatus.Text="当前已是最新版本";if(manual)MessageBox.Show(this,"当前没有更新版本。","检查更新");}}
  catch{UpdateStatus.Text="暂时无法检查更新";if(manual)MessageBox.Show(this,"无法连接或验证更新。现有汉化功能不受影响，请稍后再试。","检查更新");}
 }
 async void CheckUpdateClick(object sender,RoutedEventArgs e)=>await CheckUpdates(true);
}
