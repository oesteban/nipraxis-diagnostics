""" Python script to validate data

Run as:

    python3 scripts/validata_data.py data
"""

import os
from pathlib import Path
import sys
import hashlib


def file_hash(filename):
    """ Get byte contents of file `filename`, return SHA1 hash

    Parameters
    ----------
    filename : str
        Name of file to read

    Returns
    -------
    hash : str
        SHA1 hexadecimal hash string for contents of `filename`.
    """
    return hashlib.sha1(
        Path(filename).read_bytes()
    ).hexdigest()
    # Open the file, read contents as bytes.
    # Calculate, return SHA1 has on the bytes from the file.


def validate_data(data_directory):
    """ Read ``data_hashes.txt`` file in `data_directory`, check hashes

    Parameters
    ----------
    data_directory : str
        Directory containing data and ``data_hashes.txt`` file.

    Returns
    -------
    None

    Raises
    ------
    ValueError:
        If hash value for any file is different from hash value recorded in
        ``data_hashes.txt`` file.
    """
    data_directory = Path(data_directory)

    # Read lines from ``data_hashes.txt`` file.
    lines = (data_directory / "hash_list.txt").read_text().splitlines()

    # Split into SHA1 hash and filename
    hash_and_file = [l.split(" ") for l in lines]

    # Calculate actual hash for given filename.
    for hashdigest, filename in hash_and_file:
        filename = filename.replace("group-00/", "")
        target_hash = file_hash(str(data_directory / filename))
        if hashdigest != target_hash:
            raise ValueError(f"File {filename} is corrupted ({hashdigest} vs. {target_hash}).")


def main():
    # This function (main) called when this file run as a script.
    #
    # Get the data directory from the command line arguments
    if len(sys.argv) < 2:
        raise RuntimeError("Please give data directory on "
                           "command line")

    data_directory = sys.argv[1]
    # Call function to validate data in data directory
    validate_data(data_directory)


if __name__ == '__main__':
    # Python is running this file as a script, not importing it.
    main()
