from langsmith import traceable
from graph.conversation_graph import build_graph
from dotenv import load_dotenv
load_dotenv()


@traceable
def call_graph(query):
    graph = build_graph()
    return graph.invoke({"query": query})
