# Install CCDASTRO Seti Astro Suite Pro Workflow (Windows)

Development version 0.1.0. Tested with Seti Astro Suite Pro (SASpro) 1.22.10. This is a Python script package loaded by SASpro.

## 1. Extract the download

1. Download `CCDASTRO-SASpro-Workflow-0.1.0-dev.zip`.
2. In File Explorer, right-click the ZIP and choose **Extract All**.
3. Open the extracted `CCDASTRO-SASpro-Workflow` folder. Find these two items:

   - `CCDASTRO_SASpro_Workflow.py`
   - `ccdastro_saspro` (a folder)

Both are required. Keep the extracted README and this guide for reference.

## 2. Install in the user scripts folder

1. Start **Seti Astro Suite Pro**.
2. Choose **Scripts > Open Scripts Folder**. Use the folder SASpro opens; do not use its Program Files installation directory.
3. Copy the launcher file and the **entire** `ccdastro_saspro` folder into that scripts folder. Copy these two items only; development tests and documentation do not need to be scanned as scripts.
4. On this Windows machine the expected installed layout is:

```text
C:\Users\chuck\AppData\Local\SASpro\scripts\
    CCDASTRO_SASpro_Workflow.py
    ccdastro_saspro\
        __init__.py
        _core.py
        _host.py
        _io.py
        _ui.py
        _demo.py
```

For other Windows accounts, the root is `%LOCALAPPDATA%\SASpro\scripts`. Preserve other scripts already there.

5. Return to SASpro and choose **Scripts > Reload Scripts**.
6. Confirm **Scripts > CCDASTRO > CCDASTRO Workflow 0.1.0** appears.

SASpro documents its script-folder locations and reload menu in the [official scripting guide](https://github.com/setiastro/setiastrosuitepro/wiki/Scripting).

## 3. Launch and check dependencies

1. Open an RGB or monochrome image in SASpro and select its image window.
2. Choose **Scripts > CCDASTRO > CCDASTRO Workflow 0.1.0**.
3. Confirm the workflow opens with the selected image. Do not double-click the launcher in File Explorer; SASpro supplies the script context it requires.

The script uses SASpro's Python runtime. NumPy and PyQt6 are required to launch. Astropy is required for direct FITS export and loading a stars FITS image. The tested host installation contains these packages. This script does not install packages into SASpro's runtime. If an import is missing, record the error from **Console / Status** and update or repair SASpro; consult the host's support for its bundled environment. Installing into a separate system Python will not fix its embedded runtime.

## 4. Confirm processing and save a result

1. For linear data, choose **Linked automatic stretch**, click **Add step**, then **Preview selected step**.
2. Compare **Current** and **Candidate**; click **Accept candidate** when satisfied.
3. Open **Color & Tone Studio**. Adjust a slider, inspect the mask, then choose **Review full-resolution result**. Back in the workflow, accept or discard the candidate.
4. Click **Open result as new host document**. Confirm a separate result document appears. The workflow may need to be closed before you interact with the host window.
5. Save that result with SASpro's normal Save/Save As controls after closing the workflow, or use **Save result + report** inside the workflow to create a new `.fit` and `.json` report.

Native commands process a separate working document. Those working documents remain open for inspection. Only native statistical stretch has been validated in this development build; optional tools need their own installation and configuration.

## Troubleshooting

- **CCDASTRO menu missing:** verify the launcher is in the folder opened by SASpro, then Reload Scripts or restart SASpro. Check Console / Status for script import errors.
- **No module named ccdastro_saspro:** the companion folder is missing or one level too deep; put it directly beside the launcher.
- **Open an image first:** select an image document before launching the script.
- **Wrong image shown:** close the workflow, select the intended image, and relaunch; the workflow reads the selected image at launch.
- **FITS export fails with an Astropy import error:** use Open result as new host document and save through SASpro; resolve the missing host package before using direct export or the stars FITS picker.
- **Output already exists:** choose a new filename; this build refuses overwrites.

## Updating or removing

Close the workflow and SASpro before replacing the launcher and its matching companion folder with a newer pair. Back up personal presets separately. Restart SASpro and reload scripts after the update.

To remove, close SASpro, delete only `CCDASTRO_SASpro_Workflow.py` and `ccdastro_saspro` from its user scripts folder, and restart SASpro. Keep your saved images, presets and reports.
