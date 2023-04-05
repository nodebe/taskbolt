from datetime import timedelta, datetime as dt
import random
from taskbolt.errors import UserError
from .utils import is_access_token_valid, send_reset_password_link
from .models import User, Otp
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from taskbolt.senders import send_email

class UserClass:

    def get_user_by_id(self, id:str):
        user = User.objects.filter(id=id).first()

        return user

    def get_user_by_email(self, email:str):
        user = User.objects.filter(email=email).first()

        return user
    
    def verify_login_password(self, db_password, login_password):
        if check_password(login_password, db_password):
            return True
        else:
            raise UserError('Incorrect Password!')
        
    def generate_auth_token(self, user):
        token = AccessToken.for_user(user)
        return token
    
    def create_user(self, data:dict):
        data['username'] = data['firstname'].lower() + data['lastname'].lower()
        user = User.objects.create(**data)
        return user

    def login_user(self, data:dict):
        user = self.get_user_by_email(data['email'])

        if user == None:
            raise UserError('Email does not exist!', '404')

        # Verify User's password
        verify_password = self.verify_login_password(db_password=user.password, login_password=data['password'])

        # Generate JWT Token for user.
        token = self.generate_auth_token(user)

        user_data = {
            'data': user,
            'token': token
        }

        return user_data

    def forgot_password(self, data):
        email = data['email']
        user = self.get_user_by_email(email)

        # Create OTP
        user_otp = OTP()
        generated_otp = user_otp.generate_otp(user)

        # Generate Token
        token = self.generate_auth_token(user)
        token.set_exp(lifetime=timedelta(minutes=5))

        # Send Reset link to email with token
        send_to_email = send_reset_password_link(token=token, email=email)

        return True
        
    def reset_password(self, data):
        # Check if access token is valid
        token_validity_check = is_access_token_valid(access_token=data['token'])

        # When Link is visited use access token to get id
        user_id = token_validity_check

        # Use id to get user
        user = self.get_user_by_id(user_id)

        # Get the OTP from the USER->OTP models
        # If OTP has expired return OTP expired
        if user.otp.status:
            raise UserError('Token Expired!', '401')
        
        # Save new password
        user.password = data['password']
        user.save()

        # Change OTP status to True
        user.otp.status = True
        user.otp.save()

        
class OTP:

    def get_otp_row(self, user):
        otp = Otp.objects.get(user=user.id)
        return otp

    def generate_otp(self, user):
        self.otp = str(random.randint(10000, 99999))
        self.store_otp(user)
        return self.otp
    
    def store_otp(self, user):
        '''Stores OTP linked with user model!'''
        set_otp = Otp(user=user, otp_value=self.otp, created_at=timezone.now())
        set_otp.status = False
        set_otp.save()
    
    def send_otp_to_email(self, email):
        subject = 'One-Time Password for TaskBolt⚡️'
        message = f"Your One Time Password is {self.otp}. It will expire in 5(five) minutes"

        send_email(subject=subject, recipient=email, message=message)
        return True

    def verify_otp(self, user, otp):
        '''Verify the otp of user if valid and correct'''
        if user.verified:
            raise UserError('User already verified!', '400')
        self.check_otp_values(input_otp=otp, user_otp=user.otp.otp_value)
        self.check_time_validity(user.otp.created_at)

        user.verified = True
        user.otp.status = True
        user.otp.save()
        user.save()

    
    def check_otp_values(self, input_otp, user_otp):
        if input_otp != user_otp:
            raise UserError('Wrong OTP!', '401')
        return True
    
    def check_time_validity(self, otp_time_created):
        created_at = otp_time_created
        current_time = dt.now(timezone.utc)

        time_difference = current_time - created_at
        time_difference_minutes = time_difference.seconds / 60

        if time_difference_minutes > 5:
            raise UserError('OTP expired!', '401')
        
        return True