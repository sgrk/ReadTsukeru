#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bluepy.btle import Scanner, DefaultDelegate

scanner = Scanner().withDelegate(DefaultDelegate())
devices = scanner.scan(10.0)
target = "xx:xx:xx:xx:xx:xx"

for dev in devices:
    if dev.addr == target:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        (adtype, desc, value) = dev.getScanData()[2]
        data = value[12:]
        if data[0] == "1":
            print(data[1:])
            data=int(data[1:],16)
            frac = float(data & 127) / 128.0
            exp = (data >> 7) & 15
            sign = (data >> 11) & 1
            sign = -1 if sign == 1 else 1
            if exp == 0:
                if frac == 0:
                    result = 0
                else:
                    result = frac / 64.0 * sign
            elif not exp == 15:
                result = (1+frac) * 2**(exp-7) * sign
            else:
                result = 0
            print(str(result) + "C")


        elif data[0] == "2":
            print(data[1:])
            data=int(data[1:],16)
            frac = float(data & 255) / 255.0
            exp = (data >> 8) & 15
            if exp == 0:
                if frac == 0:
                    result = 0
                else:
                    result = frac / 64.0
            elif not exp == 15:
                result = (1+frac) * 2**(exp-7)
            else:
                result = 0
            print(str(result) + "%")
