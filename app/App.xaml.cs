using System.IO;
using System.Windows;
using System.Windows.Media;
using System.Windows.Media.Imaging;
namespace ZephyrPatcher;
public partial class App : Application
{
 protected override void OnStartup(StartupEventArgs e)
 {
  base.OnStartup(e);
  var window=new MainWindow();MainWindow=window;
  if(e.Args.Length==2 && e.Args[0]=="--render-preview")
  {
   window.PreparePreview();window.Show();window.UpdateLayout();
   var bounds=VisualTreeHelper.GetDescendantBounds(window);
   var bitmap=new RenderTargetBitmap((int)Math.Ceiling(bounds.Right),(int)Math.Ceiling(bounds.Bottom),96,96,PixelFormats.Pbgra32);bitmap.Render(window);
   var encoder=new PngBitmapEncoder();encoder.Frames.Add(BitmapFrame.Create(bitmap));using(var file=File.Create(e.Args[1]))encoder.Save(file);
   Shutdown();return;
  }
  window.Show();window.Initialize();
 }
}
