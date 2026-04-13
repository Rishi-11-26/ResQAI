from volunteer_scoring import calculate_score

def match_volunteers(volunteers_df, tasks_df):

    matches = []

    for _, task in tasks_df.iterrows():

        scored = []

        for _, volunteer in volunteers_df.iterrows():

            score = calculate_score(volunteer, task)

            scored.append((volunteer["name"], score))

        scored.sort(key=lambda x: x[1], reverse=True)

        top = scored[:task["volunteers_needed"]]

        for name, score in top:

            matches.append({
                "task": task["task_name"],
                "volunteer": name,
                "score": score
            })

    return matches