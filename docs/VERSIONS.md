# 应用、硬件、SDK 与镜像的版本关联

一个 EinkOS Release 是一组固定输入及其镜像，不是多个仓库分支“当前最新”的组合。
应用与硬件仓库有各自的提交历史，不要求两者 SHA 相同；要求发布清单中的对应关系一致。

## 版本对应关系（以提交和哈希为准）

| 项目 | 此镜像使用的版本 |
| --- | --- |
| EinkOS | `v0.1.0` · [087cbaf80cebcbc5d101d37ab3520b3c6fe461c5](https://github.com/dshanpi/EinkOS/tree/087cbaf80cebcbc5d101d37ab3520b3c6fe461c5) |
| 硬件开发分支 | [`einkos-240x360`](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/einkos-240x360)（会继续更新） |
| 硬件固定版本 | [`einkos-v0.1.0`](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/einkos-v0.1.0) · [d24ebd7af24d4b07b0912b19f06a6dad22123eb5](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/d24ebd7af24d4b07b0912b19f06a6dad22123eb5) |
| SDK | TinaSDK 5.0 v1.2；122 个组件的精确提交见 `build-info.json` 的 `sdk_projects` |
| 构建配置 | `t113` / `evb1_auto_nand` / `linux-5.4` / `openwrt` |
| 镜像 SHA-256（解压后） | `f9e73d80b03c7af3df8ca8935a1fd45309ed0355ea5d2c2a33b4871471a8f3fb` |

附件 `release-lock.json` 将应用、硬件包配方、SDK 组件清单和镜像哈希绑定；
`SHA256SUMS` 包含该文件。硬件包配方固定同一应用提交，禁止用分支最新代码代替此版本。
SDK 有 5 个组件记录了本地修改；提交清单不是完整源码或补丁包，
仍须补齐对应源码/修改内容及分发审核后才能公开镜像。安装工具统一使用 [LYNX](https://github.com/dshanpi/lynx-releases)。


## 当前 v0.1.0 的可读记录

- [版本锁定文件](../releases/v0.1.0.json)：与 Release 附件 `release-lock.json` 内容完全一致。
- [SDK 122 个组件的提交记录](../releases/v0.1.0-sdk.json)：来自镜像原始 `build-info.json`，按组件路径锁定。
- 原硬件基线分支为 `tina5v1p2-xr829`，其基线提交为
  [0612287ad1bf7ea2cf66e09fa248580ba6be2bf5](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/0612287ad1bf7ea2cf66e09fa248580ba6be2bf5)。
  墨水屏适配在 `einkos-240x360` 上维护，镜像必须使用上表固定提交。
- SDK 是多仓库工程，没有一个应用 Git 标签能替代整个 SDK 的版本。TinaSDK 5.0 v1.2
  是基线名称；每个组件的精确提交和已记录修改以锁定清单为准。
- 文档 main、硬件开发分支可以继续前进；两个发布标签不得移动，不得把旧镜像标成新提交构建。

本次仅补充可追溯的关联元数据，未重建或替换 v0.1.0 镜像、应用源码包、原始 build-info
及 validation。草稿附件新增锁定文件，SHA256SUMS 增加一项；它仍是待验收草稿。
原构建记录只列出了 5 个 SDK 组件的已跟踪修改路径，未保存完整补丁及所有未跟踪文件，
所以尚不能宣称拿到这些提交就能完整复现镜像。对应源码/补丁补齐后才满足公开发布门禁。

## 获取对应的两个仓库版本

```sh
git clone --branch v0.1.0 https://github.com/dshanpi/EinkOS.git EinkOS-v0.1.0
git clone --branch einkos-v0.1.0 https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5.git EinkOS-hardware-v0.1.0
git -C EinkOS-v0.1.0 rev-parse HEAD
git -C EinkOS-hardware-v0.1.0 rev-parse HEAD
```

结果必须分别等于锁定文件的 `application.commit` 和 `hardware.commit`。
完整 SDK 还需要按清单获取对应组件并应用匹配的覆盖层/补丁，硬件仓库本身不是完整 SDK。

## 后续版本的顺序

1. 先提交应用代码，确定应用版本和提交 A。
2. 硬件仓库的 OpenWrt 包配方固定 A、PKG_VERSION、GitHub 归档 PKG_HASH 和源码时间；
   提交为硬件版本 H。该 GitHub 归档与 Release 的独立源码包格式不同，不能混用二者哈希。
3. 使用 H 及固定 SDK 组件构建、打包、验证实际镜像。记录安装进 rootfs 的应用提交，
   核对镜像内容；保存 SDK 本地补丁/配置和未跟踪构建输入，不能只列修改文件名。
4. 在应用仓库给 A 创建 `vX.Y.Z`，在硬件仓库给 H 创建 `einkos-vX.Y.Z`，推送两个标签。
   分支名用于日常开发，发布以标签解析出的完整 SHA 为准。
5. 运行 `scripts/release.py`，自动读取 H 中的包配方并生成 `release-lock.json` 和校验和。
   将锁定文件及 SDK 组件清单同步到 `releases/` 留档；它们生成于构建之后，避免互相引用提交号的循环。
6. `publish-release.sh` 校验资产、远端两个标签及 H 中的实际配方，再创建草稿；
   `promote-release.sh` 从 GitHub 重新下载全部资产，再次校验后才允许公开。

```sh
python3 scripts/check_release.py dist --channel draft
python3 scripts/version_lock.py dist --verify-remote
```

离线门禁检查各文件之间的一致性；远端门禁检查标签未移动以及硬件包确实固定同一应用。
这些检查不能替代镜像内容核验、完整系统源码分发审核或实机验收。
