import streamlit as st
import plotly.graph_objects as go
import base64

# Set page config
st.set_page_config(page_title="IAIO Leadership Alignment Tracker")

# Initialize session state variables if they don't exist
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "target_accuracy" not in st.session_state:
    st.session_state.target_accuracy = 80

# Create the speedometer chart
def create_speedometer(percentage, target):

    fig = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=percentage,
            mode="gauge+number+delta",
            delta={
                "suffix": "%",
                "reference": target,
                "increasing": {"color": "RebeccaPurple"},
            },
            title={"text": "Accuracy"},
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [None, 100]},
                "steps": [
                    {"range": [-1, target // 2], "color": "#FF5B61"},
                    {"range": [target // 2, target], "color": "lightgoldenrodyellow"},
                    {"range": [target, 100], "color": "lightgreen"},
                ],
                "bar": {"color": "royalblue"},
                "threshold": {
                    "line": {"color": "green", "width": 4},
                    "thickness": 0.75,
                    "value": target,
                },
            },
        )
    )

 # Add text annotations on the left and right
    fig.add_annotation(
        x=0.05,  # Position on the left
        y=0.5,   # Vertical center
        text="Towards<br>happy hour :D",
        showarrow=False,
        font=dict(size=15),
        xanchor="left",
        yanchor="middle",
        align="center"
    )

    fig.add_annotation(
        x=0.955,  # Position on the right
        y=0.5,   # Vertical center
        text="No happy hour<br>for us :(",
        showarrow=False,
        font=dict(size=15),
        xanchor="right",
        yanchor="middle",
        align="center"
    )

    fig.update_layout(
        height = 300,
        margin = dict(l=10, r=10, t=50, b=10)
    )
    return fig


# Add title and description
st.title("IAIO Leadership Alignment Tracker")
st.write("Do you think the leadership is aligned with the employees in the team? Lets see.")

# Add target accuracy setting
target_accuracy = st.slider(
    "Set Target for Leadeship (%). Accuracy less than this means the team wins, and gets their happy hours. Accuracy more than this means we do a rematch.", 0, 100, st.session_state.target_accuracy, 5
)
st.session_state.target_accuracy = target_accuracy

# Function to handle answer submission
def record_answer(is_correct):
    st.session_state.total_questions += 1
    if is_correct:
        st.session_state.correct_answers += 1
    st.rerun()


# Function to reset stats
def reset_stats():
    st.session_state.correct_answers = 0
    st.session_state.total_questions = 0
    st.rerun()


# Create columns for the buttons

# Calculate percentage
percentage = (
    (st.session_state.correct_answers / st.session_state.total_questions * 100)
    if st.session_state.total_questions > 0
    else 0
)

# Display the speedometer
st.plotly_chart(
    create_speedometer(percentage, target_accuracy),
    use_container_width=True,
    theme="streamlit",
)

left_col, right_col = st.columns(2)
# Create two buttons side by side
with right_col:
    if st.button("✅ Correct", use_container_width=True):
        record_answer(True)
with left_col:
    if st.button("❌ Incorrect", use_container_width=True):
        record_answer(False)

# Display stats in columns
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
with stat_col1:
    st.metric("Correct Answers", st.session_state.correct_answers)
with stat_col2:
    st.metric("Total Questions", st.session_state.total_questions)
with stat_col3:
    st.metric("Current Accuracy", f"{percentage:.1f}%")
with stat_col4:
    st.metric("Target Accuracy", f"{target_accuracy}%")

# Add goal status message
if st.session_state.total_questions > 0:
    if percentage >= target_accuracy:
        st.success(
            f"🎉 Congratulations on achieving {target_accuracy}%! You're making sure no one in the team gets happy (hours)"
        )
    else:
        st.warning(
            f"Keep going! You need {(target_accuracy - percentage):.1f}% more to stop the team from getting happy hours."
        )

# Add explanation section with theme-aware markdown
st.markdown("### Happy Hour Zones")
zone_col1, zone_col2, zone_col3 = st.columns(3)
with zone_col1:
    st.markdown(f"😀 0-{st.session_state.target_accuracy // 2}%: Happy hours everyday")
with zone_col2:
    st.markdown(
        f"😊 {st.session_state.target_accuracy // 2}-{st.session_state.target_accuracy}%: Biweekly happy hours"
    )
with zone_col3:
    st.markdown(f"😔 {st.session_state.target_accuracy}-100%: We are not having happy hours")

# Add reset button
if st.button("Reset Stats"):
    reset_stats()
