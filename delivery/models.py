from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):

    STATUS_CHOICES = [
        ("ON_TRACK", "On Track"),
        ("AT_RISK", "At Risk"),
        ("BLOCKED", "Blocked"),
        ("COMPLETED", "Completed"),
    ]

    name = models.CharField(max_length=200)
    customer_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    owners = models.ManyToManyField(
        Owner,
        related_name="projects"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ON_TRACK"
    )

    start_date = models.DateField()
    target_date = models.DateField()

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Milestone(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("BLOCKED", "Blocked"),
        ("DONE", "Done"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones"
    )

    name = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    due_date = models.DateField()

    def __str__(self):
        return self.name


class Task(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("BLOCKED", "Blocked"),
        ("DONE", "Done"),
    ]

    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    name = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    due_date = models.DateField()

    def __str__(self):
        return self.name


class Issue(models.Model):

    CATEGORY_CHOICES = [
    ("BUG", "Bug"),
    ("FEATURE", "Feature Request"),
    ("QUESTION", "Question"),
    ("SUPPORT", "Support"),
    ("IMPLEMENTATION", "Implementation"),
    ]
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="issues"
    )

    title = models.CharField(max_length=250)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    status = models.CharField(max_length=50)

    priority = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectUpdate(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="updates"
    )

    raw_text = models.TextField()

    structured_data = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.project.name} - {self.created_at}"
class ProjectDocument(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    name = models.CharField(max_length=200)

    file = models.FileField(
        upload_to="project_documents/"
    )

    visible_to_customer = models.BooleanField(
        default=False
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name