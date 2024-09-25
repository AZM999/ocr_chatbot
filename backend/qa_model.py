from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.llms import CTransformers, huggingface_hub 

from langchain.llms import huggingface_hub
from langchain.chains import RetrievalQA, conversational_retrieval
from langchain.prompts import PromptTemplate, ChatPromptTemplate
import os


# self.llm          local mistral llm instance
# self.document     chunked document data to be used 
# self.embeddings   embeddings to generate the vectorstore
# 

class qa_model:
    def __init__(self):
        HF_TOKEN = os.environ.get("HF_TOKEN")

    prompt_template = """
    Answer the question truthfully based solely on the given documents. If the documents do not contain the answer to the question, say that answering is not possible given the available information. Your answer should be no longer than 50 words.
    Documents:{documents}
    Question:{question}
    Answer:
    """
    # loading the local mistral 
    def load_llm(self) -> CTransformers:
        # Load the locally downloaded model here
        self.llm = CTransformers(
            model = "Mistral-7B-Instruct-v0.2-Q5_K_M.gguf",
            model_type="mistral",
            max_new_tokens = 1048,
            temperature = 0.3
        )
        return self.llm

    # chunking the extracted text
    def get_text_chunks (self, text) -> str:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
        self.document = text_splitter.split_text(text)
        return self.document

    # create embeddings with mpnet-base
    def generate_embeddings(self) -> HuggingFaceInstructEmbeddings:
        self.embeddings = HuggingFaceInstructEmbeddings(
            model_name = "sentence-transformers/all-mpnet-base-v2")
        return self.embeddings

    # create FAISS vectordb with documents
    def create_vectorstore (self) -> FAISS:
        self.vectorstore = FAISS.from_texts(texts=self.document,
                                             embedding=self.embeddings)
        return self.vectorstore

    
    # intitalize the chain
    def llm_pipeline (self) -> RetrievalQA:
        self.load_llm()
        self.Conversation_gen_chain = RetrievalQA.from_chain_type(llm=self.llm,
                                                    chain_type = "stuff",
                                                    retriever=self.vectorstore.as_retriever()
                                                    )
        return self.Conversation_gen_chain


    # running query with context
    def get_answer(self, question:str) -> dict:

        prompt_template = ChatPromptTemplate.from_template(self.prompt_template)
        prompt = prompt_template.format(documents=self.document, question=question)
        ans = self.Conversation_gen_chain (prompt)
        return {"question": question, "answer" :ans['result']}



#prompt_template = ChatPromptTemplate.from_template(prompt_template)
#prompt = prompt_template.format(documents=document, question=question)
#print (prompt)
#print (PromptTemplate(template=prompt_template, input_variables=["documents", "question"]))

#print (txt_chunks, db)
#print (load_llm().invoke('Ai is going to'))
