import pandas as pd
import streamlit as st

def load_leaderboard(file_path="progress.csv"):
    """
    Load leaderboard data from a CSV file.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Exercise", "Total Reps"])

def display_leaderboard():
    """
    Displays the leaderboard in a Streamlit app.
    """
    st.header("Leaderboard")
    st.markdown("### Top Performers")

    leaderboard = load_leaderboard()

    if leaderboard.empty:
        st.info("No records found. Start exercising to add entries!")
        return

    # Display top performers by exercise
    for exercise in ["Pushups", "Situps"]:
        st.markdown(f"#### {exercise.capitalize()} Leaderboard")
        exercise_data = leaderboard[leaderboard["Exercise"] == exercise]
        sorted_data = exercise_data.sort_values("Reps", ascending=False).head(10)
        st.table(sorted_data)