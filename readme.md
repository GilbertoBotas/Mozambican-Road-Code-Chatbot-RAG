# Mozambique Road Code RAG Assistant

A Retrieval-Augmented Generation (RAG) powered assistant that helps drivers, students, and citizens understand the Mozambique Road Code (Código de Estrada). This project uses Google Gemini AI to provide accurate, context-based answers about traffic rules, road signals, driver duties, penalties, and safe driving practices.

## 📋 Project Overview

This project implements a conversational AI assistant specialized in the Mozambique Road Code. It combines:

- **RAG (Retrieval-Augmented Generation)**: Retrieves relevant information from Road Code documents
- **Vector Database**: Uses Chroma for efficient document storage and retrieval
- **Large Language Model**: Powered by Google Gemini for intelligent responses
- **Structured Output**: Returns answers in a standardized format with articles and follow-up questions
- **FastAPI Backend**: Provides a REST API endpoint for integration
- **Console Interface**: Interactive command-line interface for direct interaction

## 🎯 Features

- **Article References**: Automatically identifies and references relevant Road Code articles
- **Follow-up Questions**: Suggests related questions for deeper learning
- **Educational Focus**: Explains rules clearly like a driving instructor or traffic officer
- **Dual Interface**: Access via REST API or interactive console

## ⚙️ Requirements

- **Python 3.12 or higher**
- **Google API Key** (for Gemini embeddings and LLM)
- **Internet Connection** (for API calls and document embedding)

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd your-project-directory
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the virtual environment:

- **On Windows:**
  ```bash
  .venv\Scripts\activate
  ```

- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```

### Step 3: Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the project root directory with your Google API credentials:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

To get your Google API Key:
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API key"
3. Copy the key to your `.env` file

### Step 5: Prepare Your Documents

Place your Mozambique Road Code PDF documents in the `docs/` directory:

```
project-root/
├── docs/
│   ├── road_code_1.pdf
│   ├── road_code_2.pdf
│   └── ...
├── console.py
├── main.py
└── ...
```

## 📖 Usage

### Option 1: Interactive Console Interface

Run the interactive console to ask questions directly:

```bash
python console.py
```

**Example interaction:**

```
Bem-vindo ao Assistente do Código de Estrada de Moçambique!
Inicializando...

Agent ready! Type 'sair' to quit.

Como posso ajudá-lo? > Qual é o limite de velocidade para carros regulares nas cidades?
Pesquisando e gerando resposta...

================================================================================
RESPOSTA DO ASSISTENTE
================================================================================

Resposta:
De acordo com o Código de Estrada de Moçambique, o limite de velocidade para 
carros regulares em zonas urbanas é de 60 km/h...

Artigos Referenciados:
  • Artigo 45 - Limites de Velocidade

Perguntas de Acompanhamento Sugeridas:
  1. Qual é o limite de velocidade nas rodovias?
  2. Quais são as penalidades por excesso de velocidade?

Escalação Necessária: False
================================================================================
```

**Commands:**
- Type your question in Portuguese
- Type `sair`, `adeus`, `exit`, or `quit` to exit
- Press `Ctrl+C` to force exit

### Option 2: FastAPI REST Endpoint

Start the FastAPI server:

```bash
fastapi run server.py
```

By default, the server runs on `http://localhost:8000`

**API Endpoints:**

#### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "ok"
}
```

#### Ask a Question
```bash
POST /ask
Content-Type: application/json

{
  "query": "Qual é o limite de velocidade nas cidades?"
}
```

Response:
```json
{
  "answer": "De acordo com o Código de Estrada de Moçambique...",
  "articles": ["Artigo 45 - Limites de Velocidade"],
  "follow_up_questions": [
    "Qual é o limite de velocidade nas rodovias?"
  ]
}
```

**Example using cURL:**

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "Qual é o limite de velocidade nas cidades?"}'
```

**Example using Python requests:**

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"query": "Qual é o limite de velocidade nas cidades?"}
)

print(response.json())
```

## 📁 Project Structure

```
project-root/
├── docs/                      # PDF documents for the Road Code
│   └── *.pdf
├── chroma_db/                 # Vector database (auto-generated)
│   └── ...
├── modules/
│   ├── rag_agent.py          # RAG agent implementation
│   ├── __init__.py
│   └── ...
├── console.py                 # Interactive console interface
├── main.py                    # FastAPI server
├── file_manager.py            # Environment and file utilities
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (not in git)
└── README.md                  # This file
```

## 🔧 Configuration

### RAG Agent Settings

In `modules/rag_agent.py`, you can customize:

- **Chunk Size**: `chunk_size=500` - Adjust how documents are split
- **Chunk Overlap**: `chunk_overlap=100` - Control overlap between chunks
- **Retriever**: Customize the number of retrieved documents
- **LLM Temperature**: Currently set to `0` for deterministic responses

### FastAPI Settings

In `main.py`, you can customize:

- **Host**: Default `0.0.0.0` (accessible from all interfaces)
- **Port**: Default `8000`
- **Reload**: Set to `True` for development, `False` for production

## 🐛 Troubleshooting

### Issue: "GOOGLE_API_KEY not found"
**Solution**: Ensure your `.env` file is in the project root with the correct API key.

### Issue: "No documents found in docs/ directory"
**Solution**: Add PDF files to the `docs/` folder and delete the `chroma_db/` folder to force re-indexing.

### Issue: "Module not found: langchain_community"
**Solution**: Run `pip install -r requirements.txt` to install all dependencies.

### Issue: Vector store loading is slow
**Solution**: This is normal on first run as it indexes all documents. Subsequent runs will use the cached database.

## 📦 Dependencies

See `requirements.txt` for the complete list.

## 🤝 Contributing

To improve this project:

1. Add more Road Code documents to `docs/`
2. Test with various questions
3. Refine the prompt in `rag_agent.py` for better responses
4. Report issues or suggest improvements

## 📝 License

This project is provided as-is for educational purposes related to road safety in Mozambique.

## ❓ FAQ

**Q: Can I use this with my own documents?**  
A: Yes! Replace the PDFs in the `docs/` folder and run with `force_reload=True` to rebuild the vector database.

**Q: How do I update the system prompt?**  
A: Edit the `qa_prompt` in `modules/rag_agent.py` to customize the assistant's behavior.

**Q: Can I deploy this to production?**  
A: Yes! Use a production ASGI server like Gunicorn with Uvicorn workers. See FastAPI deployment docs for details.

**Q: What language should questions be in?**  
A: Portuguese is recommended for best results, but the system may handle other languages.

---

**Happy learning! Stay safe on the road! 🚗🛣️**