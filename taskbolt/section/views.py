from taskbolt.schemas import ErrorResponse, SuccessResponse
from taskbolt.errors import UserError
from django.http import JsonResponse
from ninja import Router
from ninja_jwt.authentication import JWTStatelessUserAuthentication
from user.utils import is_access_token_valid

from user.classes import UserClass

from .classes import SectionClass
from .schemas import CreateSectionSchema, SectionResponseSchema, SectionsResponseSchema


router = Router()

@router.post('/create', auth=JWTStatelessUserAuthentication())
def create_section(request, payload:CreateSectionSchema):
    data = payload.dict()

    try:
        access_token = request.auth.token
        if not data['user_id'] == is_access_token_valid(access_token):
            raise UserError('Unauthorised action!', '400')
        
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

@router.get('/sections/{user_id}/{project_id}', auth=JWTStatelessUserAuthentication())
def get_sections(request, user_id:str, project_id:str):
    try:
        access_token = request.auth.token
        if not user_id == is_access_token_valid(access_token):
            raise UserError('Unauthorised action!', '400')
        
        # Get user Queryset
        user = UserClass().get_user_by_id(user_id)

        section_obj = SectionClass()
        project = section_obj.get_project(project_id)

        validate_user = section_obj.validate_member_for_section(project, user)

        get_sections = section_obj.get_project_sections(project)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=SectionsResponseSchema(
                sections = list(get_sections)
            )
        )
    
    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')