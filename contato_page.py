from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication,
    QScrollArea
)


LARGURA_MAXIMA_CARD = 560

CHAVE_PIX = "marcelosantiagok@gmail.com"

WEBSITE = "https://marcelosantiagok.github.io/"

DESENVOLVEDOR = "Marcelo Vasconcelos Santiago"

ANO = "2026"


class ContatoPage(QWidget):

    def __init__(self):
        super().__init__()

        self.criar_interface()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        layout_pagina = QVBoxLayout()

        layout_pagina.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_pagina)

        # ==================================================
        # ÁREA DE SCROLL
        # ==================================================

        area_scroll = QScrollArea()

        area_scroll.setWidgetResizable(True)

        area_scroll.setFrameShape(QScrollArea.NoFrame)

        conteudo = QWidget()

        layout_conteudo = QVBoxLayout()

        layout_conteudo.setContentsMargins(30, 26, 30, 30)

        layout_conteudo.setSpacing(18)

        conteudo.setLayout(layout_conteudo)

        area_scroll.setWidget(conteudo)

        layout_pagina.addWidget(area_scroll)

        # ==================================================
        # TÍTULO
        # ==================================================

        titulo = QLabel("💙 Ajude o Projeto")

        titulo.setObjectName("tituloPagina")

        titulo.setAlignment(Qt.AlignCenter)

        layout_conteudo.addWidget(titulo)

        # ==================================================
        # CENTRALIZAÇÃO DO CARD
        # ==================================================

        linha_central = QHBoxLayout()

        linha_central.addStretch()

        card = QWidget()

        card.setObjectName("card")

        card.setMaximumWidth(LARGURA_MAXIMA_CARD)

        layout_card = QVBoxLayout()

        layout_card.setContentsMargins(30, 28, 30, 28)

        layout_card.setSpacing(14)

        card.setLayout(layout_card)

        linha_central.addWidget(card, 3)

        linha_central.addStretch()

        layout_conteudo.addLayout(linha_central)

        # ==================================================
        # SOBRE O DESENVOLVEDOR
        # ==================================================

        icone = QLabel("📚")

        icone.setAlignment(Qt.AlignCenter)

        icone.setStyleSheet("font-size:40px;")

        layout_card.addWidget(icone)

        nome = QLabel(DESENVOLVEDOR)

        nome.setAlignment(Qt.AlignCenter)

        nome.setObjectName("subtituloPagina")

        layout_card.addWidget(nome)

        subtitulo = QLabel(
            f"Desenvolvedor do Concurso Trainer — {ANO}"
        )

        subtitulo.setAlignment(Qt.AlignCenter)

        subtitulo.setObjectName("textoSecundario")

        layout_card.addWidget(subtitulo)

        # ==================================================
        # BOTÃO DO WEBSITE
        # ==================================================

        botao_site = QPushButton("🌐 Acessar meu site")

        botao_site.setObjectName("botaoSecundario")

        botao_site.setCursor(Qt.PointingHandCursor)

        botao_site.clicked.connect(self.abrir_site)

        layout_card.addWidget(botao_site)

        # ==================================================
        # LINHA SEPARADORA
        # ==================================================

        linha_separadora = QLabel()

        linha_separadora.setFixedHeight(1)

        linha_separadora.setStyleSheet(
            "background-color:#E1E4EC;"
            "margin-top:8px;"
            "margin-bottom:8px;"
        )

        layout_card.addWidget(linha_separadora)

        # ==================================================
        # MENSAGEM DE APOIO / DOAÇÃO
        # ==================================================

        mensagem = QLabel(
            "O Concurso Trainer é um projeto independente, feito para "
            "ajudar quem estuda para concursos públicos. Se ele tem sido "
            "útil pra você, considere apoiar o desenvolvimento com uma "
            "doação — qualquer valor ajuda a manter o projeto vivo. 💙"
        )

        mensagem.setWordWrap(True)

        mensagem.setAlignment(Qt.AlignCenter)

        layout_card.addWidget(mensagem)

        # ==================================================
        # RÓTULO PIX
        # ==================================================

        rotulo_pix = QLabel("Chave PIX (e-mail)")

        rotulo_pix.setAlignment(Qt.AlignCenter)

        rotulo_pix.setObjectName("campoRotulo")

        layout_card.addWidget(rotulo_pix)

        # ==================================================
        # CHAVE PIX
        # ==================================================

        linha_pix = QHBoxLayout()

        linha_pix.addStretch()

        valor_pix = QLabel(CHAVE_PIX)

        valor_pix.setObjectName("badge")

        valor_pix.setAlignment(Qt.AlignCenter)

        linha_pix.addWidget(valor_pix)

        linha_pix.addStretch()

        layout_card.addLayout(linha_pix)

        # ==================================================
        # BOTÃO COPIAR PIX
        # ==================================================

        botao_copiar = QPushButton("📋 Copiar chave PIX")

        botao_copiar.setObjectName("botaoSecundario")

        botao_copiar.setCursor(Qt.PointingHandCursor)

        botao_copiar.clicked.connect(self.copiar_pix)

        layout_card.addWidget(botao_copiar)

        # ==================================================
        # MENSAGEM DE COPIADO
        # ==================================================

        self.lbl_copiado = QLabel("")

        self.lbl_copiado.setAlignment(Qt.AlignCenter)

        self.lbl_copiado.setObjectName("textoSecundario")

        layout_card.addWidget(self.lbl_copiado)

        # ==================================================
        # AGRADECIMENTO
        # ==================================================

        agradecimento = QLabel(
            "Obrigado por usar o Concurso Trainer e por qualquer apoio, "
            "de coração! 🙏"
        )

        agradecimento.setWordWrap(True)

        agradecimento.setAlignment(Qt.AlignCenter)

        agradecimento.setObjectName("textoSecundario")

        layout_card.addWidget(agradecimento)

    # ==================================================
    # ABRIR WEBSITE
    # ==================================================

    def abrir_site(self):

        QDesktopServices.openUrl(
            QUrl(WEBSITE)
        )

    # ==================================================
    # COPIAR CHAVE PIX
    # ==================================================

    def copiar_pix(self):

        QApplication.clipboard().setText(CHAVE_PIX)

        self.lbl_copiado.setText(
            "✅ Chave PIX copiada!"
        )