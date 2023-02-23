import openai
import streamlit as st

from model import GeneralModel


def app():
    # Creating an object of prediction service
    pred = GeneralModel()

    api_key = st.sidebar.text_input("APIkey", type="password")

    # Using the streamlit cache

    @st.cache
    def process_prompt(input):
        return pred.model_prediction(input=input.strip(), api_key=api_key)

    if api_key:
        # Setting up the Title
        st.title("Career Advice")

        s_example = "I am a high school student. I really like animals but I'm not very good at science"
        input = st.text_area(
            "Tell us a little bit more about yourself! "
            "Educational background, hobbies, personality traits, anything!",
            value=s_example,
            max_chars=150,
            height=100,
        )

        if st.button("Submit"):
            with st.spinner(text="In progress"):
                report_text = process_prompt(input)
                print(report_text)
                st.markdown(report_text)
    else:
        st.error("🔑 Please enter API Key")
