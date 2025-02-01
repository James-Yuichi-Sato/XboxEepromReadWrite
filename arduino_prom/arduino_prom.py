"""
https://github.com/James-Yuichi-Sato/XboxEepromReadWrite

Minimal Python application to interface with ArduinoProm:
An Arduino based Original Xbox EEPROM reader and writer.
Can be used to recover from a corrupt BIOS or recover HDD key etc.

This repo is forked from Ryzee119's ArduinoProm
https://github.com/Ryzee119/ArduinoProm

ArduinoProm is inpired and based upon the awesome work by Grimdoomer on PiPROM.
https://github.com/grimdoomer/PiPROM


This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from pathlib import Path
import logging
import time

from serial import Serial


def eeprom_read(ser: Serial, out_filepath: str = ""):
    if out_filepath:
        logging.info("Creating output directory for: %s", out_filepath)
        out_path = Path(out_filepath)
        out_path.parent.mkdir(parents=True, exist_ok=True)

    logging.info("Reading EEPROM via: %s", ser.port)
    ser.flushInput()
    ser.flushOutput()
    rx_data = bytes()
    ser.write(bytearray(b'\x00'))
    rx_data = ser.read(256)
    logging.info("EEPROM Read")
    try:
        logging.info(f"Xbox Serial Number: {rx_data[0x34:0x40]}")
    except Exception:
        logging.error("No data at rx_data[0x34:0x40]")

    if len(rx_data) != 256:
        raise ValueError("<255 bytes read from EEPROM. Check connections")

    if out_filepath:
        logging.info("Saving EEPROM file to: %s", out_filepath)
        with open(out_path, 'wb') as eeprom_file:
            eeprom_file.write(rx_data)
        logging.info("EEPROM Saved, Job Complete")

    return rx_data


def eeprom_write(ser: Serial, input_filepath: str):
    print("Opening EEPROM image at: %s", input_filepath)
    with open(Path(input_filepath), 'rb') as eeprom_file:
        eeprom_data = eeprom_file.read()

    if len(eeprom_data) == 256:
        logging.warning("This will rewrite the EEPROM ")
        input("Ctrl+C to Cancel, Press Enter to write EEPROM...")
        logging.info("Writing EEPROM file via: %s", ser.port)
    else:
        raise ValueError("Invalid EEPROM Data, Please Verify File")

    ser.flushInput()
    ser.flushOutput()
    ser.write(bytearray(b'\x01'))
    ser.write(eeprom_data)
    ser.flushOutput()
    time.sleep(.1)

    if ser.read(1) == b'\x00':
        logging.info("Write successful")

    logging.info("Verifying EEPROM Data")
    result = eeprom_read(ser)
    if eeprom_data == result:
        logging.info("Verification Successful")
    else:
        logging.critical("Error writing EEPROM")
        raise ValueError("EEPROM write corruption, "
                         "Check Connections and Rerun Write")


def eeprom_erase(ser: Serial):
    logging.warning("This will erase the EEPROM!")
    input("Ctrl+C to Cancel, Press Enter to erase EEPROM...")
    logging.warning("Are you sure? This will erase the EEPROM!")
    input("Ctrl+C to Cancel, Press Enter to erase EEPROM...")
    logging.info("Erasing EEPROM, waiting 5 seconds"
                 " before starting job as safeguard")
    time.sleep(5)
    logging.warning("Erasing EEPROM")
    ser.write(bytearray(b'\x02'))
    ser.flushOutput()
    logging.info("EEPROM Erase command sent, verifying erase")
    time.sleep(.1)

    if ser.read(1) == b'\x00':
        logging.info("Erase successful.")
    else:
        logging.info("Error erasing device. Check connections")
