# ==========================================================
# IMPORTADOR DE PDF
# ==========================================================
#
# Extrai questões, alternativas e (quando possível) o gabarito
# de um PDF de prova, para reduzir o trabalho de cadastro manual.
#
# IMPORTANTE — limitações honestas:
# - Funciona com PDFs que têm texto real (não escaneados/imagem).
#   Um PDF escaneado sem OCR não tem texto pra extrair.
# - A separação em questões é feita por heurística (numeração
#   sequencial). Provas com formatação muito fora do padrão
#   podem sair com blocos errados.
# - O gabarito só é preenchido automaticamente se estiver no
#   mesmo PDF, em uma seção reconhecível como "GABARITO".
#   Caso contrário, a resposta fica em branco para revisão manual.
#
# Por isso este módulo NUNCA deve salvar direto no banco — o
# resultado sempre passa por uma tela de revisão antes.
# ==========================================================

import re

from pypdf import PdfReader


# ==========================================================
# EXTRAÇÃO DE TEXTO BRUTO
# ==========================================================

def extrair_texto_pdf(caminho):

    leitor = PdfReader(caminho)

    paginas = []

    for pagina in leitor.pages:

        texto = pagina.extract_text() or ""

        paginas.append(texto)

    return "\n".join(paginas)


# ==========================================================
# PADRÕES DE RECONHECIMENTO
# ==========================================================

# Início de questão: "1.", "01)", "Questão 12 -", "QUESTÃO 5."
PADRAO_QUESTAO = re.compile(
    r'(?:\n|^)\s*(?:QUEST[ÃA]O\s+)?0*(\d{1,3})\s*[\.\)\-–:]\s+',
    re.IGNORECASE
)

# Início de alternativa: "A)", "(A)", "a.", "A -"
PADRAO_ALTERNATIVA = re.compile(
    r'(?:\n|^)\s*\(?([A-Ea-e])\)?\s*[\.\)\-–]\s+'
)

# Cabeçalho de gabarito em qualquer lugar do texto
PADRAO_CABECALHO_GABARITO = re.compile(
    r'GABARITO', re.IGNORECASE
)

# Pares "número + resposta" dentro da área do gabarito
PADRAO_PAR_GABARITO = re.compile(
    r'0*(\d{1,3})\D{0,4}\b([A-Ea-e]|CERTO|ERRADO)\b',
    re.IGNORECASE
)


# ==========================================================
# SEPARAR TEXTO EM BLOCOS DE QUESTÃO
# ==========================================================
# Só aceita números que dão sequência (1, 2, 3, ...) para não
# confundir "100." no meio de um enunciado com uma questão nova.

def localizar_blocos_questao(texto):

    candidatos = list(PADRAO_QUESTAO.finditer(texto))

    aceitos = []

    proximo_esperado = None

    for match in candidatos:

        numero = int(match.group(1))

        if numero < 1 or numero > 300:
            continue

        if proximo_esperado is None:

            # primeira questão aceita: só pode ser 1 (formato mais
            # comum) para evitar começar a sequência em qualquer
            # número aleatório do documento
            if numero != 1:
                continue

            aceitos.append(match)

            proximo_esperado = numero + 1

        elif numero == proximo_esperado:

            aceitos.append(match)

            proximo_esperado = numero + 1

    blocos = []

    for i, match in enumerate(aceitos):

        inicio = match.end()

        fim = (
            aceitos[i + 1].start()
            if i + 1 < len(aceitos)
            else len(texto)
        )

        numero = int(match.group(1))

        conteudo = texto[inicio:fim]

        # Corta fora tudo a partir de um cabeçalho de gabarito
        # que porventura esteja dentro do bloco da última questão
        corte = PADRAO_CABECALHO_GABARITO.search(conteudo)

        if corte:

            conteudo = conteudo[:corte.start()]

        blocos.append((numero, conteudo.strip()))

    return blocos


# ==========================================================
# SEPARAR UM BLOCO EM PERGUNTA + ALTERNATIVAS
# ==========================================================

def separar_pergunta_alternativas(conteudo):

    matches = list(PADRAO_ALTERNATIVA.finditer(conteudo))

    # Filtra só letras em sequência alfabética válida (A, B, C...)
    # começando em A, pra não confundir texto solto com alternativa
    sequencia = []

    esperada = "A"

    for match in matches:

        letra = match.group(1).upper()

        if letra == esperada:

            sequencia.append(match)

            esperada = chr(ord(esperada) + 1)

    if len(sequencia) < 2:

        # Não achou alternativas de verdade -> provavelmente
        # questão do tipo CERTO/ERRADO (comum em provas CESPE)
        return {
            "tipo": "CERTO_ERRADO",
            "pergunta": conteudo.strip(),
            "alternativas": {"A": "", "B": "", "C": "", "D": "", "E": ""}
        }

    pergunta = conteudo[:sequencia[0].start()].strip()

    alternativas = {"A": "", "B": "", "C": "", "D": "", "E": ""}

    for i, match in enumerate(sequencia):

        letra = match.group(1).upper()

        inicio = match.end()

        fim = (
            sequencia[i + 1].start()
            if i + 1 < len(sequencia)
            else len(conteudo)
        )

        alternativas[letra] = conteudo[inicio:fim].strip()

    return {
        "tipo": "MULTIPLA",
        "pergunta": pergunta,
        "alternativas": alternativas
    }


# ==========================================================
# EXTRAIR GABARITO (se existir no PDF)
# ==========================================================

def extrair_gabarito(texto, tipos_por_numero):

    cabecalho = PADRAO_CABECALHO_GABARITO.search(texto)

    if not cabecalho:

        return {}

    area_gabarito = texto[cabecalho.end():]

    respostas = {}

    for match in PADRAO_PAR_GABARITO.finditer(area_gabarito):

        numero = int(match.group(1))

        bruto = match.group(2).upper()

        tipo_questao = tipos_por_numero.get(numero)

        if tipo_questao == "CERTO_ERRADO":

            if bruto in ("C", "CERTO"):
                respostas[numero] = "CERTO"
            elif bruto in ("E", "ERRADO"):
                respostas[numero] = "ERRADO"

        elif tipo_questao == "MULTIPLA":

            if bruto in ("A", "B", "C", "D", "E"):
                respostas[numero] = bruto

    return respostas


# ==========================================================
# FUNÇÃO PRINCIPAL: PDF -> LISTA DE QUESTÕES
# ==========================================================

def importar_questoes_pdf(caminho):

    texto = extrair_texto_pdf(caminho)

    texto_limpo = texto.strip()

    if len(texto_limpo) < 50:

        raise Exception(
            "Não foi possível extrair texto suficiente deste PDF. "
            "Ele pode ser um arquivo escaneado (imagem), que este "
            "importador não consegue ler."
        )

    blocos = localizar_blocos_questao(texto)

    if not blocos:

        raise Exception(
            "Nenhuma questão foi reconhecida neste PDF. O formato "
            "de numeração pode ser diferente do esperado (ex.: "
            "\"1.\", \"Questão 1 -\", \"01)\")."
        )

    questoes = []

    tipos_por_numero = {}

    for numero, conteudo in blocos:

        dados = separar_pergunta_alternativas(conteudo)

        questoes.append({
            "numero": numero,
            "tipo": dados["tipo"],
            "pergunta": dados["pergunta"],
            "alternativas": dados["alternativas"],
            "resposta": None,
        })

        tipos_por_numero[numero] = dados["tipo"]

    gabarito = extrair_gabarito(texto, tipos_por_numero)

    for questao in questoes:

        questao["resposta"] = gabarito.get(questao["numero"])

    return questoes