# 开发与发行

维护者需要 Windows、.NET 10 SDK、Python 3.14；玩家不需要这些工具。建议创建独立 Python 虚拟环境后安装 `requirements.txt`。完整传递依赖版本见 `dependency-versions.json`。

```powershell
python -m venv C:\Build\zephyr-venv
C:\Build\zephyr-venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pwsh -File scripts/build.ps1 -OutputDirectory C:\Build\zephyr-release-001
```

构建输出必须在仓库之外。`app/bin`、`app/obj` 是临时编译结果，不提交、不打进源码审阅包。主程序通过 .NET 原生 PublishSingleFile 与 IncludeNativeLibrariesForSelfExtract 将托管和原生运行库打包，保留 zh-Hans 资源，不做 WPF 裁剪；无需引入 Fody。Python 引擎仍放在 tools 内，payload 与许可证必须完整保留。图标为本项目原创几何羽笔，可用 scripts/create-icon.ps1 重建。第一版尚未承诺不同 SDK/传递依赖下的逐字节可重复 EXE 构建。

## 测试

`tests/integration.py --fixture <原版测试副本> --work <新空目录>` 会再复制一份资源进行安装、恢复、故障和路径保护测试。fixture 必须包含受支持的 EXE、18 个目标文件和两项 `.resS` 依赖；官方文件只能由维护者本地提供，不能提交或上传到 CI。

测试内仅对其新建副本跳过进程占用检测，生产安装、恢复没有此开关。发行引擎支持只读 `verify --game <原版目录> --payload <payload目录>`，在工具工作区重建所有资源并检查精确输出哈希，不修改游戏。另应验证游戏运行时安装被拒绝、界面显示、签名校验、公开文件内容与包内哈希。

## 数据更新

当前 `payload` 是经过核验的发行数据；`engine/trusted_payload.py` 固定这两个文件的 SHA-256。不能只改 pin 来跳过一次失败。

新译文版本需从维护者私有的原版／候选工作副本重新导出叶字段操作和许可字体字形块，重新检查所有原版哈希、最终输出 SHA、Unity 原生 CRC、catalog。将原版字形转换为本地复制引用，新字形须有逐块许可来源证明。不要把压缩 bundle 的粗粒度二进制差分当成“没有官方资源”的证明。内部游戏素材和生成工具工作区不应加入仓库。

升级游戏支持版本需要独立重建和回归，不能修改旧版哈希冒充兼容。工具版本由 `app/Updates.cs`、项目版本与 UI 显示同步维护；资源数据版本由 `engine/main.py` 和 payload 对应维护。beta.2 仅修正文档与界面提示，资源数据保持 beta.1，已安装的同一数据无需再次回填。

## 发布签名

私钥保存在仓库外，并单独做安全备份。仓库内只有 `release-public.pem` 和 `app/ReleaseKey.cs` 公钥。打包后执行：

```powershell
pwsh -File scripts/sign-release.ps1 -Archive C:\Build\Zephyr-Chinese-Patcher-0.1.0-beta.1.zip -Version 0.1.0-beta.1 -PrivateKeyPath C:\Private\release-private.pem -OutputDirectory C:\Build\release-metadata
```

GitHub tag 使用 `v` 前缀；该 tag 的 Release 附上程序 ZIP、`release.json`、`release.sig`、SHA-256 清单。程序从固定仓库读取发布记录，用 RSA-PSS/SHA-256 核验元数据再提示更新。程序不自动执行下载内容；用户需按发布清单核对手动下载的 ZIP。元数据签名不等于对 EXE 的 Authenticode 签名。

发布前扫描仓库及 ZIP，排除官方资源、原文全集、私钥、令牌、游戏备份、存档和个人路径；核对字体和所有运行依赖许可证。Release 不上传测试 fixture。

v0.1.0 为首个正式工具版本，用户已确认 beta.4 可正常安装汉化和恢复原版。保留已验证的引擎与资源数据版本 beta.1，不因工具转正而重写数据版本；相同汉化数据无需重复安装。
