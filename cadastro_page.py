from database import inserir_questao

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QScrollArea
)

from PySide6.QtCore import Qt


# Largura máxima do card do formulário. Isso é o que resolve
# o problema de "esticar" quando a janela é maximizada: o
# conteúdo cresce até esse limite e depois fica centralizado,
# em vez de ocupar a tela inteira de ponta a ponta.
LARGURA_MAXIMA_CARD = 760


class CadastroPage(QWidget):

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

        # ------------------------------------------
        # Área rolável (necessária pois o formulário
        # é mais alto do que a maioria das telas)
        # ------------------------------------------

        area_scroll = QScrollArea()

        area_scroll.setWidgetResizable(True)

        conteudo = QWidget()

        layout_conteudo = QVBoxLayout()

        layout_conteudo.setContentsMargins(30, 26, 30, 30)

        layout_conteudo.setSpacing(18)

        conteudo.setLayout(layout_conteudo)

        area_scroll.setWidget(conteudo)

        layout_pagina.addWidget(area_scroll)

        # ------------------------------------------
        # Título
        # ------------------------------------------

        titulo = QLabel("➕ Cadastro de Questões")

        titulo.setObjectName("tituloPagina")

        titulo.setAlignment(Qt.AlignCenter)

        layout_conteudo.addWidget(titulo)

        # ------------------------------------------
        # Card central (largura máxima + centralizado)
        # ------------------------------------------

        linha_central = QHBoxLayout()

        linha_central.addStretch()

        card = QWidget()

        card.setObjectName("card")

        card.setMaximumWidth(LARGURA_MAXIMA_CARD)

        layout_card = QVBoxLayout()

        layout_card.setContentsMargins(28, 26, 28, 26)

        layout_card.setSpacing(14)

        card.setLayout(layout_card)

        linha_central.addWidget(card, 3)

        linha_central.addStretch()

        layout_conteudo.addLayout(linha_central)

        # ==========================================
        # Categoria / Subcategoria
        # ==========================================

        layout_card.addWidget(
            self.criar_rotulo("Categoria")
        )

        self.categoria = QLineEdit()

        self.categoria.setPlaceholderText(
            "Ex.: Direito Constitucional"
        )

        layout_card.addWidget(self.categoria)

        layout_card.addWidget(
            self.criar_rotulo("Subcategoria")
        )

        self.subcategoria = QLineEdit()

        self.subcategoria.setPlaceholderText(
            "Ex.: Poder Executivo"
        )

        layout_card.addWidget(self.subcategoria)

        # ==========================================
        # Banca
        # ==========================================

        layout_card.addWidget(
            self.criar_rotulo("Banca")
        )

        self.banca = QLineEdit()

        self.banca.setPlaceholderText("Ex.: CEBRASPE")

        layout_card.addWidget(self.banca)

        # ==========================================
        # Ano e dificuldade (lado a lado)
        # ==========================================

        linha_info = QHBoxLayout()

        linha_info.setSpacing(14)

        coluna_ano = QVBoxLayout()

        coluna_ano.addWidget(self.criar_rotulo("Ano"))

        self.ano = QSpinBox()

        self.ano.setRange(0, 2100)

        coluna_ano.addWidget(self.ano)

        coluna_dificuldade = QVBoxLayout()

        coluna_dificuldade.addWidget(
            self.criar_rotulo("Dificuldade")
        )

        self.dificuldade = QComboBox()

        self.dificuldade.addItems([
            "FÁCIL",
            "NORMAL",
            "DIFÍCIL"
        ])

        coluna_dificuldade.addWidget(self.dificuldade)

        linha_info.addLayout(coluna_ano, 1)

        linha_info.addLayout(coluna_dificuldade, 1)

        layout_card.addLayout(linha_info)

        # ==========================================
        # Tipo
        # ==========================================

        layout_card.addWidget(
            self.criar_rotulo("Tipo da questão")
        )

        self.tipo = QComboBox()

        self.tipo.addItems([
            "MULTIPLA",
            "CERTO_ERRADO"
        ])

        self.tipo.currentTextChanged.connect(
            self.alterar_tipo
        )

        layout_card.addWidget(self.tipo)

        # ==========================================
        # Pergunta
        # ==========================================

        layout_card.addWidget(
            self.criar_rotulo("Pergunta")
        )

        self.pergunta = QTextEdit()

        self.pergunta.setMinimumHeight(120)

        layout_card.addWidget(self.pergunta)

        # ==========================================
        # Alternativas
        # ==========================================

        self.rotulo_alternativas = self.criar_rotulo(
            "Alternativas"
        )

        layout_card.addWidget(self.rotulo_alternativas)

        self.alternativas = []

        self.linhas_alternativas = []

        letras = ["A", "B", "C", "D", "E"]

        for letra in letras:

            linha_widget = QWidget()

            linha = QHBoxLayout()

            linha.setContentsMargins(0, 0, 0, 0)

            linha.setSpacing(10)

            linha_widget.setLayout(linha)

            selo = QLabel(letra)

            selo.setObjectName("badge")

            selo.setAlignment(Qt.AlignCenter)

            selo.setFixedWidth(28)

            campo = QLineEdit()

            campo.setPlaceholderText(f"Alternativa {letra}")

            self.alternativas.append(campo)

            self.linhas_alternativas.append(linha_widget)

            linha.addWidget(selo)

            linha.addWidget(campo)

            layout_card.addWidget(linha_widget)

        # ==========================================
        # Resposta correta
        # ==========================================

        layout_card.addWidget(
            self.criar_rotulo("Resposta correta")
        )

        self.resposta = QComboBox()

        layout_card.addWidget(self.resposta)

        # ==========================================
        # Comentário
        # ==========================================

        layout_card.addWidget(
            self.criar_rotulo("Comentário / Explicação")
        )

        self.comentario = QTextEdit()

        self.comentario.setMinimumHeight(100)

        layout_card.addWidget(self.comentario)

        # ==========================================
        # Botões
        # ==========================================

        linha_botoes = QHBoxLayout()

        linha_botoes.setSpacing(10)

        self.botao_salvar = QPushButton("💾 Salvar Questão")

        self.botao_limpar = QPushButton("🧹 Limpar")

        self.botao_limpar.setObjectName("botaoSecundario")

        self.botao_salvar.clicked.connect(self.salvar)

        self.botao_limpar.clicked.connect(self.limpar)

        linha_botoes.addWidget(self.botao_salvar, 2)

        linha_botoes.addWidget(self.botao_limpar, 1)

        layout_card.addSpacing(6)

        layout_card.addLayout(linha_botoes)

        # sincroniza visibilidade inicial (MULTIPLA)
        self.alterar_tipo()

    # ==================================================
    # ROTULO PADRÃO DE CAMPO
    # ==================================================

    def criar_rotulo(self, texto):

        rotulo = QLabel(texto)

        rotulo.setObjectName("campoRotulo")

        return rotulo

    # ==================================================
    # SALVAR QUESTÃO
    # ==================================================

    def salvar(self):

        pergunta = self.pergunta.toPlainText().strip()

        if not pergunta:

            QMessageBox.warning(
                self,
                "Atenção",
                "Digite a pergunta."
            )

            return

        try:

            inserir_questao(

                self.categoria.text(),

                self.subcategoria.text(),

                pergunta,

                self.tipo.currentText(),

                self.alternativas[0].text(),

                self.alternativas[1].text(),

                self.alternativas[2].text(),

                self.alternativas[3].text(),

                self.alternativas[4].text(),

                self.resposta.currentText(),

                self.comentario.toPlainText(),

                self.banca.text(),

                self.ano.value(),

                self.dificuldade.currentText()

            )

            QMessageBox.information(
                self,
                "Sucesso",
                "Questão cadastrada com sucesso!"
            )

            self.limpar()

        except Exception as erro:

            QMessageBox.critical(
                self,
                "Erro",
                str(erro)
            )

    # ==================================================
    # LIMPAR CAMPOS
    # ==================================================

    def limpar(self):

        self.categoria.clear()

        self.subcategoria.clear()

        self.banca.clear()

        self.ano.setValue(0)

        self.dificuldade.setCurrentText("NORMAL")

        self.tipo.setCurrentText("MULTIPLA")

        self.pergunta.clear()

        for campo in self.alternativas:
            campo.clear()

        self.comentario.clear()

        self.alterar_tipo()

    # ==================================================
    # ALTERAR TIPO (mostra/esconde alternativas)
    # ==================================================

    def alterar_tipo(self):

        if self.tipo.currentText() == "CERTO_ERRADO":

            self.rotulo_alternativas.hide()

            for linha_widget in self.linhas_alternativas:
                linha_widget.hide()

            self.resposta.clear()

            self.resposta.addItems([
                "CERTO",
                "ERRADO"
            ])

        else:

            self.rotulo_alternativas.show()

            for linha_widget in self.linhas_alternativas:
                linha_widget.show()

            self.resposta.clear()

            self.resposta.addItems([
                "A",
                "B",
                "C",
                "D",
                "E"
            ])