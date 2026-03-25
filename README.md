<h1 align="center"> Mini-Rag </h1>

<p align="center">
A lightweight RAG pipeline with vector search and transformer-based generation for QA tasks. Implemented retrieval via dense embeddings and integrated it with a seq2seq model for answer synthesis.
</p>

## Overview

This project implements a minimal yet functional RAG system that retrieves relevant document chunks using dense embeddings and generates answers using a sequence-to-sequence transformer model.

The goal is to provide a clean and modular pipeline that demonstrates how retrieval and generation can be combined for knowledge-grounded QA.


## Table of Contents
1. [Requirements](#requirements)
    - [Install Conda and Docker compose](#install-conda-and-docker-compose)

2. [Usage](#usage)
    - [Clone the Repository](#1-clone-the-repository)
    - [Installation](#2-installation)
    - [Run Docker Compose](#3-run-docker-compose)

3. [Features](#features)
    - [How It Works](#how-it-works)

4. [Tech Stack](#tech-stack)


## Requirements

### Install Conda and Docker compose
```
- Python 3.10 or later
- Conda environment
- Docker-compose
```

## Usage
### 1 Clone the Repository
```bash
$ git clone git@github.com:HusamettinYilmazz/Mini-RAG.git
$ cd mini-rag
```

### 2 Installation
Install the required packages
```bash
$ pip install -r src/requirements.txt
```

Setup the environment variables
```bash
$ cp src/.env.example src/.env
```
- update `.env` with your credentials

### 3 Run Docker Compose
Setup the environment variables
```bash
$ cd docker
$ cp .env.example .env
```
- update `.env` with your credentials

Run docker compose
```bash
$ sudo docker compose up -d
```

### Run the FastAPI server

```bash
$ cd ../src
$ uvicorn main:app --reload --reload-dir .
```

## Features

- Dense embedding-based semantic search  
- Document chunking and indexing pipeline 
- Vector similarity retrieval
- LLM based answer generation  
- FastAPI backend for serving queries  
- Dockerized environment


### How It Works

1. **Document Processing**  
   - Input documents are split into smaller chunks.

2. **Embedding Generation**  
   - Each chunk is converted into a dense vector representation.

3. **Vector Storage**  
   - Embeddings are stored in a vector database (Qdrant) for efficient similarity search.

4. **Query Handling**  
   - User query is embedded
   - Top-k similar chunks are retrieved

5. **Answer Generation**  
   - Retrieved context is passed to a seq2seq transformer model (LLM) to generate the final answer.

## Tech Stack

- Python
- FastAPI
- LLMs: Ollama (local) + OpenAI / Cohere APIs  
- Vector search: Qdrant
- Docker & Docker Compose
