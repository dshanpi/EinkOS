# 确认硬件与系统

烧录前确认板型、存储配置、屏幕和转接板一致。当前配置不能直接套用到同系列其他板卡、eMMC 版本或不同尺寸屏幕。

## 核对配套配置

| 项目 | 当前配置 |
| --- | --- |
| 开发板 | 100ASK T113-PRO |
| 显示屏 | 3.52 英寸、240×360、单色 EPD |
| 转接方式 | 100ASK SPI-to-EPD 转接板，接底板 9 针 SPI TFT 接口 |
| 存储与板级配置 | NAND，`evb1_auto_nand` |
| SDK 基线 | TinaSDK 5.0 v1.2 |
| 构建选择 | `t113 / evb1_auto_nand / linux-5.4 / openwrt` |
| 显示设备 | `/dev/epd_100ask` |
| 帧格式 | 240×360、1bpp、MSB first、白色为 1，单帧 10800 字节 |
| 启动管理 | OpenWrt procd |

## 检查屏幕接线

断电后按板卡和转接板原理图核对方向及连接关系：

| EPD 信号 | T113 引脚 | 说明 |
| --- | --- | --- |
| CS | PD10 | SPI1_CS0 |
| SCK | PD11 | SPI1_CLK |
| MOSI | PD12 | SPI1_MOSI |
| RESET | PD13 | 原 MISO 引脚改作复位，不进行 SPI 读取 |
| DC | PB5 | 命令与数据选择 |
| BUSY | PD22 | 低电平忙，高电平空闲 |

这些引脚与 LCD0、PWM7 存在复用冲突；当前板级配置关闭冲突功能。不要使用旧需求中的 `DC=PD22、BUSY=PB3` 接线。

连接依据及设备树路径见[硬件移植记录](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/blob/einkos-240x360/eink-3.52/PORTING_240X360_T113.md)。

## 选择源码仓库

应用、用户态显示适配和连接服务在 EinkOS 维护。内核、设备树、Bootloader 和 OpenWrt 包配方在[硬件仓库](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/einkos-240x360)维护；该仓库是覆盖层，不是完整 TinaSDK。

复现 v0.1.0 时使用[版本锁定信息](VERSIONS.md)中的固定提交。日常开发分支可能已变化，不能替代历史版本记录。
