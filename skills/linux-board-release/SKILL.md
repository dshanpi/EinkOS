---
name: linux-board-release
description: Apply the dshanpi Linux board open-source and release standard when onboarding another board or preparing a coordinated application, hardware, SDK and system-image release. Use for projects adopting DSP-LINUX-001; not for unrelated Linux administration or ordinary application-only edits.
---

# Linux board releases

Read the project's AGENTS.md. Use the pinned [standard entrypoint](../../standards/linux-board-release/README.md),
then [onboarding checklist](../../standards/linux-board-release/v1.0.0/ONBOARDING.md) for the requested phase.
The standard and templates must travel with this skill at the same relative paths when reused in another repo.
Do not install globally or change unrelated repositories just because the skill is present.

## New board

Read the [specification](../../standards/linux-board-release/v1.0.0/SPEC.md) and
[field contract](../../standards/linux-board-release/v1.0.0/CONTRACT.md).
Create the project's board profile from the linked templates using observed hardware/SDK facts.
Keep unknown values unresolved and label support as planned or in progress. Determine application versus board
ownership, actual build tooling, storage/display variants and LYNX support before claiming installation support.
Do not assume LVGL, T113, Tina, OpenWrt or an e-paper display applies to another board.
Implement and test the board adapter: existing EinkOS release scripts are T113-specific, not a generic engine.

## Release

Pin application A; make the hardware integration recipe consume A and its source hash; pin hardware H.
Capture SDK component identities, patches, configs and untracked build inputs, not only git status paths.
Build from these inputs, verify the actual packaged image identity and bind test evidence to its image hash.
Generate the release lock and per-board assets using the project's implemented adapter. Never fill test results
from templates or infer hardware success from screenshots, host tests or a successful compiler invocation.

Verify remote tags and the actual recipe at H; after upload download and recheck actual remote assets.
Keep pending source/distribution evidence in Draft; apply prerelease/stable gates per supported board.
Preserve existing release images/tags and historical metadata. Record later documentation separately.
For multi-board releases, use unique per-board filenames and independent evidence; one board's test does not cover another.

Perform only the work authorized by the user's task; existing authorization persists. This skill does not grant
permission to flash hardware, publish externally or change global configuration. If a remote write is ambiguous,
inspect its result before retrying; never overwrite public assets or move tags to make a check pass.
Report exact missing evidence and continue independent authorized work. Read the
[T113 example](../../standards/linux-board-release/v1.0.0/examples/T113.md) only for legacy mapping or migration.
