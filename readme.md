# ÔnibusCerto

## 1. Identificação do projeto

| Campo | Descrição |
|---|---|
| **Projeto** | ÔnibusCerto |
| **Disciplina** | Computational Thinking with Python |
| **Global Solution** | FIAP 2026.2 — CitizenTech |
| **Região de referência** | Vila Yara — Osasco |
| **Público beneficiado** | Moradores e trabalhadores que utilizam transporte público na região metropolitana de São Paulo |
| **Problema** | O usuário pode enfrentar atrasos e lotação sem ter informações comunitárias organizadas para comparar as linhas disponíveis. |

## 2. Objetivo e funcionamento

O ÔnibusCerto é uma aplicação de terminal que permite cadastrar linhas, registrar informações comunitárias de atraso e lotação, consultar estatísticas e comparar linhas por uma pontuação estimada.

O sistema utiliza dados simulados armazenados localmente em `dados.json`. Portanto, não consulta GPS, horários oficiais ou posição de ônibus em tempo real. Os resultados servem para demonstrar a lógica da solução acadêmica.

## 3. Integrantes

- HENRIQUE VIEIRA FERREIRA — RM569586
- LEONARDO BARROCAL — RM571031
- VALDEMAR FORMIGA — RM573382

## 4. Funcionalidades

| Opção | Funcionalidade |
|---|---|
| 1 | Registrar ocorrência: linha, atraso em minutos e lotação |
| 2 | Comparar linhas com registros e apresentar uma recomendação |
| 3 | Consultar estatísticas: total, médias, mínimos, máximos e situação |
| 4 | Listar todos os registros |
| 5 | Remover registro após confirmação do usuário |
| 6 | Cadastrar uma nova linha, sem permitir nome vazio ou duplicado |
| 0 | Encerrar o programa |

## 5. Regras de classificação e recomendação

A classificação utiliza as médias dos registros da linha:

| Situação | Regra |
|---|---|
| **NORMAL** | Atraso médio de até 7 minutos e lotação média abaixo de 2,5 |
| **ATENÇÃO** | Atraso médio acima de 7 e até 12 minutos, ou lotação média a partir de 2,5 |
| **CRÍTICO** | Atraso médio acima de 12 minutos |

A análise de recomendação considera até os cinco registros mais recentes de cada linha. A pontuação é:

`atraso médio + 3 × (lotação média − 1)`

Quanto menor a pontuação, melhor a classificação comparativa dentro dos dados cadastrados. A recomendação não substitui informações oficiais de transporte.

## 6. Requisitos e execução

- Python 3.10 ou superior (necessário para `match/case`).
- Não utiliza bibliotecas externas.
- Os arquivos `main.py` e `dados.json` devem permanecer na mesma pasta.

No terminal, entre na pasta do projeto e execute:

```bash
python main.py
```

Em alguns computadores Windows, pode ser necessário:

```bash
py main.py
```

O arquivo `dados.json` contém dados simulados de demonstração. O programa lê e grava as alterações nesse arquivo. Se o arquivo não existir, uma base vazia será criada. Se o conteúdo estiver inválido, o programa avisa e inicia com uma estrutura vazia; nesse caso, restaure uma cópia válida do JSON se quiser recuperar os dados anteriores.

## 7. Conceitos de programação aplicados

- **Decisão:** `if`, `elif`, `else` e `match/case`.
- **Repetição:** `while` para menu e validações; `for` para percorrer linhas e registros.
- **Funções:** funções com parâmetros e valores de retorno.
- **Estruturas de dados:** listas, tuplas e dicionários.
- **Persistência:** leitura e gravação de dados em JSON.
- **Validação:** limites numéricos, opção de menu, linha vazia e duplicada, confirmação de exclusão.
- **Tratamento de exceções:** `try/except` para entradas, arquivos e JSON inválido.

## 8. Estrutura de arquivos

```text
onibus_certo/
├── main.py
├── dados.json
├── readme.md
└── prompt.md
```

## 9. Dados e impacto esperado

Os dados do arquivo `dados.json` são simulados para fins educacionais e não representam medições oficiais ou atuais das linhas. O indicador demonstrado pelo programa é o atraso médio por linha, acompanhado da lotação média e da comparação entre linhas com dados disponíveis.

O projeto se relaciona principalmente ao **ODS 11 — Cidades e Comunidades Sustentáveis**, especialmente ao tema de acesso a transporte público, e ao **ODS 10 — Redução das Desigualdades**, ao propor uma forma simples de organizar informações comunitárias.

## 10. Limitações conhecidas

- Não há integração com API de transporte público.
- Não há localização GPS ou previsão em tempo real.
- Os registros dependem de preenchimento manual.
- A qualidade das recomendações depende da quantidade e confiabilidade dos registros informados.
