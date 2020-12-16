import serial
import serial.tools.list_ports
import asyncio
import struct
import typing

SLEEP_TIME = 0.2  # seconds
ANALOG2VOLT = 3.3 / 4095.0
VOLT2TEMP = (1000.0 / 5.0)

CMD_SUBMIT_CODE = 0xF0
CMD_ERROR_CODE = 0xE0
CMD_ACQ = 0xFA


def get_ports() -> typing.List[typing.Tuple[str, str]]:
    return [(port, name) for (port, name, _) in serial.tools.list_ports.comports()]


class TempSensorSerial:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.__ser = ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout,
                                         xonxoff=False, rtscts=False, dsrdtr=False)
        ser.flushInput()
        ser.flushOutput()

    def close(self):
        self.__ser.flushInput()
        self.__ser.flushOutput()
        self.__ser.close()

    async def __read_bytes(self, n):
        while self.__ser.inWaiting() < n:
            await asyncio.sleep(SLEEP_TIME)
        return self.__ser.read(n)

    async def __read_uint16(self):
        return int.from_bytes(await self.__read_bytes(2), "little")

    async def __read_float(self) -> float:
        bytes = await self.__read_bytes(4)
        return struct.unpack("<f", bytes)[0]

    async def __read_voltages(self) -> typing.Optional[typing.List[float]]:
        self.__ser.write(bytes([CMD_ACQ]))  # ask for acquisition
        while True:
            ans = int.from_bytes(await self.__read_bytes(1), "little")
            if ans == CMD_SUBMIT_CODE:
                break
            elif ans == CMD_ERROR_CODE:
                return None
            await asyncio.sleep(SLEEP_TIME)
        buf = []
        for _ in range(5):
            v = await self.__read_uint16()
            buf.append(v * ANALOG2VOLT)
        return buf

    async def read_voltages(self, timeout: float):
        """
            Return an array of 5 float values.
            Value can be None if measure fail.
            Return None in case of errors or timeout.
        """
        try:
            return await asyncio.wait_for(self.__read_voltages(), timeout)
        except asyncio.TimeoutError:
            return None

    async def read_temp(self, timeout: float):
        """
            Return an array of 5 temperature in degres Celsius.
            Return None in case of errors or timeout.
        """
        voltages = await self.read_voltages(timeout)
        return [v * VOLT2TEMP for v in voltages] if voltages != None else None


async def main(use_voltages=False):
    import os
    ser = TempSensorSerial("COM6")

    while True:
        values = await (ser.read_voltages(1) if use_voltages else ser.read_temp(1))
        os.system("cls")
        if values:
            for i in range(5):
                print("[%s]\t%s %s" % (
                    i,
                    "%4.4f" % values[i] if values[i] != None else "----",
                    "V" if use_voltages else "°C"
                ))
        else:
            print("Acquisition failure ...")
        print("-----------------------------")
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main(0))
# for (port, name) in get_ports():
# 	print("{} : {}".format(port, name))
