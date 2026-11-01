import argparse
import logging
import math
import os
import sys
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_entropy(data):
    """
    Calculates the Shannon entropy of a byte string.

    Args:
        data (bytes): The byte string to analyze.

    Returns:
        float: The Shannon entropy in bits per byte.
    """
    if not data:
        return 0  # Empty data has zero entropy

    return _entropy_from_counts(Counter(data), len(data))


def _entropy_from_counts(counts, total):
    # The formula only ever needs the tally, not the data itself. Keeping it
    # separate lets analyze_file feed it counts built chunk by chunk, so a
    # large file is never held in memory just to count its bytes.
    entropy = 0
    for count in counts.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy


# One number for the whole file is the design and also the limit: a
# small packed or encrypted region inside a large plain file is diluted
# by everything around it and the average can look unremarkable. A
# per block breakdown would catch that shape; this tool does not try,
# and its number should not be read as proof a file has no such region.
def analyze_file(filepath):
    """
    Analyzes the entropy of a file.

    Args:
        filepath (str): The path to the file to analyze.

    Returns:
        float: The Shannon entropy of the file's contents, or None if an error occurs.
    """
    try:
        counts = Counter()
        total = 0
        with open(filepath, 'rb') as f:
            while chunk := f.read(65536):
                counts.update(chunk)
                total += len(chunk)
        if total == 0:
            return 0
        return _entropy_from_counts(counts, total)
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None
    except IOError as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing {filepath}: {e}")
        return None


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Calculate the Shannon entropy of files to identify potential obfuscation or encryption."
    )
    parser.add_argument("filepath", help="The path to the file to analyze.")
    parser.add_argument(
        "-o", "--output", help="Optional: Specify an output file to store the entropy value.", metavar="output_file"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level)."
    )
    return parser


def main():
    """
    Main function to parse arguments, analyze the file, and output the results.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")

    filepath = args.filepath

    # Input validation: Check if the file exists
    if not os.path.isfile(filepath):
        logging.error(f"Error: File '{filepath}' does not exist.")
        sys.exit(1)

    entropy_value = analyze_file(filepath)

    if entropy_value is None:
        sys.exit(1)
    if entropy_value is not None:
        print(f"Shannon entropy of {filepath}: {entropy_value:.4f} bits per byte")

        if args.output:
            try:
                with open(args.output, "w") as outfile:
                    # The file gets full float precision and no trailing
                    # newline, while the console above prints four
                    # decimals. A script reading the file and a person
                    # reading the terminal are looking at the same value
                    # written two ways, and only the file form is exact.
                    outfile.write(str(entropy_value))  # Store entropy as string
                logging.info(f"Entropy value written to {args.output}")
            except IOError as e:
                logging.error(f"Error writing to output file {args.output}: {e}")
                sys.exit(1)

if __name__ == "__main__":
    main()
