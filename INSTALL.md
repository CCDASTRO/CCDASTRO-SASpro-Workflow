# Install and update CCDASTRO Seti Astro Suite Pro Workflow

Version 0.4.0 — development release for Windows. Tested with SASpro 1.22.10.

## Recommended: Windows installer

1. Download `CCDASTRO-SASpro-Workflow-0.4.0-Setup.exe` from the [GitHub releases page](https://github.com/CCDASTRO/CCDASTRO-SASpro-Workflow/releases).
2. Close Seti Astro Suite Pro and its workflow windows. The installer checks this and asks you to close the host if it is running.
3. Run the installer under your normal Windows account. It installs for that account without administrator access.
4. Complete the wizard. The Start menu gets installation-guide, downloads/updates and uninstall shortcuts.

The default folder is `%LOCALAPPDATA%\SASpro\scripts\CCDASTROWorkflow`.

Restart SASpro, open/select an image, then choose **Scripts > Reload Scripts**, followed by **Scripts > CCDASTRO > CCDASTRO Workflow 0.4.0**. SASpro scans the installed subfolder. The launcher and complete `ccdastro_saspro` companion folder are installed together.

The script uses SASpro's bundled Python runtime. NumPy and PyQt6 are needed for the UI; Astropy is needed for direct FITS export and loading a stars FITS. If an import is missing, update/repair SASpro or consult its support. Installing packages into a separate system Python does not change the bundled runtime.

## Updating later

**Check for updates at startup** is enabled by default. It quietly checks this project’s GitHub releases in the background at most once every 24 hours, including development releases. When a newer version is found, a small **Update available: v… — Downloads** button appears in the workflow. Click it to open that release page. A known newer version remains visible on later launches between checks. No startup popup interrupts processing; offline failures are quiet. Clear the startup checkbox to disable automatic checks; that choice is remembered separately for this workflow. **Check for updates** still checks immediately whenever you choose, even if startup checks are disabled or a daily check already ran. Closing the workflow never waits for the network check. Updates are downloaded and installed manually: close the host and run the new Windows installer. Existing images and personal presets stay where you saved them. Setup reuses the same installation directory and replaces the application files.

You can also use **Start > CCDASTRO SASpro Workflow > Downloads and updates**. The installer is the same tool for first installation and upgrades; no manual copying is needed. Keep your images and personal presets outside the installation directory. A newer installer is published for every versioned release. Development releases are explicitly labeled on GitHub.

## Moving from the earlier ZIP build

Close the old workflow first. Remove only the old `CCDASTRO_SASpro_Workflow.py` and matching `ccdastro_saspro` folder from the user scripts root after backing up any personal files. Keep other scripts. The new installer uses its own CCDASTROWorkflow subfolder, avoiding two copies in the Scripts menu.

## Portable ZIP option

Extract the ZIP into a permanent writable folder. Keep the launcher file and its companion package folder together. Copy `CCDASTRO_SASpro_Workflow.py` and the full `ccdastro_saspro` folder into the folder opened by Scripts > Open Scripts Folder (or a dedicated subfolder there), then Reload Scripts. Launch it from SASpro with an image selected.

## First processing check

1. Open a small RGB or monochrome image and wait for loading to finish.
2. For linear data, choose Linked automatic stretch, Add step, then Preview selected step.
3. Compare Current/Candidate, then Accept candidate if satisfied.
4. Open Color & Tone Studio, inspect a mask and adjust a slider/curve. Review the full-resolution result before accepting it.
5. Save result + report under a new FITS filename. Existing files are refused.

## Troubleshooting and removal

- Missing menu entry: restart the host and check the registered directory/layout above.
- Missing companion module: reinstall; the launcher alone is insufficient.
- No usable image: finish opening a single image before launching the workflow.
- Update check unavailable: try again later or open the GitHub releases page directly. Normal processing still works offline once dependencies are installed.
- The installer currently has no Windows Authenticode signature. Use the release page and SHA256SUMS.txt to identify the distributed files; checksums are not a publisher signature.
- Uninstall using Windows Installed apps or the workflow's Start menu shortcut. Close the host first. Only installed workflow files are removed. Siril setup removes its own search-path entry when uninstalling and keeps settings backups. Shared host packages, your images and separately saved presets remain.

## Maintainer release process

Run the tests, update the version in the runtime, installer and packaging script together, and run `scripts/build.ps1`. Review the resulting installer, ZIP and SHA256SUMS.txt. Push a `vX.Y.Z` tag; the repository's GitHub Actions release job builds, tests and publishes that development release. Check its completed job and release assets. Public downloads are at the Releases link above.

After installation, use the Independent channel stretch button on linear data before other nonlinear finishing. See the README for RGB and registered mono-master instructions.

## Set up optional SyQon Studio

Install Studio separately, sign in and finish Required Items. In the workflow choose SyQon Studio CLI… > Add step, locate syqon-cli.exe, check its models and declare the input domain. Preview selected step, then accept or discard. See README.md for model domains and generated stars. No SyQon software, model assets or licenses are included in this installer.
