import os
import logging

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA

from config.vector_store import get_vector_store

load_dotenv()

logger = logging.getLogger(__name__)

llm = ChatOpenAI(
    model="openrouter/auto",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def ask_question(question: str) -> dict:
    vector_store = get_vector_store()

    if vector_store is None:
        return {
            "answer": "No documents available. Please upload documents first.",
            "sources": [],
        }

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
    )

    try:
        result = qa_chain.invoke({"query": question})
        answer = result["result"]
        sources = [
            {
                "document_id": doc.metadata.get("document_id"),
                "title": doc.metadata.get("title"),
                "excerpt": doc.page_content[:200],
            }
            for doc in result.get("source_documents", [])
        ]
    except Exception as e:
        logger.error(f"QA chain failed: {e}")
        return {
            "answer": "Failed to generate an answer. Please try again.",
            "sources": [],
        }

    return {"answer": answer, "sources": sources}
