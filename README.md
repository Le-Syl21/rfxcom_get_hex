# rfxcom_get_hex

A python script to convert RFXCom Raw/Hex input in output RFXCom Raw/Hex command for non rotating RF signals

## Installation
Linux:
```bash
git clone "https://github.com/Le-Syl21/rfxcom_get_hex.git"
python3 -m venv "rfxcom_get_hex"
cd "rfxcom_get_hex"
source .bin/activate
pip3 install -r requirements.txt
```

## Usage/Examples

```bash
# IN rfxcom_get_hex DIR
source .bin/activate
./rfxcom_get_hex.py -h
usage: rfxcom_get_hex.py [-h] [-p PORT] [-r REPEAT] [-s SOURCE]

options:
  -h, --help            	show this help message and exit
  -p PORT, --port PORT 		RFXtrx port like '/dev/ttyUSB0'
  -r REPEAT, --repeat REPEAT	Repeat number (default=8) but if doesn't work you can try to grow up to 16, 32, 64, max 255 but no sens
  -s SOURCE, --source SOURCE	Your own hex source string like '0x78 0x7f 0x00 0x00 0x01' or '0x78 0x7f 0x00 0x00 0x01' or '78 7f 00 00 01' or '787f000001'
  -n, --nofiles			Don't create output files
```

## Work with

RFXCOM receiver but can also work with just an undec raw hex output with option --source

![Receiver](https://shop.strato.com/WebRoot/StoreNL2/Shops/78165469/6479/B429/0818/BFF6/B981/0A0C/6D0C/4A09/RFXtrx433E.jpg)

## Related

You can buy RF module at: [RFXCom Shop](http://www.rfxcom.com)

You can use the output to create Home Assistant Button CARD to use service rfxtrx.send to pilot RF devices

[Home Assistant rfxtrx](https://www.home-assistant.io/integrations/rfxtrx/#services)

## License

[GPL3](https://www.gnu.org/licenses/gpl-3.0.html)
