import network, socket, random, time, math
from time import sleep
from machine import Pin, ADC


class PicoServer:
    def __init__(self, SSID, PASSWORD):
        
        self.SSID = SSID
        self.PASSWORD = PASSWORD

        # activate the networking properties of the pico
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        # If it is not connected, try to connect
        if not self.wlan.isconnected():
            print("connecting to wifi")
            self.wlan.connect(self.SSID, self.PASSWORD)
            # Keep trying to connect until the connection is established
            while not self.wlan.isconnected():
                time.sleep(1)
        else:
            print("already on the network")
        print("Connected:", self.wlan.ifconfig())
    

    def SetupListen(self, port): 
        #Make a socket which is listening for inputs or signals
        self.addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
        self.s = socket.socket()
        self.s.bind(self.addr)
        self.s.listen(1)

    def CollectData(self): 
        print("Listening on", self.addr)
        while True:
            cl, remote_addr = self.s.accept()
            print("Client connected from", remote_addr)

            while True:
                data = cl.recv(64)  # small packets
                if not data:
                    print("Client disconnected")
                    break
                try:
                    msg = data.decode().strip()
                    a, b, d = msg.split(",")
                    print(f"num1={a}, num2={b}, dir={d}")
                except Exception as e:
                    print("Bad packet:", e, data)
            cl.close()

class PicoClient:
    def __init__(self, SSID, PASSWORD, GPIOADC_x, GPIOADC_y):
        
        self.SSID = SSID
        self.PASSWORD = PASSWORD

        # activate the networking properties of the pico
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        # If it is not connected, try to connect
        if not self.wlan.isconnected():
            print("connecting to wifi")
            self.wlan.connect(self.SSID, self.PASSWORD)
            # Keep trying to connect until the connection is established
            while not self.wlan.isconnected():
                time.sleep(1)
        else:
            print("already on the network")
        print("Connected:", self.wlan.ifconfig())


        self.x_axis = ADC(Pin(GPIOADC_x))  # ADC0
        self.y_axis = ADC(Pin(GPIOADC_y))  # ADC1

    def ConnectToServer(self, server_ip, port):
        self.s = socket.socket()
        self.s.connect((server_ip, port))

    def JoystickDataConverter(self, x_val, y_val):
        motor1 = 0
        motor2 = 0

        x_val=(x_val-16307)/(49900-16308)-0.5
        y_val=(y_val-16307)/(49900-16308)-0.5
        motor1 = y_val
        motor2 = y_val
        
        if x_val > 0:
            motor1 += abs(x_val)
        
        if x_val < 0:
            motor2 += abs(x_val)
        print("X =", motor1, "Y =", motor2)
        
        return motor1, motor2
    
    def SendToServer(self):
        # Read 16-bit analog values (0–65535)
        x_val = self.x_axis.read_u16()
        y_val = self.y_axis.read_u16()
        
        num1, num2 = self.JoystickDataConverter(x_val, y_val)
        direction = 1
        
        msg = f"{num1},{num2},{direction}\n" # Make a CSV string of 3 values e.g(0.231,0.977,-1)
        self.s.send(msg.encode()) # Send the message to the socket
        sleep(0.4)