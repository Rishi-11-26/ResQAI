import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


from data_store import *
from volunteer_matching import match_volunteers
from resource_optimizer import optimize_resources
from gemini_ai import setup_gemini, ai_recommendation
from disaster_map import show_map


# Configure Gemini AI
from dotenv import load_dotenv
import os
load_dotenv()
setup_gemini(os.getenv("GEMINI_API_KEY"))


st.set_page_config(page_title="ResQAI", layout="wide")

st.title("🚑 ResQAI")
st.subheader("AI Powered Volunteer & Resource Coordination Platform")


# Sidebar Navigation
with st.sidebar:

    selected = option_menu(
        "Navigation",
        ["Volunteers","Tasks","Resources","AI Matching","Dashboard"],
        icons=["people","list-task","box","cpu","speedometer"],
        default_index=0,
    )


# ==========================
# Volunteers Section
# ==========================

if selected == "Volunteers":

    st.header("Volunteer Registration")

    name = st.text_input("Name")
    location = st.text_input("Location")
    skills = st.text_input("Skills")
    availability = st.number_input("Availability (hours)",1,24)

    if st.button("Register Volunteer"):

        add_volunteer(name,location,skills,availability)

        st.success("Volunteer Registered")


    # CSV Upload
    st.subheader("Upload Volunteers CSV")

    uploaded_file = st.file_uploader(
        "Upload volunteer dataset",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        for _, row in df.iterrows():

            add_volunteer(
                row["name"],
                row["location"],
                row["skills"],
                int(row["availability"])
            )

        st.success("Volunteers imported successfully!")


    st.subheader("Current Volunteers")

    volunteers_df = get_volunteers()

    if not volunteers_df.empty:

        st.dataframe(volunteers_df)



# ==========================
# Tasks Section
# ==========================

elif selected == "Tasks":

    st.header("Create Task")

    task_name = st.text_input("Task Name")
    location = st.text_input("Location")
    skill_required = st.text_input("Skill Required")
    volunteers_needed = st.number_input("Volunteers Needed",1,20)
    priority = st.selectbox("Priority",["Low","Medium","High"])

    if st.button("Create Task"):

        add_task(
            task_name,
            location,
            skill_required,
            volunteers_needed,
            priority
        )

        st.success("Task Created")


    # CSV Upload for Tasks
    st.subheader("Upload Tasks CSV")

    uploaded_tasks = st.file_uploader(
        "Upload tasks dataset",
        type=["csv"]
    )

    if uploaded_tasks is not None:

        df = pd.read_csv(uploaded_tasks)

        for _, row in df.iterrows():

            add_task(
                row["task_name"],
                row["location"],
                row["skill_required"],
                int(row["volunteers_needed"]),
                row["priority"]
            )

        st.success("Tasks imported successfully!")


    tasks_df = get_tasks()

    if not tasks_df.empty:

        st.subheader("Current Tasks")

        st.dataframe(tasks_df)



# ==========================
# Resources Section
# ==========================

elif selected == "Resources":

    st.header("Add Resources")

    resource_name = st.text_input("Resource Name")
    quantity = st.number_input("Quantity",1,1000)
    location = st.text_input("Location")

    if st.button("Add Resource"):

        add_resource(resource_name,quantity,location)

        st.success("Resource Added")


    resources_df = get_resources()

    if not resources_df.empty:

        st.subheader("Current Resources")

        st.dataframe(resources_df)

        st.subheader("Resource Priority")

        optimized = optimize_resources(resources_df)

        st.dataframe(pd.DataFrame(optimized))



# ==========================
# AI Matching Section
# ==========================

elif selected == "AI Matching":

    st.header("AI Volunteer Matching")

    volunteers_df = get_volunteers()
    tasks_df = get_tasks()

    if volunteers_df.empty or tasks_df.empty:

        st.warning("Please add volunteers and tasks first.")

    else:

        matches = match_volunteers(volunteers_df,tasks_df)

        st.dataframe(pd.DataFrame(matches))
        task_name = tasks_df.iloc[0]["task_name"]

# get volunteers matched to the first task
        matched_volunteers = [
    m["volunteer"] for m in matches
    if m["task"] == task_name
]

        if st.button("AI Recommendation"):

            suggestion = ai_recommendation(
            task_name,
            matched_volunteers
        )


            st.markdown(
                f"### 🤖 AI Recommendation\n\n{suggestion}"
            )



# ==========================
# Dashboard Section
# ==========================

elif selected == "Dashboard":

    st.header("Operations Dashboard")

    volunteers_df = get_volunteers()
    tasks_df = get_tasks()
    resources_df = get_resources()

    col1,col2,col3 = st.columns(3)

    col1.metric("Volunteers",len(volunteers_df))
    col2.metric("Tasks",len(tasks_df))
    col3.metric("Resources",len(resources_df))


    if not volunteers_df.empty:

        st.subheader("Volunteer Map")

        show_map(volunteers_df)