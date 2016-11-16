#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from bluepy.btle import Scanner, DefaultDelegate

class Tsukeru:
    temperature = 0
    humidity = 0
    rssi = 0
    isExist = False
    
    def __init__(self,address="00:00:00:00:00:00"):
        #macアドレス設定 小文字に変換
        self.address = address.lower()
    
    def readTemperature(self,data):
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
        return result
    
    
    def readHumidity(self,data):
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
        return result
    

    def read(self):
        scanner = Scanner().withDelegate(DefaultDelegate())
        temp_flg  = False
        humid_flg = False
        self.isExist =False
        retry_count = 3;
        while not (temp_flg and humid_flg) and retry_count > 0:
            devices = scanner.scan(7.0)
            for dev in devices:
                if dev.addr == self.address:
                    self.isExist = True
                    self.rssi = dev.rssi
                    (adtype, desc, value) = dev.getScanData()[2]
                    data = value[12:]
                    if data[0] == "1" and temp_flg == False:
                        temp_flg = True
                        self.temperature = self.readTemperature(data)
                    elif data[0] == "2" and humid_flg == False:
                        humid_flg = True
                        self.humidity = self.readHumidity(data)
            if not self.isExist:
                retry_count -= 1
                           
        
if __name__ == '__main__':
    #set your device's address
    device = Tsukeru("xx:xx:xx:xx:xx:xx")
    device.read()
    print("RSSI:"+str(device.rssi)+"dB")
    print("Temperature:"+str(device.temperature)+"C")
    print("Humidity:"+str(device.humidity)+"%")

    