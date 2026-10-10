# 构建 EinkOS

需要 Linux、GNU Make、C 编译器和 Python 3。LVGL 已包含在源码中，无需联网拉取子模块。

## 主机测试

```sh
make test
make -j2 eink-dashboard
./eink-dashboard --version
```

主机编译用于检验可移植构建和版本信息，不提供屏幕模拟器。不要在开发电脑上
启动 `eink-connectd`：Tina 后端需要操作网络、时间和系统服务。

## ARM 交叉编译

从原硬件项目配置并构建过的 SDK 获取工具链及目标 staging 目录。先 `make clean`，
避免复用另一架构的对象文件：

```sh
export EINK_SDK=/path/to/T113-tina5v1.2-sdk
export EINK_TOOLCHAIN="$EINK_SDK/out/t113/evb1_auto_nand/buildroot/buildroot/host/opt/ext-toolchain/bin/arm-linux-gnueabi-"
export EINK_STAGING="$EINK_SDK/out/t113/evb1_auto_nand/openwrt/staging_dir/target"
make clean
make -j2 CC="${EINK_TOOLCHAIN}gcc" \
  BT_INCLUDE_DIR="$EINK_STAGING/usr/include" PLATFORM=tina
```

编译器使用自身默认 sysroot；如使用其他工具链，可通过 `SYSROOT` 显式指定匹配的
目标 sysroot。不要将任意宿主机头文件与目标编译器混用。
`LVGL_DIR` 可替换默认 LVGL 源码路径，正式发布应使用仓库附带版本。
`COMMIT` 和 `SOURCE_DATE_EPOCH` 由 Git 或源码包内版本文件读取。
连接服务为动态链接；运行时由板级系统提供 `libbtmg.so`、`/bin/wifi`、`iw`、
`dnsmasq`、`ntpd` 和 procd。应用源码不附带厂商 SDK 头文件及库。

安装到目标根文件系统的暂存目录：

```sh
make DESTDIR=/path/to/rootfs install
```

应用安装两个程序和两个 procd 服务；驱动诊断工具 `epd-test` 由硬件仓库提供。

## 构建完整系统

按照原硬件仓库说明，将其覆盖层应用到对应 TinaSDK。选择 `t113`、
`evb1_auto_nand`、`linux-5.4`、`openwrt`，执行：

```sh
./build.sh
./build.sh pack
```

输出为 `out/t113_linux_evb1_auto_nand_uart0.img`。
板级 OpenWrt 包固定本项目提交和下载 SHA-256，从本仓库获取源码构建。
升级应用时更新硬件仓库的固定提交、版本、构建时间和源码哈希，再重新编译系统。
不要使用旧镜像作为新版本产物。

## 兼容接口

保持 `/usr/bin/eink-dashboard`、`/usr/bin/eink-connectd`、
`/etc/eink-dashboard.conf` 和 `/etc/eink-os/` 状态目录不变。
显示仍使用 `/dev/epd_100ask`、240×360 / 10800 字节帧和原 ioctl；
`include/uapi/epd_100ask.h` 与硬件驱动共同定义 ABI。
现有连接服务本地协议保持版本及布局不变。
厂商网络和蓝牙调用集中在 `platforms/tina/connectd.c`，屏幕访问在
`platforms/tina/epd_disp.c`。新平台需提供适配实现，首版不宣称已支持。
