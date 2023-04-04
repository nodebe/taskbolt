from taskbolt.schemas import ErrorResponse, SuccessResponse
from taskbolt.errors import UserError
from django.http import JsonResponse
from .classes import OTP, UserClass
from .schemas import UserIDSchema, UserLoginSchema, UserRegisterSchema, UserDataSchema, ForgotPasswordSchema, ResetPasswordSchema
from ninja import Router


router = Router()

@router.post('/register')
def register(request, payload:UserRegisterSchema):
    data = payload.dict()

    try:
        user_object = UserClass()
        create_user = user_object.create_user(data)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=UserIDSchema(
                **create_user.__dict__
            )
        )
    
    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')

@router.post('/login')
def login(request, payload:UserLoginSchema):
    data = payload.dict()

    try:
        user_object = UserClass()
        login_user = user_object.login_user(data)
        access_token = str(login_user['token'])

        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=UserDataSchema(
                **login_user['data'].__dict__,
                token = access_token
            ),
        )

    except UserError as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status=e.code)
    
    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')

@router.post('/forgotpassword')
def forgotpassword(request, payload:ForgotPasswordSchema):
    data = payload.dict()

    try:
        user_object = UserClass()
        send_new_password = user_object.forgot_password(data)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            msg='New Password sent to your email address!',
        )

    except UserError as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status=e.code)
    
    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')

@router.post('/resetpassword')
def resetpassword(request, payload:ResetPasswordSchema):
    data = payload.dict()

    try:
        user_object = UserClass()
        reset_password = user_object.reset_password(data)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            msg='Password reset successful!',
        )

    except UserError as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status=e.code)

    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')

@router.post('/registerotp')
def registerotp(request, payload:UserIDSchema):
    data = payload.dict()

    try:
        user_object = UserClass()
        user = user_object.get_user_by_id(id=data['id'])

        if user == None:
            raise UserError('User not found', '404')

        otp_object = OTP()
        otp = otp_object.generate_otp(user)
        otp_object.send_otp_to_email(user.email)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            msg='One-Time Password sent successfully!',
        )

    except UserError as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status=e.code)

    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')