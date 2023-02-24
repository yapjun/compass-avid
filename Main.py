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

    with st.sidebar:
        api_key = st.sidebar.text_input("Enter your APIkey here", type="password")
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
        Simply load your PDF and convert it to single-page or multi-page text to be processed by our AI!.
        """)
        st.markdown(html_temp.format("rgba(55, 53, 47, 0.16)"), unsafe_allow_html=True)

    # drop box for PDF
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
                texts, nbPages = images_to_txt(path, languages[option])
                totalPages = "Pages: " + str(nbPages) + " in total"
                text_data_f = "\n\n".join(texts)
            else:
                text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
                totalPages = "Pages: " + str(nbPages) + " in total"

            st.info(totalPages)
            st.download_button("Download txt file", text_data_f)

        else:
            if ocr_box:
                text_data, nbPages = images_to_txt(path, languages[option])
                totalPages = "Pages: " + str(nbPages) + " in total"
            else:
                text_data, nbPages = convert_pdf_to_txt_pages(pdf_file)
                totalPages = "Pages: " + str(nbPages) + " in total"

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
