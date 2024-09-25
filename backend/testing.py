from qa_model import qa_model

# test
llm = qa_model()
llm.load_llm()

document = "Architecturally, the school has a Catholic character. Atop the Main Building\'s gold dome is a golden statue of the Virgin Mary. Immediately in front of the Main Building and facing it, is a copper statue of Christ with arms upraised with the legend 'Venite Ad Me Omnes' Next to the Main Building is the Basilica of the Sacred Heart. Immediately behind the basilica is the Grotto, a Marian place of prayer and reflection. It is a replica of the grotto at Lourdes, France where the Virgin Mary reputedly appeared to Saint Bernadette Soubirous in 1858. At the end of the main drive (and in a direct line that connects through 3 statues and the Gold Dome), is a simple, modern stone statue of Mary."
question = ["Where is jesus currently burried ?", 
            "To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?",
            "Where did Super Bowl 50 take place?",
            "where is the statue of mary located?",
            "what material is the statue of mary made out of?"]
            
llm.get_text_chunks(document)
llm.generate_embeddings()
db = llm.create_vectorstore()
llm.llm_pipeline()
#txt_chunks = get_text_chunks(document)
#embeddings = generate_embeddings()
#db = create_vectorstore (txt_chunks, embeddings)
print (" intial db:" , db)
#
for i in question:
    print (llm.get_answer(question=i))

