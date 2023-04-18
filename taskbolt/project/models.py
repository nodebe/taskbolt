from django.db import models
import uuid

from user.models import User


class ProjectStatus(models.Model):
    status = models.CharField(max_length=9, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    id = models.CharField(max_length=36, primary_key=True, null=False)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    members = models.ManyToManyField(User, through='ProjectMember')
    status = models.ForeignKey(ProjectStatus, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex)
        super().save(*args, **kwargs)


class ProjectSection(models.Model):
    title = models.CharField(max_length=15, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectMemberStatus(models.Model):
    status = models.CharField(max_length=7, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectInviteStatus(models.Model):
    status = models.CharField(max_length=9, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectMember(models.Model):
    invited_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField()

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    member_status = models.ForeignKey(ProjectMemberStatus, on_delete=models.PROTECT)
    invite_status = models.ForeignKey(ProjectInviteStatus, on_delete=models.PROTECT)
