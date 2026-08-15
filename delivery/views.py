from django.shortcuts import render, get_object_or_404
from django.http import FileResponse 
from .pdf_service import generate_project_report
from .forms import ProjectUpdateForm
from .models import Project, ProjectUpdate, Task
from .ai_service import process_project_update
from .update_project_state import apply_ai_result
from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch

def dashboard(request):

    projects = Project.objects.prefetch_related(
        "owners",
        "milestones",
        "milestones__tasks",
        Prefetch(
            "updates",
            queryset=ProjectUpdate.objects.order_by("-created_at")
        ),
    )

    context = {
        "projects": projects,
        "total_projects": projects.count(),
        "on_track": projects.filter(status="ON_TRACK").count(),
        "at_risk": projects.filter(status="AT_RISK").count(),
        "blocked": projects.filter(status="BLOCKED").count(),
        "completed": projects.filter(status="COMPLETED").count(),
    }

    return render(
        request,
        "delivery/dashboard.html",
        context
    )


def project_detail(request, project_id):

    project = get_object_or_404(
        Project.objects.prefetch_related(
            "owners",
            "milestones",
            "milestones__tasks",
            "issues",
            "updates",
            "documents",
        ),
        id=project_id
    )

    return render(
        request,
        "delivery/project_detail.html",
        {
            "project": project,
            "view_type": "internal",
        }
    )


def customer_project_detail(request, project_id):

    project = get_object_or_404(
        Project.objects.prefetch_related(
            "milestones",
            "milestones__tasks",
            "updates",
            "documents",
        ),
        id=project_id
    )

    customer_documents = project.documents.filter(
        visible_to_customer=True
    )

    return render(
        request,
        "delivery/customer_project_detail.html",
        {
            "project": project,
            "view_type": "customer",
            "customer_documents": customer_documents,
        }
    )

# ==========================================
# AI PROJECT UPDATE
# ==========================================

def project_update(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        form = ProjectUpdateForm(request.POST)

        if form.is_valid():

            raw_text = form.cleaned_data["update_text"]

            # 1. Save the original customer/update message
            update = ProjectUpdate.objects.create(
                project=project,
                raw_text=raw_text,
            )

            try:

                # 2. Send the update to AI
                structured_data = process_project_update(
                    project,
                    raw_text
                )

                # 3. Save AI result
                update.structured_data = structured_data
                update.save()

                # 4. Apply AI result to project/task/milestone/issue
                apply_ai_result(
                    project,
                    structured_data
                )

            except Exception as e:

                print("AI processing error:", e)

                structured_data = {
                    "error": str(e)
                }

            # 5. Show AI result
            return render(
                request,
                "delivery/update_result.html",
                {
                    "project": project,
                    "update": update,
                    "structured_data": structured_data,
                }
            )

    else:

        form = ProjectUpdateForm()

    return render(
        request,
        "delivery/project_update.html",
        {
            "project": project,
            "form": form,
        }
    )


# ==========================================
# KANBAN
# ==========================================

def project_kanban(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    tasks = Task.objects.filter(
        milestone__project=project
    ).select_related(
        "milestone",
        "owner"
    )

    kanban = {
        "OPEN": [],
        "IN_PROGRESS": [],
        "BLOCKED": [],
        "DONE": [],
    }

    for task in tasks:

        if task.status in kanban:
            kanban[task.status].append(task)

    return render(
        request,
        "delivery/kanban.html",
        {
            "project": project,
            "kanban": kanban,
        }
    )

def generate_project_report_view(request, project_id):

    project = get_object_or_404(
        Project.objects.prefetch_related(
            "owners",
            "milestones__tasks",
            "issues",
            "updates",
        ),
        id=project_id
    )

    pdf = generate_project_report(project)

    filename = (
        project.name.replace(" ", "_")
        + "_Report.pdf"
    )

    return FileResponse(
        pdf,
        as_attachment=True,
        filename=filename,
        content_type="application/pdf",
    )

def dashboard(request):

    projects = Project.objects.prefetch_related(
        "owners",
        "milestones",
        "milestones__tasks",
        "updates",
    )

    cutoff_date = timezone.now() - timedelta(days=7)

    stale_projects = []

    for project in projects:

        latest_update = project.updates.order_by(
            "-created_at"
        ).first()

        if latest_update:

            if latest_update.created_at < cutoff_date:
                stale_projects.append(project)

        else:

            # Project has never received an update
            stale_projects.append(project)

    context = {
        "projects": projects,

        "total_projects": projects.count(),

        "on_track": projects.filter(
            status="ON_TRACK"
        ).count(),

        "at_risk": projects.filter(
            status="AT_RISK"
        ).count(),

        "blocked": projects.filter(
            status="BLOCKED"
        ).count(),

        "completed": projects.filter(
            status="COMPLETED"
        ).count(),

        "stale_projects": stale_projects,
    }

    return render(
        request,
        "delivery/dashboard.html",
        context
    )