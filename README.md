# RO Crates Preparer

## Overview

The RO Crates Preparer is a Python-based tool designed to prepare Research Object (RO) crates for various pipelines. It supports generating RO-Crate metadata, extracting files from subdirectories, and creating HTML previews.

## Features

- Generates RO-Crate metadata for pipeline outputs.
- Supports multiple RO crates preparation from a list of directories.
- Extracts files from subdirectories and prepares them for inclusion in the RO crate.
- Creates HTML previews and zips the output folder.

## Requirements

- Python 3.6+
- `tqdm==4.64.1`
- `requests==2.27.1`
- `beautifulsoup4==4.12.3`
- `arcp==0.2.1`

## Installation

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To prepare an RO crate, run the following command:

```sh
python ro_crates_preparer.py <original_crate_zip_url> <destination_folder> [--extract_multiple]

```

- `<original_crate_zip_url>`: The URL of the original RO crate zip file.
- `<destination_folder>`: The path to the destination folder where the RO crate will be prepared.
- --extract_multiple: Optional flag to extract files from multiple subdirectories.

### Example
python ro_crates_preparer.py https://example.com/original_crate.zip /path/to/destination --extract_multiple
```sh

