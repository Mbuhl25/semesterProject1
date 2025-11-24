# Send data via UART
from machine import UART, Pin
import utime
led = Pin("LED", Pin.OUT)
# Initialize UART on the sender Pico
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1)) # TX on GPIO 1, RX on GPIO 2
while True:
    message = "Hello, World!"
    uart.write(message) # Send message to the receiver
    led.toggle()
    print(f"Sent: {message}")
    utime.sleep(1) # Wait for 1 second before sending again

