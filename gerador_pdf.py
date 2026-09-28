from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    PageBreak

)


from reportlab.lib.styles import getSampleStyleSheet


from database import (

    buscar_todas_questoes

)


# =====================================================
# TEXTO SEGURO PARA O REPORTLAB
# =====================================================
# O reportlab interpreta o texto do Paragraph como um XML
# simplificado. Qualquer "<", ">" ou "&" que vier colado de
# um site/PDF (ex.: "<br>" sem fechar) quebra o parser dele
# com "paraparser: syntax error". Por isso todo texto que
# vem do banco de dados passa por aqui antes de entrar em
# um Paragraph — assim vira texto literal e nunca quebra o
# PDF, não importa o que tenha sido colado na questão.

def texto_seguro(texto):

    if texto is None:

        return ""

    texto = str(texto)

    texto = escape(texto)

    texto = texto.replace("\n", "<br/>")

    return texto


# =====================================================
# CONFIGURAÇÃO DO PDF
# =====================================================


def criar_pdf(

        caminho

):


    documento = SimpleDocTemplate(

        caminho,

        pagesize=A4

    )



    elementos = []



    estilos = getSampleStyleSheet()



    titulo = estilos["Title"]


    normal = estilos["Normal"]


    subtitulo = estilos["Heading2"]





    # ---------------------------------------------
    # CABEÇALHO
    # ---------------------------------------------


    elementos.append(

        Paragraph(

            "📚 Concurso Trainer 2.0",

            titulo

        )

    )


    elementos.append(

        Spacer(

            1,

            20

        )

    )



    elementos.append(

        Paragraph(

            "Banco de Questões",

            subtitulo

        )

    )



    elementos.append(

        Spacer(

            1,

            20

        )

    )





    # ---------------------------------------------
    # BUSCAR QUESTÕES
    # ---------------------------------------------


    questoes = buscar_todas_questoes()



    if not questoes:


        elementos.append(

            Paragraph(

                "Nenhuma questão cadastrada.",

                normal

            )

        )


        documento.build(

            elementos

        )


        return True

    contador = 1



    for questao in questoes:


        texto = (

            f"<b>{contador}. "

            f"{texto_seguro(questao['pergunta'])}</b>"

        )



        elementos.append(

            Paragraph(

                texto,

                normal

            )

        )



        elementos.append(

            Spacer(

                1,

                10

            )

        )
        
        # ---------------------------------------------
        # INFORMAÇÕES DA QUESTÃO
        # ---------------------------------------------


        categoria = (

            questao["categoria"]

            or

            "Sem categoria"

        )


        subcategoria = (

            questao["subcategoria"]

            or

            ""

        )



        tipo = (

            questao["tipo"]

            or

            "MULTIPLA"

        )



        elementos.append(

            Paragraph(

                f"<b>Categoria:</b> {texto_seguro(categoria)}",

                normal

            )

        )



        if subcategoria:


            elementos.append(

                Paragraph(

                    f"<b>Subcategoria:</b> {texto_seguro(subcategoria)}",

                    normal

                )

            )





        elementos.append(

            Paragraph(

                f"<b>Tipo:</b> {texto_seguro(tipo)}",

                normal

            )

        )



        elementos.append(

            Spacer(

                1,

                10

            )

        )





        # ---------------------------------------------
        # ALTERNATIVAS
        # ---------------------------------------------


        if tipo == "CERTO_ERRADO":



            alternativas = [

                "CERTO",

                "ERRADO"

            ]



            for alternativa in alternativas:



                elementos.append(

                    Paragraph(

                        alternativa,

                        normal

                    )

                )



        else:



            letras = [

                "A",

                "B",

                "C",

                "D",

                "E"

            ]



            valores = [

                questao["alternativa_a"],

                questao["alternativa_b"],

                questao["alternativa_c"],

                questao["alternativa_d"],

                questao["alternativa_e"]

            ]





            for letra, valor in zip(

                letras,

                valores

            ):



                if valor:



                    elementos.append(

                        Paragraph(

                            f"{letra}) {texto_seguro(valor)}",

                            normal

                        )

                    )







        elementos.append(

            Spacer(

                1,

                10

            )

        )





        # ---------------------------------------------
        # RESPOSTA
        # ---------------------------------------------


        elementos.append(

            Paragraph(

                f"<b>Resposta correta:</b> "

                f"{texto_seguro(questao['resposta'])}",

                normal

            )

        )





        # ---------------------------------------------
        # COMENTÁRIO
        # ---------------------------------------------


        comentario = (

            questao["comentario"]

            or

            "Sem comentário."

        )



        elementos.append(

            Paragraph(

                f"<b>Comentário:</b> {texto_seguro(comentario)}",

                normal

            )

        )





        elementos.append(

            Spacer(

                1,

                20

            )

        )



        contador += 1
        
        # ---------------------------------------------
        # QUEBRA ENTRE QUESTÕES
        # ---------------------------------------------

        elementos.append(

            Spacer(

                1,

                20

            )

        )


    # =================================================
    # GERAR PDF
    # =================================================


    try:


        documento.build(

            elementos

        )


        return True



    except Exception as erro:


        print(

            "Erro ao gerar PDF:",

            erro

        )


        return False