import streamlit as st
from google import genai
import time

# -----------------------------------------------------------------------------
# 1. Page Configuration & Setup (Full English UI)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="IELTS Listening Prep Master", page_icon="🎧", layout="wide")

st.title("🎧 IELTS Listening Preparation App")
st.caption("Intermediate Level (CEFR B2/B3) • Comprehensive Practice & Mock Tests")

# Sidebar - Settings & Mode Selection
st.sidebar.header("⚙️ Settings & Navigation")
api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Enter key for AI evaluation")
app_mode = st.sidebar.radio("Select Mode:", ["Practice Mode (20+ Videos)", "IELTS Mock Test Mode"])

# -----------------------------------------------------------------------------
# 2. Data Store: 20 Video Lessons & Question Datasets
# -----------------------------------------------------------------------------
# sample dataset structure (Expand this to 20+ videos from your target YouTube Channel)
YOUTUBE_PRACTICE_DATA = [
    {
        "id": 1,
        "title": "Practice 1: Daily Routine & University Accommodation",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # Replace with actual YouTube video URL
        "questions": [
            {"type": "mcq", "q": "1. What type of room does the student want to book?", "options": ["Single Room", "Shared Room", "Studio Apartment"], "ans": "Single Room"},
            {"type": "mcq", "q": "2. When is the check-in date?", "options": ["1st September", "15th September", "1st October"], "ans": "15th September"},
            {"type": "short", "q": "3. What is the maximum weekly budget mentioned? (Write number only)", "ans": "150"},
            {"type": "mcq", "q": "4. Which facility is included in the price?", "options": ["Free Wi-Fi", "Laundry", "Breakfast"], "ans": "Free Wi-Fi"},
            {"type": "short", "q": "5. What contact detail did the speaker request?", "ans": "Phone number"}
        ]
    },
    {
        "id": 2,
        "title": "Practice 2: Campus Library Tour & Rules",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "questions": [
            {"type": "mcq", "q": "1. Where is the main quiet zone located?", "options": ["1st Floor", "2nd Floor", "Basement"], "ans": "2nd Floor"},
            {"type": "short", "q": "2. How many books can undergraduate students borrow?", "ans": "10"},
            {"type": "mcq", "q": "3. What happens if a student returns a book late?", "options": ["Fine charged", "Library card suspended", "Warning email"], "ans": "Fine charged"},
            {"type": "mcq", "q": "4. The library closes early on which day?", "options": ["Friday", "Saturday", "Sunday"], "ans": "Sunday"},
            {"type": "short", "q": "5. What item is NOT allowed inside the computer lab?", "ans": "Drinks"}
        ]
    }
    # Add items 3 to 20 following the same JSON structure
]

# Function to calculate IELTS Band Score
def get_ielts_band(score_out_of_40):
    if score_out_of_40 >= 39: return 9.0
    elif score_out_of_40 >= 37: return 8.5
    elif score_out_of_40 >= 35: return 8.0
    elif score_out_of_40 >= 32: return 7.5
    elif score_out_of_40 >= 30: return 7.0
    elif score_out_of_40 >= 26: return 6.5
    elif score_out_of_40 >= 23: return 6.0
    elif score_out_of_40 >= 18: return 5.5
    elif score_out_of_40 >= 16: return 5.0
    else: return 4.5

# -----------------------------------------------------------------------------
# MODE 1: PRACTICE MODE (20+ YouTube Videos)
# -----------------------------------------------------------------------------
if app_mode == "Practice Mode (20+ Videos)":
    st.header("📺 Video Practice Section")
    st.info("Instructions: Watch the video carefully, answer all 5 questions below, and submit for instant scoring and AI explanation.")

    video_titles = [f"Video {item['id']}: {item['title']}" for item in YOUTUBE_PRACTICE_DATA]
    selected_video_title = st.selectbox("Select a Practice Lesson:", video_titles)
    
    # Selected Video Index
    video_idx = video_titles.index(selected_video_title)
    current_data = YOUTUBE_PRACTICE_DATA[video_idx]

    # Embed YouTube Video
    st.subheader(current_data["title"])
    st.video(current_data["url"])

    # Question Form
    st.subheader("📝 Practice Questions (Intermediate Level)")
    user_answers = {}
    
    with st.form(key=f"practice_form_{current_data['id']}"):
        for idx, q_data in enumerate(current_data["questions"]):
            st.markdown(f"**{q_data['q']}**")
            if q_data["type"] == "mcq":
                user_answers[idx] = st.radio(f"Select answer for Q{idx+1}:", q_data["options"], key=f"q_{current_data['id']}_{idx}")
            else:
                user_answers[idx] = st.text_input(f"Your answer for Q{idx+1}:", key=f"q_{current_data['id']}_{idx}")
            st.write("---")

        submit_practice = st.form_submit_button("Submit Answers & Get AI Evaluation")

    if submit_practice:
        correct_count = 0
        st.subheader("📊 Evaluation & Detailed Feedback")
        
        for idx, q_data in enumerate(current_data["questions"]):
            user_ans = user_answers[idx].strip().lower()
            correct_ans = q_data["ans"].strip().lower()

            if user_ans == correct_ans:
                st.success(f"Q{idx+1}: Correct! (Your Answer: {user_answers[idx]})")
                correct_count += 1
            else:
                st.error(f"Q{idx+1}: Incorrect. Your Answer: '{user_answers[idx]}' | Correct Answer: '{q_data['ans']}'")
                
                # AI Feedback Evaluation for wrong/short answers
                if api_key:
                    try:
                        client = genai.Client(api_key=api_key)
                        fb_prompt = f"""
                        Context: IELTS Listening Intermediate Level.
                        Question: {q_data['q']}
                        Student Answer: {user_answers[idx]}
                        Correct Answer: {q_data['ans']}
                        Provide a brief 2-sentence grammatical/contextual explanation in clear English on why the correct answer is right.
                        """
                        res = client.models.generate_content(model='gemini-2.5-flash', contents=fb_prompt)
                        st.info(f"💡 **AI Explanation:** {res.text}")
                    except Exception as e:
                        st.caption("AI explanation unavailable. Check API Key.")
        
        st.metric("Total Score", f"{correct_count} / {len(current_data['questions'])}")

# -----------------------------------------------------------------------------
# MODE 2: FULL IELTS MOCK TEST MODE (Tests 1-4 with Timer & Band Score)
# -----------------------------------------------------------------------------
else:
    st.header("⏱️ IELTS Full Listening Test (Test 1–4)")
    st.warning("Official Test Conditions: You will have 30 minutes to complete the test. Track your remaining time using the timer.")

    selected_test = st.selectbox("Select Test Package:", ["IELTS 6 - Test 1", "IELTS 6 - Test 2", "IELTS 6 - Test 3", "IELTS 6 - Test 4"])
    
    # Session State for Test Timer
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("▶️ Start Official Timer (30 Minutes)"):
            st.session_state.start_time = time.time()

    with col2:
        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
            remaining = max(0, 1800 - elapsed) # 30 minutes = 1800 seconds
            mins, secs = divmod(remaining, 60)
            st.metric("⏳ Time Remaining", f"{mins:02d}:{secs:02d}")
            if remaining == 0:
                st.error("⏰ Time is UP! Please submit your test now.")

    st.write("---")
    st.subheader(f"Audio Track: {selected_test}")
    # Placeholder for official test audio file/video
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 

    with st.form(key="mock_test_form"):
        st.subheader("Answer Sheet (Section 1 to 4)")
        test_answers = {}
        for i in range(1, 41): # 40 Questions standard IELTS format
            test_answers[i] = st.text_input(f"Question {i}:", key=f"test_q_{i}")
        
        submit_test = st.form_submit_button("Submit Full Test")

    if submit_test:
        # Dummy evaluation logic (simulating 40 questions evaluation)
        # In actual deployment, compare test_answers with official key for Test 1-4
        score = 28 # Example correct answers
        band = get_ielts_band(score)
        
        st.balloons()
        st.success("🎉 Test Submitted Successfully!")
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Raw Score", f"{score} / 40")
        col_res2.metric("Official Estimated IELTS Band", f"Band {band}")