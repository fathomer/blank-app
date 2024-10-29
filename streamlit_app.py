import streamlit as st
import plotly.graph_objects as go
import base64

# Set page config
st.set_page_config(page_title="Answer Accuracy Speedometer", layout="wide")

# Initialize session state variables if they don't exist
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'target_accuracy' not in st.session_state:
    st.session_state.target_accuracy = 80

# Get current theme
def get_theme_colors():
    # Check if dark theme is enabled
    is_dark_theme = st.config.get_option('theme.base') == 'dark'
    
    print(f"{is_dark_theme=}")
    
    if is_dark_theme:
        
        return {
            'background': 'rgba(0,0,0,0)',
            'text': '#FFFFFF',        # White text
            'grid': '#333333',
            'metric_color': '#FFFFFF',
            'metric_label': 'rgba(255, 255, 255, 0.6)'
        }

    return {
        'background': 'rgba(0,0,0,0)',
        'text': '#000000',        # Black text
        'grid': '#dddddd',
        'metric_color': '#000000',
        'metric_label': 'rgba(0, 0, 0, 0.6)'
    }

# Create the speedometer chart
def create_speedometer(percentage, target):
    
    theme = get_theme_colors()
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': "Accuracy", 
            'font': {'size': 24, 'color': theme['text']}
        },
        number = {
            'font': {'color': theme['text']},
            'suffix': "%"
        },
        gauge = {
            'axis': {
                'range': [0, 100], 
                'tickwidth': 1, 
                'tickcolor': theme['text'],
                'tickfont': {'color': theme['text']}
            },
            'bar': {'color': "#1f77b4"},
            'bgcolor': theme['background'],
            'borderwidth': 2,
            'bordercolor': theme['grid'],
            'steps': [
                {'range': [0, 33], 'color': 'rgba(255, 0, 0, 0.3)'},
                {'range': [33, 66], 'color': 'rgba(255, 255, 0, 0.3)'},
                {'range': [66, 100], 'color': 'rgba(0, 255, 0, 0.3)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor = theme['background'],
        plot_bgcolor = theme['background'],
        height = 400,
        margin = dict(l=10, r=10, t=50, b=10),
        font = {'color': theme['text']}
    )
    return fig

# Custom CSS for theme-aware styling
theme = get_theme_colors()

# Add title and description
st.title("Answer Accuracy Tracker")
st.write("Click the button to record your answer as correct or incorrect.")

# Add target accuracy setting
target_accuracy = st.slider("Set Target Accuracy (%)", 0, 100, st.session_state.target_accuracy, 5)
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
st.plotly_chart(create_speedometer(percentage, target_accuracy), use_container_width=True)

# Display stats in columns with theme-aware styling
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
        st.success(f"🎉 Congratulations! You're meeting your target accuracy of {target_accuracy}%")
    else:
        st.warning(f"Keep going! You need {(target_accuracy - percentage):.1f}% more to reach your target")

# Add explanation section with theme-aware markdown
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
    