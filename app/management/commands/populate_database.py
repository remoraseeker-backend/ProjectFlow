import random
from typing import cast

from django.core.management import BaseCommand

from authentication.models import User
from projects.models import Project
from sections.models import Section
from tasks.models import Task
from tasks.models import TaskPriority
from tasks.models import TaskStatus


class Command(BaseCommand):
    help = 'Populate the database with test entities.'

    def handle(self, *args, **options):
        self.create_users(amount=10)
        self.create_projects(amount_for_user=5)
        self.create_sections(amount_for_project=5)
        self.create_tasks(amount_for_section=5)

    def create_users(self, amount: int):
        User.objects.create_superuser(username='admin', password='admin', email='admin@gmail.com')
        for i in range(1, amount):
            User.objects.create_user(username=f'user{i}', password=f'user{i}', email=f'user{i}@gmail.com')

    def create_projects(self, amount_for_user: int):
        users = User.objects.all()
        projects_list = list()
        for user in users:
            for i in range(1, amount_for_user+1):
                project = Project(
                    title=f'Project {i} [owner: {user.username}]',
                    owner=user,
                )
                projects_list.append(project)
        projects = Project.objects.bulk_create(projects_list)
        for project in projects:
            project.members.set(random.choices(users, k=random.randint(2, len(users))))

    def create_sections(self, amount_for_project: int):
        sections_list = list()
        for project in Project.objects.all():
            for i in range(1, amount_for_project+1):
                section = Section(
                    name=f'Section {i} [project: {project.title}]',
                    project=project,
                )
                sections_list.append(section)
        Section.objects.bulk_create(sections_list)

    def create_tasks(self, amount_for_section: int):
        tasks_list = list()
        for section in Section.objects.all():
            for i in range(1, amount_for_section+1):
                executor = cast(User, random.choice(section.project.members.all()))
                creator = cast(User, random.choice(section.project.members.all()))
                task = Task(
                    title=f'Task {i} [creator: {creator.username}, executor: {executor.username}, section: {section.name}]',  # noqa E501
                    description=f'Description of task {i} [section: {section.name}]',
                    priority=random.choice(TaskPriority.values),
                    status=random.choice(TaskStatus.values),
                    executor=executor,
                    creator=creator,
                    section=section,
                )
                tasks_list.append(task)
        Task.objects.bulk_create(tasks_list)
