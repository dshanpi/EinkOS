# EinkOS repository guidance

- Application source, user-space adapters, runtime service files, screenshots and documentation live here.
  Kernel drivers, device trees, bootloader, board configuration and the OpenWrt package recipe live in the
  [hardware repository](https://github.com/DongshanPI/100ASK_T113-PRO_TinaSDK5/tree/einkos-240x360).
- Use the relevant workflow in [the project skill](skills/einkos-development/SKILL.md) for application,
  screenshot or release work. Detailed requirements: [DEVELOPMENT](docs/DEVELOPMENT.md).
- Preserve installed paths, state formats, the local protocol and the EPD ABI unless the task includes a migration.
- UI changes require regenerated production-rendered screenshots and visual review. Capture tools use
  fictional fixtures; never start the production network daemon on the host just for screenshots.
- Run `make test` for logic/tooling changes, `make screenshots` for UI changes, and
  `python3 scripts/check_docs.py` for documentation/gallery changes. Cross-compile product code changes.
- Source packages and images must match recorded commits. Documentation HEAD may be newer than a firmware release.
  Use [release gates](docs/RELEASING.md); never label missing hardware tests as passed or drafts as public downloads.
- Firmware binaries belong in GitHub Release assets, not Git. Installation points users to
  https://github.com/dshanpi/lynx-releases. Preserve third-party licenses and don't commit personal device data.

- For new Linux boards or general release-process work, use [DSP-LINUX-001](standards/linux-board-release/README.md)
  and [linux-board-release](skills/linux-board-release/SKILL.md). Existing T113 releases retain their recorded schema and evidence;
  a standards document alone does not implement multi-board support.

- Release classification is mandatory under [DSP-LINUX-001 1.1.0](standards/linux-board-release/v1.1.0/SPEC.md):
  application releases are independent of system images. Do not require hardware churn, SDK rebuilds or a new image
  for compatible application-only work. Preserve each system's original preinstalled application identity.
- Application updates must satisfy compatibility, trusted signature, payload-boundary, transactional install,
  power-loss recovery, health/rollback and user-data gates. Never package kernel/DTB/bootloader/base-system changes
  as an application update. Current scripts are system-only; the device updater and application gate implementation
  are pending, so do not claim OTA readiness or bypass the missing implementation with metadata.
