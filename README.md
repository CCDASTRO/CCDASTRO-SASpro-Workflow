# CCDASTRO Seti Astro Suite Pro Workflow

Version 0.3.0 — development release, October 22, 2026.

A standalone image-processing workflow for Seti Astro Suite Pro, with Color & Tone controls, masks, curves and review of each processing pass. This project maintains its own source, presets, tests and versioning.

## Download, install and update

Current release: **v0.3.0** (development release). [Release notes](https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases/tag/v0.3.0) · [Windows installer](https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases/download/v0.3.0/CCDASTRO-SASpro-Workflow-0.3.0-Setup.exe).

Includes Color & Tone Studio, reviewed processing passes, FITS export, presets and reports. Optional host tools use native command settings; dedicated Siril integration panels are not included in this release.

[Download the Windows installer or ZIP](https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases). Use the Windows installer for first installation and later upgrades. See [INSTALL.md](INSTALL.md) for exact steps, migration from earlier ZIP copies, and troubleshooting. The workflow's **Check for updates** button finds new releases and opens their download page. Each installer uses a stable per-user folder and preserves separately saved images/presets.

## What works

- Work on a copy of an open RGB or monochrome image.
- Add, reorder and review individual processing passes; accept or discard each candidate.
- Independent channel stretch with R/G/B target and amount sliders, individual channel views, RGB recombination review, and optional registered mono FITS inputs.
- Linked automatic stretch, a simple background-plane fit, and green suppression.
- Color & Tone Studio: live sampled before/after/mask/overlay views, hue presets and picker, feathered hue and tonal selections, inversion, amount, exposure, contrast, shadows/highlights, whites/blacks, saturation, vibrance, temperature/tint, and master/R/G/B curve sliders.
- Review full-resolution Color & Tone output before accepting it. Use stretched data for these adjustments.
- Recombine with a separately supplied, registered stars FITS image after inspecting alignment.
- Save/load host-specific JSON workflow presets. Save a new float32 FITS result with a JSON pass report.
- Optional native host commands on a separate working image. Parameters currently use a JSON editor.

## Scope of this build

This is an initial development build. There is no unattended run-all, automatic LRGB/narrowband orchestration, reference-color matching, automatic registration or starless/stars pairing, or full-resolution pan/zoom inspector yet. Color & Tone settings are recorded in the output report; the dialog starts with neutral controls on each new pass. The simple background-plane fit is not AutoDBE or an AI background model. Use conservative amounts and inspect nebulosity.

No third-party AI model, plugin or commercial license is bundled. Native AI, color-calibration and other optional commands depend on the host's installed tools, paths, models, licenses and preset schema. Only the native stretch has been exercised in the installed application; the other allowlisted native commands still need individual validation. An unsuccessful native command may leave a working image open for inspection.

FITS is the portable interchange format. The original image/file is preserved. Existing output files are refused. FITS headers are preserved where supplied by the host; arbitrary host application state, layers and display settings are not serialized to FITS. Save through the host if its native project metadata is needed.

## Independent channel stretch (linear input)

Use **Independent channel stretch (linear RGB / mono masters)** before the final nonlinear stretch, instead of adding a linked stretch as well. Work from a linear RGB image, or select three already registered mono FITS masters for the R / G / B output slots. For SHO, assign SII to R, Ha to G and OIII to B; choose the mapping appropriate to your palette. This tool does not register images or infer filters. Matching dimensions alone do not prove registration.

1. Confirm that the inputs are linear and registered. If loading masters, all three must be mono and have identical dimensions. Their source files remain unchanged; output uses the first master’s FITS header, with structural cards updated for RGB. Conflicting per-filter metadata is not merged.
2. Start with the shared median target of **0.23**. Adjust each channel’s target (0.01–0.50) and stretch amount (0–100%) independently. A lower R target or amount can reduce red dominance. Amount zero leaves that channel unchanged.
3. Click **Update preview**. Inspect Recombined RGB, each grayscale channel and Before RGB. Preview sampling uses the same fixed per-channel plan as the full-resolution result.
4. Click **Review full-resolution result**, then **Accept candidate** or **Discard candidate** in the workflow. Nothing is committed before acceptance. The configured step is added to the workflow list for presets; previewing it again opens the review and requires linear confirmation again. Choose mono input files again for each new review; presets store controls, not image paths. Accepted reports record the loaded master paths when applicable.
5. Continue with stretched-image finishing, Color & Tone or your optional finishing tools. Do not add another automatic stretch to the accepted result.

Each channel uses a robust median/MAD black-point estimate and its own midtones transfer function, followed by its amount blend with the original channel. The Python builds estimate statistics on a grid of at most 512 × 512 samples. Processing is independent per channel and recombines the output planes into RGB. Applying those transforms to the channels of a linear RGB mapping is mathematically equivalent to stretching the same mapped mono planes before combination. Equal targets are an artistic balance choice: they change relative emission brightness and do not preserve calibrated flux ratios or guarantee a particular palette. Already stretched data should use Color & Tone instead.

## Installation

Start with [INSTALL.md](INSTALL.md). It includes Windows folder layouts, menu steps, first-launch checks, updates and troubleshooting. Extract the ZIP before installation; keep the launcher and its complete companion package folder together.

## First test

1. Open a small, saved FITS copy of an image in the host.
2. Launch the workflow, add Linked automatic stretch for linear input, then Preview selected step.
3. Switch Current/Candidate to compare. Accept candidate only when satisfied.
4. Open Color & Tone Studio. Choose a hue or tonal range, inspect Mask/Mask overlay, then adjust sliders and curves.
5. Click Review full-resolution result. Back in the workflow, accept or discard it.
6. Save result + report to a new filename. Or use Open result as new host document to preserve the host metadata in a new document.

Each accepted pass starts from the current workflow result. Re-previewing a pass applies it again to that current result. Presets contain the workflow list, while the result report records passes actually accepted. Presets for the other host are rejected.

## Native passes

Example parameters: `{"command":"stat_stretch","preset":{"target_median":0.23}}`. Other allowlisted command IDs are listed in `ccdastro_saspro/_host.py`. Obtain valid preset fields from the host's own command settings and current scripting documentation.

The adapter creates a separate working document, passes it explicitly as `target_doc` to `ctx.run_command`, reads the result and restores the previous active view. Working documents remain open. Open result as new host document creates another document without replacing the source. Commands that create a separate output rather than updating their target need additional adapter handling and are not yet verified.

## Development and verification

Python 3.10+ with NumPy, PyQt6 and Astropy. The SASpro launcher uses its embedded environment; development tests can use a separate Python environment.

Run `python -m unittest discover -s tests -v` from this repository with dependencies installed. The offline UI demo is `python -m ccdastro_saspro._demo`; it processes only a synthetic image.

Automated checks cover source-copy protection, mask boundaries, curve monotonicity, Color & Tone reference outputs, stretch behavior, background-plane fitting, FITS roundtrips/no overwrite, and host adapter behavior. See `validation/` for the native application smoke-test records. Tests use small synthetic inputs; large astrophotography datasets and optional AI commands need further field testing. Processing is synchronous, so full-resolution operations may temporarily make the dialog unresponsive.

## Credits and ownership

CCDASTRO workflow/UI and the Color & Tone implementation: Chuck Faranda / CCDASTRO, Inc. The color controls were inspired by Lighthouse by Neven Krcmarek; the Siril Lighthouse header also credits Yannick Dutertre (Cuiv) for its port. No Lighthouse source is bundled. Color & Tone processing is implemented by CCDASTRO and checked against saved reference values.

Seti Astro Suite Pro and Cosmic Clarity: Franklin Marek / Seti Astro and contributors — https://www.setiastro.com/ and https://github.com/setiastro/setiastrosuitepro/wiki/Scripting . Optional GraXpert, StarNet (Mikita Misiura), RC Astro (Russell Croman), and SyQon integrations remain their authors' work and require separate installation/licensing. No source, model weights, executables or credentials for those tools are bundled.

This workflow brings host features together; underlying algorithms and external tools remain the work of their respective authors. Third-party packages and optional tools retain their own licenses. No endorsement or affiliation is implied. See THIRD_PARTY_NOTICES.md.

Copyright 2026 CCDASTRO, Inc. All rights reserved. No new open-source license is granted by this development package.
