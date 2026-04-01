# 🚀 Codebasics Q&A System (LLM + RAG Project)

An end-to-end **LLM-powered Question Answering System** built for the e-learning platform **Codebasics**.
This project uses **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers from a custom knowledge base.

---

## 📌 Project Overview

This system allows users to:

* Ask questions related to courses
* Retrieve relevant answers from a dataset
* Avoid hallucinations using strict prompt control
* View source context used to generate answers

---

## 🧠 Architecture

```
User Query → Embeddings → FAISS Vector DB → Retriever → LLM → Answer
```

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **LLM:** Google Gemini (gemini-2.5-flash)
* **Embeddings:** GoogleGenerativeAIEmbeddings
* **Vector DB:** FAISS
* **Framework:** LangChain (LCEL)

---

## 📁 Project Structure

```
📦 Codebasics-QA
 ┣ 📜 main.py                  # Streamlit UI
 ┣ 📜 langchain_helper.py      # Core backend logic
 ┣ 📜 codebasics_faqs.csv      # Dataset (Q&A)
 ┣ 📜 requirements.txt         # Dependencies
 ┣ 📜 .env                     # API Key config
 ┗ 📜 README.md                # Documentation
```

---

## ✨ Features

* ✅ Clean and interactive Streamlit UI
* ✅ Chat history using session state
* ✅ FAISS-based fast retrieval
* ✅ Context-aware answers
* ✅ "I don’t know" fallback (anti-hallucination)
* ✅ Source document viewer

---

## 🔐 Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add API Key

Create `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```bash
streamlit run main.py
```

---

## ⚠️ Important Step

👉 After launching the app:
Click **"Create Knowledgebase"** in the sidebar before asking questions.

---

## 🛠️ Key Components Explained

### 🔹 Data Processing

* CSV-based FAQ dataset
* Clean parsing with proper formatting

### 🔹 Embeddings

* Uses Google embeddings for better contextual understanding

### 🔹 Vector Store

* FAISS for efficient similarity search

### 🔹 LLM Pipeline

* Custom prompt template
* Prevents hallucination
* Returns "I don’t know" if answer not found

---

## 🐞 Issues Fixed

* ✅ CSV parsing errors (comma handling)
* ✅ PyTorch DLL errors removed (no heavy dependencies)
* ✅ Deprecated API errors fixed
* ✅ Environment variable reload issues resolved
* ✅ LangChain version compatibility handled

---

## 🚀 Future Improvements

* 🔹 Add authentication (login system)
* 🔹 Upload custom documents (PDF support)
* 🔹 Deploy on cloud (AWS / GCP)
* 🔹 Add multi-language support
* 🔹 Improve UI/UX design

---

---

## 🤝 Contributing

Feel free to fork this repo and improve the system!

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 💡 Author

Developed by **Uday Avula**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
