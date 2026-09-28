# ==========================================================
# VISOR PDF DIALOG (BETA)
# ==========================================================
#
# Janela que mostra a página do PDF como imagem e permite ao
# usuário arrastar o mouse para marcar uma área (a pergunta, uma
# alternativa, o comentário...). O texto dentro da área marcada é
# extraído com o PyMuPDF (fitz) e enviado para o campo escolhido
# no formulário de revisão da tela de Importar PDF.
#
# Por que isso existe: a extração automática por heurística
# (numeração sequencial) erra bastante em provas com formatação
# fora do padrão, às vezes reconhecendo só 1 a 3 questões. Este
# modo é mais lento (questão por questão), mas muito mais
# confiável, já que o usuário decide exatamente qual texto vai
# para qual campo.
#
# IMPORTANTE: este recurso ainda está em desenvolvimento (beta).
# Requer a biblioteca PyMuPDF instalada (pip install pymupdf).
# ==========================================================

import fitz  # PyMuPDF

from PySide6.QtCore import Qt, QRect, Signal

from PySide6.QtGui import QImage, QPixmap

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QScrollArea,
    QMessageBox,
    QRubberBand
)


ZOOM_INICIAL = 1.6
ZOOM_MINIMO = 0.6
ZOOM_MAXIMO = 4.0
PASSO_ZOOM = 0.2


# ==========================================================
# LABEL COM SUPORTE A SELEÇÃO POR ARRASTE (RUBBER BAND)
# ==========================================================

class RotuloSelecionavel(QLabel):

    selecao_feita = Signal(QRect)

    def __init__(self):

        super().__init__()

        self.ponto_inicial = None

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

    def mousePressEvent(self, evento):

        if evento.button() == Qt.LeftButton:

            self.ponto_inicial = evento.position().toPoint()

            self.rubber_band.setGeometry(
                QRect(self.ponto_inicial, self.ponto_inicial)
            )

            self.rubber_band.show()

    def mouseMoveEvent(self, evento):

        if self.ponto_inicial is not None:

            retangulo = QRect(
                self.ponto_inicial,
                evento.position().toPoint()
            ).normalized()

            self.rubber_band.setGeometry(retangulo)

    def mouseReleaseEvent(self, evento):

        if self.ponto_inicial is not None:

            retangulo = QRect(
                self.ponto_inicial,
                evento.position().toPoint()
            ).normalized()

            self.rubber_band.hide()

            self.ponto_inicial = None

            # ignora cliques/arrastes muito pequenos (acidentais)
            if retangulo.width() > 4 and retangulo.height() > 4:

                self.selecao_feita.emit(retangulo)


# ==========================================================
# DIÁLOGO PRINCIPAL
# ==========================================================

class VisorPdfSelecaoDialog(QDialog):

    def __init__(
        self,
        caminho_pdf,
        ao_enviar_texto,
        ao_nova_questao,
        parent=None
    ):

        super().__init__(parent)

        self.setWindowTitle("Seleção Visual do PDF (Beta)")

        self.resize(1000, 780)

        # callbacks fornecidos pela ImportarPdfPage
        self.ao_enviar_texto = ao_enviar_texto

        self.ao_nova_questao = ao_nova_questao

        try:

            self.documento = fitz.open(caminho_pdf)

        except Exception as erro:

            raise Exception(f"Não foi possível abrir o PDF: {erro}")

        if self.documento.page_count == 0:

            self.documento.close()

            raise Exception("Este PDF não tem páginas.")

        self.pagina_atual = 0

        self.zoom = ZOOM_INICIAL

        self.ultimo_texto_capturado = ""

        self.criar_interface()

        self.renderizar_pagina()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        layout = QVBoxLayout()

        self.setLayout(layout)

        aviso = QLabel(
            "🚧 Recurso em desenvolvimento (Beta). Arraste o mouse sobre "
            "o texto da pergunta, de uma alternativa ou do comentário, "
            "escolha o campo de destino e clique em \"Enviar seleção\". "
            "Revise sempre o texto antes de importar."
        )

        aviso.setWordWrap(True)

        aviso.setStyleSheet(
            "color:#C98A1B; background-color:#FBF1DF; "
            "border:1px solid #C98A1B; border-radius:8px; "
            "padding:8px; font-weight:600;"
        )

        layout.addWidget(aviso)

        # ------------------------------------------
        # Navegação de página / zoom
        # ------------------------------------------

        barra_navegacao = QHBoxLayout()

        self.botao_anterior = QPushButton("⬅ Página anterior")

        self.botao_anterior.clicked.connect(self.pagina_anterior)

        self.botao_proxima = QPushButton("Próxima página ➡")

        self.botao_proxima.clicked.connect(self.proxima_pagina)

        self.lbl_pagina = QLabel("")

        self.lbl_pagina.setAlignment(Qt.AlignCenter)

        self.botao_zoom_menos = QPushButton("🔍−")

        self.botao_zoom_menos.setObjectName("botaoSecundario")

        self.botao_zoom_menos.clicked.connect(self.zoom_menos)

        self.botao_zoom_mais = QPushButton("🔍+")

        self.botao_zoom_mais.setObjectName("botaoSecundario")

        self.botao_zoom_mais.clicked.connect(self.zoom_mais)

        barra_navegacao.addWidget(self.botao_anterior)

        barra_navegacao.addWidget(self.lbl_pagina, 1)

        barra_navegacao.addWidget(self.botao_proxima)

        barra_navegacao.addSpacing(20)

        barra_navegacao.addWidget(self.botao_zoom_menos)

        barra_navegacao.addWidget(self.botao_zoom_mais)

        layout.addLayout(barra_navegacao)

        # ------------------------------------------
        # Área da imagem da página (com scroll)
        # ------------------------------------------

        self.area_scroll = QScrollArea()

        self.area_scroll.setWidgetResizable(False)

        self.rotulo_imagem = RotuloSelecionavel()

        self.rotulo_imagem.selecao_feita.connect(
            self.capturar_texto_da_selecao
        )

        self.area_scroll.setWidget(self.rotulo_imagem)

        layout.addWidget(self.area_scroll, 1)

        # ------------------------------------------
        # Texto capturado na última seleção
        # ------------------------------------------

        layout.addWidget(QLabel("Texto capturado na última seleção:"))

        self.lbl_texto_capturado = QLabel("(nenhuma seleção ainda)")

        self.lbl_texto_capturado.setWordWrap(True)

        self.lbl_texto_capturado.setObjectName("textoSecundario")

        self.lbl_texto_capturado.setMaximumHeight(80)

        layout.addWidget(self.lbl_texto_capturado)

        # ------------------------------------------
        # Envio do texto capturado para um campo
        # ------------------------------------------

        linha_envio = QHBoxLayout()

        linha_envio.addWidget(QLabel("Enviar para:"))

        self.combo_destino = QComboBox()

        self.combo_destino.addItems([
            "Pergunta",
            "Alternativa A",
            "Alternativa B",
            "Alternativa C",
            "Alternativa D",
            "Alternativa E",
            "Comentário"
        ])

        linha_envio.addWidget(self.combo_destino, 1)

        self.botao_enviar = QPushButton("➡ Enviar seleção para o campo")

        self.botao_enviar.clicked.connect(self.enviar_para_campo)

        linha_envio.addWidget(self.botao_enviar)

        layout.addLayout(linha_envio)

        # ------------------------------------------
        # Nova questão / fechar
        # ------------------------------------------

        linha_final = QHBoxLayout()

        self.botao_nova_questao = QPushButton(
            "➕ Começar nova questão"
        )

        self.botao_nova_questao.setObjectName("botaoSecundario")

        self.botao_nova_questao.clicked.connect(self.nova_questao)

        linha_final.addWidget(self.botao_nova_questao)

        linha_final.addStretch()

        self.botao_fechar = QPushButton("Fechar")

        self.botao_fechar.setObjectName("botaoSecundario")

        self.botao_fechar.clicked.connect(self.accept)

        linha_final.addWidget(self.botao_fechar)

        layout.addLayout(linha_final)

    # ==================================================
    # RENDERIZAR A PÁGINA ATUAL COMO IMAGEM
    # ==================================================

    def renderizar_pagina(self):

        pagina = self.documento[self.pagina_atual]

        matriz = fitz.Matrix(self.zoom, self.zoom)

        pixmap_pdf = pagina.get_pixmap(matrix=matriz)

        formato = (
            QImage.Format_RGB888
            if pixmap_pdf.n < 4
            else QImage.Format_RGBA8888
        )

        imagem = QImage(
            pixmap_pdf.samples,
            pixmap_pdf.width,
            pixmap_pdf.height,
            pixmap_pdf.stride,
            formato
        )

        pixmap_qt = QPixmap.fromImage(imagem.copy())

        self.rotulo_imagem.setPixmap(pixmap_qt)

        self.rotulo_imagem.resize(pixmap_qt.size())

        self.lbl_pagina.setText(
            f"Página {self.pagina_atual + 1} de {self.documento.page_count}"
        )

    # ==================================================
    # NAVEGAÇÃO
    # ==================================================

    def pagina_anterior(self):

        if self.pagina_atual > 0:

            self.pagina_atual -= 1

            self.renderizar_pagina()

    def proxima_pagina(self):

        if self.pagina_atual < self.documento.page_count - 1:

            self.pagina_atual += 1

            self.renderizar_pagina()

    def zoom_mais(self):

        self.zoom = min(self.zoom + PASSO_ZOOM, ZOOM_MAXIMO)

        self.renderizar_pagina()

    def zoom_menos(self):

        self.zoom = max(self.zoom - PASSO_ZOOM, ZOOM_MINIMO)

        self.renderizar_pagina()

    # ==================================================
    # CAPTURAR TEXTO DA ÁREA SELECIONADA
    # ==================================================

    def capturar_texto_da_selecao(self, retangulo):

        pagina = self.documento[self.pagina_atual]

        # o retângulo veio em pixels da imagem renderizada; para
        # voltar às coordenadas do PDF (em pontos) é só dividir
        # pelo fator de zoom usado ao renderizar.
        retangulo_pdf = fitz.Rect(
            retangulo.left() / self.zoom,
            retangulo.top() / self.zoom,
            retangulo.right() / self.zoom,
            retangulo.bottom() / self.zoom
        )

        texto = pagina.get_textbox(retangulo_pdf).strip()

        self.ultimo_texto_capturado = texto

        self.lbl_texto_capturado.setText(
            texto if texto else "(nenhum texto encontrado nessa área)"
        )

    # ==================================================
    # ENVIAR TEXTO CAPTURADO PARA O CAMPO ESCOLHIDO
    # ==================================================

    def enviar_para_campo(self):

        if not self.ultimo_texto_capturado:

            QMessageBox.warning(
                self,
                "Atenção",
                "Arraste o mouse sobre um trecho do PDF antes de enviar."
            )

            return

        destino = self.combo_destino.currentText()

        self.ao_enviar_texto(destino, self.ultimo_texto_capturado)

    # ==================================================
    # NOVA QUESTÃO
    # ==================================================

    def nova_questao(self):

        self.ao_nova_questao()

        QMessageBox.information(
            self,
            "Nova questão",
            "Nova questão criada na lista de revisão. Agora selecione "
            "os trechos no PDF e envie para os campos dela."
        )

    # ==================================================
    # FECHAR O DOCUMENTO AO SAIR
    # ==================================================

    def closeEvent(self, evento):

        self.documento.close()

        super().closeEvent(evento)

    def accept(self):

        self.documento.close()

        super().accept()
