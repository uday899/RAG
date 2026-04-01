# Codebasics Q&A System

An end-to-end LLM-based Question Answering system built for an e-learning company called "Codebasics". This system allows students to ask questions related to courses and receives accurate answers using an FAQ dataset, effectively reducing the workload of human support staff.

## Tech Stack
- **LLM**: Google Generative AI (PaLM / Gemini) via MakerSuite
- **Framework**: LangChain
- **UI**: Streamlit
- **Embeddings**: HuggingFace Instructor Embeddings (`hkunlp/instructor-large`)
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Language**: Python

## Project Structure
- `main.py`: Contains the Streamlit web application layout, UI state handling, and interactive chat interface.
- `langchain_helper.py`: Contains the core logic layer using LangChain to read CSV data, generate embeddings, interact with FAISS vector store, and communicate context to the LLM.
- `requirements.txt`: Python package dependencies necessary for execution.
- `.env`: Environment variables file configured to secure API keys.
- `codebasics_faqs.csv`: Sample FAQ dataset providing course context.

## Setup Instructions

1. **Open your project folder** in your Terminal/Command Prompt. Ensure you are at the `q&A` folder.
2. **Set up a virtual environment** (recommended to avoid conflicts):
   ```bash
   python -m venv venv
   # On Windows (cmd): venv\Scripts\activate.bat
   # On Windows (Powershell): .\venv\Scripts\Activate.ps1
   # On Mac/Linux: source venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Get a Google API Key**:
   - Go to [Google AI Studio](https://aistudio.google.com/) (formerly MakerSuite).
   - Sign in using your Google account and create an API key.
5. **Configure Environment Variables**:
   - Open the `.env` file located in the root folder and replace `your_api_key_here` with your actual generated Google API key.
6. **Run the Streamlit App**:
   ```bash
   streamlit run main.py
   ```

## Usage
1. Provide the code stream access and a browser window should pop up automatically. If not, open the local URL formatted as `http://localhost:8501`.
2. Look at the sidebar on the left and click **"Create Knowledgebase"**. This command reads the CSV file, creates large instruction embeddings matching semantics, and stores them via FAISS on disk locally in a `faiss_index` folder. You only need to perform this action when the source dataset (`codebasics_faqs.csv`) is modified.
3. Type your question in the chat input box at the bottom. Use queries that logically map to the sample code for best results. Examples: 
   - "Do you guys provide job assistance?"
   - "Can a beginner enroll?"
   - "Will I get refunds if I drop out?"
4. The system assistant will analyze your query iteratively, retrieve the most precise context chunks, fetch an answer natively tied to your internal data structure, and return the answer. Let know what you think of the custom "Sources Context" expansion!

## Common Errors and Fixes
- `KeyError: 'GOOGLE_API_KEY'` or `Validation Error: google_api_key not provided`: Ensure your `.env` file is appropriately populated using valid authentication.
- `ValueError: Could not find sentence-transformers`: InstructorEmbeddings strictly requires `sentence-transformers` under the hood. The current `requirements.txt` should tackle this. Try a fresh re-installation of dependencies. 
- `Missing FAISS Index / FAISS Load Error`: Before your first conversation, you MUST click the "Create Knowledgebase" button in the sidebar. This ensures the index exists before it retrieves anything. 
- `File not found: codebasics_faqs.csv`: The backend expects the CSV directly beside the module scripts.

## Component Breakdown & Explanations
1. **HuggingFace Instructor Embeddings (`hkunlp/instructor-large`)**: A high-performing embedder converting sentences into vectors. Instructor embeddings are known to capture context instruction effectively, giving improved matches for FAQ-style documents.
2. **FAISS**: The semantic search vector database engine. It compares queries and answers geometrically. It can operate in-memory but we use `save_local()` and `load_local()` to serialize its state and reduce computational overhead for subsequent queries.
3. **PromptTemplate**: LLMs tend to "hallucinate" (making up info unprompted). We utilize manual string formatting injection directing the Generative AI behavior to answer purely using `{context}` provided. We strictly set limits such as "If the answer is not found, state I don't know."
4. **RetrievalQA**: The LangChain mechanism which automates receiving a text stream, encoding it to vector, querying Vector DB, decoding top matches (Top-K parameter configured for top-3 limits context lengths efficiently), and forwarding results alongside strings attached smoothly.

## Suggestions for Future Development
1. **Document Expansion:** Implement `PyPDFLoader` next to text and structured datasets. This brings massive capability increments, integrating syllabus guidelines seamlessly.
2. **History Context (Conversational QA):** Upgrade chains into memory buffers `ConversationalRetrievalChain` enabling references pointing back seamlessly. 
3. **Similarity Metrics display:** By utilizing `vec.similarity_search_with_score()`, you could render cosine-similarity percentages via UI indicating retrieval confidence.
4. **Cloud Database Scale up:** If vector loads bloat your storage, migrate memory to dedicated DB formats (Pinecone/Chroma) and switch out the Vector Store integration line!
