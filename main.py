from flask import Flask, request, jsonify
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

app = Flask(__name__)

# Initialize Embeddings
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

vs = Chroma(
    collection_name="rag",
    embedding_function=embed_model,
    persist_directory="./db",  # Where to save data locally, remove if not necessary
)

chat_model = ChatGroq(temperature=0,
                      model_name="llama-3.1-70b-versatile",
                      api_key="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",)

retriever = vs.as_retriever(search_kwargs={'k': 3})

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

prompt = set_custom_prompt()

qa = RetrievalQA.from_chain_type(
    llm=chat_model,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()  # Receive JSON data from React
    query = data.get('query', '')

    if query:
        response = qa.invoke({"query": query})
        result = response['result']  # Extract the result from the response
        return jsonify({'result': result})  # Send back the result as JSON
    else:
        return jsonify({'error': 'No query provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)
