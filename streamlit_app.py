import streamlit as st

hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-1q8dd3e {visibility: hidden;}  /* Hides the GitHub button */
    .stActionButton {display: none;}  /* Hides the Fork button */
    </style>
    """

st.markdown(hide_menu_style, unsafe_allow_html=True)


# Indonesian rating scale
rating_scale = {
    "0": "Tidak berlaku sama sekali",
    "1": "Kadang berlaku",
    "2": "Sering berlaku",
    "3": "Sangat sering berlaku"
}

# Full list of questions translated to Indonesian
questions = [
    {"text": "Saya merasa sulit untuk rileks", "type": "Stress"},
    {"text": "Saya merasakan mulut saya kering", "type": "Anxiety"},
    {"text": "Saya tidak bisa merasakan perasaan positif sama sekali", "type": "Depression"},
    {"text": "Saya mengalami kesulitan bernapas (misalnya, napas cepat yang berlebihan, sesak napas tanpa aktivitas fisik)", "type": "Anxiety"},
    {"text": "Saya merasa sulit untuk memulai melakukan sesuatu", "type": "Depression"},
    {"text": "Saya cenderung bereaksi berlebihan terhadap situasi", "type": "Stress"},
    {"text": "Saya mengalami gemetaran (misalnya, di tangan)", "type": "Anxiety"},
    {"text": "Saya merasa menggunakan banyak energi gugup", "type": "Stress"},
    {"text": "Saya khawatir tentang situasi di mana saya mungkin panik dan mempermalukan diri sendiri", "type": "Anxiety"},
    {"text": "Saya merasa tidak ada yang dinantikan", "type": "Depression"},
    {"text": "Saya merasa mudah gelisah", "type": "Stress"},
    {"text": "Saya merasa sulit untuk bersantai", "type": "Stress"},
    {"text": "Saya merasa sedih dan muram", "type": "Depression"},
    {"text": "Saya tidak toleran terhadap apa pun yang menghalangi saya melakukan sesuatu", "type": "Stress"},
    {"text": "Saya merasa hampir panik", "type": "Anxiety"},
    {"text": "Saya merasa tidak mampu bersemangat tentang apa pun", "type": "Depression"},
    {"text": "Saya merasa tidak berharga sebagai manusia", "type": "Depression"},
    {"text": "Saya merasa sangat sensitif", "type": "Stress"},
    {"text": "Saya merasakan detak jantung saya tanpa aktivitas fisik (misalnya, jantung berdetak lebih cepat, jantung berdebar-debar)", "type": "Anxiety"},
    {"text": "Saya merasa takut tanpa alasan yang jelas", "type": "Anxiety"},
    {"text": "Saya merasa hidup tidak berarti", "type": "Depression"}
]

# Scoring ranges
scoring_table = {
    "Depression": [(0, 9, "Normal", "green"), (10, 13, "Mild", "yellow"), (14, 20, "Moderate", "orange"), (21, 27, "Severe", "red"), (28, float('inf'), "Extremely Severe", "darkred")],
    "Anxiety": [(0, 7, "Normal", "green"), (8, 9, "Mild", "yellow"), (10, 14, "Moderate", "orange"), (15, 19, "Severe", "red"), (20, float('inf'), "Extremely Severe", "darkred")],
    "Stress": [(0, 14, "Normal", "green"), (15, 18, "Mild", "yellow"), (19, 25, "Moderate", "orange"), (26, 33, "Severe", "red"), (34, float('inf'), "Extremely Severe", "darkred")]
}

# Streamlit app layout
st.title("Kuesioner Penilaian Diri (DASS-21)")
st.write("Berdasarkan form penelitian Lovibond [disini](https://maic.qld.gov.au/wp-content/uploads/2016/07/DASS-21.pdf)")
responses = {"Depression": 0, "Anxiety": 0, "Stress": 0}

# Display each question with radio buttons for rating
with st.form("assessment_form"):
    for i, question in enumerate(questions, 1):
        response = st.radio(f"{i}. {question['text']}", options=list(rating_scale.keys()), format_func=lambda x: rating_scale[x], key=f"question_{i}")
        responses[question["type"]] += int(response)

    # Submit button
    submitted = st.form_submit_button("Submit")

# Calculate and display results if the form is submitted
if submitted:
    st.write("### Hasil Penilaian:")

    final_categories = []

    # Function to determine the level and color based on score
    def determine_level(score, category):
        score *= 2  # Multiply by 2 to calculate the final score
        for min_score, max_score, level, color in scoring_table[category]:
            if min_score <= score <= max_score:
                final_categories.append(level)
                return level, color

    # Show results for each category with appropriate color
    for category, score in responses.items():
        level, color = determine_level(score, category)
        st.markdown(f"**{category}:** {score * 2} ({level})", unsafe_allow_html=True)
        st.markdown(f"<p style='color:{color}; font-weight:bold'>{level}</p>", unsafe_allow_html=True)

    # Determine the final overall category
    final_category = max(set(final_categories), key=final_categories.count)
    final_color = [color for _, _, level, color in scoring_table["Depression"] if level == final_category][0]

    st.write("### Kesimpulan Akhir:")
    st.markdown(f"<p style='color:{final_color}; font-weight:bold'>{final_category}</p>", unsafe_allow_html=True)
