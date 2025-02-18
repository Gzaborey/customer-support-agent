from langchain_core.tools import tool
from chatbot.utils import initialize_huggingface_retriever


retriever = initialize_huggingface_retriever()

@tool
def get_faq_info(query: str) -> str:
    """
    Retrieve relevant documents from the Chroma vector store based on a query.
    """
    documents = retriever.invoke(query)
    faq_info = "\n".join([document.page_content for document in documents])
    return faq_info