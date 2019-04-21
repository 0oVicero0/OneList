# OneList

本版本不需要使用Redis!

## Installation

```bash
# apt install python3-pip redis-server

git clone https://github.com/0oVicero0/OneList.git
cd OneList

pip3 install -r requirements.txt
# Get refresh_token --> Setup config
# The <refresh_token> in config.json does not need "<" and ">".

gunicorn app:app -b 127.0.0.1:5000 -D
```

## Configuration

Create a config file named `config.json`

```json
{
  "token": "<refresh_token>",
  "location_path": "/",
  "start_directory": "/",
  "threads": 3,
  "diff_seconds": 480,
  "refresh_seconds": 720,
  "metadata_cached_seconds": 768,
  "structure_cached_seconds": 840
}
```
## Get refresh_token

### Method 1 (Auto, Recommend): 

#### Get refresh_token

> https://login.microsoftonline.com/common/oauth2/authorize?response_type=code&client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&redirect_uri=https://api.moeclub.org/onedrive-login

### Method 2 (Manual): 

#### Get auth_token in url

> https://login.microsoftonline.com/common/oauth2/authorize?response_type=code&client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&redirect_uri=http://localhost/onedrive-login

#### Get refresh_token

```bash
code="<auth_token>"
wget --no-check-certificate --post-data="client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&client_secret=h27zG8pr8BNsLU0JbBh5AOznNS5Of5Y540l/koc7048=&grant_type=authorization_code&resource=https://api.office.com/discovery/&redirect_uri=http://localhost/onedrive-login&code=$code" 'https://login.microsoftonline.com/common/oauth2/token' -qO-
```

## Demo
> https://moeclub.org/onedrive
