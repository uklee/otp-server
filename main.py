import flask
from flask_htpasswd import HtPasswdAuth
import otp
import json
import os
import datetime


CONFIG_PATH = "/srv/.config.json"

with open(".default_config.json", 'r') as config_f:
    config = json.load(config_f)

if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as config_f:
        config.update(json.load(config_f))





app = flask.Flask(__name__)
app.config['FLASK_HTPASSWD_PATH'] = config["htpasswd_path"]
app.config['FLASK_SECRET'] = config["secret"]
htpasswd = HtPasswdAuth(app)

def generate_otp(username):
    with open(config["otp_info_path"], 'r') as otp_info_f:
        otp_info = json.load(otp_info_f)
    otp_for_user = dict()
    for otp_name, otp_data in otp_info[username].items():
        otp_for_user[otp_name] = otp.OTPGenerator(key=otp_data["key"], method=otp_data["method"]).generate()
    return otp_for_user

@app.route('/', methods=['GET'])
@htpasswd.required
def index(user):
    otp_for_user = generate_otp(user)

    with open(config["log_path"], 'a') as log_f:
        log_f.write(f"{datetime.datetime.now()}: {user} on {flask.request.environ.get('HTTP_X_REAL_IP', flask.request.remote_addr)} requested OTPs\n")
        log_f.write(f"user-agent: {flask.request.user_agent}\n")
        log_f.write(f"OTP info: {otp_for_user}\n\n")
    return flask.jsonify(otp_for_user)

if __name__ == '__main__':
    app.run(host=config["host_address"], debug=config["debug"], port=config["server_port"])



