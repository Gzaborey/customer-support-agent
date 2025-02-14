from app.common.utils import parse_faq_file
from langchain.docstore.document import Document
from pathlib import Path
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import CHROMADB_PATH


FAQTXT_PATH = Path(r"data\processed\updated_faq_doc.txt")

def main() -> None:
    faq_data = parse_faq_file(FAQTXT_PATH)

    docs = []
    for text in faq_data:
        docs.append(Document(text, metadata={"source": "Tee Customizer FAQ"}))
    
    embedding_function = HuggingFaceEmbeddings(model_name="BAAI/llm-embedder")
    
    Chroma.from_documents(documents=docs,
                          embedding=embedding_function,
                          persist_directory=CHROMADB_PATH,
                          collection_name="faq_collection")


if __name__=="__main__":
    main()