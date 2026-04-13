def optimize_resources(resources_df):

    optimized = []

    for _, r in resources_df.iterrows():

        score = 0

        if r["resource_name"].lower() in ["medicine", "medical kit"]:
            score += 50
        elif r["resource_name"].lower() in ["food", "water"]:
            score += 40
        else:
            score += 20

        score += min(r["quantity"], 50)

        optimized.append({
            "resource": r["resource_name"],
            "location": r["location"],
            "priority_score": score
        })

    optimized.sort(key=lambda x: x["priority_score"], reverse=True)

    return optimized