class No:
    def __init__(self, orientacao):
        self.orientacao = orientacao  # O objeto Orientacao que já tens
        self.proximo = None           # Referência explícita para o próximo nó


class ListaEncadeada:
    def __init__(self):
        self.cabeca = None            # Início da lista
        self._tamanho = 3             # Contador de elementos (opcional)

    def esta_vazia(self):
        return self.cabeca is None

    def inserir_fim(self, orientacao):
        """Insere um novo registo no final da lista encadeada (equivalente ao cadastro)."""
        novo_no = No(orientacao)
        if self.esta_vazia():
            self.cabeca = novo_no
        else:
            atual = self.cabeca
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no

    def remover_por_id(self, id_alvo):
        """Exclui um registo ajustando corretamente os ponteiros da lista encadeada."""
        if self.esta_vazia():
            return False

        # Se o nó a remover for a cabeça
        if self.cabeca.orientacao.id == id_alvo:
            self.cabeca = self.cabeca.proximo
            return True

        atual = self.cabeca
        while atual.proximo:
            if atual.proximo.orientacao.id == id_alvo:
                atual.proximo = atual.proximo.proximo  # Pula o nó removido
                return True
            atual = atual.proximo
        return False

    def buscar_por_id(self, id_alvo):
        """Pesquisa um registo pelo identificador único."""
        atual = self.cabeca
        while atual:
            if atual.orientacao.id == id_alvo:
                return atual.orientacao
            atual = atual.proximo
        return None

    def listar_todos(self):
        """Retorna uma lista em Python comum apenas para fins de exibição/iteração."""
        elementos = []
        atual = self.cabeca
        while atual:
            elementos.append(atual.orientacao)
            atual = atual.proximo
        return elementos

    def ordenar_por_titulo(self):
        """
        Ordena os nós da lista encadeada por Bubble Sort / Selection Sort 
        trocando os valores dos dados entre os nós (ou ajustando ponteiros).
        """
        if self.esta_vazia() or self.cabeca.proximo is None:
            return

        trocou = True
        while trocou:
            trocou = False
            atual = self.cabeca
            while atual.proximo:
                if atual.orientacao.titulo > atual.proximo.orientacao.titulo:
                    # Troca os dados (orientações) entre os nós
                    aux = atual.orientacao
                    atual.orientacao = atual.proximo.orientacao
                    atual.proximo.orientacao = aux
                    trocou = True
                atual = atual.proximo