import pyotp
import datetime

class OTPGenerator:
    def __init__(self, key, method="TOTP"):
        if method == "TOTP":
            self.otp = pyotp.TOTP(key)
        else:
            raise NotImplementedError("Only TOTP is supported for now.")
    
    def generate(self):
        otp_value = self.otp.now()
        current_time = datetime.datetime.now()
        valid_from = current_time.replace(second=current_time.second//30*30, microsecond=0)
        valid_until = valid_from + datetime.timedelta(seconds=30)

        return {"otp_value": str(otp_value), "valid_from": str(valid_from), "valid_until": str(valid_until)}
    
