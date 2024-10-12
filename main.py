import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

# Function to inject custom CSS for font styling
def set_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        /* Apply font to all elements */
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        /* Title style */
        h1, h2, h3 {
            font-family: 'Poppins', sans-serif;
        }

        /* Specific styles for Streamlit components */
        .stTextInput input, .stButton, .stText, .stMarkdown {
            font-family: 'Poppins', sans-serif;
        }

        /* Additional customizations for input fields */
        .stTextInput input {
            font-family: 'Poppins', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def create_streamlit_app(llm, portfolio, clean_text):
    st.markdown("<h1 style='font-family: Poppins;'>📧 Business Mail Generator</h1>", unsafe_allow_html=True)
    url_input = st.text_input("Enter a URL:", value="Paste Job description link here")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    set_custom_css()  # Call the function to set custom CSS
    create_streamlit_app(chain, portfolio, clean_text)
