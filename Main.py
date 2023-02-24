import openai
from model import GeneralModel
import streamlit as st
from functions import convert_pdf_to_txt_pages, convert_pdf_to_txt_file, save_pages, displayPDF, images_to_txt


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

def app():
    # Creating an object of prediction service
    pred = GeneralModel()


    st.title("Compass AI 🧭")
    st.caption("Transform your academic, professional, and personal "
                 "development with individualized AI-powered guidance!")
    # Using the streamlit cache
    @st.cache
    def process_prompt(input, cv=False, career=False, edu=False, pd=False):
        if cv:
            return pred.model_prediction(input=input.strip(), api_key=api_key, cv=True)
        elif career:
            return pred.model_prediction(input=input.strip(), api_key=api_key, career=True)
        elif edu:
            return pred.model_prediction(input=input.strip(), api_key=api_key, edu=True)
        elif pd:
            return pred.model_prediction(input=input.strip(), api_key=api_key, pd=True)

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
        ocr_box = st.checkbox('Enable OCR (scanned document)')

        st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)
        st.markdown("""
        # How does it work?
        Simply load your PDF and convert it to single-page or multi-page text to be processed by our AI!
        """)
        st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)


    # create tabs
    cv_tab, career_tab, education_tab, pd_tab = st.tabs(["CV Checker", "Career Advice", "Educational Advice", "Personal Development Advice"])
    # only when API key is entered, render elements within tabs
    if api_key:
        # render cv tab contents
        with cv_tab:
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
                if ocr_box:
                    option = st.selectbox('Select the document language', list(languages.keys()))

                # pdf to text
                if textOutput == 'One text file (.txt)':
                    if ocr_box:
                        # poppler
                        texts, nb_pages = images_to_txt(path, languages[option])

                        totalPages = "Pages: " + str(nb_pages) + " in total"
                        text_data_f = "\n\n".join(texts)
                    else:
                        text_data_f, nb_pages = convert_pdf_to_txt_file(pdf_file)
                        print(text_data_f)
                        totalPages = "Pages: " + str(nb_pages) + " in total"

                    print(text_data_f)
                    st.info(totalPages)
                    st.download_button("Download txt file", text_data_f)
                    if st.button("Check my CV"):
                        # with st.spinner(text="In progress"):
                        report_text = process_prompt(text_data_f, cv=True)
                        print(report_text)
                        st.markdown(report_text)

                else:
                    if ocr_box:
                        text_data, nb_pages = images_to_txt(path, languages[option])
                        totalPages = "Pages: " + str(nb_pages) + " in total"
                    else:
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

        # render advice tab contents
        with career_tab:
            # set up title
            st.title("Career Advice")

            # example input
            s_example = "I am a recent graduate. I am looking for ways to increase my chances " \
                        "of acquiring an internship. What can I do?"
            input = st.text_area(
                "Tell us a little bit more about yourself! "
                "Educational background, hobbies, personality traits, anything!",
                value=s_example,
                max_chars=150,
                height=100,
            )

            if st.button("Submit", key="career"):
                # with st.spinner(text="In progress"):
                report_text = process_prompt(input, career=True)
                print(report_text)
                st.markdown(report_text)

        with education_tab:
            # set up title
            st.title("Education Advice")

            # example input
            s_example = "I am in my final year of high school and I don't know where to go for" \
                        " university. I am also a big animal lover. What are my options?"
            input = st.text_area(
                "Tell us a little bit more about yourself! "
                "Educational background, hobbies, personality traits, anything!",
                value=s_example,
                max_chars=150,
                height=100,
            )

            if st.button("Submit", key="edu"):
                # with st.spinner(text="In progress"):
                report_text = process_prompt(input, edu=True)
                print(report_text)
                st.markdown(report_text)

        with pd_tab:
            # set up title
            st.title("Personal Development Advice")

            # example input
            s_example = "How can I increase my work productivity?"
            input = st.text_area(
                "Tell us a little bit more about yourself! "
                "What's troubling you?",
                value=s_example,
                max_chars=150,
                height=100,
            )

            if st.button("Submit", key="pd"):
                # with st.spinner(text="In progress"):
                report_text = process_prompt(input, pd=True)
                print(report_text)
                st.markdown(report_text)

    else:
        st.error("🔑 Please enter an API Key")







