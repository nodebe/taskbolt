from django.db import models
from project.models import Project

# Create your models here.

class ProjectSection(models.Model):
    title = models.CharField(max_length=15, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    project = models.ForeignKey(Project, on_delete=models.CASCADE)