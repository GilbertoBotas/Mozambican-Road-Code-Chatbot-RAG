import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_community.document_loaders import DirectoryLoader, UnstructuredMarkdownLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import warnings
from modules.file_manager import validate_and_load_environment

validate_and_load_environment()

warnings.filterwarnings("ignore", category=UserWarning, message="Pydantic serializer warnings")

# ── Structured output schema ───────────────────────────────────────────────

class RAGAgentResponse(BaseModel):
    """Structured response from the RAG agent."""
    answer: str = Field(description="The natural language answer to the user's prompt")
    articles: Optional[list[str]] = Field(
        default=None,
        description="List of articles (name and number) referenced in the answer, if any"
    )
    follow_up_questions: Optional[list[str]] = Field(
        default=None,
        description="A list of suggested follow-up questions the user might ask next."
    )

class RAGAgent:
    def __init__(self):
        """
        Initialize RAG Agent with Google Gemini API.
        """
        self.docs_dir = "docs"
        self.db_dir = "chroma_db"
        
        # Use Google Gemini embeddings and LLM
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", task_type="retrieval_document")
        self.llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite", temperature=0)
        self.structured_llm = self.llm.with_structured_output(RAGAgentResponse)
        
        self.vector_store = None
        self.chain = None

    def initialize(self, force_reload=False):
        """Initializes the vector store and the RAG chain."""

        # ── Build or load vector store ────────────────────────────────────────
        if not os.path.exists(self.db_dir) or force_reload:
            print(f"Building vector store from {self.docs_dir}...")
            
            # Load markdown documents
            loader = DirectoryLoader(
                self.docs_dir, 
                glob="./*.md", # change to glob="./*.md" if you want to load markdown files
                loader_cls=UnstructuredMarkdownLoader # change to UnstructuredMarkdownLoader if you want to load markdown files
            )
            documents = loader.load()
            
            # Split documents into chunks
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500, 
                chunk_overlap=100
            )
            splits = splitter.split_documents(documents)
            
            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings,
                persist_directory=self.db_dir
            )
        else:
            print(f"Loading vector store from {self.db_dir}...")
            self.vector_store = Chroma(
                persist_directory=self.db_dir,
                embedding_function=self.embeddings
            )

        # ── Create retriever ──────────────────────────────────────────────────
        retriever = self.vector_store.as_retriever()

        # ── QA Prompt ──────────────────────────
        qa_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                You are a virtual instructor specialized in the Mozambique Road Code (Código de Estrada).
                Your mission is to help drivers, driving students, and citizens understand
                the traffic rules, road signals, driver duties, penalties, safety procedures,
                and good driving practices.
                
                You will receive a CONTEXT containing excerpts from the Mozambique Road Code.
                Your responses must be based primarily on this context.

                RULES:
                1. Always respond in clear and accessible Portuguese.
                2. Explain the rules in an educational way, like a driving instructor or traffic officer.
                3. If the context contains the answer, base your explanation on the information provided.
                4. If the context does not contain sufficient information to answer safely, clearly state:
                   "Não encontrei informação suficiente no Código de Estrada fornecido para responder a essa questão."
                5. Never invent articles, fines, penalties, or rules not supported by the context.
                6. If the question is ambiguous, ask for clarification before answering.
                7. When appropriate, present the answer in bullet points for easy reading.
                8. The main goal is to teach and promote safe and responsible driving.

                Recommended response structure:
                - Direct answer
                - Explanation of the rule
                - Practical example (when applicable)
                - Reference of article number and name (when available)

                CONTEXT:
                {context}
                """
            ),
            ("human", "{input}")
        ])

        # ── Chain: retriever → format docs → structured LLM ──────────────────
        def format_docs(inputs: dict) -> dict:
            """Formats retrieved docs into a context string."""
            docs = inputs["context"]
            formatted_context = "\n\n".join(doc.page_content for doc in docs)
            inputs["context"] = formatted_context
            return inputs

        # Build the chain
        self.chain = (
            {"context": retriever, "input": RunnablePassthrough()}
            | RunnableLambda(format_docs)
            | qa_prompt
            | self.structured_llm
        )

    def ask(self, query: str) -> RAGAgentResponse:
        """
        Get a structured response for the given query.
        
        Args:
            query: User's question
            
        Returns:
            RAGAgentResponse: Structured response with answer, articles, and follow-up questions
            
        Raises:
            ValueError: If RAGAgent not initialized
        """
        if not self.chain:
            raise ValueError("RAGAgent not initialized. Call initialize() first.")
        
        result = self.chain.invoke(query) 
        return result