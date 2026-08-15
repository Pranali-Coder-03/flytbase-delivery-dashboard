import os
import json

from google import genai


def process_project_update(project, update_text):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
        )

    client = genai.Client(api_key=api_key)

    # Get existing milestones and tasks
    milestones = project.milestones.prefetch_related("tasks").all()

    project_structure = []

    for milestone in milestones:

        tasks = []

        for task in milestone.tasks.all():

            tasks.append({
                "name": task.name,
                "status": task.status
            })

        project_structure.append({
            "milestone": milestone.name,
            "status": milestone.status,
            "tasks": tasks
        })


    prompt = f"""
You are a project delivery management AI.

You must analyze a project update and map it
to the EXISTING project structure.

PROJECT:
{project.name}

CUSTOMER:
{project.customer_name}


EXISTING PROJECT STRUCTURE:

{json.dumps(project_structure, indent=2)}


NEW PROJECT UPDATE:

{update_text}


IMPORTANT RULES:

1. You MUST choose a milestone from the existing milestones.

2. You MUST choose a task from the existing tasks
   whenever the update clearly relates to one.

3. DO NOT invent a new milestone.

4. DO NOT invent a new task.

5. If no exact task exists, choose the closest existing task.

6. If the update says something is blocked,
   project_status should normally be BLOCKED or AT_RISK.

7. Extract owner and ETA only when mentioned.

8. Do not invent information.


Return ONLY valid JSON using this structure:

{{
    "project_status":
        "ON_TRACK | AT_RISK | BLOCKED | COMPLETED",

    "milestone":
        "EXACT EXISTING MILESTONE NAME",

    "task":
        "EXACT EXISTING TASK NAME",

    "task_status":
        "OPEN | IN_PROGRESS | BLOCKED | DONE",

    "blocker":
        "string or null",

    "owner":
        "string or null",

    "eta":
        "string or null",

    "issue_category":
        "BUG | FEATURE | QUESTION | SUPPORT | IMPLEMENTATION | null",

    "summary":
        "short summary"
}}
"""


    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )


    text = response.text.strip()


    if text.startswith("```"):

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()


    return json.loads(text)