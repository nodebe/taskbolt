"""liftsmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import router as user_router
from project.views import router as project_router
from section.views import router as section_router
from ninja import NinjaAPI


api = NinjaAPI()
api.add_router('/users/', user_router, tags=['User'])
api.add_router('/project/', project_router, tags=['Project'])
api.add_router('/section/', section_router, tags=['Section'])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
]
