# CCDASTRO Seti Astro Suite Pro Workflow

Version 0.5.0 — development release, October 22, 2026.

A standalone image-processing workflow for Seti Astro Suite Pro, with Color & Tone controls, masks, curves and review of each processing pass. This project maintains its own source, presets, tests and versioning.

## Download, install and update

Current release: **v0.5.0** (development release). [Release notes](https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases/tag/v0.5.0) · [Windows installer](https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases/download/v0.5.0/CCDASTRO-SASpro-Workflow-0.5.0-Setup.exe).

Includes Color & Tone Studio, reviewed processing passes, FITS export, presets and reports. Includes direct SyQon Studio CLI controls and separately configured native host commands.

[Download the Windows installer or ZIP](https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases). Use the Windows installer for first installation and later upgrades. See [INSTALL.md](INSTALL.md) for exact steps, migration from earlier ZIP copies, and troubleshooting. The workflow provides optional daily startup update notices and a manual **Check for updates** button. Each installer uses a stable per-user folder and preserves separately saved images/presets.

**Check for updates at startup** is enabled by default. It quietly checks this project’s GitHub releases in the background at most once every 24 hours, including development releases. When a newer version is found, a small **Update available: v… — Downloads** button appears in the workflow. Click it to open that release page. A known newer version remains visible on later launches between checks. No startup popup interrupts processing; offline failures are quiet. Clear the startup checkbox to disable automatic checks; that choice is remembered separately for this workflow. **Check for updates** still checks immediately whenever you choose, even if startup checks are disabled or a daily check already ran. Closing the workflow never waits for the network check. Updates are downloaded and installed manually: close the host and run the new Windows installer. Existing images and personal presets stay where you saved them.

## What works

- Work on a copy of an open RGB or monochrome image.
- Add, reorder and review individual processing passes; accept or discard each candidate.
- Independent channel stretch with R/G/B target and amount sliders, individual channel views, RGB recombination review, and optional registered mono FITS inputs.
- Linked automatic stretch, a simple background-plane fit, and green suppression.
- Color & Tone Studio: live sampled before/after/mask/overlay views, hue presets and picker, feathered hue and tonal selections, inversion, amount, exposure, contrast, shadows/highlights, whites/blacks, saturation, vibrance, temperature/tint, and master/R/G/B curve sliders.
- Review full-resolution Color & Tone output before accepting it. Use stretched data for these adjustments.
- Recombine with a separately supplied, registered stars FITS image after inspecting alignment.
- Save/load host-specific JSON workflow presets. Save a new float32 FITS result with a JSON pass report.
- SyQon Studio CLI: supported neural models, declared domain, application amount, Parallax stages, Axiom stars output, cancellable processing and explicit candidate acceptance.
- Optional native host commands on a separate working image. Parameters currently use a JSON editor.

## Scope of this build

This is an initial development build. There is no unattended run-all, automatic LRGB/narrowband orchestration, reference-color matching, automatic registration or discovery of unrelated stars files, or full-resolution pan/zoom inspector yet. Color & Tone settings are recorded in the output report; the dialog starts with neutral controls on each new pass. The simple background-plane fit is not AutoDBE or an AI background model. Use conservative amounts and inspect nebulosity.

No third-party AI model, plugin or commercial license is bundled. Native AI, color-calibration and other optional commands depend on the host's installed tools, paths, models, licenses and preset schema. Only the native stretch has been exercised in the installed application; the other allowlisted native commands still need individual validation. An unsuccessful native command may leave a working image open for inspection.

FITS is the portable interchange format. The original image/file is preserved. Existing output files are refused. FITS headers are preserved where supplied by the host; arbitrary host application state, layers and display settings are not serialized to FITS. Save through the host if its native project metadata is needed.

## Independent channel stretch (linear input)

Use **Independent channel stretch (linear RGB / mono masters)** before the final nonlinear stretch, instead of adding a linked stretch as well. Work from a linear RGB image, or select three already registered mono FITS masters for the R / G / B output slots. For SHO, assign SII to R, Ha to G and OIII to B; choose the mapping appropriate to your palette. This tool does not register images or infer filters. Matching dimensions alone do not prove registration.

1. Confirm that the inputs are linear and registered. If loading masters, all three must be mono and have identical dimensions. Their source files remain unchanged; output uses the first master’s FITS header, with structural cards updated for RGB. Conflicting per-filter metadata is not merged.
2. Start with the shared median target of **0.23**. Adjust each channel’s target (0.01–0.50) and stretch amount (0–100%) independently. A lower R target or amount can reduce red dominance. Amount zero leaves that channel unchanged.
3. Click **Update preview**. Inspect Recombined RGB, each grayscale channel and Before RGB. Preview sampling uses the same fixed per-channel plan as the full-resolution result.
4. Click **Review full-resolution result**, then **Accept candidate** or **Discard candidate** in the workflow. Nothing is committed before acceptance. The configured step is added to the workflow list for presets; previewing it again opens the review and requires linear confirmation again. Choose mono input files again for each new review; presets store controls, not image paths. Accepted reports record the loaded master paths when applicable.
5. Continue with stretched-image finishing, Color & Tone or your optional finishing tools. Do not add another automatic stretch to the accepted result.

Each channel uses a robust median/MAD black-point estimate and its own midtones transfer function, followed by its amount blend with the original channel. The Python builds estimate statistics on a grid of at most 532 × 532 samples. Processing is independent per channel and recombines the output planes into RGB. Applying those transforms to the channels of a linear RGB mapping is mathematically equivalent to stretching the same mapped mono planes before combination. Equal targets are an artistic balance choice: they change relative emission brightness and do not preserve calibrated flux ratios or guarantee a particular palette. Already stretched data should use Color & Tone instead.

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

## SyQon graphical editor (new in v0.5.0)

1. Install or update SyQon Studio, sign in and finish Required Items. This option needs a Studio CLI whose `--help` advertises `-gui`; Seti v1.22.12 describes support for an upcoming Studio release. Updating Seti alone does not add that capability to Studio.
2. Choose **SyQon Studio CLI... > Add step**, then select **Studio Editor (GUI)** in the model list. **Check CLI / models** verifies the executable and editor support. Existing model choices remain available on older Studio versions; an unavailable editor produces an update message before image processing.
3. Select the step and click **Preview selected step**. The editor opens with a temporary FITS copy of the current workflow result. Choose the model, region of interest (ROI), display-only autostretch and processing intensity inside Studio. Its editor owns these controls, so our domain, amount, Parallax and stars controls are disabled in this mode.
4. Click **Done** in Studio. Back in our workflow, compare Current and Candidate, then **Accept candidate** or **Discard candidate**. Done alone does not accept the result. No additional host mask or intensity blend is applied to the returned candidate.
5. Click **Cancel** in Studio, or cancel in our waiting dialog, to retain the previous result without an error popup. Closing the waiting dialog requests cancellation and waits for the process to stop before cleaning its temporary files.

Editor input and output use matching FITS containers. Output must have valid finite pixels and the original geometry. The original host image and metadata are preserved. Editor mode does not request separate stars/gradient files; use the existing Axiom model option when separate stars are needed. Presets remember the editor choice, not adjustments made inside Studio. Reports identify GUI mode and editor-managed domain; they do not claim to capture the editor's internal model/ROI/control choices.

Validation for v0.5.0: 53 processing/Qt tests passed, including editor capability detection, command construction, simulated Done/Cancel, candidate handling and preservation of input. The new vendor editor has not been exercised end-to-end in the installed application. Earlier live Studio 1.1.9 tests below cover the headless models only.

## SyQon Studio CLI (introduced in v0.4.0)

This direct integration uses the separately installed Studio `syqon-cli`. It is independent of the host-native `syqontools` command, which remains available through Host-native command. Sign in and install **Required Items** in SyQon Studio first. The CLI resolves the installed models and account entitlements; the workflow never loads model weights or credentials. See the [official integration guide](https://syqon.eu/develop).

1. In the step selector, choose **SyQon Studio CLI…**, then **Add step**.
2. Confirm the executable path, or browse to `syqon-cli.exe` inside your Studio installation. Automatic detection checks the saved path, `SYQON_CLI_PATH`, the Windows application-path registration and standard locations. **Check CLI / models** reads `--version` and `--list-models`; the list describes supported model IDs, not installed models or licensed access.
3. Choose DeepGradient, a Prism model, Parallax or Axiom. Set the actual **Input domain** and application amount. DeepGradient, Prism Essential/Advanced and Legacy V2 require linear input; Legacy V1 requires nonlinear input. Ultra/Max and Parallax accept both. Parallax exposes independent correction, reduction and deblur stages, plus a family selector for premium Parallax; at least one stage must be enabled. Studio chooses the device.
4. For Axiom, optionally request a separate stars image. **OK** stores the step controls; executable selection is remembered locally and omitted from shared presets.
5. Select the step and click **Preview selected step**. Processing runs in a cancellable worker on a temporary float32 FITS copy. **Accept candidate** commits to the workflow copy; **Discard candidate** preserves the prior result. Original documents and source files are unchanged.
6. After accepting Axiom with stars output, use **Recombine with generated SyQon stars** or **Save generated SyQon stars FITS**. Recombination itself is another reviewed candidate. The returned starless/stars pair is compared with the input to select additive or screen recombination; neural processing can change the result, so exact reconstruction is not promised. Generated stars are retained only when their pass is accepted.

Metadata supplied by the host is retained, input/output geometry and finite pixels are checked, and FITS row orientation is normalized. Accepted reports record the chosen model, runtime Studio version, input domain and recombination method. Requests fail without acceptance if the model is unavailable, access is denied, output is missing/invalid or processing is cancelled. A supported model ID does not prove entitlement or completed Required Items installation.

Validated with **Studio 1.1.9** on Windows: DeepGradient, Prism Essential, Parallax Nano and Axiom Mini passed synthetic CLI and Qt candidate/acceptance checks; zero-amount orientation was exact. Licensed variants use the documented option contract but were not individually exercised. Pano Studio and Observatory 3D remain Studio workspaces; this integration runs the neural CLI and does not automate those interfaces. The existing native host commands remain separately configured.

## Native passes

Example parameters: `{"command":"stat_stretch","preset":{"target_median":0.23}}`. Other allowlisted command IDs are listed in `ccdastro_saspro/_host.py`. Obtain valid preset fields from the host's own command settings and current scripting documentation.

The adapter creates a separate working document, passes it explicitly as `target_doc` to `ctx.run_command`, reads the result and restores the previous active view. Working documents remain open. Open result as new host document creates another document without replacing the source. Commands that create a separate output rather than updating their target need additional adapter handling and are not yet verified.

## Development and verification

Python 3.10+ with NumPy, PyQt6 and Astropy. The SASpro launcher uses its embedded environment; development tests can use a separate Python environment.

Run `python -m unittest discover -s tests -v` from this repository with dependencies installed. The offline UI demo is `python -m ccdastro_saspro._demo`; it processes only a synthetic image.

Automated checks cover source-copy protection, mask boundaries, curve monotonicity, Color & Tone reference outputs, stretch behavior, background-plane fitting, FITS roundtrips/no overwrite, and host adapter behavior. See `validation/` for the native application smoke-test records. Tests use small synthetic inputs; large astrophotography datasets and optional AI commands need further field testing. SyQon inference runs in a cancellable worker. Other full-resolution portable operations are synchronous and may temporarily make the dialog unresponsive.

## Credits and ownership

CCDASTRO workflow/UI and the Color & Tone implementation: Chuck Faranda / CCDASTRO, Inc. The color controls were inspired by Lighthouse by Neven Krcmarek; the Siril Lighthouse header also credits Yannick Dutertre (Cuiv) for its port. No Lighthouse source is bundled. Color & Tone processing is implemented by CCDASTRO and checked against saved reference values.

Seti Astro Suite Pro and Cosmic Clarity: Franklin Marek / Seti Astro and contributors — https://www.setiastro.com/ and https://github.com/setiastro/setiastrosuitepro/wiki/Scripting . Optional GraXpert, StarNet (Mikita Misiura), RC Astro (Russell Croman), and SyQon integrations remain their authors' work and require separate installation/licensing. No source, model weights, executables or credentials for those tools are bundled.

This workflow brings host features together; underlying algorithms and external tools remain the work of their respective authors. Third-party packages and optional tools retain their own licenses. No endorsement or affiliation is implied. See THIRD_PARTY_NOTICES.md.

Copyright 2026 CCDASTRO, Inc. All rights reserved. No new open-source license is granted by this development package.
