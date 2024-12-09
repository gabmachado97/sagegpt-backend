from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores import Qdrant
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

app = Flask(__name__)


# Enable CORS for the entire app and allow all origins (adjust for production)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://your-frontend-url.com"]}})

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Initialize Embeddings
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

vs = Qdrant.from_existing_collection(
        embedding=embed_model,
        path="./db",
        collection_name="sage_manual",
    )

chat_model = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
   #model_name="llama-3.1-70b-versatile",
    api_key="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",
)

retriever = vs.as_retriever(search_kwargs={"k": 1, "fetch_k": 10})

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
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt


prompt = set_custom_prompt()

qa = RetrievalQA.from_chain_type(
    llm=chat_model,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt},
)


@app.route("/api/value", methods=["POST", "OPTIONS"])
def handle_query():

    if request.method == "OPTIONS": # CORS preflight
      return _build_cors_preflight_response()
    else:
      data = request.get_json()  # Receive JSON data from React
        
      query = data.get("query", "")

      if query:
          try:
              new_resp = qa.invoke({"query": query})
            #  result = response["result"]  # Extract the result from the response
              return _corsify_actual_response(jsonify({"result": query}))  # Send back the result as JSON
             # return _corsify_actual_response(jsonify({"result": result}))  # Send back the result as JSON
          except Exception as e:
              return _corsify_actual_response(jsonify({"error": str(e)}), 500 )
      else:
          return _corsify_actual_response(jsonify({"error": "No query provided"}), 400)


if __name__ == "__main__":
    app.run(debug=True)
