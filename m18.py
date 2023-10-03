# import sys
import configparser
import datetime
import wiringpi
from wiringpi import GPIO
from miio import ChuangmiPlug

PIN = 14
SKIP_ROM_COMMAND = 0xCC
MATCH_ROM_COMMAND = 0x55


def oneWireReset(pin):
    wiringpi.pinMode(pin, GPIO.OUTPUT)
    wiringpi.digitalWrite(pin, GPIO.HIGH)
    wiringpi.digitalWrite(pin, GPIO.LOW)
    wiringpi.delayMicroseconds(500)
    wiringpi.digitalWrite(pin, GPIO.HIGH)
    wiringpi.delayMicroseconds(60)
    wiringpi.pinMode(pin, GPIO.INPUT)
    if not wiringpi.digitalRead(pin):
        ack = 1
    else:
        ack = 0
    wiringpi.delayMicroseconds(500)
    return ack


def writeBit(pin, bit):
    wiringpi.pinMode(pin, GPIO.OUTPUT)
    wiringpi.digitalWrite(pin, GPIO.LOW)
    wiringpi.delayMicroseconds(2)
    wiringpi.digitalWrite(pin, bit)
    wiringpi.delayMicroseconds(80)
    wiringpi.digitalWrite(pin, GPIO.HIGH)
    wiringpi.delayMicroseconds(1)


def oneWireSendComm(pin, byte):
    i = 0
    while i < 8:
        sta = byte & 0x01
        writeBit(pin, sta)
        byte >>= 1
        i += 1


def readBit(pin):
    wiringpi.pinMode(pin, GPIO.OUTPUT)
    wiringpi.digitalWrite(pin, GPIO.HIGH)
    wiringpi.digitalWrite(pin, GPIO.LOW)
    wiringpi.delayMicroseconds(2)
    wiringpi.digitalWrite(pin, GPIO.HIGH)

    wiringpi.pinMode(pin, GPIO.INPUT)
    wiringpi.delayMicroseconds(2)

    tmp = wiringpi.digitalRead(pin)
    wiringpi.delayMicroseconds(40)
    return tmp


def oneWireReceive(pin):
    i = 0
    k = 0
    while i < 8:
        j = readBit(pin)
        k = (j << 7) | (k >> 1)
        i += 1
    k = k & 0x00FF
    return k


def tempchange(lsb, msb):
    if msb >= 0xF0:
        msb = 255 - msb
        lsb = 256 - lsb
        tem = -(msb * 16 * 16 + lsb)
    else:
        tem = (msb * 16 * 16 + lsb)
    temp = tem * 0.0625
    print("Current Temp: %.2f" % temp)
    return temp


def skip_ROM():
    oneWireSendComm(PIN, SKIP_ROM_COMMAND)


def match_ROM(ROMData):
    if ROMData is None:
        return False
    oneWireSendComm(PIN, MATCH_ROM_COMMAND)
    for i in range(8):
        oneWireSendComm(PIN, ROMData[i])
    return True


def device_Rom(address=None):
    if address is None:
        skip_ROM()
    else:
        if not match_ROM(address):
            return False
    return True


def save_temp(value):
    date = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    f = open('/home/orangepi/wiringOP-Python/' + date + ".txt", "a")
    f.write(str(datetime.datetime.now()) + ": " + str(value) + "\n")
    f.close()


def main(address=None):
    temp = False
    wiringpi.wiringPiSetup()
    if oneWireReset(PIN):
        if not device_Rom(address):
            return False
        oneWireSendComm(PIN, 0x44)
    if oneWireReset(PIN):
        if not device_Rom(address):
            return False
        oneWireSendComm(PIN, 0xbe)
        lsb = oneWireReceive(PIN)
        msb = oneWireReceive(PIN)
        temp = tempchange(lsb, msb)
    return temp


if __name__ == '__main__':
    attempt = 0
    RomData = [40, 205, 15, 129, 227, 3, 60, 153]
    while attempt < 10:
        attempt += 1
        t1 = main(address=RomData)
        t2 = main(address=RomData)
        if 40 > t1 > 10 and 40 > t2 > 10:
            diff = abs(t1 - t2)
            if diff > 0.5:
                print("the attempt #" + str(attempt) + " failed")
                continue
            else:
                save_temp(t2)
                quit()
        else:
            print("the attempt #" + str(attempt) + " failed")
