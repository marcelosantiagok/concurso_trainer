from database import inserir_questao

from importador_pdf import importar_questoes_pdf

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
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QScrollArea
)

from PySide6.QtCore import Qt


LARGURA_MAXIMA_PAGINA = 1300


class ImportarPdfPage(QWidget):

    def __init__(self):

        super().__init__()

        self.questoes_importadas = []

        self.indice_atual = None

        self.criar_interface()

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

        titulo = QLabel("📥 Importar Questões de PDF")

        titulo.setObjectName("tituloPagina")

        titulo.setAlignment(Qt.AlignCenter)

        layout_conteudo.addWidget(titulo)

        alerta_dev = QLabel(
            "🚧 Esta página ainda está em desenvolvimento. A extração "
            "automática funciona por heurística e, dependendo do "
            "formato do PDF, pode reconhecer só 1 a 3 questões (ou "
            "misturar pergunta/alternativas), o que deixa o simulado "
            "bagunçado se não for revisado. Sempre confira cada "
            "questão antes de importar — ou use a Seleção Visual "
            "abaixo, mais lenta, mas mais confiável."
        )

        alerta_dev.setWordWrap(True)

        alerta_dev.setAlignment(Qt.AlignCenter)

        alerta_dev.setStyleSheet(
            "color:#C98A1B; background-color:#FBF1DF; "
            "border:1px solid #C98A1B; border-radius:8px; "
            "padding:10px; font-weight:600;"
        )

        layout_conteudo.addWidget(alerta_dev)

        aviso = QLabel(
            "Funciona melhor com PDFs de texto real (não escaneados) e "
            "numeração de questões sequencial. O sistema tenta detectar "
            "o gabarito automaticamente — quando não encontra, você "
            "marca a resposta manualmente aqui antes de importar. "
            "Nada é salvo no banco sem você revisar e confirmar."
        )

        aviso.setObjectName("textoSecundario")

        aviso.setWordWrap(True)

        aviso.setAlignment(Qt.AlignCenter)

        layout_conteudo.addWidget(aviso)

        linha_central = QHBoxLayout()

        linha_central.addStretch()

        container = QWidget()

        container.setMaximumWidth(LARGURA_MAXIMA_PAGINA)

        layout_container = QVBoxLayout()

        layout_container.setSpacing(16)

        container.setLayout(layout_container)

        linha_central.addWidget(container, 5)

        linha_central.addStretch()

        layout_conteudo.addLayout(linha_central)

        # ==========================================
        # SELEÇÃO DO ARQUIVO
        # ==========================================

        card_arquivo = QWidget()

        card_arquivo.setObjectName("card")

        layout_arquivo = QVBoxLayout()

        layout_arquivo.setContentsMargins(20, 18, 20, 18)

        layout_arquivo.setSpacing(10)

        card_arquivo.setLayout(layout_arquivo)

        self.botao_selecionar = QPushButton(
            "📄 Selecionar PDF (extração automática)"
        )

        self.botao_selecionar.clicked.connect(self.selecionar_pdf)

        layout_arquivo.addWidget(self.botao_selecionar)

        self.botao_selecao_visual = QPushButton(
            "🖱️ Selecionar Trechos do PDF Manualmente (Beta)"
        )

        self.botao_selecao_visual.setObjectName("botaoSecundario")

        self.botao_selecao_visual.clicked.connect(
            self.abrir_selecao_visual
        )

        layout_arquivo.addWidget(self.botao_selecao_visual)

        dica_visual = QLabel(
            "Na seleção manual você abre o PDF, arrasta o mouse sobre "
            "a pergunta ou cada alternativa e manda o texto direto "
            "para o campo certo no formulário de revisão, questão por "
            "questão — evita a bagunça da detecção automática."
        )

        dica_visual.setObjectName("textoSecundario")

        dica_visual.setWordWrap(True)

        layout_arquivo.addWidget(dica_visual)

        self.lbl_resumo = QLabel("Nenhum arquivo importado ainda.")

        self.lbl_resumo.setObjectName("textoSecundario")

        self.lbl_resumo.setWordWrap(True)

        layout_arquivo.addWidget(self.lbl_resumo)

        layout_container.addWidget(card_arquivo)

        # ==========================================
        # APLICAR A TODAS
        # ==========================================

        card_todas = QWidget()

        card_todas.setObjectName("card")

        layout_todas = QVBoxLayout()

        layout_todas.setContentsMargins(20, 18, 20, 18)

        layout_todas.setSpacing(10)

        card_todas.setLayout(layout_todas)

        layout_todas.addWidget(
            self.criar_rotulo(
                "Aplicar a todas as questões importadas (opcional)"
            )
        )

        linha_todas_1 = QHBoxLayout()

        linha_todas_1.setSpacing(12)

        coluna_cat = QVBoxLayout()
        coluna_cat.addWidget(self.criar_rotulo("Categoria"))
        self.campo_todas_categoria = QLineEdit()
        coluna_cat.addWidget(self.campo_todas_categoria)

        coluna_sub = QVBoxLayout()
        coluna_sub.addWidget(self.criar_rotulo("Subcategoria"))
        self.campo_todas_subcategoria = QLineEdit()
        coluna_sub.addWidget(self.campo_todas_subcategoria)

        linha_todas_1.addLayout(coluna_cat, 1)
        linha_todas_1.addLayout(coluna_sub, 1)

        layout_todas.addLayout(linha_todas_1)

        linha_todas_2 = QHBoxLayout()

        linha_todas_2.setSpacing(12)

        coluna_banca = QVBoxLayout()
        coluna_banca.addWidget(self.criar_rotulo("Banca"))
        self.campo_todas_banca = QLineEdit()
        coluna_banca.addWidget(self.campo_todas_banca)

        coluna_ano = QVBoxLayout()
        coluna_ano.addWidget(self.criar_rotulo("Ano"))
        self.campo_todas_ano = QSpinBox()
        self.campo_todas_ano.setRange(0, 2100)
        coluna_ano.addWidget(self.campo_todas_ano)

        coluna_dificuldade = QVBoxLayout()
        coluna_dificuldade.addWidget(self.criar_rotulo("Dificuldade"))
        self.campo_todas_dificuldade = QComboBox()
        self.campo_todas_dificuldade.addItems(
            ["NORMAL", "FÁCIL", "DIFÍCIL"]
        )
        coluna_dificuldade.addWidget(self.campo_todas_dificuldade)

        linha_todas_2.addLayout(coluna_banca, 1)
        linha_todas_2.addLayout(coluna_ano, 1)
        linha_todas_2.addLayout(coluna_dificuldade, 1)

        layout_todas.addLayout(linha_todas_2)

        self.botao_aplicar_todas = QPushButton(
            "Aplicar estes dados a todas as questões da lista"
        )

        self.botao_aplicar_todas.setObjectName("botaoSecundario")

        self.botao_aplicar_todas.clicked.connect(self.aplicar_a_todas)

        layout_todas.addWidget(self.botao_aplicar_todas)

        layout_container.addWidget(card_todas)

        # ==========================================
        # LISTA + FORMULÁRIO DE REVISÃO
        # ==========================================

        layout_revisao = QHBoxLayout()

        layout_revisao.setSpacing(16)

        # ---- painel da lista ----

        painel_lista = QWidget()

        painel_lista.setObjectName("card")

        layout_lista = QVBoxLayout()

        layout_lista.setContentsMargins(16, 16, 16, 16)

        layout_lista.setSpacing(8)

        painel_lista.setLayout(layout_lista)

        layout_lista.addWidget(
            self.criar_subtitulo("Questões encontradas")
        )

        dica_lista = QLabel(
            "✅ = gabarito identificado   ⚠️ = confira a resposta"
        )

        dica_lista.setObjectName("textoSecundario")

        layout_lista.addWidget(dica_lista)

        self.lista = QListWidget()

        self.lista.itemClicked.connect(self.selecionar_item)

        layout_lista.addWidget(self.lista)

        layout_revisao.addWidget(painel_lista, 4)

        # ---- painel de edição ----

        painel_edicao = QWidget()

        painel_edicao.setObjectName("card")

        layout_edicao = QVBoxLayout()

        layout_edicao.setContentsMargins(20, 18, 20, 18)

        layout_edicao.setSpacing(10)

        painel_edicao.setLayout(layout_edicao)

        layout_edicao.addWidget(
            self.criar_subtitulo("Revisar questão selecionada")
        )

        layout_edicao.addWidget(self.criar_rotulo("Categoria"))
        self.campo_categoria = QLineEdit()
        layout_edicao.addWidget(self.campo_categoria)

        layout_edicao.addWidget(self.criar_rotulo("Subcategoria"))
        self.campo_subcategoria = QLineEdit()
        layout_edicao.addWidget(self.campo_subcategoria)

        linha_banca_ano = QHBoxLayout()

        linha_banca_ano.setSpacing(12)

        coluna_b = QVBoxLayout()
        coluna_b.addWidget(self.criar_rotulo("Banca"))
        self.campo_banca = QLineEdit()
        coluna_b.addWidget(self.campo_banca)

        coluna_a = QVBoxLayout()
        coluna_a.addWidget(self.criar_rotulo("Ano"))
        self.campo_ano = QSpinBox()
        self.campo_ano.setRange(0, 2100)
        coluna_a.addWidget(self.campo_ano)

        linha_banca_ano.addLayout(coluna_b, 1)
        linha_banca_ano.addLayout(coluna_a, 1)

        layout_edicao.addLayout(linha_banca_ano)

        layout_edicao.addWidget(self.criar_rotulo("Tipo"))

        self.campo_tipo = QComboBox()

        self.campo_tipo.addItems(["MULTIPLA", "CERTO_ERRADO"])

        self.campo_tipo.currentTextChanged.connect(self.alterar_tipo)

        layout_edicao.addWidget(self.campo_tipo)

        layout_edicao.addWidget(self.criar_rotulo("Pergunta"))

        self.campo_pergunta = QTextEdit()

        self.campo_pergunta.setMinimumHeight(90)

        layout_edicao.addWidget(self.campo_pergunta)

        self.rotulo_alternativas = self.criar_rotulo("Alternativas")

        layout_edicao.addWidget(self.rotulo_alternativas)

        self.campos_alternativas = {}

        self.linhas_alternativas = []

        for letra in ["A", "B", "C", "D", "E"]:

            linha_widget = QWidget()

            linha = QHBoxLayout()

            linha.setContentsMargins(0, 0, 0, 0)

            linha.setSpacing(8)

            linha_widget.setLayout(linha)

            selo = QLabel(letra)

            selo.setObjectName("badge")

            selo.setFixedWidth(24)

            selo.setAlignment(Qt.AlignCenter)

            campo = QLineEdit()

            self.campos_alternativas[letra] = campo

            self.linhas_alternativas.append(linha_widget)

            linha.addWidget(selo)

            linha.addWidget(campo)

            layout_edicao.addWidget(linha_widget)

        layout_edicao.addWidget(self.criar_rotulo("Resposta correta"))

        self.campo_resposta = QComboBox()

        layout_edicao.addWidget(self.campo_resposta)

        layout_edicao.addWidget(self.criar_rotulo("Comentário (opcional)"))

        self.campo_comentario = QTextEdit()

        self.campo_comentario.setMinimumHeight(70)

        layout_edicao.addWidget(self.campo_comentario)

        layout_revisao.addWidget(painel_edicao, 6)

        layout_container.addLayout(layout_revisao)

        # ==========================================
        # BOTÃO DE IMPORTAR
        # ==========================================

        self.botao_importar = QPushButton(
            "📥 Importar Questões Selecionadas"
        )

        self.botao_importar.clicked.connect(self.importar_selecionadas)

        layout_container.addWidget(self.botao_importar)

        self.alterar_tipo("MULTIPLA")

        self.habilitar_formulario(False)

    # ==================================================
    # RÓTULOS PADRÃO
    # ==================================================

    def criar_rotulo(self, texto):

        rotulo = QLabel(texto)

        rotulo.setObjectName("campoRotulo")

        return rotulo

    def criar_subtitulo(self, texto):

        rotulo = QLabel(texto)

        rotulo.setObjectName("subtituloPagina")

        return rotulo

    # ==================================================
    # HABILITAR/DESABILITAR FORMULÁRIO
    # ==================================================

    def habilitar_formulario(self, habilitado):

        for campo in [
            self.campo_categoria, self.campo_subcategoria,
            self.campo_banca, self.campo_ano, self.campo_tipo,
            self.campo_pergunta, self.campo_resposta,
            self.campo_comentario
        ]:

            campo.setEnabled(habilitado)

        for campo in self.campos_alternativas.values():

            campo.setEnabled(habilitado)

    # ==================================================
    # ALTERAR TIPO (mostra/esconde alternativas)
    # ==================================================

    def alterar_tipo(self, tipo):

        if tipo == "CERTO_ERRADO":

            self.rotulo_alternativas.hide()

            for linha in self.linhas_alternativas:
                linha.hide()

            self.campo_resposta.clear()

            self.campo_resposta.addItems(["CERTO", "ERRADO"])

        else:

            self.rotulo_alternativas.show()

            for linha in self.linhas_alternativas:
                linha.show()

            self.campo_resposta.clear()

            self.campo_resposta.addItems(["A", "B", "C", "D", "E"])

    # ==================================================
    # SELECIONAR PDF E EXTRAIR QUESTÕES
    # ==================================================

    def selecionar_pdf(self):

        caminho, _ = QFileDialog.getOpenFileName(

            self,

            "Selecionar PDF da prova",

            "",

            "Arquivo PDF (*.pdf)"

        )

        if not caminho:

            return

        try:

            questoes = importar_questoes_pdf(caminho)

        except Exception as erro:

            QMessageBox.critical(

                self,

                "Não foi possível importar",

                str(erro)

            )

            return

        self.questoes_importadas = questoes

        self.indice_atual = None

        self.habilitar_formulario(False)

        self.atualizar_lista()

        com_gabarito = sum(
            1 for q in questoes if q["resposta"]
        )

        self.lbl_resumo.setText(
            f"✅ {len(questoes)} questões encontradas — "
            f"{com_gabarito} com gabarito identificado, "
            f"{len(questoes) - com_gabarito} precisam de revisão manual "
            f"da resposta. Clique em cada uma na lista para conferir."
        )

    # ==================================================
    # SELEÇÃO VISUAL DO PDF (BETA)
    # ==================================================
    # Abre o PDF em um visualizador onde o usuário arrasta o mouse
    # para marcar a área da pergunta/alternativa e envia o texto
    # capturado direto para o campo correspondente do formulário de
    # revisão (o mesmo painel usado pela extração automática).

    def abrir_selecao_visual(self):

        caminho, _ = QFileDialog.getOpenFileName(

            self,

            "Selecionar PDF da prova",

            "",

            "Arquivo PDF (*.pdf)"

        )

        if not caminho:

            return

        try:

            from visor_pdf_dialog import VisorPdfSelecaoDialog

        except ImportError:

            QMessageBox.critical(

                self,

                "Biblioteca ausente",

                "A seleção visual precisa da biblioteca PyMuPDF.\n\n"
                "Instale com:\npip install pymupdf"

            )

            return

        try:

            dialogo = VisorPdfSelecaoDialog(

                caminho,

                ao_enviar_texto=self.receber_texto_selecionado,

                ao_nova_questao=self.criar_questao_manual_vazia,

                parent=self

            )

        except Exception as erro:

            QMessageBox.critical(

                self,

                "Erro ao abrir PDF",

                str(erro)

            )

            return

        dialogo.exec()

    # ==================================================
    # CRIAR UMA QUESTÃO VAZIA (usada pela seleção visual)
    # ==================================================

    def criar_questao_manual_vazia(self):

        self.salvar_edicao_atual()

        novo_numero = len(self.questoes_importadas) + 1

        questao = {
            "numero": novo_numero,
            "tipo": "MULTIPLA",
            "pergunta": "",
            "alternativas": {"A": "", "B": "", "C": "", "D": "", "E": ""},
            "resposta": None,
            "categoria": "",
            "subcategoria": "",
            "banca": "",
            "ano": 0,
            "comentario": "",
        }

        self.questoes_importadas.append(questao)

        self.atualizar_lista()

        ultimo_item = self.lista.item(self.lista.count() - 1)

        self.lista.setCurrentItem(ultimo_item)

        self.selecionar_item(ultimo_item)

    # ==================================================
    # RECEBER TEXTO CAPTURADO NA SELEÇÃO VISUAL
    # ==================================================
    # destino: "Pergunta", "Alternativa A".."E" ou "Comentário"

    def receber_texto_selecionado(self, destino, texto):

        if self.indice_atual is None:

            self.criar_questao_manual_vazia()

        if destino == "Pergunta":

            atual = self.campo_pergunta.toPlainText().strip()

            self.campo_pergunta.setPlainText(
                (atual + "\n" + texto).strip() if atual else texto
            )

        elif destino.startswith("Alternativa "):

            letra = destino.split(" ")[-1]

            campo = self.campos_alternativas.get(letra)

            if campo:

                campo.setText(texto)

        elif destino == "Comentário":

            atual = self.campo_comentario.toPlainText().strip()

            self.campo_comentario.setPlainText(
                (atual + "\n" + texto).strip() if atual else texto
            )

        self.salvar_edicao_atual()

    # ==================================================
    # ATUALIZAR LISTA
    # ==================================================

    def atualizar_lista(self):

        self.lista.clear()

        for i, questao in enumerate(self.questoes_importadas):

            selo = "✅" if questao["resposta"] else "⚠️"

            texto_resumido = questao["pergunta"][:70] or "(sem texto)"

            item = QListWidgetItem(
                f"{selo} {questao['numero']}) {texto_resumido}"
            )

            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)

            item.setCheckState(Qt.Checked)

            item.setData(Qt.UserRole, i)

            self.lista.addItem(item)

    # ==================================================
    # SELECIONAR UMA QUESTÃO DA LISTA PARA REVISAR
    # ==================================================

    def selecionar_item(self, item):

        self.salvar_edicao_atual()

        indice = item.data(Qt.UserRole)

        self.indice_atual = indice

        questao = self.questoes_importadas[indice]

        self.habilitar_formulario(True)

        self.campo_categoria.setText(questao.get("categoria", ""))

        self.campo_subcategoria.setText(questao.get("subcategoria", ""))

        self.campo_banca.setText(questao.get("banca", ""))

        self.campo_ano.setValue(questao.get("ano") or 0)

        self.campo_tipo.setCurrentText(questao["tipo"])

        self.campo_pergunta.setPlainText(questao["pergunta"])

        for letra, campo in self.campos_alternativas.items():

            campo.setText(questao["alternativas"].get(letra, ""))

        if questao["resposta"]:

            self.campo_resposta.setCurrentText(questao["resposta"])

        self.campo_comentario.setPlainText(questao.get("comentario", ""))

    # ==================================================
    # SALVAR EDIÇÃO DA QUESTÃO ATUALMENTE ABERTA
    # ==================================================

    def salvar_edicao_atual(self):

        if self.indice_atual is None:

            return

        questao = self.questoes_importadas[self.indice_atual]

        questao["categoria"] = self.campo_categoria.text().strip()

        questao["subcategoria"] = self.campo_subcategoria.text().strip()

        questao["banca"] = self.campo_banca.text().strip()

        questao["ano"] = self.campo_ano.value()

        questao["tipo"] = self.campo_tipo.currentText()

        questao["pergunta"] = self.campo_pergunta.toPlainText().strip()

        questao["alternativas"] = {
            letra: campo.text().strip()
            for letra, campo in self.campos_alternativas.items()
        }

        questao["resposta"] = self.campo_resposta.currentText()

        questao["comentario"] = self.campo_comentario.toPlainText().strip()

        self.atualizar_item_lista(self.indice_atual)

    # ==================================================
    # ATUALIZAR O TEXTO DE UM ITEM NA LISTA (sem perder seleção)
    # ==================================================

    def atualizar_item_lista(self, indice):

        item = self.lista.item(indice)

        if item is None:

            return

        questao = self.questoes_importadas[indice]

        selo = "✅" if questao["resposta"] else "⚠️"

        texto_resumido = questao["pergunta"][:70] or "(sem texto)"

        item.setText(f"{selo} {questao['numero']}) {texto_resumido}")

    # ==================================================
    # APLICAR CATEGORIA/BANCA/ANO/DIFICULDADE A TODAS
    # ==================================================

    def aplicar_a_todas(self):

        if not self.questoes_importadas:

            QMessageBox.warning(

                self,

                "Atenção",

                "Importe um PDF primeiro."

            )

            return

        self.salvar_edicao_atual()

        categoria = self.campo_todas_categoria.text().strip()

        subcategoria = self.campo_todas_subcategoria.text().strip()

        banca = self.campo_todas_banca.text().strip()

        ano = self.campo_todas_ano.value()

        dificuldade = self.campo_todas_dificuldade.currentText()

        for questao in self.questoes_importadas:

            if categoria:
                questao["categoria"] = categoria

            if subcategoria:
                questao["subcategoria"] = subcategoria

            if banca:
                questao["banca"] = banca

            if ano:
                questao["ano"] = ano

            questao["dificuldade"] = dificuldade

        if self.indice_atual is not None:

            self.selecionar_item(self.lista.item(self.indice_atual))

        QMessageBox.information(

            self,

            "Aplicado",

            "Dados aplicados a todas as questões da lista."

        )

    # ==================================================
    # IMPORTAR QUESTÕES SELECIONADAS PARA O BANCO
    # ==================================================

    def importar_selecionadas(self):

        if not self.questoes_importadas:

            QMessageBox.warning(

                self,

                "Atenção",

                "Nenhuma questão para importar. Selecione um PDF primeiro."

            )

            return

        self.salvar_edicao_atual()

        importadas = 0

        puladas = 0

        erros = []

        for i in range(self.lista.count()):

            item = self.lista.item(i)

            if item.checkState() != Qt.Checked:

                puladas += 1

                continue

            questao = self.questoes_importadas[i]

            pergunta = questao["pergunta"].strip()

            resposta = questao["resposta"]

            if not pergunta or not resposta:

                erros.append(
                    f"Questão {questao['numero']}: falta pergunta ou "
                    f"resposta correta definida."
                )

                continue

            alt = questao["alternativas"]

            try:

                inserir_questao(

                    questao.get("categoria", ""),

                    questao.get("subcategoria", ""),

                    pergunta,

                    questao["tipo"],

                    alt.get("A", ""),

                    alt.get("B", ""),

                    alt.get("C", ""),

                    alt.get("D", ""),

                    alt.get("E", ""),

                    resposta,

                    questao.get("comentario", ""),

                    questao.get("banca", ""),

                    questao.get("ano", 0) or 0,

                    questao.get("dificuldade", "NORMAL")

                )

                importadas += 1

            except Exception as erro:

                erros.append(f"Questão {questao['numero']}: {erro}")

        mensagem = (
            f"✅ {importadas} questões importadas com sucesso.\n"
            f"⏭ {puladas} não selecionadas.\n"
        )

        if erros:

            mensagem += (
                f"\n⚠️ {len(erros)} não puderam ser importadas:\n"
                + "\n".join(erros[:10])
            )

            if len(erros) > 10:

                mensagem += f"\n... e mais {len(erros) - 10}."

        QMessageBox.information(

            self,

            "Importação concluída",

            mensagem

        )

        if importadas > 0:

            self.questoes_importadas = []

            self.indice_atual = None

            self.lista.clear()

            self.habilitar_formulario(False)

            self.lbl_resumo.setText(
                "Nenhum arquivo importado ainda."
            )