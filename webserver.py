html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <!-- meta http-equiv="refresh" content="30" -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="icon" href="data:;base64,=">
        <title> WiPy 2.0 </title>
    </head>
    <div class="container">
    <body>
        <div class="well"> <h1> Expansion Board </h1> </div>
        <div class="well-sm"> <h2> Button Status </h2> </div>
        <table class="table table-bordered table-sm">
            <thead class="thead-inverse">
                <tr> <th> Pin </th> <th> Value </th> </tr>
            </thead>
            <tbody>
                %s
            </tbody>
        </table>
        <div class="well-sm"> <h2> LED </h2> </div>
        <form>
            <button name="LED" value="On" type="submit"> LED ON </button>
            <button name="LED" value="Off" type="submit"> LED OFF </button>
        </form>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </body>
    </div>
</html>
"""

from machine import Pin
import socket

# Connect to the user led on the expansion board
led = Pin(Pin.exp_board.G16, mode=Pin.OUT)
led(1)

# Connect to the user button on the expansion board plus one additional pin
pins = [Pin(i, mode=Pin.IN, pull=Pin.PULL_UP) for i in (Pin.exp_board.G17, Pin.exp_board.G22)]

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(socket.getaddrinfo('0.0.0.0', 80)[0][-1])
serversocket.listen(1)

while True:
    conn, addr = serversocket.accept()
    print("new connection from {0}".format(addr))

    request = conn.readline()
    while True:
        line = conn.readline()
        if line == b"" or line == b"\r\n":
            break

    conn.sendall("HTTP/1.1 200 OK\nConnection: close\nServer: WiPy\nContent-Type: text/html\n\n")

    print("request:", request)

    if request.find(b"/?LED=On") != -1:
        led(0)
    elif request.find(b"/?LED=Off") != -1:
        led(1)

    rows = ["<tr> <td> %s </td> <td> %d </td> </tr>" % (p.id(), p.value()) for p in pins]

    response = html % "\n".join(rows)

    conn.send(response)
    conn.sendall("\n")
    conn.close()

    print("closed connection with {0}".format(addr))
