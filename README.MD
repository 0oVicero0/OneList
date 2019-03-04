# OneList

## Installation

```bash
git clone https://github.com/0oVicero0/OneList.git
cd OneList

pip3 install -r requirements.txt
gunicorn app:app -b 127.0.0.1:5000 -D
```

## Configuration

Create a config file named `config.json`

```json
{
  "token": "<secret>",
  "location_path": "/",
  "start_directory": "/",
  "refresh_seconds": 720
}
```

## Get refresh_token

> https://login.microsoftonline.com/common/oauth2/authorize?response_type=code&client_id=ea2b36f6-b8ad-40be-bc0f-e5e4a4a7d4fa&redirect_uri=http://localhost/onedrive-login
