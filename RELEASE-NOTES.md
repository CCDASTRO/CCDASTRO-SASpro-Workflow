# v0.3.0 — Independent channel stretch

Adds an optional reviewed final stretch for linear RGB or three registered mono FITS masters. R/G/B targets and amounts are independent, with individual channel and recombined previews. Shared starting target 0.23; sources are preserved and the full-resolution candidate requires explicit acceptance. Controls are saved in workflow presets; accepted reports record settings and selected master paths. Use this instead of an additional automatic stretch. Equal targets change relative emission balance; no alignment or physical color calibration is performed.

Validated October 22, 2026: 25 unit/Qt tests pass, including source preservation, targets, amount blending, cancellation, fixed preview/full-resolution plans, FITS loading, explicit acceptance and replay. Windows installer lifecycle checks are recorded separately.

CCDASTRO Seti Astro Suite Pro Workflow 0.2.1 — development release.

Windows users: download and run **CCDASTRO-SASpro-Workflow-0.2.1-Setup.exe**. Close the host application first. This per-user installer also handles future version upgrades. Follow the included INSTALL.md for launch/migration details. A portable ZIP and SHA256SUMS.txt are provided.

Includes Color & Tone masks/sliders/curves, reviewed processing passes, FITS result/report export, a Check for updates button, and installer/uninstall support. Optional native/AI commands still require individual configuration and validation; see README scope. Windows installers are not Authenticode signed.
