import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import os

# Save session data
def save_session(name, exercise, reps):
    progress_file = "progress.csv"
    data = pd.read_csv(progress_file) if os.path.exists(progress_file) else pd.DataFrame(columns=["Name", "Date", "Exercise", "Reps"])
    new_entry = pd.DataFrame([{"Name": name, "Date": pd.Timestamp.now(), "Exercise": exercise, "Reps": reps}])
    data = pd.concat([data, new_entry], ignore_index=True)
    data.to_csv(progress_file, index=False)

# Generate progress chart
def generate_chart(data, user):
    user_data = data[data["Name"] == user]
    if user_data.empty:
        st.warning("No progress data available for this user.")
        return

    fig, ax = plt.subplots()
    for exercise in user_data["Exercise"].unique():
        exercise_data = user_data[user_data["Exercise"] == exercise]
        ax.plot(exercise_data["Date"], exercise_data["Reps"], label=exercise)

    ax.set_title("Progress Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Reps")
    ax.legend()
    st.pyplot(fig)

# Calculate IPPT Points
def calculate_ippt_points(pushups, situps, run_time, age):
    pushup_points = min(pushups, 60) * 0.5
    situp_points = min(situps, 60) * 0.5
    run_points = max(0, 50 - run_time)

    total_points = pushup_points + situp_points + run_points
    award = "Gold" if total_points >= 85 else "Silver" if total_points >= 75 else "Pass" if total_points >= 61 else "Fail"

    return {"total": total_points, "award": award}

# Load leaderboard
def load_leaderboard():
    if not os.path.exists("progress.csv"):
        return pd.DataFrame(columns=["Name", "Best Pushups", "Best Situps"])
    data = pd.read_csv("progress.csv")
    leaderboard = data.groupby("Name").max().reset_index()[["Name", "Reps"]]
    leaderboard.columns = ["Name", "Best Performance"]
    return leaderboard
