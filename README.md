# Document Agent

## Overview
This project is a Flask-based application that uses Retrieval-Augmented Generation (RAG) to process and query documents. It supports uploading `.pdf` files, 
embedding them into a ChromaDB collection, querying for relevant information, and clearing all stored documents.

## Features
- **Upload Documents**: `.pdf` files into ChromaDB.
- **Query**: Retrieve relevant information based on user queries.
- **Clear All**: Delete all stored documents from the database.

## Prerequisites
- Docker
- Python 3.11
- A `.env` file with the following variables:
  ```env
  ANTHROPIC_API_KEY="your_anthropic_api_key_here"
  TOKENIZERS_PARALLELISM=false
  CHROMA_TELEMETRY_ENABLED=false
  ```

## How to Run

### 1. Create a `.env` File
Create a `.env` file in the project root with the following content:
```env
ANTHROPIC_API_KEY="your_anthropic_api_key_here"
TOKENIZERS_PARALLELISM=false
CHROMA_TELEMETRY_ENABLED=false
```

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


- Replace `your_anthropic_api_key_here` with your actual API key.


