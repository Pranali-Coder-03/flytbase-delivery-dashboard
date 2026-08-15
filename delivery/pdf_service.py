from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.lib import colors


def generate_project_report(project):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    story = []

    # Title
    story.append(
        Paragraph(
            "FlytBase - Customer Project Report",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"{project.name} - {project.customer_name}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 15))

    # Project information
    project_data = [
        ["Project", project.name],
        ["Customer", project.customer_name],
        ["Status", project.get_status_display()],
        ["Start Date", str(project.start_date)],
        ["Target Date", str(project.target_date)],
    ]

    table = Table(project_data, colWidths=[130, 350])

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 7),
        ])
    )

    story.append(table)

    story.append(Spacer(1, 20))

    # Owners
    story.append(
        Paragraph(
            "Project Owners",
            styles["Heading2"]
        )
    )

    owners = ", ".join(
        owner.name for owner in project.owners.all()
    )

    story.append(
        Paragraph(
            owners or "No owners assigned",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 15))

    # Milestones
    story.append(
        Paragraph(
            "Milestones & Tasks",
            styles["Heading2"]
        )
    )

    for milestone in project.milestones.prefetch_related("tasks"):

        story.append(
            Paragraph(
                f"<b>{milestone.name}</b> - "
                f"{milestone.get_status_display()} "
                f"(Due: {milestone.due_date})",
                styles["BodyText"]
            )
        )

        for task in milestone.tasks.all():

            owner = task.owner.name if task.owner else "Unassigned"

            story.append(
                Paragraph(
                    f"• {task.name} - "
                    f"{task.get_status_display()} - "
                    f"Owner: {owner}",
                    styles["BodyText"]
                )
            )

        story.append(Spacer(1, 8))

    # Issues
    story.append(
        Paragraph(
            "Issues",
            styles["Heading2"]
        )
    )

    issues = project.issues.all()

    if issues.exists():

        for issue in issues:

            story.append(
                Paragraph(
                    f"• <b>{issue.title}</b> - "
                    f"{issue.get_category_display()} - "
                    f"{issue.status} - "
                    f"Priority: {issue.priority}",
                    styles["BodyText"]
                )
            )

    else:

        story.append(
            Paragraph(
                "No issues reported.",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 15))

    # Updates
    story.append(
        Paragraph(
            "Recent Project Updates",
            styles["Heading2"]
        )
    )

    updates = project.updates.order_by("-created_at")[:10]

    if updates.exists():

        for update in updates:

            story.append(
                Paragraph(
                    f"<b>{update.created_at.strftime('%d %b %Y, %I:%M %p')}</b>",
                    styles["BodyText"]
                )
            )

            story.append(
                Paragraph(
                    update.raw_text,
                    styles["BodyText"]
                )
            )

            story.append(Spacer(1, 8))

    else:

        story.append(
            Paragraph(
                "No updates available.",
                styles["BodyText"]
            )
        )

    # Description
    story.append(
        Paragraph(
            "Project Description",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            project.description or "No description available.",
            styles["BodyText"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer