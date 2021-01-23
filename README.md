# WiPy-2.0-Web-Interface
Web Interface to control the LED and user button on WiPy Expansion Board 2.0

### Summary
The WiPy expansion board contains a user controllable led and a push-button. By using the WiPy's wireless capabilities it is easy to create a web interface to switch the led on and off, and read the status of the button. This example shows how to setup such an interface.

### HTML
The HTML code is based on the Bootstrap 3 framework. With just a few extra commands Bootstrap provides you with a pretty interface which scales nicely with the device you are using. The key elements to look for in the HTML code are the two buttons to switch the led on and off, and the table to hold the status of the WiPy's button (plus for demonstration purposes one additional pin).

### Code
The server waits for an HTML request. Only the first line of the request is kept and the rest - the header fields - is discarded. If any parameters were passed they will be in the request line, preceded by a question mark. For example, this is the request after pressing the LED Off button.
```
GET /?LED=Off HTTP/1.1
```
Any parameter present is decoded by the server, and then a fresh webpage with the WiPy's current button status is returned. So, switching a led on or off implicitly refreshes the webpage. When this must be done on a regular basis - for example when you want to monitor constantly changing inputs - then uncomment the following line in the HTML.
```html
<meta http-equiv="refresh" content="30">
```
This will make the page refresh itself every thirty seconds.

Note that this is not particularly efficient. Another approach can be found [here](https://github.com/erikdelange/WiPy-2.0-Web-Interface-using-JavaScript).

The resulting web page looks like this.

![](https://github.com/erikdelange/WiPy-2.0-Web-Interface/blob/master/ui.png)

### Sources
This example combines elements from the following code snippets which can found in the MicroPython documentation.

* <https://github.com/micropython/micropython/blob/master/examples/network/http_server.py>
* <https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_tcp.html>
