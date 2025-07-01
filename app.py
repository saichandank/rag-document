from flask import Flask, request, jsonify
import os
from RAG import RAG

app = Flask(__name__)
rag = RAG()

@app.route('/upload', methods=['POST'])
def upload_document():

    data = request.get_json()
    filepath = data.get('file')
    print("File received:", filepath)

    if not filepath:
        return jsonify({"error": "No file part"}), 400
    

    rag.document_embedding(filepath)
    return jsonify({"message": f"File '{filepath}' uploaded and embedded."})


@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_text = data.get('query')

    if not query_text:
        return jsonify({"error": "No query provided"}), 400
    
    response = rag.generate_response(query_text)
    return jsonify({"response": response})


@app.route('/clearall', methods=['DELETE'])
def clearall():
    rag.clear_all_documents()
    return jsonify({"message": "All documents cleared."}), 200


if __name__ == '__main__':
    app.run(debug=True)