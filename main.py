"""
ÔnibusCerto - CitizenTech da Minha Cidade
Global Solution FIAP 2026.2 | Computational Thinking with Python

Integrantes:
- HENRIQUE VIEIRA FERREIRA - RM569586
- LEONARDO BARROCAL - RM571031
- VALDEMAR FORMIGA - RM573382

Aplicação de terminal que ajuda moradores a comparar linhas de ônibus
com base em registros comunitários de atraso e lotação.
Os dados incluídos são simulados para fins educacionais.
"""

import json
from datetime import datetime
from pathlib import Path

# O arquivo JSON fica sempre na mesma pasta deste programa.
ARQUIVO_DADOS = Path(__file__).resolve().parent / "dados.json"

ATRASO_MIN, ATRASO_MAX = 0, 180
LOTACAO_MIN, LOTACAO_MAX = 1, 3
ROTULOS_LOTACAO = ("vazio", "normal", "lotado")
LIMITE_ATRASO_NORMAL = 7
LIMITE_ATRASO_CRITICO = 12
LIMITE_LOTACAO_ATENCAO = 2.5
PESO_LOTACAO = 3
QTD_REGISTROS_ANALISE = 5
LARGURA_COLUNA_LINHA = 51


def dados_iniciais():
    """Retorna a estrutura vazia usada quando ainda não há arquivo de dados."""
    return {
        "bairro": "Vila Yara - Osasco",
        "fonte": "Dados simulados para fins educacionais",
        "linhas": [],
        "registros": [],
    }


def validar_estrutura(dados):
    """Confere os campos e tipos essenciais do JSON antes de usá-lo."""
    if not isinstance(dados, dict):
        return False
    if not isinstance(dados.get("linhas"), list):
        return False
    if not isinstance(dados.get("registros"), list):
        return False
    if not all(isinstance(linha, str) and linha.strip() for linha in dados["linhas"]):
        return False

    for registro in dados["registros"]:
        if not isinstance(registro, dict):
            return False
        if not isinstance(registro.get("linha"), str):
            return False
        atraso = registro.get("atraso_min")
        lotacao = registro.get("lotacao")
        horario = registro.get("horario")
        if not isinstance(atraso, int) or isinstance(atraso, bool):
            return False
        if not ATRASO_MIN <= atraso <= ATRASO_MAX:
            return False
        if not isinstance(lotacao, int) or isinstance(lotacao, bool):
            return False
        if not LOTACAO_MIN <= lotacao <= LOTACAO_MAX:
            return False
        if not isinstance(horario, str):
            return False
    return True


def salvar_dados(dados, mensagem=""):
    """Grava os dados no JSON e informa falhas de acesso ao arquivo."""
    try:
        with ARQUIVO_DADOS.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        if mensagem:
            print(f"[OK] {mensagem}")
        return True
    except OSError as erro:
        print(f"[!] Não foi possível salvar os dados: {erro}")
        return False


def carregar_dados():
    """Carrega e valida o JSON; cria uma base vazia se o arquivo não existir."""
    try:
        with ARQUIVO_DADOS.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print("[i] Arquivo de dados não encontrado. Criando uma base inicial.")
        dados = dados_iniciais()
        salvar_dados(dados)
        return dados
    except json.JSONDecodeError:
        print("[!] O JSON está inválido. Uma base vazia será utilizada.")
        return dados_iniciais()
    except OSError as erro:
        print(f"[!] Não foi possível ler os dados: {erro}")
        return dados_iniciais()

    if not validar_estrutura(dados):
        print("[!] A estrutura do JSON está inválida ou incompleta.")
        print("[i] Uma base vazia será utilizada para evitar falhas.")
        return dados_iniciais()
    return dados


def ler_inteiro(mensagem, minimo, maximo):
    """Solicita um inteiro dentro do intervalo permitido."""
    while True:
        try:
            valor = int(input(mensagem).strip())
        except ValueError:
            print("[!] Digite um número inteiro válido.")
            continue

        if valor < minimo or valor > maximo:
            print(f"[!] O valor deve estar entre {minimo} e {maximo}.")
        else:
            return valor


def ler_confirmacao(mensagem):
    """Retorna True para sim e False para não, aceitando variações comuns."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("[!] Responda com S para sim ou N para não.")


def escolher_linha(dados):
    """Mostra as linhas cadastradas e devolve a escolhida pelo usuário."""
    linhas = dados["linhas"]
    if not linhas:
        print("Nenhuma linha cadastrada. Use a opção 6 para cadastrar.")
        return None

    print("\nLinhas cadastradas:")
    for posicao, linha in enumerate(linhas, start=1):
        print(f"  {posicao} - {linha}")
    escolha = ler_inteiro("Escolha a linha pelo número: ", 1, len(linhas))
    return linhas[escolha - 1]


def registros_da_linha(registros, linha, limite):
    """Filtra os registros de uma linha e mantém somente os mais recentes."""
    encontrados = []
    for registro in registros:
        if registro["linha"] == linha:
            encontrados.append(registro)
    if limite <= 0:
        return encontrados
    return encontrados[-limite:]


def calcular_medias(registros):
    """Calcula as médias de atraso e lotação; retorna None sem registros."""
    if not registros:
        return None

    soma_atraso = 0
    soma_lotacao = 0
    for registro in registros:
        soma_atraso += registro["atraso_min"]
        soma_lotacao += registro["lotacao"]

    total = len(registros)
    return soma_atraso / total, soma_lotacao / total


def classificar(atraso_medio, lotacao_media):
    """Classifica a situação da linha conforme os limites do projeto."""
    if atraso_medio > LIMITE_ATRASO_CRITICO:
        return "CRITICO"
    elif atraso_medio > LIMITE_ATRASO_NORMAL or lotacao_media >= LIMITE_LOTACAO_ATENCAO:
        return "ATENCAO"
    else:
        return "NORMAL"


def analisar_linhas(dados):
    """Calcula médias e pontuação para cada linha que possui registros."""
    analise = {}
    for linha in dados["linhas"]:
        recentes = registros_da_linha(
            dados["registros"], linha, QTD_REGISTROS_ANALISE
        )
        medias = calcular_medias(recentes)
        if medias is None:
            continue

        atraso, lotacao = medias
        pontuacao = atraso + PESO_LOTACAO * (lotacao - 1)
        analise[linha] = (
            atraso,
            lotacao,
            classificar(atraso, lotacao),
            pontuacao,
        )
    return analise


def recomendar_linha(analise):
    """Retorna a linha de menor pontuação ou None se não houver análise."""
    melhor = None
    menor_pontuacao = None
    for linha, (_, _, _, pontuacao) in analise.items():
        if menor_pontuacao is None or pontuacao < menor_pontuacao:
            melhor = linha
            menor_pontuacao = pontuacao
    return melhor


def registrar_ocorrencia(dados):
    """Registra atraso e lotação informados pelo usuário."""
    linha = escolher_linha(dados)
    if linha is None:
        return

    atraso = ler_inteiro(
        f"Atraso em minutos ({ATRASO_MIN} a {ATRASO_MAX}): ",
        ATRASO_MIN,
        ATRASO_MAX,
    )
    lotacao = ler_inteiro(
        "Lotação (1=vazio, 2=normal, 3=lotado): ",
        LOTACAO_MIN,
        LOTACAO_MAX,
    )
    dados["registros"].append({
        "linha": linha,
        "atraso_min": atraso,
        "lotacao": lotacao,
        "horario": datetime.now().strftime("%H:%M"),
    })
    salvar_dados(dados, "Registro salvo!")


def consultar_recomendacao(dados):
    """Exibe a situação das linhas e recomenda a menor pontuação."""
    analise = analisar_linhas(dados)
    if not analise:
        print("Ainda não há registros suficientes para recomendar uma linha.")
        return

    print(f"\nAnalisando até os últimos {QTD_REGISTROS_ANALISE} registros de cada linha:\n")
    for linha, (atraso, lotacao, status, _) in analise.items():
        print(
            f"Linha {linha} -> atraso médio {atraso:4.1f} min | "
            f"lotação média {lotacao:.1f} | {status}"
        )

    recomendada = recomendar_linha(analise)
    print(f"\n>> Recomendação: considere a linha {recomendada} (menor pontuação estimada).")
    print("[i] Recomendação baseada em registros comunitários simulados, não em GPS ao vivo.")


def mostrar_estatisticas(dados):
    """Exibe total, médias, valores mínimo/máximo e situação de uma linha."""
    linha = escolher_linha(dados)
    if linha is None:
        return

    registros = registros_da_linha(dados["registros"], linha, 0)
    medias = calcular_medias(registros)
    if medias is None:
        print(f"A linha {linha} ainda não possui registros.")
        return

    atraso_medio, lotacao_media = medias
    atrasos = []
    lotacoes = []
    for registro in registros:
        atrasos.append(registro["atraso_min"])
        lotacoes.append(registro["lotacao"])

    print(f"\n--- Estatísticas da linha {linha} ---")
    print(f"Total de registros : {len(registros)}")
    print(f"Atraso médio       : {atraso_medio:.1f} min")
    print(f"Atraso mínimo      : {min(atrasos)} min")
    print(f"Atraso máximo      : {max(atrasos)} min")
    print(f"Lotação média      : {lotacao_media:.1f}")
    print(f"Lotação mínima     : {min(lotacoes)} ({ROTULOS_LOTACAO[min(lotacoes) - 1]})")
    print(f"Lotação máxima     : {max(lotacoes)} ({ROTULOS_LOTACAO[max(lotacoes) - 1]})")
    print(f"Situação geral     : {classificar(atraso_medio, lotacao_media)}")


def listar_registros(dados):
    """Lista todos os registros armazenados."""
    registros = dados["registros"]
    if not registros:
        print("Nenhum registro salvo ainda.")
        return

    print(f"\n{'Nº':>4} | {'Linha':<{LARGURA_COLUNA_LINHA}} | Atraso | Lotação | Horário")
    for posicao, registro in enumerate(registros, start=1):
        rotulo = ROTULOS_LOTACAO[registro["lotacao"] - 1]
        print(
            f"{posicao:4} | {registro['linha']:<{LARGURA_COLUNA_LINHA}} | "
            f"{registro['atraso_min']:3} min | {rotulo:7} | {registro['horario']}"
        )


def remover_registro(dados):
    """Remove um registro somente após confirmação explícita."""
    registros = dados["registros"]
    if not registros:
        print("Não há registros para remover.")
        return

    listar_registros(dados)
    numero = ler_inteiro(
        f"\nNúmero do registro a remover (0 a {len(registros)}, 0 para cancelar): ",
        0,
        len(registros),
    )
    if numero == 0:
        print("Remoção cancelada.")
        return

    registro = registros[numero - 1]
    print(
        f"Você selecionou: linha {registro['linha']}, "
        f"atraso {registro['atraso_min']} min, horário {registro['horario']}."
    )
    if not ler_confirmacao("Confirma a remoção deste registro? (S/N): "):
        print("Remoção cancelada. Nenhum dado foi alterado.")
        return

    registros.pop(numero - 1)
    salvar_dados(dados, "Registro removido com sucesso.")


def cadastrar_linha(dados):
    """Cadastra uma linha, impedindo nome vazio ou duplicado."""
    while True:
        linha = input("Número/nome da nova linha: ").strip()
        if not linha:
            print("[!] O nome da linha não pode ficar vazio.")
        elif linha in dados["linhas"]:
            print("[!] Essa linha já está cadastrada.")
        else:
            break

    dados["linhas"].append(linha)
    salvar_dados(dados, f"Linha {linha} cadastrada!")


def exibir_menu(bairro):
    """Mostra o menu principal."""
    print(f"\n=== ÔnibusCerto | {bairro} ===")
    print("1 - Registrar ocorrência (atraso/lotação)")
    print("2 - Qual ônibus pegar agora?")
    print("3 - Estatísticas de uma linha")
    print("4 - Listar registros")
    print("5 - Remover registro")
    print("6 - Cadastrar nova linha")
    print("0 - Sair")


def main():
    """Executa o fluxo principal do sistema."""
    dados = carregar_dados()

    while True:
        exibir_menu(dados.get("bairro", "Meu bairro"))
        opcao = ler_inteiro("Escolha: ", 0, 6)

        match opcao:
            case 1:
                registrar_ocorrencia(dados)
            case 2:
                consultar_recomendacao(dados)
            case 3:
                mostrar_estatisticas(dados)
            case 4:
                listar_registros(dados)
            case 5:
                remover_registro(dados)
            case 6:
                cadastrar_linha(dados)
            case 0:
                print("Até logo! Bom trajeto.")
                break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado pelo usuário.")
