from taskbolt.schemas import ErrorResponse, SuccessResponse
from taskbolt.errors import UserError
from django.http import JsonResponse
from ninja import Router
from ninja_jwt.authentication import JWTStatelessUserAuthentication
from .schemas import CreateTaskSchema
from user.utils import is_access_token_valid


router = Router()

@router.post('/create', auth=JWTStatelessUserAuthentication())
def create_task(request, payload:CreateTaskSchema):
    data = payload.dict()

    try:
        access_token = request.auth.token
        if not data['user_id'] == is_access_token_valid(access_token):
            raise UserError('Unauthorised action!', '400')
        
        # Write code here
    
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