from user.utils import is_access_token_valid
from .classes import UserClass
from .classes import ProjectClass
from taskbolt.schemas import ErrorResponse, SuccessResponse
from taskbolt.errors import UserError
from django.http import JsonResponse
from .schemas import CreateProjectSchema, ProjectMembersSchema, ProjectResponseSchema, ProjectsResponseSchema
from ninja import Router
from ninja_jwt.authentication import JWTStatelessUserAuthentication
import itertools


router = Router()

@router.post('/create', auth=JWTStatelessUserAuthentication())
def create_project(request, payload:CreateProjectSchema):
    data = payload.dict()

    try:
        access_token = request.auth.token
        if not data['user_id'] == is_access_token_valid(access_token):
            raise UserError('Unauthorised action!', '400')
        
        project_obj = ProjectClass()
        create_project = project_obj.create_project(data)
    
        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=ProjectResponseSchema(
                **create_project.__dict__,
                status = create_project.status
            )
        )
    
    except Exception as e:
        response = ErrorResponse(
            msg=str(e)
        ).dict()
        return JsonResponse(response, status='500')

    return JsonResponse(response.dict(), status='200')

@router.get('/projects/{user_id}', auth=JWTStatelessUserAuthentication())
def get_projects(request, user_id:str):
    try:
        access_token = request.auth.token
        if not user_id == is_access_token_valid(access_token):
            raise UserError('Unauthorised action!', '400')
        
        user_obj = UserClass()
        user = user_obj.get_user_by_id(user_id)

        get_projects = ProjectClass().get_projects_by_user(user)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=ProjectsResponseSchema(
                projects = list(get_projects)
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

@router.get('/project/{user_id}/{project_id}', auth=JWTStatelessUserAuthentication())
def get_project(request, user_id:str, project_id:str):
    try:
        access_token = request.auth.token
        if not user_id == is_access_token_valid(access_token):
            raise UserError('Unauthorised action!', '400')
        
        user_obj = UserClass()
        user = user_obj.get_user_by_id(user_id)

        get_user_projects = ProjectClass().get_projects_ids_by_user(user)

        # Make a flat list of the get_user_projects i.e remove it from the iternal tuples they are returned as
        flat_get_user_projects = list(itertools.chain.from_iterable(get_user_projects))

        if project_id not in flat_get_user_projects:
            raise UserError('Not authorised to view this project!', code='400')

        project_obj = ProjectClass()
        project = project_obj.get_project_by_id(project_id)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=ProjectResponseSchema(
                **project.__dict__,
                status = project.status
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

@router.get('/members/{user_id}/{project_id}', auth=JWTStatelessUserAuthentication())
def get_project_members(request, user_id:str, project_id:str):
    try:
        access_token = request.auth.token
        if not user_id == is_access_token_valid(access_token):
            raise UserError('Unauthorised action!', '400')
        
        # Get project members
        # Check if user_id is in project members
        # Return project members

        project_obj = ProjectClass()
        project = project_obj.verify_member_in_project(user_id, project_id)

        project_members = project_obj.get_project_members(project_id)

        # Serialize the response to return the created user id
        response = SuccessResponse(
            data=ProjectMembersSchema(
                members = list(project_members)
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