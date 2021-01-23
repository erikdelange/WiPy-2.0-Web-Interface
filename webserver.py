html = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- meta http-equiv="refresh" content="15" -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <link rel="icon" href="data:;base64,=">
        <title> WiPy </title>
    </head>
    <style>
        .container {
            max-width: 360px;
            }
    </style>
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
    </body>
    </div>
</html>
"""
import socket
import gc

from machine import Pin

# Connect variable 'led' to the user led on the expansion board
led = Pin(Pin.exp_board.G16, mode=Pin.OUT)
led(1)

# Connect 'pins' to the user button on the expansion board plus one additional pin
pins = [Pin(i, mode=Pin.IN, pull=Pin.PULL_UP) for i in (Pin.exp_board.G17, Pin.exp_board.G22)]


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(socket.getaddrinfo('0.0.0.0', 80)[0][-1])
serversocket.listen()

while True:
    gc.collect()

    conn, addr = serversocket.accept()
    request_line = conn.readline()

    print("request:", request_line, "from", addr)

    if request_line in [b"", b"\r\n"]:
        print("malformed request")
        conn.close()
        continue

    while True:
        line = conn.readline()
        if line in [b"", b"\r\n"]:
            break

    conn.write(b"HTTP/1.1 200 OK\r\n")
    conn.write(b"Connection: close\r\n")
    conn.write(b"Content-Type: text/html\r\n\r\n")

    if request_line.find(b"LED=On") != -1:
        led(0)
    elif request_line.find(b"LED=Off") != -1:
        led(1)

    rows = ["<tr> <td> %s </td> <td> %d </td> </tr>" % (p.id(), p.value()) for p in pins]

    response = html % "\n".join(rows)
    conn.send(response)

    conn.close()
