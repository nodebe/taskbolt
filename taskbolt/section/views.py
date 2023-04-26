from taskbolt.schemas import ErrorResponse, SuccessResponse
from taskbolt.errors import UserError
from django.http import JsonResponse
from ninja import Router
from ninja_jwt.authentication import JWTStatelessUserAuthentication

from .classes import SectionClass
from .schemas import CreateSectionSchema, SectionResponseSchema


router = Router()

@router.post('/create', auth=JWTStatelessUserAuthentication())
def create_section(request, payload:CreateSectionSchema):
    data = payload.dict()

    try:
        section_obj = SectionClass()
        create_section = section_obj.create_section(data)
    
        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=SectionResponseSchema(
                **create_section.__dict__
            )
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