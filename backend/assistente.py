import time
import json
import os
import csv

class Assistente:
    def __init__(self, nome, base_conhecimento):
        self.nome = nome
        self.base = base_conhecimento
        self.historico = []
        
        # Caminhos para arquivos de histórico e CSV
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.caminho_historico = os.path.join(diretorio_atual, "..", "data", "historico.json")
        self.caminho_csv = os.path.join(diretorio_atual, "..", "data", "atendimentos.csv")
        
        self.carregar_historico()

    def carregar_historico(self):
        """Carrega o histórico existente do JSON, se houver."""
        if os.path.exists(self.caminho_historico):
            try:
                with open(self.caminho_historico, "r", encoding="utf-8") as f:
                    self.historico = json.load(f)
            except Exception:
                self.historico = []

    def salvar_historico(self):
        """Salva o histórico atualizado no arquivo JSON."""
        try:
            with open(self.caminho_historico, "w", encoding="utf-8") as f:
                json.dump(self.historico, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")

    def validar_dado_pessoal(self, texto):
        """
        Retorna True se encontrar indícios de dados pessoais (8+ dígitos seguidos ou '@').
        Conforme a regra de segurança do projeto.
        """
        if "@" in texto:
            return True
        
        # Verifica se há sequências de 8 ou mais dígitos (como CPF, telefones, etc.)
        digitos_consecutivos = 0
        for caractere in texto:
            if caractere.isdigit():
                digitos_consecutivos += 1
                if digitos_consecutivos >= 8:
                    return True
            else:
                digitos_consecutivos = 0
        return False

    def perguntar(self):
        """
        Loop principal de atendimento ao cidadão no terminal.
        """
        print(f"\n=== Olá! Eu sou o {self.nome} ===")
        print("Digite sua dúvida ou '0' para ver as categorias / sair.")

        while True:
            # Mede o tempo de atendimento
            inicio_tempo = time.time()
            
            pergunta = input("\nDigite sua dúvida (0 para voltar/sair): ").strip()
            
            # Opção de saída ou navegação
            if pergunta == "0":
                print("\nEncerrando atendimento. Até logo!")
                break
            
            # Validação de dados pessoais (Segurança)
            if self.validar_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue
            
            if not pergunta:
                print("Por favor, digite uma pergunta válida.")
                continue

            # Realiza a busca na Base de Conhecimento
            resultados_pontuados = self.base.pontuar(pergunta)
            melhores_resultados = self.base.buscar(pergunta)
            
            encontrou = len(melhores_resultados) > 0
            id_orientacao = None
            
            if encontrou:
                # Pega a pontuação e a melhor orientação da primeira tupla
                maior_pontos, melhor_orientacao = resultados_pontuados[0]
                id_orientacao = melhor_orientacao.id
                
                # Define o nível de confiança[cite: 12]
                if maior_pontos >= 6:
                    confianca = "ALTA"
                elif maior_pontos >= 3:
                    confianca = "MÉDIA"
                else:
                    confianca = "BAIXA"
                
                print(f"\nConfiança da resposta: {confianca} ({maior_pontos} pontos)")
                
                # Exibe a melhor orientação (usando o método exibir da classe Orientacao)
                melhor_orientacao.exibir()
                
                # Exibe até duas alternativas secundárias se existirem[cite: 12, 14]
                if len(resultados_pontuados) > 1:
                    print("\n--- Alternativas relacionadas ---")
                    for idx in range(1, min(3, len(resultados_pontuados))):
                        pts, alt = resultados_pontuados[idx]
                        print(f"• [{alt.categoria}] {alt.titulo} ({pts} pts)")

                # Pergunta se ajudou (s/n) com tratamento de entrada inválida
                ajudou_str = ""
                while ajudou_str not in ["s", "n"]:
                    ajudou_str = input("\nEssa orientação respondeu sua dúvida? (s/n): ").lower().strip()
                    if ajudou_str not in ["s", "n"]:
                        print("Opção inválida. Digite apenas 's' para sim ou 'n' para não.")
                
                ajudou = True if ajudou_str == 's' else False
            else:
                print("\nNão encontrei nenhuma orientação exata para sua dúvida.")
                print("Sugestão: tente usar outras palavras-chave ou navegue pelas categorias digitando 'cat'.")
                ajudou = False

            # Calcula o tempo decorrido em segundos (arredondado a 1 casa decimal)
            tempo_decorrido = round(time.time() - inicio_tempo, 1)

            # Registra o atendimento no histórico
            self.registrar(
                origem="pergunta",
                pergunta=pergunta,
                id_orientacao=id_orientacao,
                encontrou=encontrou,
                ajudou=ajudou,
                tentativas=1,
                tempo=tempo_decorrido
            )

    def registrar(self, origem, pergunta, id_orientacao, encontrou, ajudou, tentativas, tempo):
        """Registra o atendimento na lista de histórico e guarda no JSON."""
        atendimento = {
            "data": time.strftime("%Y-%m-%d %H:%M:%S"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo": tempo
        }
        self.historico.append(atendimento)
        self.salvar_historico()
        self.exportar_csv()

    def exportar_csv(self):
        """Exporta todos os atendimentos para um arquivo CSV usando DictWriter[cite: 13]."""
        if not self.historico:
            return
        
        try:
            chaves = self.historico[0].keys()
            with open(self.caminho_csv, "w", newline="", encoding="utf-8") as f:
                escritor = csv.DictWriter(f, fieldnames=chaves)
                escritor.writeheader()
                escritor.writerows(self.historico)
        except Exception as e:
            print(f"Erro ao exportar CSV: {e}")

    def indicadores(self):
        """Calcula e exibe os indicadores de desempenho exigidos[cite: 13]."""
        total = len(self.historico)
        if total == 0:
            print("\nNenhum atendimento registado ainda.")
            return

        encontrados = sum(1 for h in self.historico if h["encontrou"])
        ajudaram = sum(1 for h in self.historico if h["ajudou"])
        tempo_total = sum(h["tempo"] for h in self.historico)
        
        taxa_encontro = (encontrados / total) * 100
        taxa_ajuda = (ajudaram / total) * 100 if encontrados > 0 else 0
        tempo_medio = tempo_total / total

        print("\n=== Indicadores do Assistente ===")
        print(f"Total de atendimentos: {total}")
        print(f"Resposta encontrada: {taxa_encontro:.1f}%")
        print(f"Taxa de acerto (ajudou): {taxa_ajuda:.1f}%")
        print(f"Tempo médio por atendimento: {tempo_medio}s")