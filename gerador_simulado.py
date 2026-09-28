# ==========================================================
# GERADOR DE SIMULADOS / PROVAS
# ==========================================================

import os

import random

from datetime import datetime

from xml.sax.saxutils import escape


from reportlab.lib.pagesizes import A4

from reportlab.lib.units import cm

from reportlab.lib import colors as rl_colors

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet


from database import buscar_todas_questoes, buscar_questoes_quantidade


# ==========================================================
# TEXTO SEGURO PARA O REPORTLAB
# ==========================================================
# O reportlab trata o texto do Paragraph como XML simplificado,
# então qualquer "<br>" sem fechar, "&", "<" ou ">" colado de
# um site quebra a geração com "paraparser: syntax error".
# Escapamos tudo antes de montar o PDF.

def texto_seguro(texto):

    if texto is None:

        return ""

    texto = str(texto)

    texto = escape(texto)

    texto = texto.replace("\n", "<br/>")

    return texto


# ==========================================================
# CRIAR SIMULADO / PROVA
# ==========================================================
# caminho_pdf: caminho completo escolhido pelo usuário para o
#   arquivo principal (ex.: "C:/Provas/Prova Turma A.pdf").
#   O gabarito é salvo na mesma pasta, com " - Gabarito.pdf"
#   no final do mesmo nome.
#
# tipo_documento: "SIMULADO" ou "PROVA" — só muda o texto do
#   título impresso no PDF.
#
# professor / turma: opcionais, aparecem no cabeçalho impresso.
#
# Retorna um dicionário com os dois caminhos gerados.

def criar_simulado(

        quantidade,

        caminho_pdf,

        tipo_documento="SIMULADO",

        categoria=None,

        professor="",

        turma="",

        titulo=""

):

    if categoria:

        questoes = list(
            buscar_questoes_quantidade(quantidade, categoria)
        )

    else:

        todas = buscar_todas_questoes()

        if not todas:

            raise Exception(
                "Não existem questões cadastradas."
            )

        if quantidade > len(todas):

            quantidade = len(todas)

        questoes = random.sample(todas, quantidade)

    if not questoes:

        raise Exception(
            "Nenhuma questão encontrada para gerar o documento."
        )

    pasta = os.path.dirname(caminho_pdf)

    if pasta:

        os.makedirs(pasta, exist_ok=True)

    nome_base, _ = os.path.splitext(caminho_pdf)

    caminho_gabarito = f"{nome_base} - Gabarito.pdf"

    gerar_pdf_prova(

        caminho_pdf,

        questoes,

        tipo_documento,

        professor,

        turma,

        titulo

    )

    gerar_pdf_gabarito(

        caminho_gabarito,

        questoes,

        tipo_documento,

        professor,

        turma,

        titulo

    )

    return {
        "pdf": caminho_pdf,
        "gabarito": caminho_gabarito,
    }


# ==========================================================
# CABEÇALHO PARA USO EM SALA (professor / aluno / turma / nota)
# ==========================================================

def construir_cabecalho(estilos, tipo_documento, professor, turma, titulo=""):

    elementos = []

    titulo_texto = (
        "PROVA" if tipo_documento == "PROVA" else "SIMULADO"
    )

    texto_titulo_final = (
        texto_seguro(titulo) if titulo and titulo.strip()
        else titulo_texto
    )

    elementos.append(
        Paragraph(
            texto_titulo_final,
            estilos["Title"]
        )
    )

    elementos.append(Spacer(1, 12))

    texto_professor = (
        f"Professor(a): {texto_seguro(professor)}"
        if professor else
        "Professor(a): " + "_" * 32
    )

    texto_turma = (
        f"Turma: {texto_seguro(turma)}"
        if turma else
        "Turma: " + "_" * 14
    )

    dados_tabela = [
        [
            Paragraph(texto_professor, estilos["Normal"]),
            Paragraph(texto_turma, estilos["Normal"]),
        ],
        [
            Paragraph(
                "Nome do Aluno: " + "_" * 48,
                estilos["Normal"]
            ),
            "",
        ],
        [
            Paragraph(
                "Data: ___ / ___ / ______",
                estilos["Normal"]
            ),
            Paragraph(
                "Nota: " + "_" * 10,
                estilos["Normal"]
            ),
        ],
    ]

    tabela = Table(
        dados_tabela,
        colWidths=[10.5 * cm, 6.5 * cm]
    )

    tabela.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.75, rl_colors.HexColor("#C7CCDA")),
        ("BACKGROUND", (0, 0), (-1, -1), rl_colors.HexColor("#F7F8FB")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("SPAN", (0, 1), (1, 1)),
    ]))

    elementos.append(tabela)

    elementos.append(Spacer(1, 22))

    return elementos


# ==========================================================
# PDF DA PROVA / SIMULADO
# ==========================================================

def gerar_pdf_prova(

        caminho,

        questoes,

        tipo_documento,

        professor,

        turma,

        titulo=""

):

    documento = SimpleDocTemplate(
        caminho,
        pagesize=A4,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm
    )

    estilos = getSampleStyleSheet()

    conteudo = []

    conteudo.extend(
        construir_cabecalho(
            estilos, tipo_documento, professor, turma, titulo
        )
    )

    numero = 1

    for q in questoes:

        tipo = q["tipo"] or "MULTIPLA"

        if tipo == "CERTO_ERRADO":

            texto = (
                f"{numero}) {texto_seguro(q['pergunta'])}<br/><br/>"
                f"A) CERTO<br/>"
                f"B) ERRADO"
            )

        else:

            linhas_alternativas = []

            letras = ["A", "B", "C", "D", "E"]

            valores = [
                q["alternativa_a"],
                q["alternativa_b"],
                q["alternativa_c"],
                q["alternativa_d"],
                q["alternativa_e"],
            ]

            for letra, valor in zip(letras, valores):

                if valor and valor.strip():

                    linhas_alternativas.append(
                        f"{letra}) {texto_seguro(valor)}"
                    )

            texto = (
                f"{numero}) {texto_seguro(q['pergunta'])}<br/><br/>"
                + "<br/>".join(linhas_alternativas)
            )

        conteudo.append(
            Paragraph(texto, estilos["Normal"])
        )

        conteudo.append(Spacer(1, 16))

        numero += 1

    documento.build(conteudo)


# ==========================================================
# PDF DO GABARITO (formato compacto: 1D, 2E, 3A ...)
# ==========================================================

def gerar_pdf_gabarito(

        caminho,

        questoes,

        tipo_documento,

        professor,

        turma,

        titulo=""

):

    documento = SimpleDocTemplate(
        caminho,
        pagesize=A4,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm
    )

    estilos = getSampleStyleSheet()

    conteudo = []

    titulo_texto = (
        "PROVA" if tipo_documento == "PROVA" else "SIMULADO"
    )

    texto_titulo_final = (
        texto_seguro(titulo) if titulo and titulo.strip()
        else titulo_texto
    )

    conteudo.append(
        Paragraph(
            f"Gabarito — {texto_titulo_final}",
            estilos["Title"]
        )
    )

    info_extra = []

    if turma:
        info_extra.append(f"Turma: {texto_seguro(turma)}")

    if professor:
        info_extra.append(f"Professor(a): {texto_seguro(professor)}")

    if info_extra:

        conteudo.append(
            Paragraph(
                "  |  ".join(info_extra),
                estilos["Normal"]
            )
        )

    conteudo.append(Spacer(1, 16))

    itens = []

    for numero, q in enumerate(questoes, start=1):

        itens.append(f"{numero}{texto_seguro(q['resposta'])}")

    texto_gabarito = ", ".join(itens)

    estilo_gabarito = estilos["Normal"].clone("gabarito")

    estilo_gabarito.fontSize = 13

    estilo_gabarito.leading = 20

    conteudo.append(
        Paragraph(texto_gabarito, estilo_gabarito)
    )

    documento.build(conteudo)