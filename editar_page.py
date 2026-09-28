from database import (
    buscar_todas_questoes,
    buscar_questao_por_id,
    atualizar_questao,
    excluir_questao
)


from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QComboBox,
    QSpinBox,
    QScrollArea
)


from PySide6.QtCore import Qt


LARGURA_MAXIMA_PAGINA = 1300


class EditarPage(QWidget):

    def __init__(self):

        super().__init__()

        self.id_questao_atual = None

        self.criar_interface()

        self.carregar_lista()

    # ==================================================
    # CRIAR INTERFACE
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

        layout_conteudo.setSpacing(16)

        conteudo.setLayout(layout_conteudo)

        area_scroll.setWidget(conteudo)

        layout_pagina.addWidget(area_scroll)

        titulo = QLabel("✏️ Editar Questões")

        titulo.setObjectName("tituloPagina")

        titulo.setAlignment(Qt.AlignCenter)

        layout_conteudo.addWidget(titulo)

        # -----------------------------------------
        # Container central (largura máxima)
        # -----------------------------------------

        linha_central = QHBoxLayout()

        linha_central.addStretch()

        container = QWidget()

        container.setMaximumWidth(LARGURA_MAXIMA_PAGINA)

        layout_container = QHBoxLayout()

        layout_container.setSpacing(20)

        container.setLayout(layout_container)

        linha_central.addWidget(container, 5)

        linha_central.addStretch()

        layout_conteudo.addLayout(linha_central)

        # ==================================================
        # PAINEL DA LISTA
        # ==================================================

        painel_lista_widget = QWidget()

        painel_lista_widget.setObjectName("card")

        painel_lista = QVBoxLayout()

        painel_lista.setContentsMargins(18, 18, 18, 18)

        painel_lista.setSpacing(10)

        painel_lista_widget.setLayout(painel_lista)

        titulo_lista = QLabel("📚 Questões cadastradas")

        titulo_lista.setObjectName("subtituloPagina")

        painel_lista.addWidget(titulo_lista)

        self.lista = QListWidget()

        self.lista.itemClicked.connect(self.selecionar_questao)

        painel_lista.addWidget(self.lista)

        layout_container.addWidget(painel_lista_widget, 4)

        # ==================================================
        # PAINEL DE EDIÇÃO
        # ==================================================

        painel_edicao_widget = QWidget()

        painel_edicao_widget.setObjectName("card")

        painel_edicao = QVBoxLayout()

        painel_edicao.setContentsMargins(22, 22, 22, 22)

        painel_edicao.setSpacing(12)

        painel_edicao_widget.setLayout(painel_edicao)

        layout_container.addWidget(painel_edicao_widget, 6)

        subtitulo = QLabel("Detalhes da questão")

        subtitulo.setObjectName("subtituloPagina")

        painel_edicao.addWidget(subtitulo)

        # ------------------------------
        # Categoria
        # ------------------------------

        painel_edicao.addWidget(self.criar_rotulo("Categoria"))

        self.categoria = QLineEdit()

        painel_edicao.addWidget(self.categoria)

        # ------------------------------
        # Subcategoria
        # ------------------------------

        painel_edicao.addWidget(self.criar_rotulo("Subcategoria"))

        self.subcategoria = QLineEdit()

        painel_edicao.addWidget(self.subcategoria)

        # ------------------------------
        # Banca
        # ------------------------------

        painel_edicao.addWidget(self.criar_rotulo("Banca"))

        self.banca = QLineEdit()

        painel_edicao.addWidget(self.banca)

        # ------------------------------
        # Ano e dificuldade
        # ------------------------------

        linha_info = QHBoxLayout()

        linha_info.setSpacing(14)

        coluna_ano = QVBoxLayout()

        coluna_ano.addWidget(self.criar_rotulo("Ano"))

        self.ano = QSpinBox()

        self.ano.setRange(0, 2100)

        coluna_ano.addWidget(self.ano)

        coluna_dificuldade = QVBoxLayout()

        coluna_dificuldade.addWidget(self.criar_rotulo("Dificuldade"))

        self.dificuldade = QComboBox()

        self.dificuldade.addItems([
            "FÁCIL",
            "NORMAL",
            "DIFÍCIL"
        ])

        coluna_dificuldade.addWidget(self.dificuldade)

        linha_info.addLayout(coluna_ano, 1)

        linha_info.addLayout(coluna_dificuldade, 1)

        painel_edicao.addLayout(linha_info)

        # ------------------------------
        # Tipo da questão
        # ------------------------------

        painel_edicao.addWidget(self.criar_rotulo("Tipo"))

        self.tipo = QComboBox()

        self.tipo.addItems([
            "MULTIPLA",
            "CERTO_ERRADO"
        ])

        self.tipo.currentTextChanged.connect(self.alterar_tipo)

        painel_edicao.addWidget(self.tipo)

        # ------------------------------
        # Pergunta
        # ------------------------------

        painel_edicao.addWidget(self.criar_rotulo("Pergunta"))

        self.pergunta = QTextEdit()

        self.pergunta.setMinimumHeight(100)

        painel_edicao.addWidget(self.pergunta)

        # ------------------------------
        # Alternativas
        # ------------------------------

        self.rotulo_alternativas = self.criar_rotulo("Alternativas")

        painel_edicao.addWidget(self.rotulo_alternativas)

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

            painel_edicao.addWidget(linha_widget)

        # ------------------------------
        # Resposta correta
        # ------------------------------

        painel_edicao.addWidget(self.criar_rotulo("Resposta correta"))

        self.resposta = QComboBox()

        painel_edicao.addWidget(self.resposta)

        # ------------------------------
        # Comentário
        # ------------------------------

        painel_edicao.addWidget(
            self.criar_rotulo("Comentário / Explicação")
        )

        self.comentario = QTextEdit()

        self.comentario.setMinimumHeight(90)

        painel_edicao.addWidget(self.comentario)

        # ==================================================
        # BOTÕES
        # ==================================================

        linha_botoes = QHBoxLayout()

        linha_botoes.setSpacing(10)

        botao_salvar = QPushButton("💾 Salvar Alteração")

        botao_salvar.clicked.connect(self.salvar_alteracao)

        botao_excluir = QPushButton("🗑 Excluir")

        botao_excluir.setObjectName("botaoPerigo")

        botao_excluir.clicked.connect(self.excluir)

        botao_limpar = QPushButton("🧹 Limpar")

        botao_limpar.setObjectName("botaoSecundario")

        botao_limpar.clicked.connect(self.limpar)

        linha_botoes.addWidget(botao_salvar, 2)

        linha_botoes.addWidget(botao_excluir, 1)

        linha_botoes.addWidget(botao_limpar, 1)

        painel_edicao.addSpacing(4)

        painel_edicao.addLayout(linha_botoes)

        self.alterar_tipo()

    # ==================================================
    # ROTULO PADRÃO DE CAMPO
    # ==================================================

    def criar_rotulo(self, texto):

        rotulo = QLabel(texto)

        rotulo.setObjectName("campoRotulo")

        return rotulo

    # ==================================================
    # CARREGAR LISTA DE QUESTÕES
    # ==================================================

    def carregar_lista(self):

        self.lista.clear()

        questoes = buscar_todas_questoes()

        for questao in questoes:

            texto = (
                f"{questao['id']} - "
                f"{questao['pergunta'][:60]}"
            )

            self.lista.addItem(texto)

    # ==================================================
    # SELECIONAR QUESTÃO NA LISTA
    # ==================================================

    def selecionar_questao(self, item):

        texto = item.text()

        id_questao = int(texto.split("-")[0].strip())

        self.id_questao_atual = id_questao

        questao = buscar_questao_por_id(id_questao)

        if questao:

            self.carregar_dados(questao)

    # ==================================================
    # CARREGAR DADOS DA QUESTÃO
    # ==================================================

    def carregar_dados(self, questao):

        self.categoria.setText(questao["categoria"] or "")

        self.subcategoria.setText(questao["subcategoria"] or "")

        self.banca.setText(questao["banca"] or "")

        if questao["ano"]:

            self.ano.setValue(int(questao["ano"]))

        else:

            self.ano.setValue(0)

        dificuldade = questao["dificuldade"]

        if dificuldade:

            self.dificuldade.setCurrentText(dificuldade)

        tipo = questao["tipo"]

        if tipo:

            self.tipo.setCurrentText(tipo)

        self.pergunta.setPlainText(questao["pergunta"] or "")

        alternativas = [
            questao["alternativa_a"],
            questao["alternativa_b"],
            questao["alternativa_c"],
            questao["alternativa_d"],
            questao["alternativa_e"]
        ]

        for i, campo in enumerate(self.alternativas):

            campo.setText(alternativas[i] or "")

        resposta = questao["resposta"]

        if resposta:

            self.resposta.setCurrentText(resposta)

        self.comentario.setPlainText(questao["comentario"] or "")

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

    # ==================================================
    # SALVAR ALTERAÇÃO
    # ==================================================

    def salvar_alteracao(self):

        if self.id_questao_atual is None:

            QMessageBox.warning(

                self,

                "Atenção",

                "Selecione uma questão para editar."

            )

            return

        try:

            atualizar_questao(

                self.id_questao_atual,

                self.categoria.text(),

                self.subcategoria.text(),

                self.pergunta.toPlainText(),

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

                "Questão atualizada com sucesso!"

            )

            self.carregar_lista()

        except Exception as erro:

            QMessageBox.critical(

                self,

                "Erro",

                str(erro)

            )

    # ==================================================
    # EXCLUIR QUESTÃO
    # ==================================================

    def excluir(self):

        if self.id_questao_atual is None:

            QMessageBox.warning(

                self,

                "Atenção",

                "Selecione uma questão para excluir."

            )

            return

        resposta = QMessageBox.question(

            self,

            "Confirmar exclusão",

            "Deseja realmente excluir esta questão?",

            QMessageBox.Yes | QMessageBox.No

        )

        if resposta == QMessageBox.Yes:

            try:

                excluir_questao(self.id_questao_atual)

                QMessageBox.information(

                    self,

                    "Sucesso",

                    "Questão excluída com sucesso!"

                )

                self.limpar()

                self.carregar_lista()

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

        self.id_questao_atual = None

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

        self.lista.clearSelection()

        self.alterar_tipo()

    # ==================================================
    # ATUALIZAR TELA
    # ==================================================

    def atualizar(self):

        self.carregar_lista()

    # ==================================================
    # EVENTO AO MOSTRAR A TELA
    # ==================================================

    def showEvent(self, event):

        super().showEvent(event)

        self.atualizar()