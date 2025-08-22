import streamlit as st
import pandas as pd
import os

# ---- Setup ----
IMAGE_FOLDER = "./ds"  

# Get list of image file paths
images = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER)
          if f.lower().endswith(".png")]


if "page" not in st.session_state:
    st.session_state.page = "instructions"
if "current" not in st.session_state:
    st.session_state.current = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# ---- Instructions ----
if st.session_state.page == "instructions":
    st.title("Welcome to the Survey")
    st.write("You will see a series of images.  For each image, decide whether it is harmful or non-harmful.")
    st.write("**Before making a decision, carefully consider how the text in the image relates to the content of the image.**")
    st.write("**An image is harmful if it is damaging, threatening, provocative, sexually suggestive, discriminatory, violent, offensive, fraudulent, or is otherwise inappropriate for general audiences.**")
    st.write("If the image is harmful, click 'Yes'.")
    st.write("If the image is non-harmful, click 'No'.")
    st.write("If you are uncertain, click 'Unsure'. For example, if the image is confusing or you cannot understand its intentions.")
    st.write("MAKE SURE YOU DOWNLOAD YOUR .CSV RESULTS AT THE END!")
    
    if st.button("Start Survey", key="start_survey"):
        st.session_state.page = "survey"
        st.rerun()

# ---- Survey ----
elif st.session_state.page == "survey":
    col1, col2, col3 = st.columns([1,2,1])
    idx = st.session_state.current
    st.write(f"Question {idx+1} of {len(images)}")
    st.write(f"**An image is harmful if it is damaging, threatening, provocative, sexually suggestive, discriminatory, violent, offensive, or is otherwise inappropriate for general audiences.**")
    #st.image(images[idx], use_container_width=True)
    with col2:
        st.image(images[idx], width=600)

    col1, col2, col3 = st.columns(3)
    if col1.button("Yes: Harmful"):
        st.session_state.answers.append([idx+1, os.path.basename(images[idx]), "Yes"])
        st.session_state.current += 1
        if st.session_state.current >= len(images):
            st.session_state.page = "done"
        st.rerun()

    if col2.button("No: Not harmful"):
        st.session_state.answers.append([idx+1, os.path.basename(images[idx]), "No"])
        st.session_state.current += 1
        if st.session_state.current >= len(images):
            st.session_state.page = "done"
        st.rerun()
    
    if col3.button("Unsure"):
        st.session_state.answers.append([idx+1, os.path.basename(images[idx]), "Unsure"])
        st.session_state.current += 1
        if st.session_state.current >= len(images):
            st.session_state.page = "done"
        st.rerun()  

# ---- Done ----
elif st.session_state.page == "done":
    st.title("Thank you for completing the survey!")
    df = pd.DataFrame(st.session_state.answers, columns=["Question", "Image", "Answer"])
    st.dataframe(df)
    st.download_button(
        "Download Results as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="survey_results.csv",
        mime="text/csv"
    )