# Original geometric quill emblem. No game artwork is used.
Add-Type -AssemblyName System.Drawing
$target = Join-Path (Split-Path $PSScriptRoot -Parent) 'app/Assets/patcher.ico'
$images = @()
foreach ($size in @(16,24,32,48,64,128,256)) {
 $bitmap = [Drawing.Bitmap]::new($size,$size)
 $g = [Drawing.Graphics]::FromImage($bitmap)
 $g.SmoothingMode = [Drawing.Drawing2D.SmoothingMode]::AntiAlias
 $g.ScaleTransform($size/256.0,$size/256.0)
 $dark = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml('#253A38'))
 $gold = [Drawing.SolidBrush]::new([Drawing.ColorTranslator]::FromHtml('#E1BC76'))
 $cream = [Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml('#FFF0C9'),9)
 $g.FillEllipse($dark,4,4,248,248)
 $edge = [Drawing.Pen]::new([Drawing.ColorTranslator]::FromHtml('#AD8750'),8)
 $g.DrawEllipse($edge,12,12,232,232)
 $feather = [Drawing.Drawing2D.GraphicsPath]::new()
 $feather.AddBezier(65,194,64,110,120,48,202,42)
 $feather.AddBezier(202,42,202,112,155,167,65,194)
 $g.FillPath($gold,$feather)
 $g.DrawLine($cream,55,211,171,78)
 $g.DrawLine($cream,109,149,153,149)
 $g.DrawLine($cream,138,116,138,81)
 $stream = [IO.MemoryStream]::new()
 $bitmap.Save($stream,[Drawing.Imaging.ImageFormat]::Png)
 $images += ,@($size,$stream.ToArray())
 $stream.Dispose(); $feather.Dispose(); $edge.Dispose(); $cream.Dispose(); $gold.Dispose(); $dark.Dispose(); $g.Dispose(); $bitmap.Dispose()
}
$output = [IO.File]::Create($target)
$writer = [IO.BinaryWriter]::new($output)
$writer.Write([uint16]0); $writer.Write([uint16]1); $writer.Write([uint16]$images.Count)
$offset = 6 + 16 * $images.Count
foreach ($entry in $images) {
 $dim = $entry[0] % 256
 $writer.Write([byte]$dim); $writer.Write([byte]$dim); $writer.Write([byte]0); $writer.Write([byte]0)
 $writer.Write([uint16]1); $writer.Write([uint16]32); $writer.Write([uint32]$entry[1].Length); $writer.Write([uint32]$offset)
 $offset += $entry[1].Length
}
foreach ($entry in $images) { $writer.Write([byte[]]$entry[1]) }
$writer.Dispose()
