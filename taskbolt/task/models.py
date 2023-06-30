from django.db import models
import uuid

from section.models import ProjectSection
from user.models import User

# Create your models here.
class Task(models.Model):
    id = models.CharField(max_length=36, primary_key=True, null=False)
    title = models.CharField(max_length=50, null=False)
    description = models.TextField()
    points = models.IntegerField()
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through='TaskMember')
    creator = models.ForeignKey(User, on_delete=models.SET_DEFAULT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4().hex)
        super().save(*args, **kwargs)

class TaskMember(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)