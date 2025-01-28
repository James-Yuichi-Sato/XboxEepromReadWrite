import argparse
import logging
from serial import Serial
from .arduino_prom import eeprom_read, eeprom_write, eeprom_erase


if __name__ == '__main__':
    # Read Arguments from User
    parser = argparse.ArgumentParser()

    # Logging
    logging.basicConfig(level=logging.DEBUG)

    # Default values for IDE/debug compiler simplicity
    com, output_filepath, image_filepath = ""
    read_bool, write_bool, erase_bool, ser = False

    # COM Port
    parser.add_argument(
        "-C", "--COM-PORT",
        dest="com",
        type=str,
        required=True,
        help="The COM Port of the Arduino to Serial connect to"
    )

    # Read Mode Argument
    parser.add_argument(
        "-r", "--read",
        dest="read_bool",
        action="store_true",
        help="Read EEPROM using Arduino"
    )

    # Output File Location Argument
    parser.add_argument(
        "-o", "--output-filepath",
        dest="output_filepath",
        default="",
        type=str,
        help="EEPROM image output file location"
    )

    # Write Mode Argument
    parser.add_argument(
        "-w", "--write",
        dest="write_bool",
        action="store_true",
        help="Write EEPROM using Arduino"
    )

    # File Location Argument
    parser.add_argument(
        "-f", "--image-filepath",
        dest="image_filepath",
        default="",
        type=str,
        help="EEPROM image file location"
    )

    # Erase Mode Argument
    parser.add_argument(
        "-e", "--erase",
        dest="erase_bool",
        action="store_true",
        help="Erase EEPROM using Arduino"
    )

    args = vars(parser.parse_args())
    locals().update(args)

    del args, parser

    logging.info(locals())

    try:
        ser: Serial = Serial(
            port=com,
            baudrate=9600,
            timeout=10,
            rtscts=1
        )
    except Exception:
        logging.critical("Could not open COM: %s", com)
        raise

    if read_bool:  # type: ignore
        logging.info("Read Flag Received")
        if not output_filepath:  # type: ignore
            logging.critical("No output filepath received.")
            raise ValueError("No output-filepath[-o] argument received")
        eeprom_read(ser, output_filepath)
    if write_bool:  # type: ignore
        logging.info("Write Flag Received")
        if not image_filepath:  # type: ignore
            logging.critical("No image filepath received.")
            raise ValueError("No image-filepath[-o] argument received")
        eeprom_write(ser, image_filepath)
    if erase_bool:  # type: ignore
        logging.info("Erase Flag Received")
        eeprom_erase(ser)
