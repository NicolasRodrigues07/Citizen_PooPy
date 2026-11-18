import time
import json
import os
import csv

class Assistente:
    def __init__(self, nome, base_conhecimento):
        self.nome = nome
        self.base = base_conhecimento
        self.historico = []
        
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        self.caminho_historico = os.path.join(diretorio_atual, "..", "data", "historico.json")
        self.caminho_csv = os.path.join(diretorio_atual, "..", "data", "atendimentos.csv")
        
        self.carregar_historico()

    def carregar_historico(self):
        """Carrega o histórico existente do JSON, se houver."""
        if os.path.exists(self.caminho_historico):
            try:
                with open(self.caminho_historico, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    if isinstance(dados, list):
                        self.historico = [h for h in dados if isinstance(h, dict)]
                    else:
                        self.historico = []
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
        Menu principal do assistente: escolhe entre Perguntar, Navegar ou Sair.
        """
        print(f"\n=== Olá! Eu sou o {self.nome} ===")

        while True:
            print("\n--- Menu Principal ---")
            print("[1] Fazer uma pergunta (Busca inteligente)")
            print("[2] Navegar por categorias")
            print("[3] Sair")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self._loop_perguntas()
            elif opcao == "2":
                self.navegar()
            elif opcao == "3" or opcao == "0":
                print("\nEncerrando atendimento. Até logo!")
                break
            else:
                print("Opção inválida. Digite 1, 2 ou 3.")

    def _loop_perguntas(self):
        """Loop interno para perguntas em texto livre."""
        print("\n--- Modo Pergunta (Digite '0' para voltar ao menu) ---")
        while True:
            inicio_tempo = time.time()
            pergunta = input("\nDigite sua dúvida: [0 para voltar]").strip()
            
            if pergunta == "0":
                break
            
            if self.validar_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue
            
            if not pergunta:
                print("Por favor, digite uma pergunta válida.")
                continue

            resultados_pontuados = self.base.pontuar(pergunta)
            melhores_resultados = self.base.buscar(pergunta)
            
            encontrou = len(melhores_resultados) > 0
            id_orientacao = None
            
            if encontrou:
                maior_pontos, melhor_orientacao = resultados_pontuados[0]
                id_orientacao = melhor_orientacao.id
                
                confianca = "ALTA" if maior_pontos >= 6 else ("MÉDIA" if maior_pontos >= 3 else "BAIXA")
                print(f"\nConfiança da resposta: {confianca} ({maior_pontos} pontos)")
                
                melhor_orientacao.exibir()
                
                if len(resultados_pontuados) > 1:
                    print("\n--- Alternativas relacionadas ---")
                    for idx in range(1, min(3, len(resultados_pontuados))):
                        pts, alt = resultados_pontuados[idx]
                        print(f"• [{alt.categoria}] {alt.titulo} ({pts} pts)")

                ajudou_str = ""
                while ajudou_str not in ["s", "n"]:
                    ajudou_str = input("\nEssa orientação respondeu sua dúvida? (s/n): ").lower().strip()
                    if ajudou_str not in ["s", "n"]:
                        print("Opção inválida. Digite apenas 's' ou 'n'.")
                
                ajudou = (ajudou_str == 's')
            else:
                print("\nNão encontrei nenhuma orientação exata para sua dúvida.")
                ajudou = False

            tempo_decorrido = round(time.time() - inicio_tempo, 1)
            self.registrar(
                origem="pergunta",
                pergunta=pergunta,
                id_orientacao=id_orientacao,
                encontrou=encontrou,
                ajudou=ajudou,
                tentativas=1,
                tempo=tempo_decorrido
            )

    def navegar(self):
        """
        Permite navegar por categorias, listar orientações e ver detalhes específicos.
        Cumpre a regra do '0 para voltar' em todas as telas.
        """
        while True:
            categorias = self.base.categorias()
            print("\n=== Navegação por Categorias ===")
            print("[0] Voltar ao menu principal")
            for idx, cat in enumerate(categorias, 1):
                print(f"[{idx}] {cat}")
            
            escolha_cat = input("\nEscolha o número da categoria (ou 0 para voltar): ").strip()
            
            if escolha_cat == "0":
                break
            
            if escolha_cat.isdigit():
                num_cat = int(escolha_cat)
                if 1 <= num_cat <= len(categorias):
                    cat_escolhida = categorias[num_cat - 1]
                    
                    while True:
                        orientacoes_cat = self.base.por_categoria(cat_escolhida)
                        print(f"\n--- Orientações em [{cat_escolhida}] ---")
                        print("[0] Voltar às categorias")
                        for o_idx, orient in enumerate(orientacoes_cat, 1):
                            print(f"[{o_idx}] {orient.titulo}")
                        
                        escolha_ori = input("\nEscolha o número da orientação (ou 0 para voltar): ").strip()
                        
                        if escolha_ori == "0":
                            break
                        
                        if escolha_ori.isdigit():
                            num_ori = int(escolha_ori)
                            if 1 <= num_ori <= len(orientacoes_cat):
                                orient_selecionada = orientacoes_cat[num_ori - 1]
                                
                                print("\n" + "="*40)
                                orient_selecionada.exibir()
                                
                                if hasattr(orient_selecionada, 'detalhes') and orient_selecionada.detalhes:
                                    print("\n--- Informações Adicionais / Detalhes ---")
                                    if isinstance(orient_selecionada.detalhes, dict):
                                        for chave, valor in orient_selecionada.detalhes.items():
                                            print(f"• {chave.capitalize()}: {valor}")
                                    else:
                                        print(f"• {orient_selecionada.detalhes}")
                                print("="*40)
                                
                                input("\nPressione Enter para continuar...")
                            else:
                                print("Número da orientação inválido.")
                        else:
                            print("Entrada inválida. Digite um número.")
                else:
                    print("Número da categoria inválido.")
            else:
                print("Entrada inválida. Digite um número.")

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
        """Exporta todos os atendimentos para um arquivo CSV usando DictWriter."""
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
        """Calcula e exibe os indicadores de desempenho exigidos."""
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