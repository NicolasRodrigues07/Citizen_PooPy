class Orientacao:
    '''
    Esta é uma classe que guarda informações para dúvidas relacionadas a saúde
    '''

    def __init__(
        self, 
        id,
        categoria,
        titulo,
        palavras_chave,
        resposta,
        onde,
        fonte,
        verificado_em,
        documentos = None,
        detalhes = None
    ):          # Metodo construtor
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em
        self.documentos = documentos if documentos is not None else []
        self.detalhes = detalhes if detalhes is not None else {}

    def exibir(self): 
        print(f"\n{self.titulo}")
        print(self.resposta)
        print(f"\nDocumentos necessários: {self.documentos}")
        print(f"Onde: {self.onde}")
        print(f"Fontes: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")

    def aviso():
        return "Conteúdo apenas informativo. Não substituímos consultas, diagnósticos ou orientações médicas profissionais."
    