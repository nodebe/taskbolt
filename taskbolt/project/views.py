from .classes import ProjectClass
from taskbolt.schemas import ErrorResponse, SuccessResponse
from taskbolt.errors import UserError
from django.http import JsonResponse
from .schemas import CreateProjectSchema, ProjectResponseSchema
from ninja import Router
from ninja_jwt.authentication import JWTStatelessUserAuthentication


router = Router()

@router.post('/create', auth=JWTStatelessUserAuthentication())
def create_project(request, payload:CreateProjectSchema):
    data = payload.dict()

    try:
        project_obj = ProjectClass()
        create_project = project_obj.create_project(data)
    
        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=ProjectResponseSchema(
                **create_project.__dict__,
                status = create_project.status.id
            )
        )
    
    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')