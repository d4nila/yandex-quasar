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

[Device(created=datetime.datetime(2022, 6, 27, 16, 29, 22), id='4777a99c-1096-4acf-9496-1eec0f7aa016', name='Яндекс Мини', room=None, room_id=None, type='devices.types.smart_speaker.yandex.station.mini', manufacturer='Yandex Services AG', model='YNDX-0004', sw_version=None), Device(created=datetime.datetime(2022, 6, 27, 16, 27, 53), id='7f604b0b-bd40-4822-a0d9-2a3fbdd0bd91', name='Яндекс Станц...
```
This method returns you a list of all devices and general information about them (there are NO control methods such as turn_on/off, they will be further in the documentation)
