# OneList

## Installation

```bash
# apt install python3-pip redis-server

git clone https://github.com/0oVicero0/OneList.git
cd OneList

pip3 install -r requirements.txt
# Get auth_token --> Get refresh_token --> Setup config

gunicorn app:app -b 127.0.0.1:5000 -D
```

## Configuration

Create a config file named `config.json`

```json
{
  "token": "<refresh_token>",
  "location_path": "/",
  "start_directory": "/",
  "refresh_seconds": 720,
  "metadata_cached_seconds": 600,
  "structure_cached_seconds": 3600
}
```

## Get auth_token

> https://login.microsoftonline.com/common/oauth2/authorize?response_type=code&client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&redirect_uri=http://localhost/onedrive-login

## Get refresh_token

```bash
code="<auth_token>"
wget --no-check-certificate --post-data="client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&client_secret=h27zG8pr8BNsLU0JbBh5AOznNS5Of5Y540l/koc7048=&grant_type=authorization_code&resource=https://api.office.com/discovery/&redirect_uri=http://localhost/onedrive-login&code=$code" 'https://login.microsoftonline.com/common/oauth2/token' -qO-
```
