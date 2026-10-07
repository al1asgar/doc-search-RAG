# Doc-Search — Chat with any PDF (RAG)

A document question-answering web app. Upload a PDF, ask questions in plain English, and get answers grounded in the document — powered by a Retrieval-Augmented Generation (RAG) pipeline.

**Live demo:** https://docsearch-rag.streamlit.app/
*(Bring your own OpenAI key — enter it in the sidebar. Nothing is stored.)*

---

## What it does

- Upload any text-based PDF and ask questions about its contents
- Answers are grounded in the document, not guessed — the app retrieves the most relevant passages and has the model answer from them
- Bring-your-own-key design: runs on the visitor's OpenAI key, so it's safe and free to host
- Handles bad input gracefully (e.g. scanned/image-only PDFs with no extractable text)

## How it works (the RAG pipeline)

1. **Load** — extract the text from the uploaded PDF
2. **Chunk** — split it into small overlapping pieces
3. **Embed** — convert each chunk into a vector (numbers that capture meaning)
4. **Store** — index the vectors in a ChromaDB vector store (cached, so indexing runs once per document)
5. **Retrieve** — for each question, find the chunks closest in meaning
6. **Generate** — pass those chunks + the question to the chat model for a grounded answer

## Tech stack

- Python
- Streamlit — UI and hosting
- LangChain — text splitting and model interfaces
- ChromaDB — vector store
- OpenAI — embeddings (`text-embedding-3-small`) and chat (`gpt-4o-mini`)

## Run it locally

```bash
git clone https://github.com/your-username/docsearch-rag.git
cd docsearch-rag
pip install -r requirements.txt
streamlit run doc-search.py
```

Then enter your OpenAI API key in the sidebar and upload a PDF.

## Notes

- **Bring your own key:** the app uses the visitor's OpenAI API key (entered in the sidebar). No keys are collected or stored.
- Works with text-based PDFs. Scanned/image-only PDFs have no extractable text and will be rejected with a message.
---

_Built by Aliasgar Dohadwala — a hands-on applied-AI project: a full retrieval-augmented generation pipeline, built and deployed end to end._
