import openai
from model import GeneralModel
import streamlit as st
from functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt
from streamlit_chat import message

html_temp = """
            <div style="background-color:{};padding:1px">
            </div>
            """

languages = {
    'English': 'eng',
    'French': 'fra',
    'Arabic': 'ara',
    'Spanish': 'spa',
}


def app(user_input=None):
    # Creating an object of prediction service
    pred = GeneralModel()

    st.title("Compass AI 🧭")
    st.caption("Transform your academic, professional, and personal "
               "development with individualized AI-powered guidance!")

    # initialize chat if user doesn't have a session
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hi! I am an AI designed to help you with your career directions. Ask me "
                                         "anything!"]
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hello!"]
    if 'chat_displayed' not in st.session_state:
        st.session_state['chat_displayed'] = False

    # Using the streamlit cache
    @st.cache
    def process_prompt(input, cv=False):
        if cv:
            return pred.model_prediction(input=input.strip(), api_key=api_key, cv=True)
        return pred.model_prediction(input=input.strip(), api_key=api_key)

    def process_input(input):
        st.session_state.past.append(input)
        st.session_state.generated.append(process_prompt(input))

    def load_chat(index=None, user_input=None):
        if st.session_state['generated']:
            # print("WE LOADING CHAT!!! \nparsed values: ", user_input, index)
            # if user_input is not None and index is not None:
            #     for i in range(len(st.session_state['past']) - 1, -1, -1):
            #         if i == index:
            #             output = process_prompt(user_input)
            #             st.session_state["generated"].append(output)
            #             message(st.session_state["generated"][i], key=str(i))
            #         else:
            #             message(st.session_state["generated"][i], key=str(i))
            #         message(st.session_state["past"][i], is_user=True, key=str(i) + '_user')
            #
            # else:
            for i in range(len(st.session_state['past']) - 1, -1, -1):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', seed=4)
                message(st.session_state["generated"][i], key=str(i))

    # create sidebar
    with st.sidebar:
        api_key = st.sidebar.text_input("Enter your APIkey here", type="password")

        # PDF section
        st.title(":outbox_tray: PDF to Text")
        st.markdown("""
                    ## Text data extractor: PDF to Text 
                    """)
        textOutput = st.selectbox(
            "How do you want your output text?",
            ('One text file (.txt)', 'Text file per page (ZIP)'))
        # ocr_box = st.checkbox('Enable OCR (scanned document)')

        st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown("""
        # How does it work?
        Simply load your PDF and convert it to single-page or multi-page text to be processed by our AI!
        """)
        st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)

    # create tabs
    # cv_tab = st.tabs("Career Advice")
    # only when API key is entered, render elements within tabs
    if api_key:
        # render cv tab contents
        # with cv_tab:
        st.header("Upload your CV and we'll give our opinions!")
        pdf_file = st.file_uploader("Load your PDF", type="pdf")
        hide = """
                    <style>
                    footer{
                        visibility: hidden;
                            position: relative;
                    }
                    .viewerBadge_container__1QSob{
                        visibility: hidden;
                    }
                    #MainMenu{
                        visibility: hidden;
                    }
                    <style>
                """
        st.markdown(hide, unsafe_allow_html=True)

        if pdf_file:
            path = pdf_file.read()

            # display document
            with st.expander("Display document"):
                displayPDF(path)
            # if ocr_box:
            #     option = st.selectbox('Select the document language', list(languages.keys()))

            # pdf to text
            if textOutput == 'One text file (.txt)':
                # if ocr_box:
                #     # poppler
                #     texts, nb_pages = images_to_txt(path, languages[option])
                #
                #     totalPages = "Pages: " + str(nb_pages) + " in total"
                #     text_data_f = "\n\n".join(texts)
                text_data_f, nb_pages = convert_pdf_to_txt_file(pdf_file)
                print(text_data_f)
                totalPages = "Pages: " + str(nb_pages) + " in total"

                print(text_data_f)
                st.info(totalPages)

                # st.download_button("Download txt file", text_data_f)
                if st.button("Check my CV!"):
                    # with st.spinner(text="In progress"):
                    report_text = process_prompt(text_data_f, cv=True)
                    process_input(report_text)
                    # print(report_text)
                    # st.markdown(report_text)
            else:
                # if ocr_box:
                #     text_data, nb_pages = images_to_txt(path, languages[option])
                #     totalPages = "Pages: " + str(nb_pages) + " in total"
                # else:
                text_data, nb_pages = convert_pdf_to_txt_pages(pdf_file)
                totalPages = "Pages: " + str(nb_pages) + " in total"

                st.info(totalPages)
                zipPath = save_pages(text_data)
                # download text data
                with open(zipPath, "rb") as fp:
                    btn = st.download_button(
                        label="Download ZIP (txt)",
                        data=fp,
                        file_name="pdf_to_txt.zip",
                        mime="application/zip"
                    )

            st.markdown('''
                        <a target="_blank" style="color: black" href="">

                        </a>
                        <style>
                        .btn{
                            display: inline-flex;
                            -moz-box-align: center;
                            align-items: center;
                            -moz-box-pack: center;
                            justify-content: center;
                            font-weight: 400;
                            padding: 0.25rem 0.75rem;
                            border-radius: 0.25rem;
                            margin: 0px;
                            line-height: 1.6;
                            color: rgb(49, 51, 63);
                            background-color: #fff;
                            width: auto;
                            user-select: none;
                            border: 1px solid rgba(49, 51, 63, 0.2);
                            }
                        .btn:hover{
                            color: #00acee;
                            background-color: #fff;
                            border: 1px solid #00acee;
                        }
                        </style>
                        ''',
                        unsafe_allow_html=True
                        )

        user_input = get_text()

        if user_input:
            process_input(user_input)
            st.empty()
        load_chat()


    else:
        st.error("🔑 Please enter an API Key")


def get_text():
    input = st.text_input("You: ", key="input")
    return input
