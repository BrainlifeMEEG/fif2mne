<h1 align="center">FIF to MNE Raw</h1>

<p align="center">
  Converts one or more MEG/EEG FIF files to MNE-Python Raw with mne.io.read_raw_fif, optionally reassigning channel types and renaming channels, and outputs the raw file(s) with a channel QC report.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.955"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.955-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Converts one or more MEG/EEG FIF files to MNE-Python Raw with mne.io.read_raw_fif, optionally reassigning channel types and renaming channels, and outputs the raw file(s) with a channel QC report.**

Reads each FIF file with MNE-Python, applies optional channel-type reassignments (for example spare EEG channels used for EOG/ECG) and channel renames, and re-saves it as raw.fif (or raw_<n>.fif for several inputs) with an HTML report of the channel information. Use it to bring FIF recordings into the brainlife MNE pipeline in a consistent format. Supersedes the single-file bl.app.632 registration.

| | |
|---|---|
| **Inputs** | `neuro/meg/fif` |
| **Outputs** | `neuro/meeg/mne/raw` |
| **Container** | `brainlifemeeg/mne:1.12.1` |
| **Resources** | 8 CPUs |
| **Run it** | [doi.org/10.25663/brainlife.app.955](https://doi.org/10.25663/brainlife.app.955) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meg/fif` | yes | One or more MEG/EEG recordings in FIF format, with optional BIDS sidecars, calibration and cross-talk files. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | MNE raw data: raw.fif for a single input, or raw_<n>.fif per input file. |

<details>
<summary><b>Parameters</b> (2)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `channel_types` | string |  | Optional channel-type reassignments, comma-separated "chan_name-new_type" pairs (e.g. "EEG061-eog,EEG062-eog,EEG063-ecg,EEG064-misc" for a system that digitizes EOG/ECG through spare EEG channels). Applied via MNE's set_channel_types() before saving. Default: no reassignment. |
| `rename_channels` | string |  | Optional channel renames, comma-separated "old_name-new_name" pairs (e.g. "EEG061-EOG061,EEG062-EOG062,EEG063-ECG063"). Applied via MNE's rename_channels(), after channel_types. Default: no renaming. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.955](https://doi.org/10.25663/brainlife.app.955), choose `neuro/meg/fif` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/meeg/mne/raw`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlifemeeg/mne:1.12.1`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "fif": "/path/to/fif/fif",
       "channels": "/path/to/fif/channels",
       "headshape": "/path/to/fif/headshape",
       "coordsystem": "/path/to/fif/coordsystem",
       "calibration": "/path/to/fif/calibration",
       "crosstalk": "/path/to/fif/crosstalk",
       "destination": "/path/to/fif/destination",
       "events": "/path/to/fif/events",
       "events_json": "/path/to/fif/events_json",
       "channel_types": "",
       "rename_channels": ""
   }
   ```

3. Run `./main`.

## Configuration Parameters

| key | type | default | description |
|---|---|---|---|
| `channel_types` | string | `""` (no reassignment) | Optional comma-separated channel-type reassignments, format `"chan_name-new_type,chan_name2-new_type2"` (e.g. `"EEG061-eog,EEG062-eog,EEG063-ecg,EEG064-misc"`). Applied via MNE's `set_channel_types()` before saving. |
| `rename_channels` | string | `""` (no renaming) | Optional comma-separated channel renames, format `"old_name-new_name,old_name2-new_name2"` (e.g. `"EEG061-EOG061,EEG062-EOG062"`). Applied via MNE's `rename_channels()`, after `channel_types`. |

## Local Testing

```bash
# Edit config.json with your own input file(s) and options, then run:
python3 main.py
```

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- FIF to MNE Raw. brainlife.io App. [doi:10.25663/brainlife.app.955](https://doi.org/10.25663/brainlife.app.955)
- Gramfort A. et al. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Guiomar Niso, Instituto Cajal, CSIC, Spain

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
