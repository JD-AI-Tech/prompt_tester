import os
import streamlit as st
from arch_assist_service import Architect_service, does_database_exist
from dotenv import load_dotenv
from langchain.vectorstores import FAISS

st.set_page_config(page_title='User Prompt')
if 'user_prompt' not in st.session_state:
    st.session_state['user_prompt'] = ''


os.environ['OPENAI_API_KEY'] = st.secrets['apikey']
#load_dotenv()

aa_service = Architect_service()
data_directory = 'data'

# set up needed folders
aa_service.setup_folders()
user_entered_prompt = ''

st.subheader("Test out the impact of different prompts")


with st.sidebar:
     st.markdown('''
        Prompt Examples:\n
        Do not guess if you do not know the answer. Just state that the answer is not part of the available content.
 
        Answer the following questions as best you can, but speaking as a caring 
            virtual medical professional. Always recommend that the user should follow up with their family physician.
            
        Answer the following questions speaking as a helpful virtual training professional. If you don't know the 
            answer, do not make up the answer and ask the user if there is anything else that you can help with.      
        
        Answer the following questions as best you can, but speaking as a very funny comedian. If you do not know the
         answer, tell a knock-knock joke.
     ''')


if not does_database_exist():
    uploaded_files = st.file_uploader("Please upload file", type='pdf', accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            with open(os.path.join(data_directory, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
                print(f"finished writing {uploaded_file} to {data_directory}")

        with st.spinner('Please wait, while I read and learn the document ..'):
            aa_service.load_files_to_db()

if does_database_exist():
    new_prompt = st.text_area(
        label="Copy and paste the example prompts on the sidebar, then come up with your own prompt",
        placeholder="Step 1: Please enter a prompt that will be used to guide bot responses")
    if st.button("Submit new prompt"):
        if new_prompt:
            user_entered_prompt = new_prompt
            st.session_state['user_prompt'] = new_prompt
        else:
            st.warning("Please enter prompt above")

    user_query = st.text_area(label='prompt',  label_visibility='hidden',
                              placeholder='Step 2: Type in your question below and then click the Submit button.')
    if st.button("Submit your question"):
        if user_query:
            # if user_entered_prompt:
            if st.session_state.user_prompt:
                with st.spinner("Please wait"):
                    returned_answer = aa_service.retrieve_data(st.session_state['user_prompt'], user_query)
                    st.session_state['user_prompt'] = ''
                    st.write(returned_answer["result"])
                    # st.write(returned_answer["source"])
            else:
                st.warning('Please enter a prompt to continue.')
        else:
            st.warning('Please enter your question, before clicking the Submit button.')
