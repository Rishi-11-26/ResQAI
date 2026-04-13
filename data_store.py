import pandas as pd

volunteers = []
tasks = []
resources = []

def add_volunteer(name, location, skills, availability):
    volunteers.append({
        "name": name,
        "location": location,
        "skills": skills,
        "availability": availability
    })

def get_volunteers():
    return pd.DataFrame(volunteers)

def add_task(task_name, location, skill_required, volunteers_needed, priority):
    tasks.append({
        "task_name": task_name,
        "location": location,
        "skill_required": skill_required,
        "volunteers_needed": volunteers_needed,
        "priority": priority
    })

def get_tasks():
    return pd.DataFrame(tasks)

def add_resource(resource_name, quantity, location):
    resources.append({
        "resource_name": resource_name,
        "quantity": quantity,
        "location": location
    })

def get_resources():
    return pd.DataFrame(resources)