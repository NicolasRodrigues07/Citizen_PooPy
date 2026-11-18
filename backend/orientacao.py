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
        self.documentos = documentos if documentos is not None else None
        self.detalhes = detalhes if detalhes is not None else None

    def exibir(self):
        """Exibe os detalhes formatados da orientação no terminal."""
        print(f">> {self.titulo} [{self.categoria}]")
        print(f"{self.resposta}")
        if self.documentos:
            print("Documentos necessários:")
            for doc in self.documentos:
                print(f"  • {doc}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte} (verificado em {self.verificado_em})")
        print("Conteúdo apenas informativo. Não substituímos consultas, diagnósticos ou orientações médicas profissionais.")
    