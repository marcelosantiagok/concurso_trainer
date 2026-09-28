from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QSpinBox,
    QComboBox,
    QLineEdit,
    QScrollArea
)


from database import (
    exportar_json,
    importar_json,
    exportar_csv,
    criar_backup,
    buscar_categorias
)


LARGURA_MAXIMA_CARD = 620

# Sem limite artificial de questões no simulado/prova em PDF —
# o próprio gerador já usa o total disponível se pedir mais
# do que existe cadastrado.
QUANTIDADE_MAXIMA_SPINBOX = 999999


class BackupPage(QWidget):

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

        area_scroll = QScrollArea()

        area_scroll.setWidgetResizable(True)

        conteudo = QWidget()

        layout_conteudo = QVBoxLayout()

        layout_conteudo.setContentsMargins(30, 26, 30, 30)

        layout_conteudo.setSpacing(18)

        conteudo.setLayout(layout_conteudo)

        area_scroll.setWidget(conteudo)

        layout_pagina.addWidget(area_scroll)

        titulo = QLabel("💾 Backup e Simulados")

        titulo.setObjectName("tituloPagina")

        titulo.setAlignment(Qt.AlignCenter)

        layout_conteudo.addWidget(titulo)

        linha_central = QHBoxLayout()

        linha_central.addStretch()

        card = QWidget()

        card.setObjectName("card")

        card.setMaximumWidth(LARGURA_MAXIMA_CARD)

        layout_card = QVBoxLayout()

        layout_card.setContentsMargins(28, 26, 28, 26)

        layout_card.setSpacing(12)

        card.setLayout(layout_card)

        linha_central.addWidget(card, 3)

        linha_central.addStretch()

        layout_conteudo.addLayout(linha_central)

        descricao = QLabel(
            "Gerencie seu banco de questões, faça backups e "
            "gere simulados ou provas em PDF."
        )

        descricao.setObjectName("textoSecundario")

        descricao.setWordWrap(True)

        layout_card.addWidget(descricao)

        # ==========================================
        # Banco de dados
        # ==========================================

        layout_card.addWidget(
            self.criar_subtitulo("Banco de dados")
        )

        self.botao_backup = QPushButton(
            "💽 Criar Backup Completo do Banco"
        )

        self.botao_backup.clicked.connect(self.fazer_backup)

        layout_card.addWidget(self.botao_backup)

        self.botao_exportar_json = QPushButton(
            "📦 Exportar Questões (JSON)"
        )

        self.botao_exportar_json.setObjectName("botaoSecundario")

        self.botao_exportar_json.clicked.connect(self.exportar_json)

        layout_card.addWidget(self.botao_exportar_json)

        self.botao_importar_json = QPushButton(
            "📂 Importar Questões (JSON)"
        )

        self.botao_importar_json.setObjectName("botaoSecundario")

        self.botao_importar_json.clicked.connect(self.importar_json)

        layout_card.addWidget(self.botao_importar_json)

        self.botao_csv = QPushButton(
            "📊 Exportar CSV"
        )

        self.botao_csv.setObjectName("botaoSecundario")

        self.botao_csv.clicked.connect(self.exportar_csv)

        layout_card.addWidget(self.botao_csv)

        # ==========================================
        # Simulado / Prova em PDF
        # ==========================================

        layout_card.addWidget(
            self.criar_subtitulo("Simulado ou Prova em PDF")
        )

        layout_card.addWidget(self.criar_rotulo("Tipo de documento"))

        self.tipo_documento = QComboBox()

        self.tipo_documento.addItems([
            "Simulado",
            "Prova"
        ])

        layout_card.addWidget(self.tipo_documento)

        layout_card.addWidget(self.criar_rotulo("Título do documento (opcional)"))

        self.campo_titulo = QLineEdit()

        self.campo_titulo.setPlaceholderText(
            "Ex.: Prova de Português - 2º Bimestre"
        )

        layout_card.addWidget(self.campo_titulo)

        layout_card.addWidget(self.criar_rotulo("Categoria (opcional)"))

        self.combo_categoria = QComboBox()

        layout_card.addWidget(self.combo_categoria)

        layout_card.addWidget(self.criar_rotulo("Quantidade de questões"))

        self.quantidade = QSpinBox()

        self.quantidade.setRange(1, QUANTIDADE_MAXIMA_SPINBOX)

        self.quantidade.setValue(30)

        layout_card.addWidget(self.quantidade)

        linha_prof_turma = QHBoxLayout()

        linha_prof_turma.setSpacing(10)

        coluna_professor = QVBoxLayout()

        coluna_professor.addWidget(
            self.criar_rotulo("Professor(a) (opcional)")
        )

        self.campo_professor = QLineEdit()

        self.campo_professor.setPlaceholderText("Ex.: Marcelo Santiago")

        coluna_professor.addWidget(self.campo_professor)

        coluna_turma = QVBoxLayout()

        coluna_turma.addWidget(
            self.criar_rotulo("Turma (opcional)")
        )

        self.campo_turma = QLineEdit()

        self.campo_turma.setPlaceholderText("Ex.: 9º Ano B")

        coluna_turma.addWidget(self.campo_turma)

        linha_prof_turma.addLayout(coluna_professor, 1)

        linha_prof_turma.addLayout(coluna_turma, 1)

        layout_card.addLayout(linha_prof_turma)

        dica = QLabel(
            "O PDF sai com um cabeçalho pronto para aplicar em sala "
            "(professor, aluno, turma e nota) e um gabarito compacto "
            "à parte. Você escolhe o nome do arquivo na hora de salvar."
        )

        dica.setObjectName("textoSecundario")

        dica.setWordWrap(True)

        layout_card.addWidget(dica)

        self.botao_simulado = QPushButton(
            "📝 Gerar PDF (Prova/Simulado + Gabarito)"
        )

        self.botao_simulado.clicked.connect(self.gerar_simulado)

        layout_card.addWidget(self.botao_simulado)

        self.carregar_categorias()

    # ==================================================
    # RÓTULOS PADRÃO
    # ==================================================

    def criar_subtitulo(self, texto):

        rotulo = QLabel(texto)

        rotulo.setObjectName("subtituloPagina")

        return rotulo

    def criar_rotulo(self, texto):

        rotulo = QLabel(texto)

        rotulo.setObjectName("campoRotulo")

        return rotulo

    # ==================================================
    # CARREGAR CATEGORIAS DISPONÍVEIS
    # ==================================================

    def carregar_categorias(self):

        self.combo_categoria.clear()

        self.combo_categoria.addItem("Todas as categorias")

        try:

            categorias = buscar_categorias()

            for item in categorias:

                self.combo_categoria.addItem(item)

        except Exception:

            pass

    # ==================================================
    # BACKUP COMPLETO
    # ==================================================

    def fazer_backup(self):

        try:

            caminho = criar_backup()

            QMessageBox.information(

                self,

                "Backup criado",

                f"Backup salvo em:\n\n{caminho}"

            )

        except Exception as erro:

            QMessageBox.critical(self, "Erro", str(erro))

    # ==================================================
    # EXPORTAR JSON
    # ==================================================

    def exportar_json(self):

        caminho, _ = QFileDialog.getSaveFileName(

            self,

            "Salvar JSON",

            "backup_questoes.json",

            "JSON (*.json)"

        )

        if caminho:

            try:

                exportar_json(caminho)

                QMessageBox.information(
                    self, "Sucesso", "Arquivo JSON criado."
                )

            except Exception as erro:

                QMessageBox.critical(self, "Erro", str(erro))

    # ==================================================
    # IMPORTAR JSON
    # ==================================================

    def importar_json(self):

        caminho, _ = QFileDialog.getOpenFileName(

            self,

            "Selecionar arquivo",

            "",

            "JSON (*.json)"

        )

        if caminho:

            try:

                quantidade = importar_json(caminho)

                QMessageBox.information(

                    self,

                    "Importação concluída",

                    f"{quantidade} questões importadas."

                )

            except Exception as erro:

                QMessageBox.critical(self, "Erro", str(erro))

    # ==================================================
    # EXPORTAR CSV
    # ==================================================

    def exportar_csv(self):

        caminho, _ = QFileDialog.getSaveFileName(

            self,

            "Salvar CSV",

            "questoes.csv",

            "CSV (*.csv)"

        )

        if caminho:

            try:

                exportar_csv(caminho)

                QMessageBox.information(
                    self, "Sucesso", "CSV criado."
                )

            except Exception as erro:

                QMessageBox.critical(self, "Erro", str(erro))

    # ==================================================
    # GERAR SIMULADO / PROVA EM PDF
    # ==================================================

    def gerar_simulado(self):

        tipo_documento = self.tipo_documento.currentText().upper()

        nome_sugerido = (
            self.campo_titulo.text().strip()
            or self.tipo_documento.currentText()
        )

        categoria = self.combo_categoria.currentText()

        if categoria == "Todas as categorias":

            categoria = None

        caminho, _ = QFileDialog.getSaveFileName(

            self,

            "Salvar como",

            f"{nome_sugerido}.pdf",

            "Arquivo PDF (*.pdf)"

        )

        if not caminho:

            return

        try:

            from gerador_simulado import criar_simulado

            resultado = criar_simulado(

                quantidade=self.quantidade.value(),

                caminho_pdf=caminho,

                tipo_documento=tipo_documento,

                categoria=categoria,

                professor=self.campo_professor.text().strip(),

                turma=self.campo_turma.text().strip(),

                titulo=self.campo_titulo.text().strip()

            )

            QMessageBox.information(

                self,

                "Documento criado",

                "Gerado com sucesso!\n\n"
                f"Prova/Simulado:\n{resultado['pdf']}\n\n"
                f"Gabarito:\n{resultado['gabarito']}"

            )

        except Exception as erro:

            QMessageBox.critical(

                self,

                "Erro ao gerar documento",

                str(erro)

            )