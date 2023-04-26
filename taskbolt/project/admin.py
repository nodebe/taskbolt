from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectStatus)
admin.site.register(ProjectMember)
admin.site.register(ProjectInviteStatus)
admin.site.register(ProjectMemberStatus)
