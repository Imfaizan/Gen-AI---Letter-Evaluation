from langchain_openai import ChatOpenAI
from app.core.embedding import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader

def evaluate_letter(file_path: str):
    # Load the document
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Set up retriever
    db = Chroma(persist_directory=settings.CHROMA_DB_DIR)
    retriever = db.as_retriever()

    # Set up LLM and prompt template
    llm = ChatOpenAI(model="gpt-4o-mini")
    prompt_template = ChatPromptTemplate.from_template(
        """
        You are an AI legal expert. Here is the letter: 
        {input}

        Based on the following policy documents:
        <context>
        {context}
        <context>
        
        Identify if there are any indemnification clauses or impermissible language that could violate the policies. Highlight such clauses in the letter and flag them as red.
        """
    )
    
    # Create document chain
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Evaluate letter
    response = retrieval_chain.invoke({'input': docs[0].page_content})
    return response['answer']
