import math
import streamlit as st
from scoringTable import pushUpTable, situpsTable, runTable, secondsTable

# Get the person's age group for IPPT
def get_age_group(person):
    ageGroup = 1

    if person.age < 22:
        pass
    elif 22 <= person.age <= 24:
        ageGroup = 2
    elif  25 <= person.age <= 27:
        ageGroup = 3
    elif 28 <= person.age <= 30:
        ageGroup = 4
    elif 31 <= person.age <= 33:
        ageGroup = 5
    elif 34 <= person.age <= 36:
        ageGroup = 6
    elif 37 <= person.age <= 39:
        ageGroup = 7
    elif 40 <= person.age <= 42:
        ageGroup = 8
    elif 43 <= person.age <= 45:
        ageGroup = 9
    elif 46 <= person.age <= 48:
        ageGroup = 10
    elif 49 <= person.age <= 51:
        ageGroup = 11
    elif 52 <= person.age <= 54:
        ageGroup = 12
    elif 55 <= person.age <= 57:
        ageGroup = 13
    else:
        ageGroup = 14

    return ageGroup

# Need to check through the Scoring Table
def calculate_situps(ag, number):
    score = 0
    scoreGroup = situpsTable[ag - 1]

    if number != 0:
        score = scoreGroup[number - 1]

    return score

# Need to check through the Scoring Table
def calculate_pushups(ag, number):
    score = 0
    scoreGroup = pushUpTable[ag - 1]

    if number != 0:
        score = scoreGroup[number - 1]

    return score

# The Run Time Table scoring needs to be updated (Outdated Table Scoring)
def calculate_run(ag, runTime):
    seconds = math.floor(((runTime[0] * 60) + runTime[1]) / 10) * 10
    scoreIndex = secondsTable.index(seconds)
    scoreGroup = runTable[ag - 1]

    return scoreGroup[scoreIndex]

def calculate_points(person, pushups = 0, situps = 0, run = [18, 0]):
    ageGroup = get_age_group(person)

    totalPushupPoints = calculate_pushups(ageGroup, pushups)
    totalSitupPoints = calculate_situps(ageGroup, situps)
    totalRunPoints = calculate_run(ageGroup, run)

    return totalPushupPoints + totalSitupPoints + totalRunPoints

# Determine the incentive based on points
def getIncentive(points):
    if 51 <= points <= 60:
        return ["Pass with no incentive", 0, 1]
    elif 61 <= points <= 74:
        return ["Pass with incentive", 200, 2]
    elif 75 <= points <= 84:
        return ["Silver", 300, 3]
    elif points >= 85:
        return ["Gold", 500, 4]
    else:
        return ["Fail", 0, 0]

def display_ippt_calculator(person):
    """
    Displays the IPPT Calculator in a Streamlit app.
    """
    st.header("IPPT Points Calculator")

    pushups = st.slider("Number of Push Ups:", min_value=0, max_value=60, step=1)
    situps = st.slider("Number of Sit Ups:", min_value=0, max_value=60, step=1)

    minutes, seconds = st.columns(2)
    with minutes:
        minutes = st.number_input("Minutes:", min_value=8, max_value=18, step=1)

    with seconds:
        if minutes == 8:
            seconds = st.number_input("Seconds:", min_value=30, max_value=59, step=1)
        elif minutes == 18:
            seconds = st.number_input("Seconds:", min_value=0, max_value=29, step=1)
        else:
            seconds = st.number_input("Seconds:", min_value=0, max_value=59, step=1)
    runTime = [minutes, seconds]

    incentive = getIncentive(calculate_points(person, pushups, situps, runTime))
    if incentive[2] == 0:
        st.subheader("Fail")
    elif incentive[2] == 1:
        st.subheader("Pass with no incentive")
    elif incentive[2] == 2:
        st.subheader("Pass with incentive: $200")
    elif incentive[2] == 3:
        st.subheader("Silver: $300")
    elif incentive[2] == 4:
        st.subheader("Gold: $500")
    else:
        pass