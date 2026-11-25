# FIF to MNE Raw

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Converts one or more MEG/EEG FIF files to MNE-Python Raw with mne.io.read_raw_fif, optionally reassigning channel types and renaming channels, and outputs the raw file(s) with a channel QC report.**

Reads each FIF file with MNE-Python, applies optional channel-type reassignments (for example spare EEG channels used for EOG/ECG) and channel renames, and re-saves it as raw.fif (or raw_<n>.fif for several inputs) with an HTML report of the channel information. Use it to bring FIF recordings into the brainlife MNE pipeline in a consistent format. Supersedes the single-file bl.app.632 registration.

| | |
|---|---|
| 📥 **Inputs** | `neuro/meg/fif` |
| 📤 **Outputs** | `neuro/meeg/mne/raw` |
| 🐳 **Container** | `brainlifemeeg/mne:1.12.1` |
| ⚙️ **Resources** | 8 CPUs |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.955](https://doi.org/10.25663/brainlife.app.955) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meg/fif` | yes | One or more MEG/EEG recordings in FIF format, with optional BIDS sidecars, calibration and cross-talk files. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | MNE raw data: raw.fif for a single input, or raw_<n>.fif per input file. |

<details>
<summary><b>⚙️ Parameters</b> (2)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `channel_types` | string |  | Optional channel-type reassignments, comma-separated "chan_name-new_type" pairs (e.g. "EEG061-eog,EEG062-eog,EEG063-ecg,EEG064-misc" for a system that digitizes EOG/ECG through spare EEG channels). Applied via MNE's set_channel_types() before saving. Default: no reassignment. |
| `rename_channels` | string |  | Optional channel renames, comma-separated "old_name-new_name" pairs (e.g. "EEG061-EOG061,EEG062-EOG062,EEG063-ECG063"). Applied via MNE's rename_channels(), after channel_types. Default: no renaming. |

</details>

📚 **References used by this App:**
- Hayashi S., Caron B. A., Heinsfeld A. S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nature Methods 21, 809-813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Gramfort A. et al. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)

<!-- brainlife-app:end -->

[![Abcdspec-compliant](https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg)](https://github.com/brain-life/abcd-spec)
[![Run on Brainlife.io](https://img.shields.io/badge/Brainlife-bl.app.955-blue.svg)](https://doi.org/10.25663/brainlife.app.955)

Supersedes the original single-file `bl.app.632` registration (owned by a different brainlife.io account and not updatable from this repo).

## Description

Converts MEG/EEG `.fif` file(s) to MNE raw data using MNE-Python's [`mne.io.read_raw_fif`](https://mne.tools/stable/generated/mne.io.read_raw_fif.html) function. Accepts either a single file or a list of several; each input file is refined and saved independently (not concatenated). Optional channel-type reassignment and channel renaming (e.g. for a system that digitizes EOG/ECG through spare EEG amplifier channels) can be applied before saving, via MNE's `set_channel_types()` and `rename_channels()`.

The app generates:
- A refined MNE raw `.fif` file per input file
- An HTML QC report with channel information
- A `product.json` summary with channel info for each processed file

## Inputs

- **`fif`** (`neuro/meg/fif`): MEG/EEG FIF data file, or a list of several (required)

## Outputs

- `out_dir/raw.fif` (`neuro/meeg/mne/raw`): refined MNE raw data file (single input file), or `out_dir/raw_<n>.fif` per input file when several fif files are given
- `out_report/report.html`: QC report with channel information for each processed file

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `channel_types` | string | `""` (no reassignment) | Optional comma-separated channel-type reassignments, format `"chan_name-new_type,chan_name2-new_type2"` (e.g. `"EEG061-eog,EEG062-eog,EEG063-ecg,EEG064-misc"`). Applied via MNE's `set_channel_types()` before saving. |
| `rename_channels` | string | `""` (no renaming) | Optional comma-separated channel renames, format `"old_name-new_name,old_name2-new_name2"` (e.g. `"EEG061-EOG061,EEG062-EOG062"`). Applied via MNE's `rename_channels()`, after `channel_types`. |

## Usage

### Running on Brainlife.io

1. Go to the [FIF to MNE Raw app page](https://brainlife.io/app/6a8d9b56ad4d4a4b5327f838) on Brainlife.io.
2. Select your project and the FIF file(s) to convert as input.
3. Optionally set `channel_types` and/or `rename_channels` in the configuration.
4. Submit the process, then download `out_dir/raw.fif` (or `raw_<n>.fif`) and `out_report/report.html` once it completes.

### Local Testing

```bash
# Edit config.json with your own input file(s) and options, then run:
python3 main.py
```

## Authors
- [Guiomar Niso](guiomar.niso@ctb.upm.es), Instituto Cajal, CSIC, Spain

## Citations
We kindly ask that you cite the following articles when publishing papers and code using this app.

1. Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2
2. Gramfort, A. et al. MEG and EEG data analysis with MNE-Python. Front. Neurosci. 7, 267 (2013). https://doi.org/10.3389/fnins.2013.00267

## Funding Acknowledgement
brainlife.io is publicly funded and for the sustainability of the project we kindly ask that you acknowledge the following funding sources:

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://grantome.com/grant/NIH/R01-EB030896-01)

## License

Copyright (c) 2026 MEEG Brainlife team. Licensed under AGPL-3.0, see [license.txt](license.txt) for details.
