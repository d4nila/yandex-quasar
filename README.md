# Yandex Quasar API
![](https://img.shields.io/badge/httpx-0.13.3-green)
![](https://img.shields.io/badge/dacite-1.6.0-brightgreen)
## Installation
```
$ python3 -m pip install yandex_quasar
```
## Authorization
My library uses cookie login - it's easier and more reliable.  
Install [this](https://chrome.google.com/webstore/detail/copy-cookies/jcbpglbplpblnagieibnemmkiamekcdg) extenstion and go to [passport.yandex.ru](https://passport.yandex.ru) (this is VERY important, follow this link) and copy the cookie by clicking on the extension icon.  
Then, in the folder where you plan to create the code, make a file with any name with the txt extension (you need to remember it), for example `btfspace.txt` and paste the copied cookies into this file.  
With authorization, consider it over.
## Supported devices
- Sensors (like Mi Temp & Humidity Sensor)
- Switches
- Sockets
- Lights (includes color, brightness changing)
- Yandex Smart Remote Cotroller (custom buttons and TV)
## Using
```python
from quasar_api import Quasar

api = Quasar('btfspace') # place here name of your file without .txt
```
Now you can use any methods of the class (if you didn't get an error).
### api.get_devices()
```python
devices = api.get_devices()
print(devices)

[Device(created=datetime.datetime(2022, 6, 27, 16, 29, 22), id='secret', name='Яндекс Мини', room=None, room_id=None, type='devices.types.smart_speaker.yandex.station.mini', manufacturer='Yandex Services AG', model='YNDX-0004', sw_version=None)...]
```
This method returns you a list of all devices and general information about them (there are NO control methods such as turn_on/off, they will be further in the documentation).
### api.get_device(id = 'secret')
This method returns detailed information and device management methods by ID.  

#### Lights
```python
led_strip = api.get_device('secret')
print(led_strip)

Extended(is_favorite=False, id='secret', name='Лента', names=['Лента'], room='Спальня', online=True, type='devices.types.light', external_id='light.strip', sensors=[], skill_id='secret', capabilities=[OnOffCapability(type='devices.capabilities.on_off', instance='on', value=True), ColorCapability(type='devices.capabilities.color_setting', instance='color', value=CurrentColor(id='', name='', type='multicolor', color={'h': 357, 's': 83, 'v': 100}), palette=[{'id': 'white', 'name': 'Белый', 'type': 'white', 'value': {'h': 33, 's': 28, 'v': 100}}, {'id': 'red', 'name': 'Красный', 'type': 'multicolor', 'value': {'h': 0, 's': 65, 'v': 10...]), RangeCapability(type='devices.capabilities.range', instance='brightness', value=54, range=Range(min=1, max=100, precision=1), unit='unit.percent')], groups=[], wss_url='wss://push.yandex.ru/v2/subscribe/websocket...')
```
In this type of device you can:
- `led_strip.turn_on()` - turn on device
- `led_strip.turn_off()` - turn off device
- `led_strip.set_brightness(77)` - set brightness (from 1 to 100)
- `led_strip.set_color('red')` - set color (available colors in Extended object in ColorCapability in palette)

#### Sockets and switches
```python
socket = api.get_device('secret')
print(socket)

Extended(is_favorite=False, id='secret', name='Ночник', names=['Ночник'], room='Спальня', online=True, type='devices.types.light', external_id='secret', sensors=[Sensor(last_updated=datetime.datetime(2022, 7, 11, 17, 48, 52), instance='voltage', name='текущее напряжение', percent=None, status=None, value=233, type='devices.properties.float', unit='unit.volt'), Sensor(last_updated=datetime.datetime(2022, 7, 11, 17, 48, 52), instance='power', name='потребляемая мощность', percent=None, status=None, value=0, type='devices.properties.float', unit='unit.watt'), Sensor(last_updated=datetime.datetime(2022, 7, 11, 17, 48, 52), instance='amperage', name='потребление тока', percent=None, status=None, value=0, type='devices.properties.float', unit='unit.ampere')], skill_id='T', capabilities=[OnOffCapability(type='devices.capabilities.on_off', instance='on', value=True)], groups=[], wss_url='wss://push.yandex.ru/v2/subscribe/websocket..')
```
In this type of device you can:
- `socket.turn_on()` - turn on device
- `socket.turn_off()` - turn off device

#### Yandex Smart Remote Cotroller
```python
hub = api.get_device('secret')
print(hub)

Extended(is_favorite=False, id='secret', name='Пульт', names=['Пульт'], room='Спальня', online=True, type='devices.types.hub', external_id='secret', sensors=[], skill_id='T', capabilities=[], groups=[], wss_url='wss://push.yandex.ru/v2/subscribe/websocket...')
```
In this type of device you can:
- `hub.get_linked()` - returns linked to remote controller devices
#### Sensor
```python
sensor = api.get_device('secret')
print(sensor)

Extended(is_favorite=False, id='secret', name='Датчик температуры', names=['Датчик температуры'], room='Спальня', online=True, type='devices.types.sensor', external_id='secret', sensors=[Sensor(last_updated=datetime.datetime(2022, 7, 11, 17, 55, 9), instance='temperature', name='температура', percent=None, status=None, value=28.4, type='devices.properties.float', unit='unit.temperature.celsius'), Sensor(last_updated=datetime.datetime(2022, 7, 11, 17, 55, 9), instance='humidity', name='влажность', percent=51, status='normal', value=51, type='devices.properties.float', unit='unit.percent'), Sensor(last_updated=datetime.datetime(2022, 7, 11, 17, 55, 9), instance='battery_level', name='уровень заряда', percent=100, status='normal', value=100, type='devices.properties.float', unit='unit.percent')], skill_id='secret', capabilities=[], groups=[], wss_url='wss://push.yandex.ru/v2/subscribe/websocket...')
```
#### TV
```python
tv = api.get_device('secret')
print(tv)

Extended(is_favorite=False, id='secret', name='Телевизор', names=['Телевизор'], room='Спальня', online=True, type='devices.types.media_device.tv', external_id='secret', sensors=[], skill_id='T', capabilities=[], groups=[], wss_url='wss://push.yandex.ru/v2/subscribe/websocket...')
```
In this type of device you can:
- `tv.power()` - emulating Power button
- `tv.set_channel(13)` - setting channel
- `tv.channel_up()` - emulatuing Channel Up Button
- `tv.channel_down()` - emulatuing Channel Down Button
- `tv.volume_up()` - emulatuing Volume Up Button
- `tv.volume_down()` - emulatuing Volume Down Button
