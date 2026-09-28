from database import (
    buscar_estatisticas,
    buscar_estatisticas_categoria,
    resetar_estatisticas
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QScrollArea
)

from PySide6.QtCore import Qt


LARGURA_MAXIMA_CONTEUDO = 1000


class EstatisticasPage(QWidget):

    def __init__(self):

        super().__init__()

        self.criar_interface()

        self.atualizar_dados()

    # ==================================================
    # INTERFACE
    # ==================================================

    def criar_interface(self):

        layout_pagina = QVBoxLayout()

        layout_pagina.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout_pagina)

        area_scroll = QScrollArea()

        area_scroll.setWidgetResizable(True)

        conteudo = QWidget()

        layout_conteudo = QVBoxLayout()

        layout_conteudo.setContentsMargins(30, 26, 30, 30)

        layout_conteudo.setSpacing(18)

        conteudo.setLayout(layout_conteudo)

        area_scroll.setWidget(conteudo)

        layout_pagina.addWidget(area_scroll)

        titulo = QLabel("📊 Estatísticas")

        titulo.setObjectName("tituloPagina")

        titulo.setAlignment(Qt.AlignCenter)

        layout_conteudo.addWidget(titulo)

        # -----------------------------------------
        # Container central com largura máxima
        # -----------------------------------------

        linha_central = QHBoxLayout()

        linha_central.addStretch()

        container = QWidget()

        container.setMaximumWidth(LARGURA_MAXIMA_CONTEUDO)

        layout_container = QVBoxLayout()

        layout_container.setSpacing(20)

        container.setLayout(layout_container)

        linha_central.addWidget(container, 5)

        linha_central.addStretch()

        layout_conteudo.addLayout(linha_central)

        # -----------------------------------------
        # Cartões de estatística
        # -----------------------------------------

        linha_cartoes = QHBoxLayout()

        linha_cartoes.setSpacing(14)

        self.cartao_total, self.valor_total = self.criar_cartao(
            "Questões cadastradas"
        )

        self.cartao_tentativas, self.valor_tentativas = self.criar_cartao(
            "Tentativas"
        )

        self.cartao_acertos, self.valor_acertos = self.criar_cartao(
            "Acertos"
        )

        self.cartao_erros, self.valor_erros = self.criar_cartao(
            "Erros"
        )

        self.cartao_percentual, self.valor_percentual = self.criar_cartao(
            "Aproveitamento"
        )

        for cartao in (
            self.cartao_total,
            self.cartao_tentativas,
            self.cartao_acertos,
            self.cartao_erros,
            self.cartao_percentual,
        ):

            linha_cartoes.addWidget(cartao)

        layout_container.addLayout(linha_cartoes)

        # -----------------------------------------
        # Tabela por categoria
        # -----------------------------------------

        titulo2 = QLabel("Desempenho por categoria")

        titulo2.setObjectName("subtituloPagina")

        layout_container.addWidget(titulo2)

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels([
            "Categoria",
            "Tentativas",
            "Acertos",
            "Erros"
        ])

        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.tabela.verticalHeader().setVisible(False)

        self.tabela.setAlternatingRowColors(True)

        self.tabela.setMinimumHeight(240)

        layout_container.addWidget(self.tabela)

        self.botao_resetar = QPushButton(
            "🔄 Resetar Estatísticas"
        )

        self.botao_resetar.setObjectName("botaoPerigo")

        self.botao_resetar.clicked.connect(
            self.resetar
        )

        layout_container.addWidget(
            self.botao_resetar,
            alignment=Qt.AlignRight
        )

    # ==================================================
    # CARTÃO DE ESTATÍSTICA
    # ==================================================

    def criar_cartao(self, rotulo_texto):

        cartao = QWidget()

        cartao.setObjectName("card")

        layout = QVBoxLayout()

        layout.setContentsMargins(16, 16, 16, 16)

        layout.setSpacing(4)

        cartao.setLayout(layout)

        valor = QLabel("0")

        valor.setObjectName("tituloPagina")

        valor.setStyleSheet("font-size:24px; padding:0px;")

        layout.addWidget(valor)

        rotulo = QLabel(rotulo_texto)

        rotulo.setObjectName("textoSecundario")

        rotulo.setWordWrap(True)

        layout.addWidget(rotulo)

        return cartao, valor

    # ==================================================
    # ATUALIZAR DADOS
    # ==================================================

    def atualizar_dados(self):

        dados = buscar_estatisticas()

        self.valor_total.setText(str(dados["total_questoes"]))

        self.valor_tentativas.setText(str(dados["tentativas"]))

        self.valor_acertos.setText(str(dados["acertos"]))

        self.valor_erros.setText(str(dados["erros"]))

        self.valor_percentual.setText(f"{dados['percentual']}%")

        self.carregar_tabela_categoria()

    # ==================================================
    # TABELA
    # ==================================================

    def carregar_tabela_categoria(self):

        dados = buscar_estatisticas_categoria()

        self.tabela.setRowCount(0)

        for linha, item in enumerate(dados):

            self.tabela.insertRow(linha)

            categoria = item["categoria"] or "Sem categoria"

            tentativas = item["tentativas"] or 0

            acertos = item["acertos"] or 0

            erros = item["erros"] or 0

            self.tabela.setItem(
                linha,
                0,
                QTableWidgetItem(str(categoria))
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(str(tentativas))
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(str(acertos))
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(str(erros))
            )

        self.tabela.resizeRowsToContents()

    # ==================================================
    # RESETAR
    # ==================================================

    def resetar(self):

        resposta = QMessageBox.question(

            self,

            "Confirmação",

            "Deseja realmente apagar todas as estatísticas?",

            QMessageBox.Yes | QMessageBox.No

        )

        if resposta == QMessageBox.No:

            return

        try:

            resetar_estatisticas()

            QMessageBox.information(

                self,

                "Sucesso",

                "Estatísticas resetadas."

            )

            self.atualizar_dados()

        except Exception as erro:

            QMessageBox.critical(

                self,

                "Erro",

                str(erro)

            )

    # ==================================================
    # ATUALIZA SEMPRE QUE ABRIR
    # ==================================================

    def showEvent(self, event):

        super().showEvent(event)

        self.atualizar_dados()