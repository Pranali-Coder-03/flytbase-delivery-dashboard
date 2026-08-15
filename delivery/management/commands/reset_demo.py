from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from delivery.models import (
    Owner,
    Project,
    Milestone,
    Task,
    Issue,
    ProjectUpdate,
)


class Command(BaseCommand):

    help = "Reset and create clean FlytBase demo data"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.WARNING(
                "Deleting existing demo data..."
            )
        )

        # -----------------------------------------
        # DELETE EXISTING DATA
        # -----------------------------------------

        ProjectUpdate.objects.all().delete()
        Issue.objects.all().delete()
        Task.objects.all().delete()
        Milestone.objects.all().delete()
        Project.objects.all().delete()
        Owner.objects.all().delete()


        # -----------------------------------------
        # OWNERS
        # -----------------------------------------

        owners_data = [
            ("Rahul Sharma", "rahul@example.com"),
            ("Neha Joshi", "neha@example.com"),
            ("Karan Gupta", "karan@example.com"),
            ("Priya Shah", "priya@example.com"),
            ("Amit Verma", "amit@example.com"),
            ("Sneha Patil", "sneha@example.com"),
        ]

        owners = {}

        for name, email in owners_data:

            owner = Owner.objects.create(
                name=name,
                email=email
            )

            owners[name] = owner


        # -----------------------------------------
        # PROJECT DATA
        # -----------------------------------------

        projects_data = [

            {
                "name": "Warehouse AMR Deployment",
                "customer": "ABC Logistics",
                "description": (
                    "Deployment of autonomous mobile robots "
                    "for warehouse automation."
                ),
                "status": "ON_TRACK",
                "owners": [
                    "Rahul Sharma",
                    "Neha Joshi",
                    "Karan Gupta",
                ],
                "start": date(2026, 6, 16),
                "target": date(2026, 9, 14),
            },

            {
                "name": "Construction Site Monitoring",
                "customer": "BuildTech Industries",
                "description": (
                    "Drone-based monitoring and inspection "
                    "of construction sites."
                ),
                "status": "AT_RISK",
                "owners": [
                    "Priya Shah",
                    "Amit Verma",
                ],
                "start": date(2026, 6, 10),
                "target": date(2026, 9, 20),
            },

            {
                "name": "Smart Parking Automation",
                "customer": "Metro Parking Solutions",
                "description": (
                    "Autonomous parking and vehicle detection "
                    "system."
                ),
                "status": "ON_TRACK",
                "owners": [
                    "Neha Joshi",
                    "Sneha Patil",
                ],
                "start": date(2026, 7, 1),
                "target": date(2026, 10, 5),
            },

            {
                "name": "Hospital Delivery Robot",
                "customer": "CityCare Hospital",
                "description": (
                    "Indoor autonomous robots for medicine "
                    "and material delivery."
                ),
                "status": "BLOCKED",
                "owners": [
                    "Rahul Sharma",
                    "Priya Shah",
                ],
                "start": date(2026, 5, 20),
                "target": date(2026, 9, 1),
            },

            {
                "name": "Retail Inventory Robot",
                "customer": "RetailMax",
                "description": (
                    "Robotic inventory scanning and shelf "
                    "monitoring solution."
                ),
                "status": "ON_TRACK",
                "owners": [
                    "Karan Gupta",
                    "Sneha Patil",
                ],
                "start": date(2026, 7, 5),
                "target": date(2026, 10, 15),
            },

            {
                "name": "Airport Security Drone",
                "customer": "National Airport Services",
                "description": (
                    "Autonomous drone system for airport "
                    "security monitoring."
                ),
                "status": "AT_RISK",
                "owners": [
                    "Amit Verma",
                    "Rahul Sharma",
                ],
                "start": date(2026, 6, 1),
                "target": date(2026, 9, 30),
            },

            {
                "name": "Factory Vision Inspection",
                "customer": "Precision Manufacturing",
                "description": (
                    "Computer vision based quality inspection "
                    "for manufacturing."
                ),
                "status": "COMPLETED",
                "owners": [
                    "Neha Joshi",
                    "Priya Shah",
                ],
                "start": date(2026, 4, 10),
                "target": date(2026, 8, 10),
            },

            {
                "name": "Autonomous Campus Shuttle",
                "customer": "University Mobility Labs",
                "description": (
                    "Autonomous shuttle deployment across "
                    "a university campus."
                ),
                "status": "ON_TRACK",
                "owners": [
                    "Karan Gupta",
                    "Amit Verma",
                ],
                "start": date(2026, 7, 15),
                "target": date(2026, 11, 1),
            },

        ]


        # -----------------------------------------
        # MILESTONES
        # -----------------------------------------

        milestone_names = [
            "Requirement Gathering",
            "Hardware Installation",
            "System Integration",
            "Robot Configuration",
            "Testing & Validation",
            "Customer Acceptance",
        ]


        task_templates = {

            "Requirement Gathering": [
                "Collect customer requirements",
                "Confirm deployment scope",
            ],

            "Hardware Installation": [
                "Complete hardware setup",
                "Configure sensors",
            ],

            "System Integration": [
                "Integrate navigation system",
                "Fix reported issues",
            ],

            "Robot Configuration": [
                "Configure robot parameters",
                "Customer validation",
            ],

            "Testing & Validation": [
                "Run system tests",
                "Perform customer testing",
            ],

            "Customer Acceptance": [
                "Final customer approval",
                "Project handover",
            ],
        }


        # -----------------------------------------
        # CREATE PROJECTS
        # -----------------------------------------

        for project_data in projects_data:

            project = Project.objects.create(

                name=project_data["name"],

                customer_name=project_data["customer"],

                description=project_data["description"],

                status=project_data["status"],

                start_date=project_data["start"],

                target_date=project_data["target"],

            )


            # Owners

            for owner_name in project_data["owners"]:

                project.owners.add(
                    owners[owner_name]
                )


            # -------------------------------------
            # CREATE MILESTONES
            # -------------------------------------

            for index, milestone_name in enumerate(
                milestone_names
            ):

                due_date = (
                    project_data["start"]
                    + timedelta(days=(index + 1) * 20)
                )


                # Decide milestone status

                if project_data["status"] == "COMPLETED":

                    milestone_status = "DONE"

                elif index == 0:

                    milestone_status = "DONE"

                elif index == 1:

                    milestone_status = "DONE"

                elif project_data["status"] == "BLOCKED" and index == 2:

                    milestone_status = "BLOCKED"

                elif index == 2:

                    milestone_status = "IN_PROGRESS"

                else:

                    milestone_status = "OPEN"


                milestone = Milestone.objects.create(

                    project=project,

                    name=milestone_name,

                    status=milestone_status,

                    due_date=due_date,

                )


                # ---------------------------------
                # CREATE TASKS
                # ---------------------------------

                for task_index, task_name in enumerate(
                    task_templates[milestone_name]
                ):

                    task_due = (
                        due_date
                        + timedelta(days=5)
                    )


                    if milestone_status == "DONE":

                        task_status = "DONE"

                    elif (
                        milestone_status == "BLOCKED"
                        and task_index == 0
                    ):

                        task_status = "BLOCKED"

                    elif (
                        milestone_status == "IN_PROGRESS"
                        and task_index == 0
                    ):

                        task_status = "IN_PROGRESS"

                    else:

                        task_status = "OPEN"


                    # Assign owner

                    project_owner_list = list(
                        project.owners.all()
                    )

                    task_owner = (
                        project_owner_list[
                            task_index
                            % len(project_owner_list)
                        ]
                    )


                    Task.objects.create(

                        milestone=milestone,

                        name=task_name,

                        status=task_status,

                        owner=task_owner,

                        due_date=task_due,

                    )


            # -------------------------------------
            # ISSUES
            # -------------------------------------

            if project_data["status"] == "BLOCKED":

                Issue.objects.create(

                    project=project,

                    title="Navigation system blocked",

                    category="BUG",

                    status="OPEN",

                    priority="HIGH",

                )


                Issue.objects.create(

                    project=project,

                    title="Sensor configuration issue",

                    category="IMPLEMENTATION",

                    status="IN_PROGRESS",

                    priority="MEDIUM",

                )


            elif project_data["status"] == "AT_RISK":

                Issue.objects.create(

                    project=project,

                    title="Testing schedule delay",

                    category="SUPPORT",

                    status="OPEN",

                    priority="MEDIUM",

                )


                Issue.objects.create(

                    project=project,

                    title="Customer requested reporting change",

                    category="FEATURE",

                    status="OPEN",

                    priority="LOW",

                )


            else:

                Issue.objects.create(

                    project=project,

                    title="Customer clarification",

                    category="QUESTION",

                    status="RESOLVED",

                    priority="LOW",

                )


        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        self.stdout.write("")

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "   DEMO DATA RESET SUCCESSFULLY"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Projects: {Project.objects.count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Owners: {Owner.objects.count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Milestones: {Milestone.objects.count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Tasks: {Task.objects.count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Issues: {Issue.objects.count()}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "======================================"
            )
        )