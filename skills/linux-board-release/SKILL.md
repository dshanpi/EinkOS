---
name: linux-board-release
description: Apply the dshanpi Linux board open-source and release standard when onboarding another board or preparing independent application updates or coordinated system-image releases. Use for projects adopting DSP-LINUX-001; not for unrelated Linux administration or ordinary application-only edits.
---

# Linux board releases

Read the project's AGENTS.md. Use the pinned [standard entrypoint](../../standards/linux-board-release/README.md),
and [current dual-release gates](../../standards/linux-board-release/v1.1.0/SPEC.md),
then the system-specific [onboarding checklist](../../standards/linux-board-release/v1.0.0/ONBOARDING.md) for the requested phase.
The standard and templates must travel with this skill at the same relative paths when reused in another repo.
Do not install globally or change unrelated repositories just because the skill is present.

## New board

For a new system baseline read the inherited [system specification](../../standards/linux-board-release/v1.0.0/SPEC.md) and
[field contract](../../standards/linux-board-release/v1.0.0/CONTRACT.md).
Create the project's board profile from the linked templates using observed hardware/SDK facts.
Keep unknown values unresolved and label support as planned or in progress. Determine application versus board
ownership, actual build tooling, storage/display variants and LYNX support before claiming installation support.
Do not assume LVGL, T113, Tina, OpenWrt or an e-paper display applies to another board.
Implement and test the board adapter: existing EinkOS release scripts are T113-specific, not a generic engine.

## Release

Require release_kind: application or system. Use independent version/tag streams; preserve legacy tags.
For application-only work with compatible base interfaces, do not require hardware churn, a rebuilt SDK or .img.gz.
Declare the supported system contracts, architectures, dependencies and update/data paths; verify real target packages
on the stated system baselines. Gate public app updates on trusted signatures, compatibility rejection, managed write
boundaries, transaction/power-loss recovery, health/rollback, data preservation and channel/replay handling.
Never disguise kernel, bootloader, partition, base-library or system-contract changes as application payloads.
Current EinkOS updater/application tooling is pending; requirements and templates do not implement it.

For system releases, pin preinstalled application A and hardware H whose recipe references A; capture SDK component
identities, patches, configs and untracked inputs. Build and verify the actual packaged image and bind evidence to its
hash. A new system baseline introducing the updater must validate the initial installation and subsequent update/recovery
chain. Existing systems retain their original A even when the running application later becomes A1.

For either track, verify applicable remote tags and downloaded release assets. Never infer hardware or update success
from a template, screenshot or successful compilation. Apply the appropriate draft/prerelease/stable gates to each target.
Preserve published artifacts, tags and historical metadata; record later docs separately. One target's tests do not cover another.

Perform only the work authorized by the user's task; existing authorization persists. This skill does not grant
permission to flash hardware, publish externally or change global configuration. If a remote write is ambiguous,
inspect its result before retrying; never overwrite public assets or move tags to make a check pass.
Report exact missing evidence and continue independent authorized work. Read the
[T113 example](../../standards/linux-board-release/v1.0.0/examples/T113.md) only for legacy mapping or migration.
