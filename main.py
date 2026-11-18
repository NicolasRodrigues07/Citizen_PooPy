from backend.base_conhecimento import BaseConhecimento
from backend.assistente import Assistente

if __name__ == "__main__":
    # Inicializa a base de conhecimento carregando o JSON
    base = BaseConhecimento()
    base.carregar()
    
    # Inicializa o assistente digital
    assistente = Assistente("Citizen Assist AI", base)
    
    # Inicia o atendimento no terminal
    assistente.perguntar()
    
    # Ao sair, exibe os indicadores finais de desempenho
    assistente.indicadores()