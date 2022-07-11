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
