technical-documentation-copilot/
│
├── data/
│   └── documents/
│       └── sample.pdf
│
├── chroma_db/
│
├── src/
│   ├── ingestion/
│   │   ├── document_loader.py
│   │   └── text_splitter.py
│   │
│   ├── embeddings/
│   │   └── embedding_model.py
│   │
│   ├── vectorstore/
│   │   └── chroma_store.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── generation/
│   │   └── llm.py
│   │
│   └── main.py
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md