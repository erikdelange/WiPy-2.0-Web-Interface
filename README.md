# WiPy-2.0-Web-Interface
Web Interface to control the LED and user button on WiPy Expansion Board 2.0

###Summary
The WiPy expansion board contains a user controllable led and a push-button. Using the WiPy's wireless capabilities it is easy to create a webinterface to switch the led on and off, and read the status of the button. This example shows how to setup such an interface.

###HTML
The HTML code is based on the Bootstrap framework. With just a few extra command Bootstrap allows you to create a slick interface which scales nicely with the device you are using. The key elements to look for in the HTML code are the two buttons to control the led, and the table to hold the status of the WiPy's buttons.

###Code
The actual server loops waiting for an HTML request. Only the first line of the request is kept and the rest is discarded. If any parameters were passed they will be in the first line, preceded by a question mark. For example this is the request after pressing the LED Off button.
```
GET /?LED=Off HTTP/1.1
```
Any paramter present is decoded by the server, and then the webpage with the WiPy's button status is returned. So switching a led on or off implicetly refreshed the webpage. When this must be done on a regular basis - for example when you want to monitor constantly changing inputs - then uncomment the following line in the HTML.
```html
<meta http-equiv="refresh" content="30">
```
This will make the page refresh itself every thirty seconds.

![](https://github.com/erikdelange/WiPy-2.0-Web-Interface/blob/master/ui.png)

###Sources
This example combines elements from the following code snippets which can found in the MicroPython documentation.

* <https://github.com/micropython/micropython/blob/master/examples/network/http_server.py>
* <https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/network_tcp.html>
