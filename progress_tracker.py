import pandas as pd
import streamlit as st


def load_progress(file_path="leaderboard.csv"):
    """
    Load progress data from a CSV file.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Exercise", "Reps", "Date"])


def display_progress(user_name):
    """
    Displays the user's progress in a Streamlit app.
    """
    st.header("Progress Tracker")
    st.markdown(f"### Progress for {user_name}")

    progress_data = load_progress()

    # Filter data by user
    user_progress = progress_data[progress_data["Name"] == user_name]

    if user_progress.empty:
        st.info("No progress data found. Start exercising to track your progress!")
        return

    # Summary stats
    summary = user_progress.groupby("Exercise").agg(
        Total_Reps=pd.NamedAgg(column="Reps", aggfunc="sum"),
        Max_Reps=pd.NamedAgg(column="Reps", aggfunc="max"),
        Sessions=pd.NamedAgg(column="Reps", aggfunc="count"),
    ).reset_index()

    st.markdown("### Summary")
    st.table(summary)

    # Session history
    st.markdown("### Session History")
    st.table(user_progress)

    # Graphs
    st.markdown("### Performance Over Time")
    for exercise in user_progress["Exercise"].unique():
        exercise_data = user_progress[user_progress["Exercise"] == exercise]
        st.line_chart(exercise_data[["Reps"]])