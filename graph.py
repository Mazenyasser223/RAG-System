import os
from typing import List, TypedDict
from langchain_ollama import OllamaLLM
from langgraph.graph import END, StateGraph
from tools import retriever

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[dict]

llm = OllamaLLM(model="llama3.2:latest")

def retrieve(state):
    print("--- RETRIEVING DOCUMENTS ---")
    question = state["question"]
    documents = retriever.invoke(question)

    if not documents:
        print("No relevant docs were retrieved using the threshold.")

    return {"documents": documents, "question": question}

def generate(state):
    print("--- GENERATING ANSWER ---")
    question = state["question"]
    documents = state["documents"]

    if not documents:
        error_msg = ("I am sorry, but the provided documents do not contain enough relevant information "
                     "to answer this question accurately within the 0.5 similarity threshold.\n\n"
                     "DISCLAIMER: This system is for educational purposes only. This is NOT professional legal, financial, or engineering advice.")
        return {"generation": error_msg, "question": question}

    context_parts = []
    for doc in documents:
        source = os.path.basename(doc.metadata.get('source', 'Unknown'))
        context_parts.append(f"SOURCE FILE: {source}\nCONTENT: {doc.page_content}")

    context = "\n\n---\n\n".join(context_parts)

    template = f"""
    You are a professional Strategic AI Analyst for Tech Giants.
    Your task is to provide a comprehensive and detailed answer based ONLY on the context provided below.

    STRICT RULES:
    1. Answer ONLY using the provided CONTEXT. If the answer is not there, say: "I am sorry, but the provided documents do not contain this information."
    2. Do NOT use your internal general knowledge or mention information outside the provided context.
    3. Every fact or claim in your response MUST cite its source file name in parentheses, for example: (Source: Nvidia.txt).
    4. Provide as much detail as possible FROM THE CONTEXT.
    5. You MUST end your response with this exact disclaimer text on a new line:

    "DISCLAIMER: This system is for educational purposes only. This is NOT professional legal, financial, or engineering advice."

    CONTEXT:
    {context}

    QUESTION: {question}
    """

    response = llm.invoke(template)
    return {"generation": response, "question": question}

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()
