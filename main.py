base = BaseConhecimento("data/base_conhecimento.json")
base.carregar() # lê o JSON e cria os objetos Orientacao
assistente = Assistente("Citizen Assist AI", base)
assistente.perguntar() # usa base.buscar() e orientacao.exibir()