# 调整配置与备份数据

本页的 Shell 命令在**目标板 Linux 串口终端**执行。修改前保留现有配置，确认系统分区可写。

## 查看当前配置

```sh
cat /etc/eink-dashboard.conf
```

| 参数 | 默认值 | 当前解析规则 |
| --- | --- | --- |
| `language` | `zh_CN` | `en_US` 为英文，其余值按中文处理 |
| `refresh_interval_sec` | `60` | 10–3600 秒；非法值回到 60 |
| `full_refresh_every` | `10` | 1–100；非法值回到 10 |
| `key_previous` | `115` | K1，上一项 |
| `key_next` | `373` | K3，下一项 |
| `key_next_alt` | `28` | 下一项兼容映射 |
| `key_confirm` | `119` | K2，确定 |
| `key_confirm_alt` | `114` | 确定兼容映射 |
| `provision_timeout_sec` | `300` | 60–1800 秒；连接服务启动时读取 |
| `timezone` | `CST-8` | POSIX 时区格式，表示中国标准时间 |
| `reader_state_path` | `/etc/eink-os/reader.state` | 阅读记录 |
| `time_state_path` | `/etc/eink-os/time.state` | 保存时间 |

配置采用 `key=value`，不要在键名或等号两侧增加空格。按键码以实际 evdev 事件为准，不根据物理标签猜测。

## 修改并重启桌面

先停止桌面再编辑，避免运行中的设置保存覆盖手工改动：

```sh
/etc/init.d/eink-dashboard stop
cp /etc/eink-dashboard.conf /etc/eink-dashboard.conf.bak
vi /etc/eink-dashboard.conf
/etc/init.d/eink-dashboard start
logread | grep -i eink
```

使用目标系统已有的文本编辑器。重启后确认桌面出现，按键、语言和刷新行为符合预期。

修改 `provision_timeout_sec` 后，还需在结束当前配网操作后执行 `/etc/init.d/eink-connectd restart`，使连接服务重新读取配置。重启连接服务会影响正在进行的连接操作。

需要恢复时停止桌面，将备份复制回原位置，再启动：

```sh
/etc/init.d/eink-dashboard stop
cp /etc/eink-dashboard.conf.bak /etc/eink-dashboard.conf
/etc/init.d/eink-dashboard start
```

## 备份配置和阅读记录

停止桌面，减少备份期间状态变动。下列压缩包位于 `/tmp`，只是传输前的暂存文件：

```sh
/etc/init.d/eink-dashboard stop
tar -czf /tmp/einkos-state-backup.tar.gz /etc/eink-dashboard.conf /etc/eink-os
tar -tzf /tmp/einkos-state-backup.tar.gz
/etc/init.d/eink-dashboard start
```

确认归档包含配置和状态目录，再将其复制到电脑或独立存储。另行复制 `/mnt/UDISK/books` 与 SD 卡书籍；此命令不包含书籍、完整系统或所有厂商网络设置。

检查备份可以读取后再烧录。不要把网络凭据、蓝牙设备信息或个人阅读记录提交到公开仓库。

## 恢复兼容状态

仅在应用版本与状态格式兼容时恢复。先解包到临时目录检查内容，再按需复制配置和状态文件，不直接对根目录执行未经检查的归档覆盖。

书籍路径、大小或修改时间变化会使旧阅读位置失效。时间状态只提供断电后的恢复参考，恢复后仍需校时。
