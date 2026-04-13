def calculate_score(volunteer, task):

    score = 0

    if task["skill_required"].lower() in volunteer["skills"].lower():
        score += 50

    if volunteer["location"].lower() == task["location"].lower():
        score += 30

    score += min(volunteer["availability"], 10)

    return score