# Document Agent

## Overview
This project is a Flask-based application that uses Retrieval-Augmented Generation (RAG) to process and query documents. It supports uploading `.pdf` files, 
embedding them into a ChromaDB collection, querying for relevant information, and clearing all stored documents.

## Features
- **Upload Documents**: `.pdf` files into ChromaDB.
- **Query**: Retrieve relevant information based on user queries.
- **Clear All**: Delete all stored documents from the database.

## Prerequisites
- Python 3.11

## How to Run

### 1. Create a `.env` File
Create a `.env` file in the project root with the following content:
```env
LLM_API_KEY= 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
CHROMA_TELEMETRY_ENABLED=false
TOKENIZERS_PARALLELISM = false
```
### 2. Setup
- run command pip install -r requirements.txt (venv recommended)
- run command python app.py

### 3. API Endpoints
#### Upload a File
- **URL**: `http://localhost:5000/upload`
- **Method**: `POST`
- **Body**: Form-data with a key `file` and the filepath to upload.

#### Query
- **URL**: `http://localhost:5000/query`
- **Method**: `POST`
- **Body**: JSON with a key `query` and the query text.

#### Clear All Documents
- **URL**: `http://localhost:5000/clearall`
- **Method**: `DELETE`





