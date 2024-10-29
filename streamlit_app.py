import streamlit as st
import plotly.graph_objects as go
import base64

# Set page config
st.set_page_config(page_title="Answer Accuracy Speedometer")

# Initialize session state variables if they don't exist
if "correct_answers" not in st.session_state:
    st.session_state.correct_answers = 0
if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0
if "target_accuracy" not in st.session_state:
    st.session_state.target_accuracy = 80

hide_streamlit_style = """
<style>
.st-emotion-cache-1d560d5 { width: 100%; padding: 2.1rem 1rem 1rem; min-width: auto; max-width: initial; }
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("""
<style>
    * {
       overflow-anchor: none !important;
       }
</style>""", unsafe_allow_html=True)

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
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, target // 2], "color": "#FF5B61"},
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
    fig.update_layout(
        height = 300,
        margin = dict(l=10, r=10, t=50, b=10)
    )
    return fig


# Add title and description
st.title("Answer Accuracy Tracker")
st.write("Click the button to record your answer as correct or incorrect.")

# Add target accuracy setting
target_accuracy = st.slider(
    "Set Target Accuracy (%)", 0, 100, st.session_state.target_accuracy, 5
)
st.session_state.target_accuracy = target_accuracy

# Function to handle answer submission
def record_answer(is_correct):
    st.session_state.total_questions += 1
    if is_correct:
        st.session_state.correct_answers += 1


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
with left_col:
    if st.button("✅ Correct", use_container_width=True):
        record_answer(True)
with right_col:
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
            f"🎉 Congratulations! You're meeting your target accuracy of {target_accuracy}%"
        )
    else:
        st.warning(
            f"Keep going! You need {(target_accuracy - percentage):.1f}% more to reach your target"
        )

# Add explanation section with theme-aware markdown
st.markdown("### Performance Zones")
zone_col1, zone_col2, zone_col3 = st.columns(3)
with zone_col1:
    st.markdown(f"🔴 0-{st.session_state.target_accuracy // 2}%: Needs Improvement")
with zone_col2:
    st.markdown(
        f"🟡 {st.session_state.target_accuracy // 2}-{st.session_state.target_accuracy}%: Good"
    )
with zone_col3:
    st.markdown(f"🟢 {st.session_state.target_accuracy}-100%: Excellent")

# Add reset button
if st.button("Reset Stats"):
    reset_stats()
