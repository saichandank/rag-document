import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import os
# import anthropic
import requests
from PyPDF2 import PdfReader



load_dotenv()

class RAG:
    def __init__(self, chroma_path="./Document-Agent/chroma_db"):
        
        self.api_key = os.getenv("LLM_API_KEY")
        self.count = 1
        try:
            if chroma_path:
                self.client = chromadb.PersistentClient(path=chroma_path)  
            else:
                raise ValueError("ChromaDB path is not set.")
        except Exception as e:
            print(f"Error connecting to ChromaDB: {e}")
            return
        
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


    def document_embedding(self, document_path):
        print(f"Processing document: {document_path}")
        document = ""
        if document_path.lower().endswith(".pdf"):
            try:
                reader = PdfReader(document_path)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        document += text
            except Exception as e:
                print(f"Error reading PDF: {e}")
                return
        else:
            print(f"Error reading the document: {e}")
            return
        

        embedding = self.embedding_model.encode(document, convert_to_tensor=False)
        collection = self.client.get_or_create_collection("document_embeddings")
        doc_id = str(self.count)+"-"+os.path.basename(document_path)

        print(f"Embedding document: {doc_id}")
        collection.add(
            embeddings=[embedding],
            documents=[document],
            ids=[doc_id]
        )
        
        print(f"Document '{doc_id}' embedded and stored.")



    def retrieve_documents(self, query, top_k=5):
        try:
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=False)
            collection = self.client.get_collection("document_embeddings")

            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            return results['documents'], results['ids']
        
        except Exception as e:
            print(f"Error retrieving documents: {e}")
            return [], []



    # def generate_response(self, query):

    #     documents, document_ids = self.retrieve_documents(query)

    #     flat_documents = [doc for sublist in documents for doc in (sublist if isinstance(sublist, list) else [sublist])]
    #     context = "\n\n".join(flat_documents)

        
    #     prompt = f"""   Please answer the user's question based on the following context.
    #                     If the context does not contain the answer, say so.

    #                     Context:
    #                     {context}

    #                     User Question: {query}

    #                     Answer:"""
        
    #     print(prompt)
    #     client = anthropic.Anthropic(api_key=self.api_key)
    #     try:
    #         response = client.messages.create(
    #             model= "claude-3-5-sonnet-20241022",
    #             max_tokens=250,
    #             messages=[
    #                 {"role": "user", "content": prompt}
    #             ]
    #         )
    #         final_answer = response.content[0].text
    #         return final_answer
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         return "Sorry, I couldn't process your request."

    def generate_response(self, query):
        documents, document_ids = self.retrieve_documents(query)
        flat_documents = [doc for sublist in documents for doc in (sublist if isinstance(sublist, list) else [sublist])]
        context = "\n\n".join(flat_documents)
        max_context_length = 80000
        if len(context) > max_context_length:
            context = context[:max_context_length]

        prompt = f"""Please answer the user's question based on the following context.
                    If the context does not contain the answer, say so.

                    Context:
                    {context}

                    User Question: {query}

                    Answer:"""

        print(prompt)
        try:
            api_url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "mistralai/mistral-small-3.2-24b-instruct:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 250
            }
            response = requests.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            # Extract only the answer part from the response
            answer = result["choices"][0]["message"]["content"]
            return answer
        #     response = requests.post(api_url, headers=headers, json=data)
        #     response.raise_for_status()
        #     result = response.json()
        #     final_answer = result["choices"][0]["message"]["content"]
        #     return final_answer
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, I couldn't process your request."


    def clear_all_documents(self):
        try:
            collection = self.client.get_or_create_collection("document_embeddings")
            collection.delete(where={})  # Delete all documents
            print("All documents deleted from db.")
        except Exception as e:
            print(f"Error deleting documents: {e}")
            return
        


if __name__ == "__main__":
    rag = RAG()
    
    query = "What is javac?"
    print("Query:", query)
    document_embedding = rag.document_embedding("/Users/chanduk55/project/leadership.txt")
    response = rag.generate_response(query)
    print("Response:", response)