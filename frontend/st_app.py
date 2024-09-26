import streamlit as st
import requests

def main ():
    st.set_page_config(page_title= "chat with the given files, Pdf or images", 
                       page_icon=":genie:")
    st.header("FileGenie! Ask question regarding your files")


    if "history" not in st.session_state:
        st.session_state.history = []


    prompt = st.chat_input("Ask any question about your files ")

    if prompt:
        
        user_chat = st.chat_message("User")
        genie_chat = st.chat_message("Genie :genie:")
        user_chat.write(f"{prompt}")
        with st.spinner(text="thinking..."):
            url = "http://localhost:8000/ask"
            response = requests.get(url, {"question":prompt})
            if response.status_code == 200:
                response = response.json()
                genie_chat.write(response)

    with st.sidebar:
        st.subheader("Your documents")
        with st.form("upload-form", clear_on_submit=False):
            uploaded_file = st.file_uploader ("upload your File here and click on process",
                                               type=['png', 'jpeg', 'pdf'])
            url = "http://localhost:8000/upload"
            submitted = st.form_submit_button("Upload and Analyze")
            if submitted:
                with st.spinner("uploading and processing"):
                    files = {  
                        "uploaded_file": (uploaded_file.name,
                                          uploaded_file.getvalue(), 
                                          uploaded_file.type) }
                    
                    response = requests.post(url, files=files)
                    if response.status_code == 200:
                        st.write("uploaded Successfully !")
                        st.json(response.json())
                    # initialize pipeline

                    response = requests.get("http://localhost:8000/init_pipeline")
                    if response.status_code == 200:
                        st.write("uploaded Successfully !")
                        st.json(response.json())


if __name__ == '__main__':
    main()