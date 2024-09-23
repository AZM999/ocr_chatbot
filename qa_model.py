from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA, conversational_retrieval
from langchain.prompts import PromptTemplate, ChatPromptTemplate
import chromadb




def load_llm():
    # Load the locally downloaded model here
    llm = CTransformers(
        model = "/home/azm/projects/ocr_chatbot/Mistral-7B-Instruct-v0.2-Q5_K_M.gguf",
        model_type="mistral",
        max_new_tokens = 1048,
        temperature = 0.3
    )
    return llm

def get_text_chunks (text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    chunks = text_splitter.split_text(text)
    return chunks

def generate_embeddings():
    embeddings = HuggingFaceInstructEmbeddings(model_name = "sentence-transformers/all-mpnet-base-v2")
    return embeddings

def create_vectorstore (text_chunks, embeddings):
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

prompt_template = """
    Answer the question truthfully based solely on the given documents. If the documents do not contain the answer to the question, say that answering is not possible given the available information. Your answer should be no longer than 50 words.
    Documents:{documents}
    Question:{question}
    Answer:
    """
def llm_pipeline (vectorstore):
    ans_gen = load_llm()
    answer_gen_chain = RetrievalQA.from_chain_type(llm=ans_gen,
                                                   chain_type = "stuff",
                                                   retriever=vectorstore.as_retriever()
                                                   )
    return answer_gen_chain



def get_answer(document:str, question:str, bot):


    prompt_template = """
    Answer the question truthfully based solely on the given documents. If the documents do not contain the answer to the question, say that answering is not possible given the available information. Your answer should be no longer than 50 words.
    Documents:{documents}
    Question:{question}
    Answer:
    """
    prompt_template = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt_template.format(documents=document, question=question)
    ans = bot (prompt)
    return {"question": question, "answer" :ans['result']}


# test
document = "Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend 'Venite Ad Me Omnes' Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary."
question = ["Where is jesus currently burried ?", 
            "To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?",
            "Where did Super Bowl 50 take place?",
            "where is the statue of mary located?",
            "what material is the statue of mary made out of?"]
            

#txt_chunks = get_text_chunks(document)
#embeddings = generate_embeddings()
#db = create_vectorstore (txt_chunks, embeddings)
#print (" intial db:" , db)

#bot = llm_pipeline(vectorstore=db)
#for i in question:
#    print (get_answer(document=document, question=i, bot=bot))


#prompt_template = ChatPromptTemplate.from_template(prompt_template)
#prompt = prompt_template.format(documents=document, question=question)
#print (prompt)
#print (PromptTemplate(template=prompt_template, input_variables=["documents", "question"]))

#print (txt_chunks, db)
#print (load_llm().invoke('Ai is going to'))
