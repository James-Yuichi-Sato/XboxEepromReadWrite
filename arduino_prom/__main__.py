import argparse
from .arduino_prom import eeprom_read, eeprom_write

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # CSV Mode Arguments
    parser.add_argument(
        "-d", "--data-directory",
        dest="data_dir",
        type=str,
        default="",
        help="The location of the parquet data files"
    )

    # Local Data Mode Arguments
    parser.add_argument(
        "-o", "--output-directory",
        dest="out_dir",
        type=str,
        default="./output_files/",
        help="A flag to run model on local "
        "DICOM data stored in /data/input directory"
    )

    parser.add_argument(
        "-n", "--max-thread-count",
        dest="max_thread_count",
        type=int,
        default=24,
        help="Number of Parallel Threads Desired"
    )

    args = vars(parser.parse_args())

    print(args)

