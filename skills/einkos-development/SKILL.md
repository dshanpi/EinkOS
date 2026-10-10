---
name: einkos-development
description: Develop EinkOS desktop applications, regenerate its real UI screenshots, or prepare and validate its firmware releases. Use within the EinkOS project; route kernel, device-tree and bootloader changes to the separate hardware repository.
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

Follow [RELEASING](../../docs/RELEASING.md) and [version linkage](../../docs/VERSIONS.md).
Bind application tag, hardware tag/recipe, SDK component revisions and image hashes in release-lock.json;
verify both remote tags and the pinned hardware recipe before uploading or promoting. Never move a release tag. Build assets identify the exact application and hardware
commits, not today's documentation HEAD. Validate draft assets with `scripts/check_release.py`.
For an authorized public promotion use `scripts/promote-release.sh`; it downloads and checks the
actual remote assets. Public prereleases require build and distribution-source evidence; stable
releases additionally require all hardware checks including LYNX flashing. Never fabricate test results.
If a remote write has an ambiguous failure, inspect the release before retrying; do not overwrite
published assets. Report unmet evidence as the exact gate result and continue independent authorized work.
