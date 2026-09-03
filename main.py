"""
Refine and convert MNE FIF files.

This app loads one or more MNE-compatible .fif files and re-saves them for
data standardization. It generates a report with channel information and
ensures consistent data format across different processing pipelines.

Input:
    - fif: Path to an MNE FIF (.fif) file, or a list of paths to several
    - channel_types: Optional comma-separated channel-type reassignments,
      format "chan_name-new_type,chan_name2-new_type2" (e.g. a system that
      digitizes EOG/ECG through spare EEG channels; MNE's set_channel_types)
    - rename_channels: Optional comma-separated channel renames, format
      "old_name-new_name,old_name2-new_name2" (MNE's rename_channels)

Output:
    - out_dir/raw.fif: Refined MNE raw data file (single input file)
      or out_dir/raw_<n>.fif per input file when several fif files are given
    - out_report/report.html: QC report with channel information
    - product.json: Metadata with channel info
"""

# Copyright (c) 2026 brainlife.io
#
# This app refines and standardizes MNE FIF files.
#
# Authors:
# - Guiomar Niso (https://github.com/guiomar)

import sys
import os
import html
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

# Standard imports
import mne

# Import shared utilities
from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    ensure_output_dirs,
    create_product_json,
    add_info_to_product,
    add_raw_info_to_product
)

# Set up matplotlib for headless execution
setup_matplotlib_backend()

# Ensure output directories exist
ensure_output_dirs('out_dir', 'out_report')

# Load configuration
config = load_config()

# == LOAD DATA ==
fnames = config.get('fif')

# Validate fif: must be a non-empty string, or a non-empty list of non-empty strings
valid_fnames = (
    (isinstance(fnames, str) and fnames)
    or (
        isinstance(fnames, list)
        and fnames
        and all(isinstance(f, str) and f for f in fnames)
    )
)
if not valid_fnames:
    product_items = []
    add_info_to_product(
        product_items,
        f"Invalid or missing 'fif' config value: {fnames!r}. Must be a non-empty file path string or a non-empty list of non-empty file path strings.",
        'error'
    )
    create_product_json(product_items)
    sys.exit(1)

if isinstance(fnames, str):
    fnames = [fnames]

# == CREATE REPORT ==
report = mne.Report(title='FIF File Refinement Report')

# Optional channel-type/name fixups (e.g. a system that digitizes EOG/ECG
# through spare EEG amplifier channels, so they arrive labeled as plain EEG
# and need retyping before anything downstream can find them by type or by
# their real name -- Wakeman & Henson ds000117 does exactly this, see
# original_scripts/04-python_filtering.py). Off by default (empty/unset):
# every other dataset/caller is unaffected. Same "old-new,old2-new2" format
# as add-montage's own rename_channels, for consistency.
def _parse_pairs(s):
    if not s or s == 'None':
        return {}
    return dict(x.strip().split('-', 1) for x in s.split(','))


channel_types = _parse_pairs(config.get('channel_types'))
rename_channels = _parse_pairs(config.get('rename_channels'))

# == PROCESS EACH FILE ==
product_items = []
for i, fname in enumerate(fnames, start=1):
    # Read FIF raw data
    raw = mne.io.read_raw_fif(fname)

    if channel_types:
        raw.set_channel_types(channel_types)
    if rename_channels:
        raw.rename_channels(rename_channels)

    label = f' ({os.path.basename(fname)})' if len(fnames) > 1 else ''
    report.add_raw(raw=raw, title=f'Raw Data{label}')

    # Add channel information to report
    info_html = f'<pre>{html.escape(str(raw.info))}</pre>'
    report.add_html(title=f'Channel Information{label}', html=info_html)

    # Save output: keep the single-file name for backward compatibility,
    # otherwise disambiguate outputs with a per-file index.
    out_name = 'raw.fif' if len(fnames) == 1 else f'raw_{i}.fif'
    raw.save(os.path.join('out_dir', out_name), overwrite=True)

    add_info_to_product(product_items, f"FIF file refined and standardized: {os.path.basename(fname)}")
    add_raw_info_to_product(product_items, raw)

# Save report
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == CREATE PRODUCT JSON ==
create_product_json(product_items)