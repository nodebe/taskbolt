from taskbolt.errors import ServerError, UserError
from user.classes import UserClass
from .models import Project, ProjectInviteStatus, ProjectMember, ProjectMemberStatus, ProjectStatus
from user.models import User


class ProjectClass:

    def get_project_by_id(self, id:str):
        self.project = Project.objects.filter(id=id).first()

        return self.project

    def get_project_member(self, project, user):
        membership = ProjectMember.objects.filter(project=project, user=user).first()

        return membership
    
    def get_projects_by_user(self, user):
        projects_ids = self.get_projects_ids_by_user(user)

        projects = Project.objects.filter(id__in=projects_ids).all()

        return projects

    def get_projects_ids_by_user(self, user):
        # Get projects that a user has access to
        projects_ids = ProjectMember.objects.filter(user=user, invite_status=2).values_list('project_id')

        return projects_ids

    def create_project(self, data:dict):
        # Fetch details of creator of project
        user = UserClass()
        project_creator = user.get_user_by_id(data['user_id'])

        # Get members of project
        members = data.pop('members')
        creator_id = data.pop('user_id')

        # Add creator email as part of member
        members.append(project_creator.email)

        # Setting the default status to 'Active'
        data['status'] = self.set_project_status(1)
        
        # Insert Project data into models
        self.project = Project.objects.create(**data)

        # Adding project members
        self.add_project_members(email_list=members)

        # Make creator active and admin of project
        self.activate_member_invite(user=project_creator)
        self.make_member_admin(user=project_creator)
        
        return self.project
    
    def set_project_status(self, status:int):
        status = ProjectStatus.objects.filter(id=status).first()
        return status
    
    def set_project_invite_status(self, status:int):
        status = ProjectInviteStatus.objects.filter(id=status).first()
        return status
    
    def set_member_status(self, status:int):
        status = ProjectMemberStatus.objects.filter(id=status).first()
        return status
    
    def activate_member_invite(self, user):
        membership = self.get_project_member(self.project, user)
        membership.invite_status = self.set_project_invite_status(2)
        membership.save()
    
    def decline_member_invite(self, user):
        membership = self.get_project_member(self.project, user)
        membership.invite_status = self.set_project_invite_status(3)
        membership.save()

    def add_project_members(self, email_list:list):
        try:
            # Get users from User model using email list
            users = User.objects.filter(email__in=email_list)

            # Add all users to the project and set them as members(default) and invite status as pending
            default_member_status = self.set_member_status(2)
            default_member_invite_status = self.set_project_invite_status(1)

            self.project.members.add(*users, through_defaults={'member_status': default_member_status, 'invite_status': default_member_invite_status})
        
        except Exception as e:
            raise ServerError('Error when adding members to project, Internal Server Error!')


    def make_member_admin(self, user):
        # Get the user from the ProjectMember model and change the member status
        membership = self.get_project_member(self.project, user)
        membership.member_status = self.set_member_status(1)
        membership.save()
    
    def make_admin_member(self, user):
        # Get the user from the ProjectMember model and change the member status
        membership = self.get_project_member(self.project, user)
        # Check if there is another admin.
        # Write code here
        
        membership.member_status = self.set_member_status(2)
        membership.save()

    def verify_member_in_project(self, user_id, project_id):
        user_obj = UserClass()
        user = user_obj.get_user_by_id(user_id)

        project = self.get_project_by_id(project_id)

        verify_member = self.get_project_member(project, user)

        if verify_member == None:
            raise UserError('User is not a member of the project!', '400')