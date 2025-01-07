import pandas as pd
import os

# Save session data
def save_session(name, exercise, reps):
    progress_file = "progress.csv"
    data = pd.read_csv(progress_file) if os.path.exists(progress_file) else pd.DataFrame(columns=["Name", "Date", "Exercise", "Reps"])
    new_entry = pd.DataFrame([{"Name": name, "Date": pd.Timestamp.now(), "Exercise": exercise, "Reps": reps}])
    data = pd.concat([data, new_entry], ignore_index=True)
    data.to_csv(progress_file, index=False)

# Load leaderboard
def load_leaderboard():
    if not os.path.exists("progress.csv"):
        return pd.DataFrame(columns=["Name", "Best Pushups", "Best Situps"])
    data = pd.read_csv("progress.csv")
    leaderboard = data.groupby("Name").max().reset_index()[["Name", "Reps"]]
    leaderboard.columns = ["Name", "Best Performance"]
    return leaderboard
