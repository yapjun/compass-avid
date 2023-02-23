import streamlit as st
from model import GeneralModel


def app():

    # Creating an object of prediction service
    pred = GeneralModel()

    api_key = st.sidebar.text_input("APIkey", type="password")
    # Using the streamlit cache

    @st.cache
    def process_prompt(input):
        # inp = str_conc(input)
        # print(inp)
        return pred.model_prediction(input=input.strip() , api_key=api_key)

    # def str_conc(input):
    #     str = ""
    #     for each in input:
    #         str = str + "." + each
    #     return str

    if api_key:

        # Setting up the Title
        st.title("Career Advice")

        # st.write("---")

        s_example = "I am a student, I am decent in maths and I like drawing"
        input = st.text_area(
            "Use the example below or input your own text in English",
            value=s_example,
            max_chars=150,
            height=100,
        )

        if st.button("Submit"):
            with st.spinner(text="In progress"):
                #inputl = pred.append_inputlist(input)
                report_text = process_prompt(input)
                st.markdown(report_text)
    else:
        st.error("🔑 Please enter API Key")
