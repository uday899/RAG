import os
import sys

# Windows compatibility fix for pwd module error
try:
    import pwd
except ImportError:
    import types
    pwd_mock = types.ModuleType('pwd')
    def getpwuid(uid):
        class PwStruct:
            pw_name = "windows_user"
        return PwStruct()
    pwd_mock.getpwuid = getpwuid
    sys.modules['pwd'] = pwd_mock

from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables (such as GOOGLE_API_KEY)
load_dotenv(override=True)

# We initialize the Gemini LLM for high accuracy outputs.
# The temperature here is set low at 0.1 for precise fact-based QA extraction from the document context.
# We will use "gemini-pro" model as text-bison-001 is being deprecated.
llm = GoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.environ.get("GOOGLE_API_KEY"), 
    temperature=0.1
)

# Initialize Google Generative AI embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Path to the locally saved FAISS vector database
vector_db_file_path = "faiss_index"

def create_vector_db():
    """
    Reads the CSV dataset, generates HuggingFace Instructor Embeddings 
    for each prompt, and stores the resulting vectors in a local FAISS database.
    """
    if not os.path.exists("codebasics_faqs.csv"):
        raise FileNotFoundError("The file codebasics_faqs.csv was not found. Please ensure it exists.")

    # Load data from FAQ csv file. Map source_column to the user's primary "prompt" or "question" column.
    loader = CSVLoader(file_path='codebasics_faqs.csv', source_column="prompt", encoding="utf-8")
    data = loader.load()

    # Create a FAISS vector database instance from documents leveraging HuggingFace embeddings
    vectordb = FAISS.from_documents(documents=data, embedding=embeddings)

    # Save vector database locally
    vectordb.save_local(vector_db_file_path)

def get_qa_chain():
    """
    Loads the locally stored FAISS vector database, initializes a custom PromptTemplate, 
    and returns a LangChain LCEL constructed runnable wrapper mimicking RetrievalQA.
    """
    # Load the vector database from the local directory
    vectordb = FAISS.load_local(
        vector_db_file_path, 
        embeddings,
        allow_dangerous_deserialization=True
    )

    # Create a retriever for querying the vector database. We pull top-3 most relevant chunks.
    retriever = vectordb.as_retriever(search_kwargs={"k": 3}, score_threshold=0.7)

    # Custom prompt clearly instructing the LLM on its behavior when answering questions
    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from the "response" section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    prompt = PromptTemplate.from_template(prompt_template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    class QARunnable:
        def invoke(self, query):
            # 1. Fetch source documents
            docs = retriever.invoke(query)
            # 2. Extract content
            context_str = format_docs(docs)
            # 3. Create core generation chain
            chain = prompt | llm | StrOutputParser()
            # 4. Generate result
            answer = chain.invoke({"context": context_str, "question": query})
            
            # Map back to standard RetrievalQA Dictionary interface
            return {"result": answer, "source_documents": docs}

    return QARunnable()

if __name__ == "__main__":
    # For testing independently via terminal:
    create_vector_db()
    chain = get_qa_chain()
    # Outputting response for a sample predefined query
    result = chain.invoke("Do you provide job assistance?")
    print("Answer:", result["result"])
