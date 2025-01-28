# ArduinoProm

Originally written by [Ryzee119](https://github.com/Ryzee119)
Updated by [James Sato](https://github.com/James-Yuichi-Sato)

ArduinoProm is adapted upon PiPROM by Grimdoomer for use with an Arduino board.
See [PiPROM](https://github.com/grimdoomer/PiPROM) for the Original Raspberry Pi version.
  
## Use at your own risk

## Setting up Arduino

### Programming Arduino

The firmware has been written around the Arduino Pro Micro Leonardo (5V/16Mhz). However, it is expected to work on any Arduino with a built in USB bootloader/Virtual Comport support with I2C support.

1. Open `ArduinoProm.ino` in [Arduino IDE](https://www.arduino.cc/en/main/software)
2. Connect the Arduino to a PC and flash the `ArduinoProm.ino`. Example of selecting the board on the Arduino IDE below
  ![Arduino IDE preview](https://i.imgur.com/V7CJpkd.png)
3. Hit the program button then confirm `ArduinoProm.ino` was compiled and written to the Arduino successfully.

### Wiring

1. Connect `GND, SDA and SCL` on the Xbox LPC port to the corresponding pins on the Arduino module.
  ![wiring](https://i.imgur.com/No7bvLF.png)
  ![installed photo](https://i.imgur.com/fokwQjY.jpg)

## ArduinoProm Functions

ArduinoProm accepts a few commands over a virtual com port interface.

- `0x00` triggers an EEPROM read.
- `0x01` triggers an EEPROM write.
- `0x02` will erase the Xbox eeprom.
- `0x03` will return 0x00 if the eeprom is detected. (-1 otherwise)

To facilitate these commands in a more user friendly way you can use the included python app `arduino_prom`.

## Python Script

`arduino_prom` is tested to run on [Python 3.13](https://www.python.org).

### Installing `arduino_prom`

Once Python3.13 is installed, install `arduino_prom` with the following shell commands:

```shell
python -m pip install git+https://github.com/James-Yuichi-Sato/XboxEepromReadWrite/
```

### `arduino_prom` Functions

`arduino_prom` usage is as follows
 (Determine your com port number by plugging in the Arduino to your PC after programming it)

```shell
//Read the EEPROM on COM1 and save to file to eeprom.bin
python -m arduino_prom COM1 READ eeprom.bin

//Write eeprom.bin to the EEPROM on COM1.
python -m arduino_prom COM1 WRITE eeprom.bin

//Write all 0's to the EEPROM effectively erasing it.
python -m arduino_prom COM1 ERASE
```

Example outputs:
  ![Write](https://i.imgur.com/mRRVvAb.png)
  ![Read](https://i.imgur.com/p308Va2.png)
  ![Erase](https://i.imgur.com/r6GWkpm.png)
