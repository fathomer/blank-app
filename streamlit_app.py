import streamlit as st
import plotly.graph_objects as go

# Set page config
st.set_page_config(page_title="Answer Accuracy Speedometer", layout="wide")

# Initialize session state variables if they don't exist
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0

# Add title and description
st.title("Answer Accuracy Tracker")
st.write("Click the button to record your answer as correct or incorrect.")

# Create the speedometer chart
def create_speedometer(percentage):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Accuracy", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 33], 'color': 'red'},
                {'range': [33, 66], 'color': 'yellow'},
                {'range': [66, 100], 'color': 'green'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': percentage}}))
    
    fig.update_layout(
        paper_bgcolor = "white",
        height=400
    )
    return fig

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
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Create two buttons side by side
    left_col, right_col = st.columns(2)
    with left_col:
        if st.button("✅ Correct", use_container_width=True):
            record_answer(True)
    with right_col:
        if st.button("❌ Incorrect", use_container_width=True):
            record_answer(False)

# Calculate percentage
percentage = (st.session_state.correct_answers / st.session_state.total_questions * 100) if st.session_state.total_questions > 0 else 0

# Display the speedometer
st.plotly_chart(create_speedometer(percentage), use_container_width=True)

# Display stats in columns
stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric("Correct Answers", st.session_state.correct_answers)
with stat_col2:
    st.metric("Total Questions", st.session_state.total_questions)
with stat_col3:
    st.metric("Accuracy", f"{percentage:.1f}%")

# Add explanation section
st.markdown("### Performance Zones")
zone_col1, zone_col2, zone_col3 = st.columns(3)
with zone_col1:
    st.markdown("🔴 0-33%: Needs Improvement")
with zone_col2:
    st.markdown("🟡 34-66%: Good")
with zone_col3:
    st.markdown("🟢 67-100%: Excellent")

# Add reset button
if st.button("Reset Stats"):
    reset_stats()