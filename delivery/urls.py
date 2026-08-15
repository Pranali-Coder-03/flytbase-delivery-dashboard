from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "project/<int:project_id>/",
        views.project_detail,
        name="project_detail"
    ),

    path(
        "customer/project/<int:project_id>/",
        views.customer_project_detail,
        name="customer_project_detail"
    ),
    path(
    "project/<int:project_id>/update/",
    views.project_update,
    name="project_update"
),
path(
    "project/<int:project_id>/kanban/",
    views.project_kanban,
    name="project_kanban"
),
path(
    "project/<int:project_id>/report/",
    views.generate_project_report_view,
    name="generate_project_report"
),

]