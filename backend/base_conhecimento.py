import json
import os
from .orientacao import Orientacao

class BaseConhecimento:

    ACENTOS = {
    "á": "a", 
    "à": "a", 
    "ã": "a", 
    "â": "a", 
    "é": "e", 
    "ê": "e",
    "í": "i",
    "ó": "o",
    "õ": "o",
    "ô": "o",
    "ú": "u",
    "ç": "c"
    }

    def __init__(self, caminho=None):
        if caminho is None:
            # Alterações feitas pois em outra IDE não estava funcionando
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            self.caminho = os.path.join(diretorio_atual, "..", "data", "base_conhecimento.json")
        else:
            self.caminho = caminho
            
        self.orientacoes = []

    @staticmethod # Método independente
    def normalizar(texto):
        texto = texto.lower().strip()
        for letra, troca in BaseConhecimento.ACENTOS.items():
            texto = texto.replace(letra, troca)
        for sinal in "?!.,;:()":
            texto = texto.replace(sinal, " ")
        return " " + " ".join(texto.split()) + " "
    
    def carregar(self):
        if not os.path.exists(self.caminho):
            print(f"Aviso: O arquivo '{self.caminho}' não foi encontrado.")
            return

        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

                lista_itens = dados.get("orientacoes", [])
                
                self.orientacoes = []
                for item in lista_itens:
                    orientacao = Orientacao(
                        # Usamos o get para o programa não retornar KeyError
                        id=item.get("id"),      
                        categoria=item.get("categoria"),
                        titulo=item.get("titulo"),
                        palavras_chave=item.get("palavras_chave", []),
                        resposta=item.get("resposta"),
                        onde=item.get("onde"),
                        fonte=item.get("fonte"),
                        verificado_em=item.get("verificado_em"),
                        documentos=item.get("documentos"),
                        detalhes=item.get("detalhes")
                    )
                    self.orientacoes.append(orientacao)
                    
            print(f"Base carregada com sucesso! {len(self.orientacoes)} orientações carregadas.")
            
        except Exception as e:
            print(f"Erro ao carregar o arquivo JSON: {e}")

    def categorias(self):
        """
        Retorna uma lista contendo os nomes de todas as categorias únicas, ordenadas alfabeticamente.
        """
        cats = set()  # Conjunto para evitar categorias duplicadas
        
        for orientacao in self.orientacoes:
            if orientacao.categoria:
                cats.add(orientacao.categoria)
                
        lista_cats = list(cats)
        
        # Algoritmo Selection Sort para complementar a GS de Data Structure
        n = len(lista_cats)
        for i in range(n):
            indice_menor = i
            for j in range(i + 1, n):
                if lista_cats[j] < lista_cats[indice_menor]:
                    indice_menor = j
            
            if indice_menor != i:
                aux = lista_cats[i]
                lista_cats[i] = lista_cats[indice_menor]
                lista_cats[indice_menor] = aux
                
        return lista_cats

    def por_categoria(self, nome_categoria):
        """
        Retorna as orientações de uma categoria comparando de forma normalizada.
        """
        filtradas = []
        
        cat_buscada = self.normalizar(nome_categoria)
        
        for orientacao in self.orientacoes:
            cat_orientacao = self.normalizar(orientacao.categoria)
            
            if cat_orientacao == cat_buscada:
                filtradas.append(orientacao)
                
        return filtradas

    def pontuar(self, pergunta):
        """
        Compara a pergunta com todas as orientações e calcula os pontos:
        - +3 pontos se a palavra-chave aparece na pergunta.
        - +1 ponto para cada palavra da pergunta (4+ letras) que aparece no título.
        Retorna uma lista de tuplas ordenadas da maior para a menor pontuação: [(pontos, orientacao), ...]
        """
        pergunta_norm = self.normalizar(pergunta)
        palavras_pergunta = pergunta_norm.split()
        
        resultados = []
        
        for orientacao in self.orientacoes:
            pontos = 0
            
            if orientacao.palavras_chave:
                for pc in orientacao.palavras_chave:
                    pc_norm = self.normalizar(pc)
                    if pc_norm and pc_norm in pergunta_norm:
                        # Valida se a palavra-chave não é vazia (and) e se ela está na pergunta
                        pontos += 3
            
            if orientacao.titulo:
                titulo_norm = self.normalizar(orientacao.titulo)
                palavras_titulo = titulo_norm.split()
                
                for palavra in palavras_pergunta:
                    if len(palavra) >= 4 and palavra in palavras_titulo:
                        pontos += 1
            
            if pontos > 0:
                resultados.append((pontos, orientacao))
                
        n = len(resultados)
        for i in range(n):
            for j in range(0, n - i - 1):
                if resultados[j][0] < resultados[j + 1][0]:
                    aux = resultados[j]
                    resultados[j] = resultados[j + 1]
                    resultados[j + 1] = aux
        
        return resultados

    def buscar(self, pergunta):
        """
        Busca as orientações com base na pergunta do usuário 
        e retorna até os 2 melhores resultados encontrados.
        """
        resultados_pontuados = self.pontuar(pergunta)
        
        melhores_resultados = []
        
        quantidade = 2 if len(resultados_pontuados) >= 2 else len(resultados_pontuados)
        
        for i in range(quantidade):
            pontos, orientacao = resultados_pontuados[i]
            melhores_resultados.append(orientacao)
            
        return melhores_resultados