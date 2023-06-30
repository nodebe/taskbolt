from django.contrib import admin
from django.urls import path
from user.views import router as user_router
from project.views import router as project_router
from section.views import router as section_router
from task.views import router as task_router
from ninja import NinjaAPI


api = NinjaAPI()
api.add_router('/users/', user_router, tags=['User'])
api.add_router('/project/', project_router, tags=['Project'])
api.add_router('/section/', section_router, tags=['Section'])
api.add_router('/task/', task_router, tags=['Task'])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
]
