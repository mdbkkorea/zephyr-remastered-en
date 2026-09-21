using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
namespace ZephyrPatcher;
public partial class App : Application
{
 protected override async void OnStartup(StartupEventArgs e)
 {
  base.OnStartup(e);
  var window=new MainWindow();MainWindow=window;
  if(e.Args.Length>=2 && e.Args[0]=="--render-preview")
  {
   window.PreparePreview(e.Args.Length>=3?e.Args[2]:"original");
   if(e.Args.Contains("small")){window.Width=940;window.Height=680;}
   window.Show();window.UpdateLayout();await Task.Delay(200);
   if(e.Args.Contains("restore")||e.Args.Contains("force"))
   {
    window.RestoreButton.RaiseEvent(new RoutedEventArgs(System.Windows.Controls.Button.ClickEvent));await Task.Delay(250);
    if(!window.Dialogs.IsOpen)throw new InvalidOperationException("Restore dialog did not open");
    if(e.Args.Contains("force"))
    {
     MaterialDesignThemes.Wpf.DialogHost.CloseDialogCommand.Execute("backup",window.Dialogs);await Task.Delay(300);
     if(!window.Dialogs.IsOpen)throw new InvalidOperationException("Force restore confirmation did not open");
    }
   }
   var bounds=VisualTreeHelper.GetDescendantBounds(window);
   var bitmap=new RenderTargetBitmap((int)Math.Ceiling(bounds.Right),(int)Math.Ceiling(bounds.Bottom),96,96,PixelFormats.Pbgra32);bitmap.Render(window);
   var encoder=new PngBitmapEncoder();encoder.Frames.Add(BitmapFrame.Create(bitmap));using(var file=File.Create(e.Args[1]))encoder.Save(file);
   if(window.Dialogs.IsOpen){MaterialDesignThemes.Wpf.DialogHost.CloseDialogCommand.Execute("cancel",window.Dialogs);await Task.Delay(100);}
   Shutdown();return;
  }
  window.Show();window.Initialize();
 }
}
