from langgraph.graph import StateGraph, END, START
from langchain_core.runnables import RunnableLambda
from chains.qa_pipeline import build_qa_chain
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from chains.load_faqs import load_faqs
import numpy as np
from typing import TypedDict

documents = load_faqs()
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents, embedding=embeddings, persist_directory="database/chroma_db"
)
threshold = 0.55


def cosine_similarity(query, documents):
    return np.dot(query, documents) / (np.linalg.norm(query) * np.linalg.norm(documents))


class ConversationState(TypedDict):
    query: str
    next: str
    response: str


def greeting_node(state):
    return {"response": "Hello! How can I assist you today?"}


def fallback_node(state):
    return {"response": "Sorry, I didn't understand that"}


def qa_node(state):
    query = state["query"]
    documents = vectorstore.similarity_search_with_score(query, k=3)
    # print("##################",documents)
    qa_chain_response = build_qa_chain(documents, query)
    return {"response": qa_chain_response}


def router(state):
    query = state["query"].lower()
    query_embedding = embeddings.embed_query(query)
    docs = vectorstore.similarity_search_with_score(query, k=3)
    if not docs:
        return {"next": "fallback"}
    similarities = []
    for doc, _score in docs:
        related_docs_emb = embeddings.embed_query(doc.page_content)
        similarities.append(cosine_similarity(
            query_embedding, related_docs_emb))
    similarity = sum(similarities)/len(similarities)
    print(similarity)
    if query in ["hi", "hello", "hey", "howdy", "greetings", "good morning", "good afternoon",
                 "good evening", "yo", "sup", "what's up", "hi there", "hello there", "hey there"]:
        return {"next": "greet"}
    elif similarity < threshold:
        return {"next": "fallback"}
    else:
        return {"next": "qa"}


def build_graph():
    builder = StateGraph(ConversationState)
    builder.add_node("greet", RunnableLambda(greeting_node))
    builder.add_node("qa", RunnableLambda(qa_node))
    builder.add_node("fallback", RunnableLambda(fallback_node))
    builder.add_node("router", RunnableLambda(router))
    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",
        lambda state: state["next"],
    )
    builder.add_edge("greet", END)
    builder.add_edge("qa", END)
    builder.add_edge("fallback", END)
    return builder.compile()
