import streamlit as st
import os
from langchain_helper import create_vector_db, get_qa_chain

# Streamlit Page Configuration
st.set_page_config(page_title="Codebasics Q&A", page_icon="🌱", layout="centered")

# Custom UI styling (Optional bonus feature)
st.markdown("""
<style>
.stApp {
    background-color: #f7f9fc;
}
.title-text {
    color: #2c3e50;
    text-align: center;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 0px;
}
.subtitle-text {
    color: #34495e;
    text-align: center;
    font-size: 1.2rem;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">Codebasics Q&A 🌱</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">Ask any questions related to Codebasics courses!</div>', unsafe_allow_html=True)

# Sidebar components
st.sidebar.title("Configuration")
btn = st.sidebar.button("Create Knowledgebase")
if btn:
    with st.spinner("Building the Knowledgebase... This might take a few moments."):
        try:
            create_vector_db()
            st.sidebar.success("Knowledgebase created successfully!")
        except Exception as e:
            st.sidebar.error(f"Failed to create Knowledgebase: {str(e)}")

# Initialize chat history (Bonus Feature: Chat Memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
question = st.chat_input("Ask a question about Codebasics courses...")

if question:
    # Display user message in chat message container
    st.chat_message("user").markdown(question)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})

    try:
        # Check if Google API Key is set
        if not os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY") == "your_api_key_here":
            st.error("Please configure your GOOGLE_API_KEY in the .env file. ")
        # Check if Knowledge Base is created
        elif not os.path.exists("faiss_index"):
            st.error("Knowledge base not found. Please click 'Create Knowledgebase' on the sidebar.")
        else:
            with st.spinner("Searching for answers... (Analyzing Context)"):
                # Load the chain
                chain = get_qa_chain()
                
                # Fetch answer using chain.invoke() since standard call is deprecated
                response = chain.invoke(question)
                answer = response["result"]

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(answer)
                # Show source documents if answer was retrieved (Bonus Feature: Similarity Match display can be derived)
                with st.expander("View Source Context"):
                    sources_str = "\n".join([f"- {doc.page_content}" for doc in response['source_documents']])
                    st.write(sources_str if sources_str else "No explicit source document retrieved.")
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        error_msg = f"An error occurred. Please ensure your API key and Environment is fully configured.\nError Details: {str(e)}"
        st.error(error_msg)
