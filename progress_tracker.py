import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

def load_progress(file_path="progress.csv"):
    """
    Load progress data from a CSV file.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Date", "Exercise", "Reps"])

def display_progress(person):
    """
    Displays the user's progress in a Streamlit app.
    """
    st.header(f"Progress Tracker for {person.name}")

    # Filter data by user
    progress_data = load_progress()
    user_progress = progress_data[progress_data["Name"] == person.name]
    if user_progress.empty:
        st.info("No progress data found. Start exercising to track your progress!")
        return

    # Session history
    st.markdown("### Session History")
    st.table(user_progress)

    # Summary stats
    summary = user_progress.groupby("Exercise").agg(
        TotalReps=pd.NamedAgg(column="Reps", aggfunc="sum"),
        Sessions=pd.NamedAgg(column="Reps", aggfunc="count"),
    ).reset_index()

    st.markdown("### Summary")
    st.table(summary)

    # Graphs
    st.markdown("### Performance Over Time")

    # Set up plotting table
    plt.style.use("fivethirtyeight")
    pushup_data = progress_data[progress_data["Exercise"] == "Pushups"]
    situp_data = progress_data[progress_data["Exercise"] == "Situps"]

    # Date format the data
    pushup_data["Date"] = pd.to_datetime(pushup_data["Date"])
    pushup_data["DateFormat"] = pushup_data["Date"].dt.strftime("%Y/%m/%d")
    situp_data["Date"] = pd.to_datetime(situp_data["Date"])
    situp_data["DateFormat"] = situp_data["Date"].dt.strftime("%Y/%m/%d")

    # Plot and display the data
    plt.figure(figsize=(15, 15))
    plt.subplot(211)
    plt.plot(pushup_data["DateFormat"], pushup_data["Reps"])
    plt.plot(situp_data["DateFormat"], situp_data["Reps"])
    plt.xlabel("Date")
    plt.ylabel("Reps")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt.gcf())