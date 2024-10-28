# otp-server
Simple OTP Server that serves as OTP Client.

It uses `HTTP basic authentication` to validate user. As the name says, it is not extremely secure.

Note that this is now in draft version, so it is not guaranteed to run normally.


## Prepare

There are 3 files to be prepared.

`.config.json` should be prepared as `.default_config.json`.

`.htpasswd` should be prepared in standard Apache htpasswd form.

`otp_info.json` should be similar to the followings. Note that the `<username>` should be same as the name in `.htpasswd`. Also, methods other than `TOTP` is not implemented at this time.


```json, otp_info.json
{
  "<username>": {
    "<otp_name>": {
      "key": "<otp_key>",
      "method": "TOTP",
    },
  },
}
```

## Run
```sh
$ pip install -r requirements.txt
$ python main.py
```
