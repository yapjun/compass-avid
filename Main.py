import openai
import streamlit as st

from model import GeneralModel


def app():
    # Creating an object of prediction service
    pred = GeneralModel()

    api_key = st.sidebar.text_input("Enter your APIkey here", type="password")

    # Using the streamlit cache
    @st.cache_data
    def process_prompt(input):
        return pred.model_prediction(input=input.strip(), api_key=api_key)

    # only when API key is entered
    if api_key:
        # set up title
        st.title("Career Advice")

        # example input
        s_example = "I am a high school student. I love writing and animals"
        input = st.text_area(
            "Tell us a little bit more about yourself! "
            "Educational background, hobbies, personality traits, anything!",
            value=s_example,
            max_chars=150,
            height=100,
        )

        if st.button("Submit"):
            # with st.spinner(text="In progress"):
            report_text = process_prompt(input)
            print(report_text)
            st.markdown(report_text)
    else:
        st.error("🔑 Please enter API Key")
