# GeoDetect
Get city name by IP. If IP not found it will return Москва.

## Clone, install and run
```
git clone https://github.com/zezic/geodetect.git
cd geodetect
python3 -m venv .venv
source .venv/bin/activate
pip install flask netaddr
python app.py
```

## Try
```
http :7341/api/my_city
http :7341/api/my_city/62.33.2.80
```
