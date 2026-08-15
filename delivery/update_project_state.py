from .models import Project, Milestone, Task, Issue


def apply_ai_result(project, ai_result):

    # -----------------------------------------
    # 1. UPDATE PROJECT STATUS
    # -----------------------------------------

    project_status = ai_result.get("project_status")

    if project_status in [
        "ON_TRACK",
        "AT_RISK",
        "BLOCKED",
        "COMPLETED",
    ]:

        project.status = project_status
        project.save()


    # -----------------------------------------
    # 2. FIND MILESTONE
    # -----------------------------------------

    milestone_name = ai_result.get("milestone")

    milestone = None

    if milestone_name:

        milestone = Milestone.objects.filter(
            project=project,
            name__iexact=milestone_name
        ).first()


    # -----------------------------------------
    # 3. FIND TASK
    # -----------------------------------------

    task_name = ai_result.get("task")

    task = None

    if task_name:

        if milestone:

            task = Task.objects.filter(
                milestone=milestone,
                name__iexact=task_name
            ).first()

        else:

            task = Task.objects.filter(
                milestone__project=project,
                name__iexact=task_name
            ).first()


    # -----------------------------------------
    # 4. UPDATE TASK
    # -----------------------------------------

    task_status = ai_result.get("task_status")

    if task and task_status:

        task.status = task_status

        if ai_result.get("owner"):

            owner = task.owner

            if owner:
                pass

        task.save()


    # -----------------------------------------
    # 5. UPDATE MILESTONE
    # -----------------------------------------

    if milestone and task_status:

        if task_status == "BLOCKED":

            milestone.status = "BLOCKED"

        elif task_status == "IN_PROGRESS":

            milestone.status = "IN_PROGRESS"

        elif task_status == "DONE":

            # Check whether all tasks are done

            remaining_tasks = milestone.tasks.exclude(
                status="DONE"
            ).exists()

            if not remaining_tasks:

                milestone.status = "DONE"

        milestone.save()


    # -----------------------------------------
    # 6. CREATE ISSUE
    # -----------------------------------------

    blocker = ai_result.get("blocker")

    issue_category = ai_result.get(
        "issue_category"
    )

    if blocker:

        existing_issue = Issue.objects.filter(
            project=project,
            title__icontains=blocker[:50],
            status__in=["OPEN", "IN_PROGRESS"]
        ).first()

        if not existing_issue:

            Issue.objects.create(

                project=project,

                title=blocker,

                category=(
                    issue_category
                    if issue_category
                    else "IMPLEMENTATION"
                ),

                status="OPEN",

                priority="HIGH",

            )


    return {
        "project": project,
        "milestone": milestone,
        "task": task,
    }