# prompt.md — Documentação do uso de Inteligência Artificial

## 1. Ferramentas utilizadas

| Ferramenta | Utilização |
|---|---|
| Assistente de IA (ChatGPT) | Apoio na revisão do código, organização da documentação, identificação de inconsistências e sugestão de casos de teste. |

## 2. Exemplos de prompts utilizados

**Prompt 1 — Revisão de código**

> Revise este programa Python de terminal. Identifique erros, entradas inválidas que possam interromper o programa, problemas na leitura e gravação do JSON e oportunidades de melhorar a clareza do código. Explique as alterações sugeridas.

**Prompt 2 — Aderência ao tema**

> Analise se a aplicação ÔnibusCerto está relacionada ao desafio CitizenTech. Considere o cidadão beneficiado, o problema de mobilidade urbana, as funcionalidades e as limitações de utilizar dados simulados.

**Prompt 3 — Experiência do usuário**

> Sugira mensagens de terminal mais claras e acolhedoras para pessoas com diferentes níveis de familiaridade com tecnologia, mantendo o programa simples e sem bibliotecas externas.

**Prompt 4 — Consistência entre código e documentação**

> Compare o código Python com o README e a documentação de IA. Aponte funcionalidades descritas que não estejam implementadas e requisitos do código que não estejam documentados.

**Prompt 5 — Testes**

> Elabore casos de teste para cadastro de linha, registro de atraso e lotação, recomendação, estatísticas, exclusão com confirmação, entrada inválida e leitura de JSON ausente ou corrompido.

## 3. Partes do projeto que receberam apoio de IA

A IA foi utilizada como apoio para:
- Revisar a organização das funções e das mensagens do menu.
- Sugerir validações para entradas numéricas e confirmação de exclusão.
- Identificar a necessidade de conferir a estrutura dos dados JSON.
- Apoiar a revisão da documentação e a elaboração de casos de teste.
- Sugerir clareza na apresentação das estatísticas e das limitações do sistema.

As regras de negócio, o tema, o público-alvo, os dados simulados e a decisão sobre as funcionalidades devem ser revisados e validados pela equipe.

## 4. Verificação humana recomendada

Antes da entrega, a equipe deve executar o programa e conferir, pelo menos:
1. Iniciar o programa e navegar pelo menu.
2. Informar letras em campos que aceitam números e verificar a mensagem de validação.
3. Tentar cadastrar uma linha vazia e uma linha já existente.
4. Registrar atraso nos limites permitidos e tentar valores fora deles.
5. Consultar recomendação e estatísticas.
6. Tentar excluir um registro e responder `N`; verificar que ele permanece.
7. Repetir a exclusão respondendo `S`; verificar que ele é removido.
8. Fechar e abrir novamente o programa para conferir a persistência no JSON.
9. Testar, em uma cópia de segurança, um JSON ausente ou inválido.

**Importante:** esta lista é um roteiro de verificação. Registre como realizados somente os testes que a equipe efetivamente executar.

## 5. Limitações e uso responsável

A IA pode sugerir soluções incorretas ou assumir comportamentos que não foram implementados. Por isso, a equipe deve ler, executar e compreender o código antes da entrega. Os dados de demonstração são simulados e não devem ser apresentados como informações oficiais ou em tempo real.
