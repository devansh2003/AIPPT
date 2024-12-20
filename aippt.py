import streamlit as st
import cv2
from aippt_utils import calculate_ippt_points, generate_chart, save_session, load_leaderboard
from pose_detection import pose, detect_reps, mp_drawing, mp_pose
import pandas as pd
import os
import time

# Detection thresholds
thresholds = {
    "pushup_up": 160,
    "pushup_down": 90,
    "situp_up": 160,
    "situp_down": 90,
}

# Real-time repetition counter
def workout_loop(video_feed, exercise, target_reps):
    cap = cv2.VideoCapture(video_feed)
    count = 0
    stage = None

    # Streamlit placeholders
    stframe = st.empty()
    count_placeholder = st.empty()
    stage_placeholder = st.empty()
    feedback_placeholder = st.empty()

    while st.session_state[f"{exercise}_active"]:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        # Detect repetitions
        count, stage = detect_reps(results, exercise, count, stage, thresholds)

        # Check if target is reached
        if count >= target_reps and not st.session_state[f"{exercise}_target_reached"]:
            st.session_state[f"{exercise}_target_reached"] = True

        # Draw landmarks
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
            )

        # Update UI elements
        count_placeholder.markdown(f"### Reps: {count} / {target_reps}")
        stage_placeholder.markdown(f"### Stage: {stage.capitalize() if stage else 'N/A'}")
        if st.session_state[f"{exercise}_target_reached"]:
            feedback_placeholder.success("🎉 Target reps reached! Keep going or finish your workout.")
        else:
            feedback_placeholder.empty()

        stframe.image(frame, channels="BGR")

        # Allow Streamlit to refresh
        time.sleep(0.03)

    cap.release()
    return count

# Helper function to end workout
def end_workout(exercise, count, name):
    st.session_state[f"{exercise}_active"] = False
    st.session_state[f"{exercise}_finish_clicked"] = True
    save_session(name, exercise, count)
    st.success(f"Total {exercise.capitalize()} Counted: {count}")

# Main application
def main():
    st.title("AIPPT - Advanced Individual Physical Proficiency Test")
    st.sidebar.header("Navigation")

    # User details
    st.sidebar.subheader("User Details")
    name = st.sidebar.text_input("Enter your Name")
    age = st.sidebar.number_input("Enter your Age", min_value=16, max_value=60, step=1)
    if not name or not age:
        st.warning("Please enter your details to proceed.")
        return

    # Settings
    st.sidebar.subheader("Settings")
    target_reps = st.sidebar.slider("Target Repetitions", min_value=5, max_value=100, step=5, value=20)

    # Menu
    menu = st.sidebar.radio("Menu", ["Train Pushups", "Train Situps", "IPPT Calculator", "Progress Tracker", "Leaderboard"])

    # Initialize session states
    exercises = ["pushup", "situp"]
    for exercise in exercises:
        if f"{exercise}_active" not in st.session_state:
            st.session_state[f"{exercise}_active"] = False
        if f"{exercise}_target_reached" not in st.session_state:
            st.session_state[f"{exercise}_target_reached"] = False
        if f"{exercise}_finish_clicked" not in st.session_state:
            st.session_state[f"{exercise}_finish_clicked"] = False

    # Push-Up Training
    if menu == "Train Pushups":
        st.header("Push-Up Training")
        st.info(f"Perform as many push-ups as you can! Your target is {target_reps} reps.")

        # Start Training Button
        if not st.session_state["pushup_active"] and not st.session_state["pushup_finish_clicked"]:
            if st.button("Start Pushup Training", key="start_pushup_button"):
                st.session_state["pushup_active"] = True
                st.session_state["pushup_target_reached"] = False

        # Workout Feed and Always Visible Finish Button
        if st.session_state["pushup_active"]:
            # Run workout feed
            count = workout_loop(0, "pushup", target_reps)

            # Finish Workout Button
            st.button("Finish Workout", key="finish_pushup_button", on_click=end_workout, args=("pushup", count, name))

    # Sit-Up Training
    elif menu == "Train Situps":
        st.header("Sit-Up Training")
        st.info(f"Perform as many sit-ups as you can! Your target is {target_reps} reps.")

        # Start Training Button
        if not st.session_state["situp_active"] and not st.session_state["situp_finish_clicked"]:
            if st.button("Start Situp Training", key="start_situp_button"):
                st.session_state["situp_active"] = True
                st.session_state["situp_target_reached"] = False

        # Workout Feed and Always Visible Finish Button
        if st.session_state["situp_active"]:
            # Run workout feed
            count = workout_loop(0, "situp", target_reps)

            # Finish Workout Button
            st.button("Finish Workout", key="finish_situp_button", on_click=end_workout, args=("situp", count, name))

if __name__ == "__main__":
    main()
