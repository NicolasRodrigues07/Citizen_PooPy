# Citizen Assist AI: Assistente Digital de Orientação ao Cidadão

Projeto desenvolvido para a GS da disciplina de **Pensamento Computacional e Automação com Python**.

## Integrantes
* **Nícolas Andrade Rodrigues** – RM: 572782
* **Lucas Caram Bueno** - RM: 570158

## Público-Alvo e Problema Escolhido
* **Público-alvo:** Cidadãos em geral que buscam informações rápidas, claras e confiáveis sobre exames médicos, medicamentos comuns e procedimentos básicos de saúde.
* **Problema:** Muitas pessoas enfrentam dificuldades para compreender preparos de exames (como tempo de jejum), regras de prescrição de medicamentos e procedimentos básicos de atendimento. As informações frequentemente encontram-se dispersas em linguagem técnica ou em sites não oficiais, gerando dúvidas e insegurança no cidadão.
* **Solução:** Um assistente digital executado via terminal que centraliza orientações verificadas em fontes oficiais (Ministério da Saúde, ANVISA e sociedades médicas), apresentando os documentos necessários, locais de atendimento e avisos de responsabilidade médica, sem recolher qualquer dado pessoal do utilizador.

##  ODS Relacionados
* **ODS 3 – Saúde e Bem-Estar:** Assegurar uma vida saudável e promover o bem-estar para todos, facilitando o acesso à informação clara e segura sobre medicamentos e exames preventivos. O nosso projeto é uma pequena ajuda para resolver  objetivos da ONU.
* **ODS 16 – Paz, Justiça e Instituições Eficazes:** Desenvolver instituições eficazes, responsáveis e transparentes, garantindo o acesso público à informação oficial de saúde.

##  Estrutura do Repositório
```text
citizen-assist-ai/
├── README.md
├── main.py
└──backend
    ├── orientacao.py
    ├── base_conhecimento.py
    ├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv

```

## Como Executar o Projeto

2. Clone este repositório ou descarregue os ficheiros para o seu computador.
3. No VSCode, navegue até o arquivo principal do projeto (`main.py`).
4. Execute o arquivo

*(Nenhuma biblioteca externa precisa ser instalada; o projeto utiliza apenas módulos nativos do Python como `json`, `os`, `csv` e `time`).*

##  Arquitetura e Regra de Pontuação

O sistema foi estruturado utilizando Programação Orientada a Objetos com três classes principais:

* **`Orientacao`**: Representa cada registo individual da base de conhecimento e realiza a formatação da saída no terminal.


* **`BaseConhecimento`**: Carrega os dados do arquivo JSON, normaliza os textos (removendo acentos, pontuações e convertendo para minúsculas), ordena as categorias utilizando *Selection Sort*(apenas em função de treinamento) e calcula a pontuação de relevância.


* **`Assistente`**: Gerencia o menu interativo, valida e bloqueia dados pessoais (CPFs, telefones ou e-mails), regista o histórico em JSON, exporta relatórios para CSV e calcula os indicadores de desempenho.



### Regra de Pontuação e Confiança

A busca inteligente compara a pergunta normalizada do utilizador com cada orientação da base de conhecimento:

* **+3 pontos:** Para cada palavra-chave (`palavras_chave`) da orientação que aparece na pergunta do utilizador.


* **+1 ponto:** Para cada palavra da pergunta (com 4 ou mais letras) que aparece no título (`titulo`) da orientação.



**Níveis de Confiança Exibidos:**

* **Confiança ALTA:** 6 pontos ou mais.


* **Confiança MÉDIA:** Entre 3 e 5 pontos.


* **Confiança BAIXA / Não encontrado:** Abaixo de 3 pontos (o sistema informa que não encontrou resposta exata e sugere a navegação por categorias).



##  Integrações com Outras Disciplinas

* **Data Structures and Algorithms:** Implementação manual de algoritmos de ordenação (*Selection Sort* para ordenar alfabeticamente as categorias únicas e *Bubble Sort* para ordenar as tuplas de resultados por pontuação) sem depender exclusivamente de funções prontas da linguagem.

##  Fontes Consultadas

Todas as 15 orientações da base de conhecimento foram verificadas em portais institucionais oficiais:

* **Ministério da Saúde / Portal Gov.br:** Protocolos de Hematologia, Guias de Vigilância em Saúde e Agendamento SUS (`gov.br/saude`).
* **ANVISA (Agência Nacional de Vigilância Sanitária):** Bulário Eletrônico Oficial (`consultas.anvisa.gov.br`), regras de medicamentos genéricos/similares, descartes e prazos de receituários (`gov.br/anvisa`).
* **Sociedades Médicas e Secretarias de Saúde:** Sociedade Brasileira de Endoscopia Digestiva (SOBED), Colégio Brasileiro de Radiologia (CBR) e Secretaria Municipal de Saúde (SMS-SP).

## Resultado dos Testes com Usuários

O sistema foi testado com **[4] usuários externos** (familiares da equipe), totalizando **[14] atendimentos** registrados no terminal:

* **Taxa de resposta encontrada:** [92.9%]%


* **Taxa de acerto (ajudou):** [71.4%]%


* **Tempo médio por atendimento:** [169.56428571428572s] segundos


* **Dúvidas sem solução observadas:** Perguntas sobre partes especificas de exames; Variações de exames que não se encontram nas bases de dados; Informações não encontradas por falta de palavras chaves


* **Melhoria aplicada após os testes:** Adição de novas palavras-chave sinónimas nas orientações para ampliar a cobertura de termos populares.



##  Limitações do Assistente

* **Base de conhecimento estática:** O assistente responde estritamente com base nos 15 registros cadastrados no arquivo `data/base_conhecimento.json`, não realizando buscas na internet em tempo real.


* **Busca por regras:** Como utiliza correspondência exata de radicais/palavras normalizadas em vez de modelos de linguagem generativos, erros graves de digitação ou sinónimos muito distantes das palavras-chave cadastradas podem resultar em baixa pontuação.
* **Caráter exclusivamente informativo:** O sistema não substitui consultas, diagnósticos ou prescrições médicas profissionais.

## 🎥 Vídeo Técnico

* **Link da demonstração no YouTube:** 
