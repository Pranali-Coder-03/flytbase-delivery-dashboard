from django.contrib import admin
from .models import (
    Owner,
    Project,
    Milestone,
    Task,
    Issue,
    ProjectUpdate,
    ProjectDocument,
)

admin.site.register(Project)
admin.site.register(Owner)
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Issue)
admin.site.register(ProjectUpdate)
admin.site.register(ProjectDocument)