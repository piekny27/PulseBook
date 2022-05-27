from turtle import delay
from testy.models import *
from time import sleep
from random import randint, uniform
import pickle
import requests
import os
import json

server_name = 'http://192.168.0.105:5000/device'
file_name = 'device.pkl'
headers = {"Content-Type": "application/json; charset=utf-8"}

class DeviceEmulator():
    def __init__(self):
        self.device = Device()
        self.device.config_state = 0
        self.device.device_key = '5c:cf:7f:94:ed:f7' #mac address
        self.device.serial_number = 'ABFJ34HI4H-2022'
        self.device.version = 'v1.0.0'
        self.pin_generated = False
        self.sp_array = []
        self.hr_array = []
        self.device_loaded = False

    def config_device(self): 
        while(True and not self.device_loaded):
            try:
                if(self.device.config_state == 0):
                    print('Config')
                    print('Step 1-Paste your D/K')
                    data = {'device_key' : self.device.device_key,
                            'serial_number'  : self.device.serial_number,
                            'version' : self.device.version}
                    response = requests.post(server_name, headers=headers , json=data)
                    data2 = response.json()
                    if(response.status_code == 202 and data2.get('device_key') == self.device.device_key):
                        print('Config')
                        print('Step 1-D/K correct')
                        self.device.config_state = 1                      
                elif(self.device.config_state == 1):
                    if(not self.pin_generated):
                        self.device.pin = randint(1000,9999)
                        self.pin_generated = True
                    data = {'device_key' : self.device.device_key,
                        'serial_number'  : self.device.serial_number,
                        'version' : self.device.version,
                        'pin' : self.device.pin}
                    print('Config')
                    print('Step 2-PIN:', self.device.pin)
                    response = requests.post(server_name, headers=headers , json=data)
                    data2 = response.json()
                    if(response.status_code == 202 and data2.get('pin') == self.device.pin):
                        print('Config')
                        print('Step 2-Correct PIN!:')
                        self.pin_generated = False
                        self.device.config_state = 2                    
                elif(self.device.config_state == 2):
                    print('Config')
                    print('Step 3-Config done')
                    with open(file_name, 'wb') as f:
                        pickle.dump(self.device, f)
                    break
                sleep(2)
            except:
                print('Error connection')
                break

    def gen_arrays(self):
        self.sp_array.clear()
        self.hr_array.clear()
        for x in range(19):
            self.sp_array.append(round(uniform(90,99),4))
            self.hr_array.append(round(uniform(60,120),6))

    def sensor_loop(self):
        try:
            while(True):
                self.gen_arrays()
                data = {'device_key' : self.device.device_key,
                                'serial_number'  : self.device.serial_number,
                                'version' : self.device.version,
                                'pin' : self.device.pin,
                                'sp_array[]' : self.sp_array,
                                'hr_array[]' : self.hr_array}
                print('Sending arrays')
                response = requests.post(server_name, headers=headers , json=data)
                data2 = response.json()
                if(response.status_code == 200 and data2.get('action') == 'reset'):
                    self.device.config_state = 0
                    self.device_loaded = False
                    self.config_device()
                input('Press Enter')
        except:
            print('Error connection')
        
    def load_device(self):
        if os.path.isfile(file_name):
            with open(file_name, 'rb') as f:
                self.device = pickle.load(f)
                self.device_loaded = True
        else:
            with open(file_name, 'w'): pass


if __name__ == "__main__":
    emulator = DeviceEmulator()
    emulator.load_device()
    emulator.config_device()
    emulator.sensor_loop()