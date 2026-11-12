# 使用 LYNX 烧录配套系统

本流程适用于 **100ASK T113-PRO、3.52 英寸 240×360 单色 EPD、evb1_auto_nand NAND 配置**。完成后应能从串口确认 Linux 启动，并在屏幕上看到 EinkOS 桌面。

## 1. 准备板卡与安装文件

准备匹配板卡、屏幕和转接板、稳定电源、可传输数据的 USB 线以及调试串口连接。先按[硬件说明](HARDWARE.md)核对板型和接线。

从 [EinkOS Releases](https://github.com/dshanpi/EinkOS/releases)选择目标版本，下载：

- `EinkOS-v<版本>-100ask-t113-pro-240x360.img.gz`
- `SHA256SUMS`
- `release-lock.json` 和 `validation.json`

文件名中的 `<版本>` 必须替换为所选 Release 的实际版本。阅读发布说明中的已知问题和未验证项；当前 v0.1.0 标记为预发布，不作为稳定版验收结论。

## 2. 备份现有数据

全量烧录会清除目标存储中的原系统及用户数据。先把需要保留的以下内容复制到电脑或其他独立存储，并确认备份可读：

- `/mnt/UDISK/books` 和需要保留的 SD 卡书籍。
- `/etc/eink-dashboard.conf`。
- `/etc/eink-os/` 中的阅读与时间状态。

具体备份操作见[备份配置和阅读记录](CONFIGURATION.md)。保存在即将烧录存储上的临时压缩包不算独立备份。

## 3. 校验镜像

在下载文件所在目录执行。以下文件名适用于 v0.1.0，选择其他版本时同步替换。

Windows PowerShell：

```powershell
Get-FileHash .\EinkOS-v0.1.0-100ask-t113-pro-240x360.img.gz -Algorithm SHA256
Get-Content .\SHA256SUMS
```

Linux：

```bash
sha256sum EinkOS-v0.1.0-100ask-t113-pro-240x360.img.gz
cat SHA256SUMS
```

macOS 使用 `shasum -a 256 <实际文件名>`。

逐字比较镜像哈希与 `SHA256SUMS` 中同名条目的值，大小写差异可以忽略。**哈希不一致时停止，重新下载并再次校验。**

## 4. 解压安装镜像

Linux/macOS 在下载目录执行：

```bash
gzip -dk EinkOS-v0.1.0-100ask-t113-pro-240x360.img.gz
```

Windows 使用支持 gzip 的解压软件。检查得到同名 `.img` 文件，保留 `.img.gz` 以便复核。LYNX 选择解压后的 `.img`，不把压缩文件直接作为镜像。

可再次计算 `.img` 的 SHA-256，与 `release-lock.json` 中的 `image.uncompressed_sha256` 比较。

## 5. 连接并识别目标板

从 [LYNX 发布仓库](https://github.com/dshanpi/lynx-releases)下载适合电脑系统的安装包。进入 Linux 工作台，新建目标单板，配置全志目标及适用烧录工具，扫描并保存 USB 烧录接口与调试串口绑定。

确认串口属于目标板，按板卡说明配置波特率、线序和电平。USB 接口、串口和 SSH 终端是不同对象，不能仅凭名称判断绑定正确。

根据板卡启动条件选择进入下载模式的方法：

| 条件 | 操作 | 检查结果 |
| --- | --- | --- |
| 能进入配套 U-Boot 控制台 | 在串口启动倒计时内中断启动，在 **U-Boot 提示符**执行 `efex` | LYNX 重新扫描后识别到全志下载设备 |
| 不能进入 U-Boot | 按当前板卡硬件说明使用物理下载按键或拨码，配合复位或重新上电 | LYNX 识别到目标 USB 下载设备 |

`efex` 依据[配套硬件仓库说明](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/einkos-240x360)，不是 Linux Shell 命令。无法进入 U-Boot 时，物理按键名称及操作顺序以所用硬件版本说明为准。

FEL 是全志芯片的下载入口；具体 FES Loader、传输和写入由适配工具处理。此处不提供未经本板验证的 Loader 或裸写地址。

如果未识别、设备被占用或目标不匹配，先停止，核对数据线、接口、USB 驱动和当前下载模式。

## 6. 写入并检查烧录结果

1. 在目标单板的烧录入口选择已校验的 `.img`。
2. 核对板卡身份、存储目标、镜像路径及工具所需 Loader。
3. 启动烧录，期间保持供电和连接稳定。
4. 等待工具报告成功终态，并核对写入与校验结果。

传输达到 100% 不代表校验通过。失败或终态不明时保存日志，确认任务已结束，再按错误处理；不要连续重复擦写。

## 7. 检查系统启动

按工具提示退出下载模式并启动系统。在**目标板 Linux 串口终端**执行：

```sh
eink-dashboard --version
ls -l /dev/epd_100ask
logread | grep -i eink
```

确认版本与所选镜像一致、EPD 设备节点存在、桌面服务没有持续重启，再检查屏幕显示和按键响应。

烧录成功、Linux 启动和桌面可用分别检查。屏幕没有桌面时，按[故障排查](TROUBLESHOOTING.md)定位；启动正常后执行[首次使用流程](QUICKSTART.md)。

## 区分系统烧录与应用更新

本流程执行全量系统烧录。兼容的应用更新在发布规范上可独立于系统镜像，但当前设备更新器及应用升级门禁工具尚未实现，不应据此宣称已支持 OTA 或自动回滚。
