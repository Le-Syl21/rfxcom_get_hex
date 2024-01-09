# rfxcom_get_hex

A python script to convert RFXCom Raw/Hex input in output RFXCom Raw/Hex command for non rotating rf433 signals

## Installation
Linux:
```bash
rfxcomdir="$PWD/rfxcom_get_hex"
python -mv venv rfxcom_get_hex
cd $rfxcomdir
git clone https://github.com/Le-Syl21/rfxcom_get_hex.git
source .bin/activate
pip install -r requirements.txt
```

## Usage/Examples

```bash
cd $rfxcomdir
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
