from project.classes import ProjectClass
from taskbolt.errors import UserError
from project.models import ProjectMember
from user.classes import UserClass
from .models import ProjectSection

class SectionClass:
    
    def get_project(self, project_id):
        self.project_obj = ProjectClass()
        project = self.project_obj.get_project_by_id(id=project_id)

        if project == None:
            raise UserError('Project does not exist!', '404')

        return project

    def get_user(self, user_id):
        user_obj = UserClass()
        user = user_obj.get_user_by_id(id=user_id)

        if user == None:
            raise UserError('User does not exist!', '404')
        
        return user
    
    def create_section(self, data:dict):
        user_id = data.pop('user_id')
        project_id = data.pop('project_id')

        # Get Project using project_id
        project = self.get_project(project_id)

        # Get Project member using user_id
        user = self.get_user(user_id)
        
        # Validate that member creating section is an active member of the project
        self.validate_member_for_section(project, user)
       
        # Create a Project model instance in the data dictionary
        data['project'] = project

        # Pushing to DB
        section = ProjectSection.objects.create(**data)
        section.save()

        return section

    def validate_member_for_section(self, project, user):
        find_project_member = self.project_obj.get_project_member(project, user)

        if find_project_member:
            if find_project_member.invite_status.id != 2:
                raise UserError('Unauthorised Action! You are not a member of this project!', '400')
        else:
            raise UserError('Unauthorised Action! You are not a member of this project!', '400')

    def get_project_sections(self, project):
        sections = ProjectSection.objects.filter(project=project).all()

        return sections
