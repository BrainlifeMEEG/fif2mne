"""
Refine and convert MNE FIF files.

This app loads MNE-compatible .fif files and re-saves them for data standardization.
It generates a report with channel information and ensures consistent data format
across different processing pipelines.

Input:
    - fif: Path to MNE FIF (.fif) file

Output:
    - out_dir/raw.fif: Refined MNE raw data file
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
fname = config['fif']

# Read FIF raw data
raw = mne.io.read_raw_fif(fname)

# == CREATE REPORT ==
report = mne.Report(title='FIF File Refinement Report')
report.add_raw(raw=raw, title='Raw Data')

# Add channel information to report
info_str = str(raw.info)
report.add_text(info_str, 'Channel Information')

# Save report
report.save(os.path.join('out_report', 'report.html'), overwrite=True, verbose=False)

# == SAVE OUTPUT ==
raw.save(os.path.join('out_dir', 'raw.fif'), overwrite=True)

# == CREATE PRODUCT JSON ==
product_items = []
add_info_to_product(product_items, f"FIF file refined and standardized successfully")
add_raw_info_to_product(product_items, raw)
create_product_json(product_items)