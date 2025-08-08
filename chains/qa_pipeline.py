from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import os
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

# def build_qa_chain():
#     documents = load_faqs()
#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )
#     vectorstore = Chroma.from_documents(
#         documents, embedding=embeddings, persist_directory="database/chroma_db"
#     )
#     vectorstore.persist()

#     llm = ChatGoogleGenerativeAI(
#         model="gemini-2.5-flash",
#         temperature=0.3,
#         google_api_key=os.environ["GOOGLE_API_KEY"]
#     )

#     qa_chain = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         return_source_documents=True
#     )
#     return qa_chain

# function to build the chain


def build_qa_chain(documents, question):

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )
    messages = [
        ("system", "You are an expert in agricultural content."),
        ("human",
         "Use only the following farming documents to answer the question:\n\n{documents}\n\nQuestion: {question} if the question is irrelevent to the documents then return like i am unable to answer your question")
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    qa_chain = prompt | llm | StrOutputParser()  # chain
    # print(">>>>>>>>>>>>>>>>>>>>",documents)
    response = qa_chain.invoke({"documents": documents, "question": question})
    return response
