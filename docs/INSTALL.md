# 通过 LYNX 安装配套系统

首版镜像仅用于 100ASK T113-PRO、3.52 英寸 240×360 单色 EPD、
当前 `evb1_auto_nand` NAND 配置。其他板型或存储配置请勿套用。

1. 在 [EinkOS Releases](https://github.com/dshanpi/EinkOS/releases) 获取
   `EinkOS-v<版本>-100ask-t113-pro-240x360.img.gz` 和 `SHA256SUMS`。
   阅读该版本的已知问题及实机验证状态。
2. 校验下载。Linux 可执行 `sha256sum <文件名>.img.gz`，macOS 可执行
   `shasum -a 256 <文件名>.img.gz`，Windows PowerShell 可执行
   `Get-FileHash <文件名>.img.gz -Algorithm SHA256`，与清单中的值比较。
3. 解压 `.gz` 得到 `.img`。Linux/macOS 使用 `gzip -dk <文件名>.img.gz`；
   Windows 使用支持 gzip 的解压软件。不要把 `.gz` 直接作为烧录镜像。
4. 从 [dshanpi/lynx-releases](https://github.com/dshanpi/lynx-releases)
   下载并安装对应平台的 LYNX。烧录工具的安装包和要求以该仓库说明为准。
5. 在 LYNX 新建全志单板，扫描并绑定该板的 USB 烧录接口和串口。
   根据硬件仓库说明，使用板上物理按键/拨码和复位或重新上电进入 FEL/FES。
   确认识别的是目标板，再选择解压后的 `.img` 进行烧录和校验。
6. 烧录完成后按提示启动，通过串口确认系统启动，再检查屏幕出现 EinkOS 桌面。
   可运行 `eink-dashboard --version` 核对版本及应用提交。

**全量烧录会清除目标存储中的原系统及用户数据。** 烧录前保存书籍、阅读记录和
配置；升级首版采用全量烧录，不提供保留数据升级或 OTA 承诺。

桌面没有出现时，检查 `dmesg` 中 EPD 探测、`/dev/epd_100ask` 是否存在，
以及 `logread` 中两个 EinkOS 服务的日志。硬件接线、BUSY 超时和启动恢复问题
请查原硬件仓库的移植记录。问题报告请附板型、镜像版本和不含密码的日志。
