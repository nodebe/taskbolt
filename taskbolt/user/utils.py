
from datetime import datetime
import os
import jwt
from taskbolt.senders import send_email
from dotenv import load_dotenv
from taskbolt.errors import UserError

load_dotenv()


def send_reset_password_link(token:str, email:str):
    subject = "TaskBolt⚡️ Reset Password",
    message = f"<p>Your reset password link is <a href='{os.getenv('RESET_PASSWORD_URL')}/reset_password?token={token}'>Reset Password</a>. It will expire in 5(five) minutes</p>"

    send_email(subject=subject, recipient=email, message=message)

    return True


def is_access_token_valid(access_token) -> str:
    try:
        payload = jwt.decode(access_token, verify=True, key=os.environ.get('SECRET_KEY'), algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        raise UserError('Invalid Token', '401')

    # check if the token has expired
    exp_timestamp = payload.get('exp')
    if exp_timestamp is not None:
        exp_datetime = datetime.fromtimestamp(exp_timestamp)
        if datetime.now() > exp_datetime:
            raise UserError('Expired Token', '401')
    
    return payload['user_id']
