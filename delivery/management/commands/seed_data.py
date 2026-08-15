from django.core.management.base import BaseCommand
from delivery.models import (
    Owner,
    Project,
    Milestone,
    Task,
    Issue,
    ProjectUpdate,
)

from datetime import date, timedelta
import random


class Command(BaseCommand):

    help = "Generate synthetic FlytBase project delivery data"

    def handle(self, *args, **kwargs):

        self.stdout.write("Creating synthetic data...")

        # ------------------------------------------------
        # Clear existing data
        # ------------------------------------------------

        ProjectUpdate.objects.all().delete()
        Issue.objects.all().delete()
        Task.objects.all().delete()
        Milestone.objects.all().delete()
        Project.objects.all().delete()
        Owner.objects.all().delete()

        # ------------------------------------------------
        # Owners
        # ------------------------------------------------

        owner_data = [
            ("Rahul Sharma", "rahul@flytbase-demo.com"),
            ("Priya Patil", "priya@flytbase-demo.com"),
            ("Amit Kulkarni", "amit@flytbase-demo.com"),
            ("Neha Joshi", "neha@flytbase-demo.com"),
            ("Rohan Mehta", "rohan@flytbase-demo.com"),
            ("Sneha Deshmukh", "sneha@flytbase-demo.com"),
            ("Arjun Shah", "arjun@flytbase-demo.com"),
            ("Karan Gupta", "karan@flytbase-demo.com"),
        ]

        owners = []

        for name, email in owner_data:

            owner = Owner.objects.create(
                name=name,
                email=email
            )

            owners.append(owner)

        # ------------------------------------------------
        # Projects
        # ------------------------------------------------

        projects = [
            (
                "Warehouse AMR Deployment",
                "ABC Logistics",
                "Deployment of autonomous mobile robots for warehouse automation.",
                "ON_TRACK",
            ),
            (
                "Factory Vision Inspection",
                "XYZ Manufacturing",
                "Computer vision based quality inspection system.",
                "AT_RISK",
            ),
            (
                "Airport Security Drone",
                "SkyTech Airports",
                "Autonomous drone monitoring and security solution.",
                "BLOCKED",
            ),
            (
                "Retail Inventory Robot",
                "MegaMart",
                "Autonomous inventory scanning robot deployment.",
                "ON_TRACK",
            ),
            (
                "Hospital Delivery Robot",
                "CityCare Hospitals",
                "Indoor autonomous robot for medical supply delivery.",
                "ON_TRACK",
            ),
            (
                "Smart Parking Automation",
                "UrbanPark",
                "Autonomous monitoring and parking management system.",
                "AT_RISK",
            ),
            (
                "Construction Site Monitoring",
                "BuildRight",
                "Drone-based construction site monitoring.",
                "COMPLETED",
            ),
            (
                "Logistics Hub Automation",
                "FastMove Logistics",
                "End-to-end logistics hub automation.",
                "ON_TRACK",
            ),
        ]

        created_projects = []

        for index, (
            name,
            customer,
            description,
            status
        ) in enumerate(projects):

            project = Project.objects.create(
                name=name,
                customer_name=customer,
                description=description,
                status=status,
                start_date=date.today() - timedelta(days=60),
                target_date=date.today() + timedelta(days=30),
            )

            # Assign 1–3 owners
            selected_owners = random.sample(
                owners,
                random.randint(1, 3)
            )

            project.owners.set(selected_owners)

            created_projects.append(project)

        # ------------------------------------------------
        # Milestones and Tasks
        # ------------------------------------------------

        milestone_names = [
            "Requirement Gathering",
            "Hardware Installation",
            "System Integration",
            "Robot Configuration",
            "Testing & Validation",
            "Customer Acceptance",
        ]

        task_names = [
            "Collect customer requirements",
            "Complete hardware setup",
            "Configure sensors",
            "Integrate navigation system",
            "Run system tests",
            "Fix reported issues",
            "Customer validation",
        ]

        for project in created_projects:

            for milestone_index, milestone_name in enumerate(
                milestone_names
            ):

                if milestone_index < 2:

                    milestone_status = "DONE"

                elif milestone_index == 2:

                    milestone_status = "IN_PROGRESS"

                else:

                    milestone_status = "OPEN"

                milestone = Milestone.objects.create(
                    project=project,
                    name=milestone_name,
                    status=milestone_status,
                    due_date=date.today()
                    + timedelta(days=(milestone_index + 1) * 10),
                )

                # Create tasks
                for task_index in range(3):

                    task_status = random.choice([
                        "DONE",
                        "DONE",
                        "IN_PROGRESS",
                        "OPEN",
                    ])

                    # Some blocked tasks for AT_RISK/BLOCKED projects
                    if (
                        project.status in ["AT_RISK", "BLOCKED"]
                        and task_index == 2
                    ):
                        task_status = "BLOCKED"

                    Task.objects.create(
                        milestone=milestone,
                        name=random.choice(task_names),
                        status=task_status,
                        owner=random.choice(owners),
                        due_date=date.today()
                        + timedelta(days=random.randint(5, 45)),
                    )

        # ------------------------------------------------
        # Issues
        # ------------------------------------------------

        issue_titles = [
            "Robot navigation failure",
            "Sensor calibration issue",
            "Customer dashboard access",
            "Request for automatic charging",
            "API integration question",
            "Deployment configuration issue",
            "Camera integration problem",
            "Additional reporting requirement",
        ]

        categories = [
            "BUG",
            "FEATURE",
            "QUESTION",
            "SUPPORT",
            "IMPLEMENTATION",
        ]

        for project in created_projects:

            for _ in range(random.randint(3, 5)):

                Issue.objects.create(
                    project=project,
                    title=random.choice(issue_titles),
                    category=random.choice(categories),
                    status=random.choice([
                        "Open",
                        "In Progress",
                        "Resolved",
                    ]),
                    priority=random.choice([
                        "Low",
                        "Medium",
                        "High",
                    ]),
                )

        # ------------------------------------------------
        # Project Updates
        # ------------------------------------------------

        update_messages = [
            "Hardware installation has been completed successfully.",
            "Robot integration is progressing as planned.",
            "Customer testing has been scheduled for next week.",
            "Navigation testing is currently blocked due to sensor configuration.",
            "The customer requested an additional reporting feature.",
            "System validation is almost complete.",
            "Deployment team completed the latest configuration changes.",
            "Integration testing identified a minor issue that is being investigated.",
        ]

        for project in created_projects:

            for _ in range(random.randint(5, 8)):

                ProjectUpdate.objects.create(
                    project=project,
                    raw_text=random.choice(update_messages),
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Synthetic FlytBase data created successfully!"
            )
        )