import copy
import wiringpi
from wiringpi import GPIO

LOGGING_ENABLED = 1

READ_ROM_COMMAND = 0x33
MATCH_ROM_COMMAND = 0x55
SKIP_ROM_COMMAND = 0xCC
SEARCH_ROM_COMMAND = 0xF0
ALARM_SEARCH_COMMAND = 0xEC
WRITE_SCRATCHPAD_COMMAND = 0x4E
READ_SCRATCHPAD_COMMAND = 0xBE
COPY_SCRATCHPAD_COMMAND = 0x48
CONVERT_TEMP_COMMAND = 0x44
RECALL_E2_COMMAND = 0xB8
READ_POWER_SUPLY_COMMAND = 0xB4

RES_9_BIT = 0x0
RES_10_BIT = 0x1
RES_11_BIT = 0x2
RES_12_BIT = 0x3

TAG = "ds18b20"
DQ_GPIO = 14
parasitePower = None

lastMatchedBitPosition = -1
needToWriteOne = False
lastROMFound = False


def wait_us(us):
    wiringpi.delayMicroseconds(us)


def ds18b20_single_get_serial_number():
    if not initialization_sequence():
        return False
    data = [0] * 8
    if not read_ROM(data):
        return False
    return data


def initialization_sequence():
    # gpio_set_direction(DQ_GPIO, GPIO.OUTPUT)
    wiringpi.pinMode(DQ_GPIO, GPIO.OUTPUT)
    # gpio_set_level(DQ_GPIO, 0)
    wiringpi.digitalWrite(DQ_GPIO, 0)
    wait_us(500)
    wiringpi.digitalWrite(DQ_GPIO, 1)
    wiringpi.pinMode(DQ_GPIO, GPIO.INPUT)
    wait_us(60)
    if wiringpi.digitalRead(DQ_GPIO):
        return False
    wait_us(500)
    return True


def read_ROM(data):
    if data is None:
        return False
    write_byte(READ_ROM_COMMAND)
    for i in range(8):
        data[i] = read_byte()
    if LOGGING_ENABLED:
        print("Family code: %x" % data[0])
        print("Serial number: %x%x%x%x%x%x" % (data[1], data[2], data[3], data[4], data[5], data[6]))
        print("CRC: %x" % data[7])
    return data[7] == CRC8(data, 7)


def CRC8(addr, len2):
    copy_addr = copy.deepcopy(addr)
    crc = 0
    while len2 > 0:
        inbyte = copy_addr.pop(0)
        for i in range(8, 0, -1):
            mix = (crc ^ inbyte) & 0x01
            crc >>= 1
            if mix:
                crc ^= 0x8C
            inbyte >>= 1
        len2 -= 1
    return crc


def write_byte(data):
    for i in range(8):
        bit = (data >> i) & 0x01
        write_bit(bit)


def read_byte():
    data = 0
    for i in range(8):
        if read_bit():
            data |= 0x01 << i
    return data


def write_bit(bit):
    wiringpi.pinMode(DQ_GPIO, GPIO.OUTPUT)
    wiringpi.digitalWrite(DQ_GPIO, 0)
    wait_us(10)
    if bit == 1:
        # gpio_set_level(DQ_GPIO, 1)
        wiringpi.digitalWrite(DQ_GPIO, 1)
    wait_us(50)
    # gpio_set_level(DQ_GPIO, 1)
    wiringpi.digitalWrite(DQ_GPIO, 1)


def read_bit():
    bit = 0
    # gpio_set_direction(DQ_GPIO, GPIO_MODE_OUTPUT)
    wiringpi.pinMode(DQ_GPIO, GPIO.OUTPUT)
    # gpio_set_level(DQ_GPIO, 0)
    wiringpi.digitalWrite(DQ_GPIO, 0)
    wait_us(1)
    # gpio_set_direction(DQ_GPIO, GPIO_MODE_INPUT)
    wiringpi.pinMode(DQ_GPIO, GPIO.INPUT)
    wait_us(12)
    if wiringpi.digitalRead(DQ_GPIO) == 1:
        bit = 1
    wait_us(47)
    return bit


def ds18b20_get_temperature(temperature, address):
    waitConversionTime = 0
    if not get_temperature_wait_time(waitConversionTime, address):
        return False
    if not initialization_sequence():
        return False
    if address is None:
        skip_ROM()
    else:
        if not match_ROM(address):
            return False
    if not convert_temperature(waitConversionTime):
        return False
    if not initialization_sequence():
        return False
    if address is None:
        skip_ROM()
    else:
        if not match_ROM(address):
            return False
    scratchpadData = [0] * 9
    if not read_scratchpad(scratchpadData):
        return False
    temperature[0] = (scratchpadData[0] + (scratchpadData[1] * 256)) / 16
    return True


def skip_ROM():
    write_byte(SKIP_ROM_COMMAND)


def match_ROM(ROMData):
    if ROMData is None:
        return False
    write_byte(MATCH_ROM_COMMAND)
    for i in range(8):
        write_byte(ROMData[i])
    return True


def convert_temperature(waitTime):
    write_byte(CONVERT_TEMP_COMMAND)
    return True


def read_scratchpad(data):
    if data is None:
        return False
    write_byte(READ_SCRATCHPAD_COMMAND)
    for i in range(9):
        data[i] = read_byte()
    if LOGGING_ENABLED:
        print("Temperature: %x%x" % (data[0], data[1]))
        print("Temp. High User: %x" % (data[2]))
        print("Temp. Low User: %x" % (data[3]))
        print("Config: %x" % (data[4]))
        print("CRC: %x" % (data[8]))
    if not initialization_sequence():
        return False
    return data[8] == CRC8(data, 8)


def get_temperature_wait_time(waitTime, address):
    res = None
    if not ds18b20_get_thermometer_resolution(res, address):
        return False

    waitTime = 0.750 / (8 >> RES_9_BIT)
    return True


def ds18b20_get_thermometer_resolution(res, address):
    if not initialization_sequence():
        return False
    if address is None:
        skip_ROM()
    else:
        if not match_ROM(address):
            return False
    scratchpadData = [0] * 9
    if not read_scratchpad(scratchpadData):
        return False
    res = (scratchpadData[4] & 0x60) >> 5
    if LOGGING_ENABLED:
        print("resolution is %x" % res)
    return True


wiringpi.wiringPiSetup()

address = ds18b20_single_get_serial_number()
if not address:
    print('Error data')

# Family code: 28
# Serial number: cdf81e333c
# CRC: 99

temperature = [0]
ds18b20_get_temperature(temperature, address)
print(temperature)
