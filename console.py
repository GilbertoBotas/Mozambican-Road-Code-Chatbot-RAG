from modules.rag_agent import RAGAgent


def print_response(result):
    """
    Pretty-print the RAG agent response.
    
    Args:
        result: RAGAgentResponse object
    """
    print("\n" + "=" * 80)
    print("RESPOSTA DO ASSISTENTE")
    print("=" * 80)
    
    print("\nResposta:")
    print(result.answer)
    
    if result.articles:
        print("\nArtigos Referenciados:")
        for article in result.articles:
            print(f"  • {article}")
    
    if result.follow_up_questions:
        print("\nPergunta de Acompanhamento Sugeridas:")
        for i, question in enumerate(result.follow_up_questions, 1):
            print(f"  {i}. {question}")
    
    print("=" * 80)


def main():
    print("Bem-vindo ao Assistente do Código de Estrada de Moçambique!")
    print("Inicializando...")
    
    agent = RAGAgent()
    try:
        agent.initialize()
    except Exception as e:
        print(f"Erro ao inicializar o agente: {e}")
        return

    print("\nAgente pronto! Digite 'sair' para encerrar.\n")
    
    while True:
        try:
            query = input("\nComo posso ajudá-lo? > ").strip()
        except KeyboardInterrupt:
            print("\n\nAté logo!")
            break
        
        if query.lower() in ["sair", "adeus", "exit", "quit", "bye"]:
            print("Até logo!")
            break
        
        if not query:
            continue

        print("Pesquisando e gerando resposta...")
        try:
            result = agent.ask(query)
            print_response(result)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    main()