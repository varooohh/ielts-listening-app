import streamlit as st
from google import genai
import time

# -----------------------------------------------------------------------------
# 1. Page Configuration & Level B3 Branding
# -----------------------------------------------------------------------------
st.set_page_config(page_title="IELTS B3 Upper-Intermediate Listening Prep", page_icon="🎧", layout="wide")

st.title("🎧 IELTS Listening Prep: CEFR Level B3")
st.subheader("Theme: Global Environmental & Sustainability Debates") 
st.caption("Targeting Upper-Intermediate Listening Skills: Implied Meanings, Speaker Attitudes, & Academic Arguments")

# Sidebar Navigation
st.sidebar.header("⚙️ Settings & Navigation")
api_key = st.sidebar.text_input("Gemini API Key:", type="password", help="Enter key for AI evaluation & explanations")
app_mode = st.sidebar.radio("Select Learning Mode:", ["B3 Video Practice (20+ Lessons)", "Full IELTS Mock Test Mode"])

# -----------------------------------------------------------------------------
# 2. IELTS Band Score Calculator
# -----------------------------------------------------------------------------
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
# 3. Data Store: 20 B3-Level YouTube Lessons (Academic Discussions, Podcasts, Debates)
# -----------------------------------------------------------------------------
YOUTUBE_PRACTICE_DATA = [
    {
        "id": 1,
        "category": "Academic Discussion",
        "title": "Lesson 1: University Seminar on Renewable Energy Solutions",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What is the speaker's attitude towards current solar tech adoption?",
                "options": ["Highly optimistic", "Cautiously skeptical", "Indifferent", "Strongly critical"],
                "ans": "Cautiously skeptical"
            },
            {
                "type": "short",
                "q": "2. What implied reason prevents small towns from switching to wind energy?",
                "ans": "High initial maintenance cost"
            },
            {
                "type": "mcq",
                "q": "3. Which main argument does Professor Davis emphasize?",
                "options": ["Storage infrastructure is lacking", "Government funding has doubled", "Public demand is declining"],
                "ans": "Storage infrastructure is lacking"
            },
            {
                "type": "short",
                "q": "4. According to the discussion, when will the new grid regulation take effect?",
                "ans": "2028"
            },
            {
                "type": "mcq",
                "q": "5. What does the speaker imply when saying 'the figures speak for themselves'?",
                "options": ["The data is obvious", "The data is fabricated", "The data needs further review"],
                "ans": "The data is obvious"
            }
        ]
    },
    {
        "id": 2,
        "category": "Authentic Podcast",
        "title": "Lesson 2: Psychological Impacts of Social Media Algorithms",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "questions": [
            {
                "type": "mcq",
                "q": "1. What speaker perspective is expressed regarding notification badges?",
                "options": ["They enhance productivity", "They induce cognitive fatigue", "They are harmless tools"],
                "ans": "They induce cognitive fatigue"
            },
            {
                "type": "short",
                "q": "2. What key term does the guest use to describe user retention strategies?",
                "ans": "Dopamine loops"
            },
            {
                "type": "mcq",
                "q": "3. The speaker implies that tech regulations are currently:",
                "options": ["Overly restrictive", "Lagging behind technological development", "Perfectly balanced"],
                "ans": "Lagging behind technological development"
            },
            {
                "type": "short",
                "q": "4. What percentage reduction in screen time led to noticeable anxiety reduction?",
                "ans": "30%"
            },
            {
                "type": "mcq",
                "q": "5. What is the main conclusion of the debate?",
                "options": ["Individual discipline is sufficient", "Systemic platform redesign is necessary", "Social media should be banned"],
                "ans": "Systemic platform redesign is necessary"
            }
        ]
    }
    # Duplicate and extend this structure to cover 20 lessons (Debates, Podcasts, Academic Talks)
]

# -----------------------------------------------------------------------------
# MODE 1: B3 LEVEL PRACTICE MODE
# -----------------------------------------------------------------------------
if app_mode == "B3 Video Practice (20+ Lessons)":
    st.header("📺 Level B3 Authentic Video Practice")
    st.info("Instructions: Watch the B3 authentic audio material (debates, podcasts, academic discussions). Focus on implied meanings, speaker attitudes, and main arguments.")

    lesson_options = [f"[{item['category']}] {item['title']}" for item in YOUTUBE_PRACTICE_DATA]
    selected_lesson = st.selectbox("Select a B3 Listening Lesson:", lesson_options)
    
    lesson_idx = lesson_options.index(selected_lesson)
    current_data = YOUTUBE_PRACTICE_DATA[lesson_idx]

    st.subheader(f"Lesson Category: {current_data['category']}")
    st.video(current_data["url"])

    st.subheader("📝 B3 Proficiency Questions (Inference & Argument Analysis)")
    user_answers = {}
    
    with st.form(key=f"b3_practice_form_{current_data['id']}"):
        for idx, q_data in enumerate(current_data["questions"]):
            st.markdown(f"**{q_data['q']}**")
            if q_data["type"] == "mcq":
                user_answers[idx] = st.radio(f"Select your answer for Q{idx+1}:", q_data["options"], key=f"q_{current_data['id']}_{idx}")
            else:
                user_answers[idx] = st.text_input(f"Your short answer for Q{idx+1}:", key=f"q_{current_data['id']}_{idx}")
            st.write("---")

        submit_b3 = st.form_submit_button("Submit & Evaluate Answers")

    if submit_b3:
        correct_count = 0
        st.subheader("📊 Pedagogical Evaluation & AI Explanation")
        
        for idx, q_data in enumerate(current_data["questions"]):
            user_ans = user_answers[idx].strip().lower()
            correct_ans = q_data["ans"].strip().lower()

            if user_ans == correct_ans:
                st.success(f"Q{idx+1}: Correct! (Your Choice: {user_answers[idx]})")
                correct_count += 1
            else:
                st.error(f"Q{idx+1}: Incorrect. Your Choice: '{user_answers[idx]}' | Expected Answer: '{q_data['ans']}'")
                
                # B3 AI Feedback Generator (Focusing on Implied Meaning & Attitude)
                if api_key:
                    try:
                        client = genai.Client(api_key=api_key)
                        fb_prompt = f"""
                        Target Level: CEFR B3 Upper-Intermediate Listening.
                        Question: {q_data['q']}
                        Student Answer: {user_answers[idx]}
                        Correct Answer: {q_data['ans']}
                        
                        Explain in 2 clear sentences why the correct answer is right based on B3 listening skills (speaker attitude, implied meaning, or contextual inference). Keep explanations encouraging and clear.
                        """
                        res = client.models.generate_content(model='gemini-2.5-flash', contents=fb_prompt)
                        st.info(f"💡 **AI B3 Diagnostic Feedback:** {res.text}")
                    except Exception as e:
                        st.caption("AI Feedback offline. Check Gemini API Key.")
        
        st.metric("Section Score", f"{correct_count} / {len(current_data['questions'])}")

# -----------------------------------------------------------------------------
# MODE 2: FULL IELTS MOCK TEST MODE (With Countdown Timer & Band Score)
# -----------------------------------------------------------------------------
else:
    st.header("⏱️ IELTS Full Listening Test (Test 1–4)")
    st.warning("Official Test Simulation: 30 minutes timed exam covering Sections 1–4.")

    selected_test = st.selectbox("Select Test Package:", ["IELTS 6 - Test 1", "IELTS 6 - Test 2", "IELTS 6 - Test 3", "IELTS 6 - Test 4"])
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("▶️ Start Official Timer (30 Minutes)"):
            st.session_state.start_time = time.time()

    with col2:
        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
            remaining = max(0, 1800 - elapsed)
            mins, secs = divmod(remaining, 60)
            st.metric("⏳ Remaining Time", f"{mins:02d}:{secs:02d}")
            if remaining == 0:
                st.error("⏰ Time Limit Reached!")

    st.write("---")
    st.subheader(f"Exam Audio Stream: {selected_test}")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 

    with st.form(key="official_test_form"):
        st.subheader("IELTS Answer Sheet (Questions 1 to 40)")
        test_answers = {}
        for i in range(1, 41):
            test_answers[i] = st.text_input(f"Question {i}:", key=f"test_q_{i}")
        
        submit_test = st.form_submit_button("Submit Complete Exam")

    if submit_test:
        score = 31 # Sample score calculation
        band = get_ielts_band(score)
        
        st.balloons()
        st.success("🎉 Test Submitted Successfully!")
        res_col1, res_col2 = st.columns(2)
        res_col1.metric("Raw Score", f"{score} / 40")
        res_col2.metric("Estimated IELTS Band Score", f"Band {band}")
