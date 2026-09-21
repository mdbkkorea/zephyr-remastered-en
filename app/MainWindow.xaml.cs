using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using MaterialDesignThemes.Wpf;
using Microsoft.Win32;
namespace ZephyrPatcher;

public partial class MainWindow : Window
{
 bool busy,initialized,preview,dialogOpen; int generation; JsonElement? lastState;
 readonly System.Windows.Threading.DispatcherTimer steamTimer=new(){Interval=TimeSpan.FromSeconds(15)};
 SteamVerificationWatch? steamWatch;
 DateTimeOffset lastSteamCheck=DateTimeOffset.MinValue;
 const string IdleText="安装前自动备份，随时恢复原版。存档不受影响。";
 public MainWindow()
 {
  InitializeComponent();Closing+=OnClosing;
  steamTimer.Tick+=async (_,_)=>await CheckSteamVerification();
  Activated+=async (_,_)=>await CheckSteamVerification();
  Closed+=(_,_)=>steamTimer.Stop();
 }
 void StopSteamWatch(){steamWatch=null;steamTimer.Stop();}
 void BeginSteamWatch()
 {
  steamWatch=new(GamePaths.Normalize(GamePath.Text),DateTimeOffset.UtcNow);
  lastSteamCheck=DateTimeOffset.MinValue;ShowSteamWaiting();steamTimer.Start();
 }
 void ShowSteamWaiting()
 {
  StateTitle.Text="等待 Steam 验证并恢复文件";
  StateDetail.Text="请在 Steam 中完成验证。工具每 15 秒自动检测一次，返回此窗口也会重新检查。";
  ProgressText.Text="正在自动检测恢复结果，无需一直点击“重新检测”。";
  SetIcon(PackIconKind.FolderSearchOutline,"#456080");
  InstallButton.IsEnabled=RestoreButton.IsEnabled=false;
  RecoverButton.Visibility=Visibility.Collapsed;
 }
 void ApplySteamState(JsonElement result)
 {
  if(steamWatch is null){ShowState(result);return;}
  string outcome=steamWatch.Evaluate(Value(result,"status"),SteamVerificationWatch.ReadFlags(steamWatch.GamePath),DateTimeOffset.UtcNow);
  ShowState(result);
  if(outcome=="waiting"){ShowSteamWaiting();return;}
  StopSteamWatch();
  ProgressText.Text=outcome=="original"?"已自动检测到原版资源，文件校验通过，可以重新安装汉化。":
   outcome=="finished"?"Steam 已结束文件处理；上方显示重新校验后的实际状态。":
   "自动检测已暂停，上方显示当前文件状态。请确认 Steam 结果后点击“重新检测”。";
 }
 async Task CheckSteamVerification()
 {
  if(preview||steamWatch is null||busy||dialogOpen||DateTimeOffset.UtcNow-lastSteamCheck<TimeSpan.FromSeconds(3))return;
  if(!string.Equals(steamWatch.GamePath,GamePaths.Normalize(GamePath.Text),StringComparison.OrdinalIgnoreCase)){StopSteamWatch();return;}
  lastSteamCheck=DateTimeOffset.UtcNow;await Refresh();
 }
 public void PreparePreview(string state="original")
 {
  preview=true;GamePath.Text=@"D:\Games\Steam\steamapps\common\The Rhapsody of Zephyr Remastered";
  using var doc=JsonDocument.Parse(JsonSerializer.Serialize(new{status=state,can_install=state=="original",can_restore=state=="installed",can_force_restore=true,backup_available=true,backup_files=19,backup_complete=true,game_build="25418345",installed_build=state=="unsupported_or_modified"?"25420000":"25418345",version=Updates.Current,installed_version=state=="installed"?Updates.Current:null}));
  ShowState(doc.RootElement.Clone());
  if(state=="steam-waiting"){BeginSteamWatch();steamTimer.Stop();}
 }
 public async void Initialize(){initialized=true;GamePath.Text=FindGame()??"";await Refresh();await CheckUpdates(false);}
 static string? FindGame()
 {
  var steam=Registry.GetValue(@"HKEY_CURRENT_USER\Software\Valve\Steam","SteamPath",null) as string;
  if(steam==null)return null;var roots=new List<string>{steam};var file=Path.Combine(steam,"steamapps","libraryfolders.vdf");
  if(File.Exists(file))foreach(Match m in Regex.Matches(File.ReadAllText(file),"\"path\"\\s+\"([^\"]+)\""))roots.Add(m.Groups[1].Value.Replace(@"\\",@"\"));
  return roots.Select(r=>GamePaths.Normalize(Path.Combine(r,"steamapps","common","The Rhapsody of Zephyr Remastered"))).FirstOrDefault(p=>File.Exists(Path.Combine(p,"ZephyrRemastered.exe")));
 }
 void OnClosing(object? sender,CancelEventArgs e){if(busy||dialogOpen){e.Cancel=true;ProgressText.Text="请等待当前操作完成，或先关闭提示窗口。";}}
 void SetBusy(bool value)
 {
  busy=value;GamePath.IsEnabled=BrowseButton.IsEnabled=!value;InstallButton.IsEnabled=RestoreButton.IsEnabled=false;RecoverButton.IsEnabled=!value;
  Progress.IsIndeterminate=true;Progress.Visibility=value?Visibility.Visible:Visibility.Collapsed;
 }
 void SetIcon(PackIconKind kind,string color){StateIcon.Kind=kind;StateIcon.Foreground=new SolidColorBrush((Color)ColorConverter.ConvertFromString(color));}
 async Task<JsonElement> RunEngine(string action)
 {
  GamePath.Text=GamePaths.Normalize(GamePath.Text);
  var start=new ProcessStartInfo(Path.Combine(AppContext.BaseDirectory,"tools","ZephyrPatchEngine.exe")){UseShellExecute=false,CreateNoWindow=true,RedirectStandardOutput=true,RedirectStandardError=true,StandardOutputEncoding=System.Text.Encoding.UTF8,StandardErrorEncoding=System.Text.Encoding.UTF8};
  start.ArgumentList.Add(action);start.ArgumentList.Add("--game");start.ArgumentList.Add(GamePath.Text.Trim());start.ArgumentList.Add("--payload");start.ArgumentList.Add(Path.Combine(AppContext.BaseDirectory,"payload"));
  if(action=="force_restore")start.ArgumentList.Add("--confirm-old-backup");
  using var process=new Process{StartInfo=start};
  process.ErrorDataReceived+=(_,e)=>{if(!string.IsNullOrWhiteSpace(e.Data))Dispatcher.BeginInvoke(()=>
  {
   ProgressText.Text=e.Data;var m=Regex.Match(e.Data,@"(\d+)/(\d+)");
   if(m.Success){Progress.IsIndeterminate=false;Progress.Maximum=int.Parse(m.Groups[2].Value);Progress.Value=int.Parse(m.Groups[1].Value);}
  });};
  process.Start();process.BeginErrorReadLine();string output=await process.StandardOutput.ReadToEndAsync();await process.WaitForExitAsync();
  JsonElement result;
  try{using var json=JsonDocument.Parse(output.Trim());result=json.RootElement.Clone();}
  catch{throw new InvalidOperationException("无法读取处理结果。请检查下载包是否完整，以及安全软件是否拦截了 tools 中的处理程序。");}
  if(!result.GetProperty("ok").GetBoolean())throw new InvalidOperationException(result.GetProperty("error").GetString());return result;
 }
 async Task Refresh()
 {
  if(preview||busy)return;
  if(string.IsNullOrWhiteSpace(GamePath.Text)){lastState=null;InstallButton.IsEnabled=RestoreButton.IsEnabled=false;StateTitle.Text="等待选择游戏目录";StateDetail.Text="请选择包含 ZephyrRemastered.exe 的文件夹。";return;}
  SetBusy(true);StateTitle.Text="正在检查游戏文件…";SetIcon(PackIconKind.FolderSearchOutline,"#456080");
  try{ApplySteamState(await RunEngine("status"));}
  catch(Exception ex)
  {
   lastState=null;
   if(steamWatch is not null)
   {
    if(steamWatch.Evaluate("unreadable",null,DateTimeOffset.UtcNow)=="timeout"){StopSteamWatch();StateTitle.Text="自动检测已暂停";StateDetail.Text="暂时无法读取资源，请确认 Steam 结果后点击“重新检测”。";}
    else{ShowSteamWaiting();StateDetail.Text="Steam 可能正在替换资源，暂时无法读取；稍后会自动重试。";}
   }
   else{StateTitle.Text="暂时不能操作";StateDetail.Text=ex.Message;BuildInfo.Text="游戏 Build：未识别";BackupInfo.Text="";SetIcon(PackIconKind.AlertCircleOutline,"#9B642A");}
  }
  finally{busy=false;GamePath.IsEnabled=BrowseButton.IsEnabled=true;Progress.Visibility=Visibility.Collapsed;}
 }
 static bool Flag(JsonElement r,string key)=>r.TryGetProperty(key,out var x)&&x.ValueKind==JsonValueKind.True;
 static string Value(JsonElement r,string key,string fallback="未识别")=>r.TryGetProperty(key,out var x)&&x.ValueKind==JsonValueKind.String?x.GetString()??fallback:fallback;
 void ShowState(JsonElement r)
 {
  lastState=r;string state=Value(r,"status");
  (StateTitle.Text,StateDetail.Text)=state switch{
   "original"=>("原版游戏，可以安装汉化","文件校验通过。安装时自动保存原版备份，存档保持原样。"),
   "installed"=>("汉化已就绪","当前汉化包已安装。可自行进入游戏；视频字幕与原版美术字保持原样。"),
   "update_available"=>("发现可更新的汉化","会使用已保存的原版备份重新构建，保留存档和恢复能力。"),
   "recovery_required"=>("上次操作尚未完成","请关闭游戏，先恢复上次操作，再继续安装或还原。"),
   "unmanaged_localization"=>("检测到已有汉化","文件与当前汉化一致，但未记录为本工具安装。可以使用恢复选项还原。"),
   _=>("游戏版本或文件发生变化","已暂停汉化。请先检查工具更新；若 Steam 更新了游戏，建议通过 Steam 验证完整性后使用适配版本。")};
  SetIcon(state is "installed" or "original"?PackIconKind.CheckCircleOutline:PackIconKind.AlertCircleOutline,state is "installed" or "original"?"#446D62":"#9B642A");
  BuildInfo.Text=$"游戏 Build：{Value(r,"installed_build")}   ·   支持 Build：{Value(r,"game_build")}";
  BackupInfo.Text=Flag(r,"backup_available")?$"本地备份：{r.GetProperty("backup_files").GetInt32()} 个文件   ·   汉化包：{Value(r,"version")}":$"本地备份：尚未建立   ·   汉化包：{Value(r,"version")}";
  InstallButton.IsEnabled=Flag(r,"can_install")&&state!="installed";InstallButton.Content=state=="update_available"?"更新汉化":state=="installed"?"已安装汉化":"安装汉化";
  RestoreButton.IsEnabled=state!="recovery_required";RecoverButton.IsEnabled=true;RecoverButton.Visibility=state=="recovery_required"?Visibility.Visible:Visibility.Collapsed;
 }
 async Task<string> Dialog(string title,string detail,params (string Label,string Action,bool Enabled)[] actions)
 {
  if(dialogOpen)return "cancel";dialogOpen=true;
  var panel=new StackPanel{Width=440,Margin=new Thickness(28)};
  panel.Children.Add(new TextBlock{Text=title,FontSize=22,FontWeight=FontWeights.SemiBold,Margin=new Thickness(0,0,0,14)});
  panel.Children.Add(new TextBlock{Text=detail,TextWrapping=TextWrapping.Wrap,LineHeight=24,Foreground=new SolidColorBrush(Color.FromRgb(85,99,118)),Margin=new Thickness(0,0,0,18)});
  foreach(var (label,action,enabled) in actions)
  {
   var button=new Button{Content=label,IsEnabled=enabled,HorizontalContentAlignment=HorizontalAlignment.Left,Margin=new Thickness(0,4,0,0),Command=DialogHost.CloseDialogCommand,CommandParameter=action};
   panel.Children.Add(button);
  }
  try{return (await Dialogs.ShowDialog(panel))?.ToString()??"cancel";}finally{dialogOpen=false;}
 }
 async Task Operate(string action)
 {
  if(busy||preview)return;SetBusy(true);ProgressText.Text="正在准备，请保持游戏关闭…";
  try{
   var result=await RunEngine(action);ShowState(result);
   ProgressText.Text=action=="install"?"汉化已完成，校验通过。现在可以进入游戏。":action=="force_restore"?"备份文件已恢复。若 Steam 更新过游戏，请继续验证完整性。":"恢复完成，文件校验通过。";
  }
  catch(Exception ex){StateTitle.Text="操作未完成";StateDetail.Text=ex.Message;await Dialog("操作未完成",ex.Message,("知道了","cancel",true));}
  finally{busy=false;GamePath.IsEnabled=BrowseButton.IsEnabled=true;Progress.Visibility=Visibility.Collapsed;await Refresh();}
 }
 async void BrowseClick(object sender,RoutedEventArgs e){if(busy)return;var dialog=new OpenFolderDialog{Title="选择包含 ZephyrRemastered.exe 的游戏文件夹"};if(dialog.ShowDialog(this)==true){GamePath.Text=GamePaths.Normalize(dialog.FolderName);await Refresh();}}
 async void PathChanged(object sender,TextChangedEventArgs e){if(!initialized||busy)return;StopSteamWatch();int ticket=++generation;await Task.Delay(600);if(ticket==generation)await Refresh();}
 async void InstallClick(object sender,RoutedEventArgs e)=>await Operate("install");
 async void RestoreClick(object sender,RoutedEventArgs e)
 {
  if(busy||lastState is not JsonElement r)return;
  bool normal=Flag(r,"can_restore"),backup=Flag(r,"can_force_restore");
  var choice=await Dialog("选择恢复方式","Steam 验证会下载与当前版本匹配的原版资源，推荐在游戏更新后使用。\n本地备份恢复无需下载，但备份可能属于旧版本。存档不会由本工具改动。",
   ("通过 Steam 验证完整性（推荐）","steam",true),(normal?"从本地备份恢复":"从旧备份强制恢复","backup",backup),("取消","cancel",true));
  if(choice=="steam")
  {
   if(await Dialog("交给 Steam 恢复","请先保存并退出游戏。接下来将打开 Steam 验证 App 5099430 的文件；由 Steam 检查并重新下载需要的资源。本工具无法代替 Steam 确认完成。\n若验证后仍有异常，可备份存档后卸载并重新安装游戏。",("打开 Steam 验证","yes",true),("取消","cancel",true))=="yes")
    try{Open("steam://validate/5099430");BeginSteamWatch();}catch{await Dialog("未能打开 Steam","请打开 Steam → 游戏属性 → 已安装文件 → 验证游戏文件的完整性。",("知道了","cancel",true));}
  }
  else if(choice=="backup")
  {
   string warning=normal?"将恢复安装前的原版资源。开始前还会备份当前文件，存档保持不变。":"游戏文件已变化。旧备份可能与 Steam 当前 EXE 或其他资源不匹配，强制恢复后可能无法启动。我们会保留本次操作前的文件，但建议优先使用 Steam 验证完整性。\n确定仍要用旧备份覆盖当前资源吗？";
   if(await Dialog(normal?"恢复原版？":"确认强制恢复旧备份",warning,(normal?"确认恢复":"我了解风险，强制恢复","yes",true),("取消","cancel",true))=="yes")await Operate(normal?"restore":"force_restore");
  }
 }
 async void RecoverClick(object sender,RoutedEventArgs e)=>await Operate("recover");
 async void RecheckClick(object sender,RoutedEventArgs e){if(!busy){ProgressText.Text=IdleText;await Refresh();}}
 static void Open(string url)=>Process.Start(new ProcessStartInfo(url){UseShellExecute=true});
 void StoreClick(object sender,RoutedEventArgs e)=>Open("https://store.steampowered.com/app/5099430/");
 void FeedbackClick(object sender,RoutedEventArgs e)=>Open("https://github.com/wanjizheng/zephyr-remastered-zh-cn/issues/new/choose");
 async Task CheckUpdates(bool manual)
 {
  if(preview)return;UpdateButton.IsEnabled=false;
  try{
   var update=await Updates.Check();UpdateStatus.Text=update!=null?"有新版本可下载":"未发现更新版本";
   if(manual&&update!=null){if(await Dialog("有新版本可下载","更新签名已验证。下载并完整解压新版程序后，再打开程序更新汉化。",("打开下载页","yes",true),("稍后","cancel",true))=="yes")Open(update);}
   else if(manual)await Dialog("暂未发现更新","当前已是最新正式版本。若游戏已更新而汉化尚未适配，请先恢复原版，等待新的汉化包。",("知道了","cancel",true));
  }catch{UpdateStatus.Text="更新检查暂不可用";if(manual)await Dialog("暂时无法检查更新","请稍后重试，或到项目的 GitHub Releases 页面查看。离线安装与恢复不受影响。",("知道了","cancel",true));}
  finally{UpdateButton.IsEnabled=true;}
 }
 async void CheckUpdateClick(object sender,RoutedEventArgs e)=>await CheckUpdates(true);
}
