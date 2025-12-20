from Wifi import PicoClient

client = PicoClient("Mathias Bergholt - iPhone (2)", "Mathias8", 26, 27)

client.ConnectToServer("172.20.10.6", 8080)

while True:
    client.SendToServer()