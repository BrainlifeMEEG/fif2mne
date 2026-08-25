"""
Refine and convert MNE FIF files.

This app loads one or more MNE-compatible .fif files and re-saves them for
data standardization. It generates a report with channel information and
ensures consistent data format across different processing pipelines.

Input:
    - fif: Path to an MNE FIF (.fif) file, or a list of paths to several

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

# == PROCESS EACH FILE ==
product_items = []
for i, fname in enumerate(fnames, start=1):
    # Read FIF raw data
    raw = mne.io.read_raw_fif(fname)

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