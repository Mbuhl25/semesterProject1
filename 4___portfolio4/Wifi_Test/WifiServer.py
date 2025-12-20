from Wifi import PicoServer

server = PicoServer("Mathias Bergholt - iPhone (2)", "Mathias8")
server.SetupListen(8080)

server.CollectData()