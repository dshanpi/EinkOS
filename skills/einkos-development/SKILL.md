---
name: einkos-development
description: Develop EinkOS desktop applications, regenerate its real UI screenshots, or prepare and validate its application or firmware releases. Use within the EinkOS project; route kernel, device-tree and bootloader changes to the separate hardware repository.
---

# EinkOS development

Read the repository's `AGENTS.md` first. Select only the workflow needed for the user's change;
this skill does not authorize publishing, flashing hardware, or modifying other repositories by itself.
Existing explicit user authorization remains valid; do not ask for it again.

## Application work

Read [architecture](../../docs/ARCHITECTURE.md) and [repository boundaries](../../docs/REPOSITORIES.md).
Keep application changes in EinkOS. The OpenWrt package recipe and drivers live in the hardware
repository; service scripts/default application settings live here. Preserve the 240×360 / 10800-byte
EPD ABI, installed paths, and versioned local protocol unless a migration is part of the task.
The desktop's IPC is synchronous: do not assume the service process makes calls nonblocking.
Run `make test`; cross-compile when application behavior changes using [BUILD](../../docs/BUILD.md).

## UI and documentation

Run `make screenshots` to render production `src/ui.c` and fonts into a host memory framebuffer.
For phone HTML changes also use `scripts/capture-portal.sh`; see [SCREENSHOTS](../../docs/SCREENSHOTS.md).
Review actual PNGs and update README coverage when adding routes or visible states. Keep demo
networks, passcodes, time and metrics fictional and label captures as host-rendered, not real hardware.
Do not substitute generated artwork or hand-drawn mockups for UI screenshots.
Run `python3 scripts/check_docs.py`. Do not launch production connectd on a workstation to take pictures.

## Releases

Classify the change with [DSP-LINUX-001 1.1.0](../../standards/linux-board-release/v1.1.0/SPEC.md)
and [RELEASING](../../docs/RELEASING.md) first. Compatible application-only releases do not require a new
hardware commit/tag, SDK build or system image. Bind the application commit/packages to supported system contracts,
architecture/dependencies, update paths and actual upgrade/rollback evidence. Preserve system baseline provenance
and record the currently installed app separately. Do not bundle base-system changes as app updates.

Before application updates are public, require trusted signature and compatibility rejection, package boundaries,
transaction recovery, health-based rollback and user-data preservation checks on declared baselines. Current
scripts are system-only and the updater/application gates are not implemented; never infer OTA support from this skill.

For system images, follow [version linkage](../../docs/VERSIONS.md). Bind preinstalled application, hardware recipe,
SDK inputs and image hashes; check both remote tags and the actual hardware recipe. Use the existing system asset
checker and promotion script only for supported system formats. Source/distribution and hardware evidence gates remain.
Never move tags, overwrite public assets or fabricate tests. If a remote write is ambiguous, inspect the result
before retrying. Existing user authorization persists; this workflow does not authorize unrelated actions.

For another Linux board, use the [shared standard](../../standards/linux-board-release/README.md)
with its board-specific adapter requirements; do not extend T113 constants and claim generic support.
