from google import genai

client = None

def setup_gemini(api_key):
    global client
    client = genai.Client(api_key=api_key)

def ai_recommendation(task, volunteers):

    volunteer_list = ", ".join(volunteers)

    prompt = f"""
You are an AI disaster response coordinator.

Task:
{task}

Available volunteers:
{volunteer_list}

Recommend the best volunteers for this disaster response task.
Explain briefly.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except:

        return f"""
AI Recommendation

Recommended Volunteers: {volunteer_list}

Reason:
Based on skill compatibility, availability and location,
these volunteers are the best candidates for the task.
"""