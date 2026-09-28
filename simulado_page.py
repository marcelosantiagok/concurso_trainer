from database import (
    buscar_categorias,
    buscar_bancas,
    buscar_anos,
    buscar_questoes_quantidade,
    registrar_resultado
)

from styles import CORES

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRadioButton,
    QButtonGroup,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QMessageBox,
    QFrame,
    QScrollArea
)

from PySide6.QtCore import Qt, QTimer


LARGURA_MAXIMA_CARD = 720

# Sem limite artificial: o número real de questões disponíveis
# já limita o valor automaticamente (ver iniciar_simulado).
QUANTIDADE_MAXIMA_SPINBOX = 999999

ESTILO_CORRETA = (
    f"background-color:{CORES['sucesso_fraco']};"
    f"border:1.5px solid {CORES['sucesso']};"
    f"border-radius:10px;"
)

ESTILO_ERRADA = (
    f"background-color:{CORES['aviso_fraco']};"
    f"border:1.5px solid {CORES['aviso']};"
    f"border-radius:10px;"
)

ESTILO_RISCADO = (
    f"color:{CORES['texto_apagado']};"
    f"text-decoration: line-through;"
)


class SimuladoPage(QWidget):

    def __init__(self):

        super().__init__()

        self.questoes = []
        self.indice = 0
        self.respostas = {}

        # Cronômetro de prova (opcional)
        self.modo_prova = False
        self.timer_prova = QTimer(self)
        self.timer_prova.timeout.connect(self.tick_cronometro)
        self.segundos_totais = 0
        self.segundos_restantes = 0
        self.pausado = False
        self.marcos_horas_notificados = set()
        self.notificado_30min = False
        self.notificado_15min = False

        self.criar_interface()

        self.mostrar_configuracao()

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

        self.layout_conteudo = QVBoxLayout()

        self.layout_conteudo.setContentsMargins(30, 26, 30, 30)

        self.layout_conteudo.setSpacing(16)

        conteudo.setLayout(self.layout_conteudo)

        area_scroll.setWidget(conteudo)

        layout_pagina.addWidget(area_scroll)

        titulo = QLabel("📝 Simulado")

        titulo.setObjectName("tituloPagina")

        titulo.setAlignment(Qt.AlignCenter)

        self.layout_conteudo.addWidget(titulo)

        linha_central = QHBoxLayout()

        linha_central.addStretch()

        self.card = QWidget()

        self.card.setObjectName("card")

        self.card.setMaximumWidth(LARGURA_MAXIMA_CARD)

        self.layout_card = QVBoxLayout()

        self.layout_card.setContentsMargins(28, 26, 28, 26)

        self.layout_card.setSpacing(14)

        self.card.setLayout(self.layout_card)

        linha_central.addWidget(self.card, 3)

        linha_central.addStretch()

        self.layout_conteudo.addLayout(linha_central)

        self.layout_conteudo.addStretch()

        self.criar_secao_configuracao()
        self.criar_secao_questao()
        self.criar_secao_resultado()

    # ==================================================
    # SEÇÃO: CONFIGURAÇÃO DO SIMULADO
    # ==================================================

    def criar_secao_configuracao(self):

        self.config_widget = QWidget()

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(10)

        self.config_widget.setLayout(layout)

        layout.addWidget(self.criar_rotulo("Categoria (opcional)"))

        self.combo_categoria = QComboBox()

        layout.addWidget(self.combo_categoria)

        linha_banca_ano = QHBoxLayout()

        linha_banca_ano.setSpacing(14)

        coluna_banca = QVBoxLayout()

        coluna_banca.addWidget(self.criar_rotulo("Banca (opcional)"))

        self.combo_banca = QComboBox()

        coluna_banca.addWidget(self.combo_banca)

        coluna_ano = QVBoxLayout()

        coluna_ano.addWidget(self.criar_rotulo("Ano (opcional)"))

        self.combo_ano = QComboBox()

        coluna_ano.addWidget(self.combo_ano)

        linha_banca_ano.addLayout(coluna_banca, 1)

        linha_banca_ano.addLayout(coluna_ano, 1)

        layout.addLayout(linha_banca_ano)

        layout.addWidget(self.criar_rotulo("Dificuldade (opcional)"))

        self.combo_dificuldade = QComboBox()

        self.combo_dificuldade.addItems([
            "Todas as dificuldades",
            "FÁCIL",
            "NORMAL",
            "DIFÍCIL"
        ])

        layout.addWidget(self.combo_dificuldade)

        layout.addWidget(self.criar_rotulo("Quantidade de questões"))

        self.spin_quantidade = QSpinBox()

        self.spin_quantidade.setRange(1, QUANTIDADE_MAXIMA_SPINBOX)

        self.spin_quantidade.setValue(10)

        layout.addWidget(self.spin_quantidade)

        dica = QLabel(
            "Se pedir mais questões do que existem cadastradas, "
            "o simulado usa todas as disponíveis."
        )

        dica.setObjectName("textoSecundario")

        dica.setWordWrap(True)

        layout.addWidget(dica)

        # -----------------------------
        # Cronômetro de prova (opcional)
        # -----------------------------

        self.checkbox_cronometro = QCheckBox(
            "⏱ Simular ambiente de prova (com cronômetro)"
        )

        self.checkbox_cronometro.toggled.connect(
            self.alternar_campos_cronometro
        )

        layout.addWidget(self.checkbox_cronometro)

        self.widget_duracao = QWidget()

        layout_duracao = QHBoxLayout()

        layout_duracao.setContentsMargins(0, 0, 0, 0)

        layout_duracao.setSpacing(14)

        self.widget_duracao.setLayout(layout_duracao)

        coluna_horas = QVBoxLayout()

        coluna_horas.addWidget(self.criar_rotulo("Horas"))

        self.spin_horas = QSpinBox()

        self.spin_horas.setRange(0, 23)

        self.spin_horas.setValue(1)

        coluna_horas.addWidget(self.spin_horas)

        coluna_minutos = QVBoxLayout()

        coluna_minutos.addWidget(self.criar_rotulo("Minutos"))

        self.spin_minutos = QSpinBox()

        self.spin_minutos.setRange(0, 59)

        self.spin_minutos.setSingleStep(5)

        self.spin_minutos.setValue(0)

        coluna_minutos.addWidget(self.spin_minutos)

        layout_duracao.addLayout(coluna_horas, 1)

        layout_duracao.addLayout(coluna_minutos, 1)

        self.widget_duracao.setVisible(False)

        layout.addWidget(self.widget_duracao)

        self.botao_iniciar = QPushButton("▶ Iniciar Simulado")

        self.botao_iniciar.clicked.connect(self.iniciar_simulado)

        layout.addSpacing(6)

        layout.addWidget(self.botao_iniciar)

        self.layout_card.addWidget(self.config_widget)

    # ==================================================
    # SEÇÃO: QUESTÃO ATUAL
    # ==================================================

    # ==================================================
    # MOSTRAR/ESCONDER CAMPOS DE DURAÇÃO DA PROVA
    # ==================================================

    def alternar_campos_cronometro(self, marcado):

        self.widget_duracao.setVisible(marcado)

    def criar_secao_questao(self):

        self.questao_widget = QWidget()

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(14)

        self.questao_widget.setLayout(layout)

        cabecalho = QHBoxLayout()

        self.lbl_contador = QLabel()

        self.lbl_contador.setObjectName("badge")

        cabecalho.addWidget(self.lbl_contador)

        cabecalho.addStretch()

        self.botao_encerrar = QPushButton("⏹ Encerrar Simulado")

        self.botao_encerrar.setObjectName("botaoSecundario")

        self.botao_encerrar.clicked.connect(self.encerrar_simulado)

        cabecalho.addWidget(self.botao_encerrar)

        layout.addLayout(cabecalho)

        # -----------------------------
        # Painel do cronômetro de prova
        # -----------------------------

        self.painel_cronometro = QWidget()

        layout_cronometro = QHBoxLayout()

        layout_cronometro.setContentsMargins(0, 0, 0, 0)

        layout_cronometro.setSpacing(8)

        self.painel_cronometro.setLayout(layout_cronometro)

        self.lbl_tempo_restante = QLabel()

        self.lbl_tempo_restante.setObjectName("badge")

        layout_cronometro.addWidget(self.lbl_tempo_restante)

        layout_cronometro.addStretch()

        self.botao_pausar = QPushButton("⏸ Pausar")

        self.botao_pausar.setObjectName("botaoSecundario")

        self.botao_pausar.clicked.connect(self.alternar_pausa)

        layout_cronometro.addWidget(self.botao_pausar)

        self.botao_reiniciar_cronometro = QPushButton("🔄 Reiniciar")

        self.botao_reiniciar_cronometro.setObjectName("botaoSecundario")

        self.botao_reiniciar_cronometro.clicked.connect(
            self.reiniciar_cronometro
        )

        layout_cronometro.addWidget(self.botao_reiniciar_cronometro)

        self.painel_cronometro.hide()

        layout.addWidget(self.painel_cronometro)

        # -----------------------------
        # Aviso discreto (toast) do cronômetro
        # -----------------------------

        self.lbl_toast = QLabel()

        self.lbl_toast.setAlignment(Qt.AlignCenter)

        self.lbl_toast.setWordWrap(True)

        self.lbl_toast.hide()

        layout.addWidget(self.lbl_toast)

        self.lbl_categoria_questao = QLabel()

        self.lbl_categoria_questao.setObjectName("textoSecundario")

        layout.addWidget(self.lbl_categoria_questao)

        self.lbl_pergunta = QLabel()

        self.lbl_pergunta.setObjectName("cardQuestao")

        self.lbl_pergunta.setWordWrap(True)

        layout.addWidget(self.lbl_pergunta)

        self.grupo = QButtonGroup()

        self.radios = []
        self.linhas = []
        self.botoes_tesoura = []
        self.labels_alternativas = []

        alternativas_widget = QWidget()

        alternativas_widget.setObjectName("card")

        self.alternativas_layout = QVBoxLayout()

        self.alternativas_layout.setContentsMargins(10, 4, 10, 4)

        self.alternativas_layout.setSpacing(4)

        alternativas_widget.setLayout(self.alternativas_layout)

        layout.addWidget(alternativas_widget)

        # -----------------------------
        # Mensagem de feedback (acerto/erro)
        # -----------------------------

        self.lbl_feedback = QLabel()

        self.lbl_feedback.setAlignment(Qt.AlignCenter)

        self.lbl_feedback.setWordWrap(True)

        self.lbl_feedback.hide()

        layout.addWidget(self.lbl_feedback)

        for _ in range(5):

            self.criar_linha_opcao()

        self.frame_comentario = QFrame()

        self.frame_comentario.setObjectName("linhaResumo")

        self.frame_comentario.hide()

        comentario_layout = QVBoxLayout()

        comentario_layout.setContentsMargins(16, 12, 16, 12)

        self.frame_comentario.setLayout(comentario_layout)

        titulo_comentario = QLabel("💬 Comentário")

        titulo_comentario.setObjectName("subtituloPagina")

        comentario_layout.addWidget(titulo_comentario)

        self.lbl_comentario_simulado = QLabel()

        self.lbl_comentario_simulado.setWordWrap(True)

        comentario_layout.addWidget(self.lbl_comentario_simulado)

        layout.addWidget(self.frame_comentario)

        botoes = QHBoxLayout()

        botoes.setSpacing(10)

        self.botao_responder = QPushButton("✔ Responder")

        self.botao_avancar = QPushButton("➡ Próxima Questão")

        self.botao_avancar.setObjectName("botaoSecundario")

        self.botao_avancar.setEnabled(False)

        self.botao_responder.clicked.connect(self.responder_questao)

        self.botao_avancar.clicked.connect(self.avancar_questao)

        botoes.addWidget(self.botao_responder)

        botoes.addWidget(self.botao_avancar)

        layout.addLayout(botoes)

        self.layout_card.addWidget(self.questao_widget)

    # ==================================================
    # CRIAR UMA LINHA DE ALTERNATIVA (radio + tesoura)
    # ==================================================

    def criar_linha_opcao(self):

        indice = len(self.radios)

        linha = QFrame()

        linha.setObjectName("linhaOpcao")

        layout = QHBoxLayout()

        layout.setContentsMargins(6, 6, 6, 6)

        layout.setSpacing(8)

        linha.setLayout(layout)

        radio = QRadioButton()

        self.grupo.addButton(radio)

        radio.toggled.connect(
            lambda marcado, i=indice: self.ao_selecionar_alternativa(i, marcado)
        )

        tesoura = QPushButton("✂")

        tesoura.setObjectName("botaoTesoura")

        tesoura.setCheckable(True)

        tesoura.setToolTip("Riscar esta alternativa")

        tesoura.clicked.connect(
            lambda marcado, i=indice: self.alternar_risco(i)
        )

        label_texto = QLabel()

        label_texto.setWordWrap(True)

        label_texto.setCursor(Qt.PointingHandCursor)

        label_texto.mousePressEvent = (
            lambda evento, r=radio: r.setChecked(True) if r.isEnabled() else None
        )

        layout.addWidget(tesoura, 0)

        layout.addWidget(radio, 0)

        layout.addWidget(label_texto, 1)

        self.radios.append(radio)
        self.linhas.append(linha)
        self.botoes_tesoura.append(tesoura)
        self.labels_alternativas.append(label_texto)

        self.alternativas_layout.addWidget(linha)

    # ==================================================
    # AO SELECIONAR UMA ALTERNATIVA
    # (remove a tesourinha se ela estava riscada)
    # ==================================================

    def ao_selecionar_alternativa(self, indice, marcado):

        if not marcado:
            return

        tesoura = self.botoes_tesoura[indice]

        if tesoura.isChecked():

            tesoura.setChecked(False)

            self.labels_alternativas[indice].setStyleSheet("")

    # ==================================================
    # RISCAR / DESRISCAR ALTERNATIVA
    # ==================================================

    def alternar_risco(self, indice):

        label_texto = self.labels_alternativas[indice]

        if self.botoes_tesoura[indice].isChecked():

            label_texto.setStyleSheet(ESTILO_RISCADO)

        else:

            label_texto.setStyleSheet("")

    # ==================================================
    # LIMPAR CORES / RISCOS DE TODAS AS LINHAS
    # ==================================================

    def limpar_visual_alternativas(self):

        for linha, radio, tesoura, label_texto in zip(
            self.linhas, self.radios,
            self.botoes_tesoura, self.labels_alternativas
        ):

            linha.setStyleSheet("")

            label_texto.setStyleSheet("")

            radio.setChecked(False)

            radio.setEnabled(True)

            tesoura.setEnabled(True)

            tesoura.setChecked(False)

        self.lbl_feedback.hide()

    # ==================================================
    # SEÇÃO: RESULTADO FINAL
    # ==================================================

    def criar_secao_resultado(self):

        self.resultado_widget = QWidget()

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(12)

        self.resultado_widget.setLayout(layout)

        titulo_resultado = QLabel("🏁 Resultado do Simulado")

        titulo_resultado.setObjectName("subtituloPagina")

        titulo_resultado.setAlignment(Qt.AlignCenter)

        layout.addWidget(titulo_resultado)

        self.lbl_nota = QLabel()

        self.lbl_nota.setAlignment(Qt.AlignCenter)

        self.lbl_nota.setStyleSheet(
            "font-size:16px; font-weight:600; padding:6px;"
        )

        layout.addWidget(self.lbl_nota)

        self.resumo_widget = QWidget()

        self.resumo_layout = QVBoxLayout()

        self.resumo_layout.setContentsMargins(0, 0, 0, 0)

        self.resumo_layout.setSpacing(8)

        self.resumo_widget.setLayout(self.resumo_layout)

        layout.addWidget(self.resumo_widget)

        self.botao_novo_simulado = QPushButton("🔄 Novo Simulado")

        self.botao_novo_simulado.clicked.connect(self.mostrar_configuracao)

        layout.addWidget(self.botao_novo_simulado)

        self.layout_card.addWidget(self.resultado_widget)

    # ==================================================
    # ROTULO PADRÃO
    # ==================================================

    def criar_rotulo(self, texto):

        rotulo = QLabel(texto)

        rotulo.setObjectName("campoRotulo")

        return rotulo

    # ==================================================
    # TROCA DE SEÇÃO VISÍVEL
    # ==================================================

    def mostrar_configuracao(self):

        self.parar_cronometro()

        self.carregar_categorias()

        self.config_widget.show()
        self.questao_widget.hide()
        self.resultado_widget.hide()

    def mostrar_questao(self):

        self.config_widget.hide()
        self.questao_widget.show()
        self.resultado_widget.hide()

    def mostrar_resultado(self):

        self.config_widget.hide()
        self.questao_widget.hide()
        self.resultado_widget.show()

    # ==================================================
    # CARREGAR OPÇÕES DE FILTRO DISPONÍVEIS
    # ==================================================

    def carregar_categorias(self):

        self.combo_categoria.clear()

        self.combo_categoria.addItem("Todas as categorias")

        try:

            for item in buscar_categorias():

                self.combo_categoria.addItem(item)

        except Exception:

            pass

        self.combo_banca.clear()

        self.combo_banca.addItem("Todas as bancas")

        try:

            for item in buscar_bancas():

                self.combo_banca.addItem(item)

        except Exception:

            pass

        self.combo_ano.clear()

        self.combo_ano.addItem("Todos os anos")

        try:

            for item in buscar_anos():

                self.combo_ano.addItem(str(item))

        except Exception:

            pass

    # ==================================================
    # INICIAR SIMULADO
    # ==================================================

    def iniciar_simulado(self):

        quantidade = self.spin_quantidade.value()

        categoria = self.combo_categoria.currentText()

        if categoria == "Todas as categorias":

            categoria = None

        dificuldade = self.combo_dificuldade.currentText()

        if dificuldade == "Todas as dificuldades":

            dificuldade = None

        banca = self.combo_banca.currentText()

        if banca == "Todas as bancas":

            banca = None

        ano_texto = self.combo_ano.currentText()

        ano = None

        if ano_texto and ano_texto != "Todos os anos":

            try:
                ano = int(ano_texto)
            except ValueError:
                ano = None

        try:

            self.questoes = list(
                buscar_questoes_quantidade(
                    quantidade, categoria, dificuldade, banca, ano
                )
            )

        except Exception as erro:

            QMessageBox.critical(self, "Erro", str(erro))

            return

        if not self.questoes:

            QMessageBox.warning(

                self,

                "Atenção",

                "Nenhuma questão encontrada para esses filtros."

            )

            return

        self.indice = 0

        self.respostas = {}

        self.mostrar_questao()

        self.carregar_questao_atual()

        if self.checkbox_cronometro.isChecked():

            duracao = (
                self.spin_horas.value() * 3600
                + self.spin_minutos.value() * 60
            )

            if duracao <= 0:

                QMessageBox.warning(

                    self,

                    "Atenção",

                    "Defina uma duração maior que zero para o cronômetro."

                )

            else:

                self.iniciar_cronometro(duracao)

        else:

            self.modo_prova = False

            self.painel_cronometro.hide()

            self.lbl_toast.hide()

    # ==================================================
    # CARREGAR QUESTÃO ATUAL DO SIMULADO
    # ==================================================

    def carregar_questao_atual(self):

        self.limpar_visual_alternativas()

        self.frame_comentario.hide()

        questao = self.questoes[self.indice]

        self.lbl_contador.setText(
            f"Questão {self.indice + 1} de {len(self.questoes)}"
        )

        categoria = questao["categoria"] or ""
        subcategoria = questao["subcategoria"] or ""

        texto_categoria = categoria

        if subcategoria:
            texto_categoria += "  •  " + subcategoria

        self.lbl_categoria_questao.setText(
            texto_categoria or "Sem categoria"
        )

        self.lbl_pergunta.setText(questao["pergunta"])

        tipo = questao["tipo"]

        if tipo == "CERTO_ERRADO":

            nomes = ["CERTO", "ERRADO"]

            for i, linha in enumerate(self.linhas):

                if i < 2:

                    linha.show()
                    self.radios[i].setChecked(False)
                    self.labels_alternativas[i].setText(nomes[i])

                else:

                    linha.hide()

        else:

            alternativas = [
                questao["alternativa_a"],
                questao["alternativa_b"],
                questao["alternativa_c"],
                questao["alternativa_d"],
                questao["alternativa_e"]
            ]

            letras = ["A", "B", "C", "D", "E"]

            for i, linha in enumerate(self.linhas):

                texto = alternativas[i]

                if texto:

                    linha.show()
                    self.radios[i].setChecked(False)
                    self.labels_alternativas[i].setText(
                        f"{letras[i]}) {texto}"
                    )

                else:

                    linha.hide()

        self.botao_responder.setEnabled(True)

        self.botao_responder.show()

        self.botao_avancar.setEnabled(False)

        ultima = self.indice == len(self.questoes) - 1

        self.botao_avancar.setText(
            "🏁 Finalizar Simulado" if ultima else "➡ Próxima Questão"
        )

    # ==================================================
    # RESPONDER QUESTÃO (mostra cores na hora)
    # ==================================================

    def responder_questao(self):

        questao = self.questoes[self.indice]

        if questao["tipo"] == "CERTO_ERRADO":
            opcoes = ["CERTO", "ERRADO"]
        else:
            opcoes = ["A", "B", "C", "D", "E"]

        indice_usuario = None

        for i, radio in enumerate(self.radios):

            if radio.isVisible() and radio.isChecked():

                indice_usuario = i

                break

        if indice_usuario is None:

            QMessageBox.warning(

                self,

                "Atenção",

                "Selecione uma alternativa antes de continuar."

            )

            return

        resposta_usuario = opcoes[indice_usuario]

        resposta_correta = questao["resposta"]

        indice_correto = (
            opcoes.index(resposta_correta)
            if resposta_correta in opcoes
            else None
        )

        if indice_correto is not None:

            self.linhas[indice_correto].setStyleSheet(ESTILO_CORRETA)

        if resposta_usuario != resposta_correta:

            self.linhas[indice_usuario].setStyleSheet(ESTILO_ERRADA)

            resultado = "ERRO"

            self.lbl_feedback.setText("😔 Que pena, você errou!!!")

            self.lbl_feedback.setStyleSheet(
                f"font-size:16px; font-weight:700; "
                f"color:{CORES['aviso']}; padding:4px;"
            )

        else:

            resultado = "ACERTO"

            self.lbl_feedback.setText("🎉 Parabéns, você acertou!")

            self.lbl_feedback.setStyleSheet(
                f"font-size:16px; font-weight:700; "
                f"color:{CORES['sucesso']}; padding:4px;"
            )

        self.lbl_feedback.show()

        registrar_resultado(
            questao["id"],
            resposta_usuario,
            resultado
        )

        self.respostas[questao["id"]] = {
            "pergunta": questao["pergunta"],
            "resposta_usuario": resposta_usuario,
            "resposta_correta": resposta_correta,
            "correta": resultado == "ACERTO"
        }

        comentario = questao["comentario"]

        self.lbl_comentario_simulado.setText(
            comentario or "Não há comentário para esta questão."
        )

        self.frame_comentario.show()

        for radio in self.radios:
            radio.setEnabled(False)

        for tesoura in self.botoes_tesoura:
            tesoura.setEnabled(False)

        self.botao_responder.setEnabled(False)

        self.botao_avancar.setEnabled(True)

    # ==================================================
    # AVANÇAR PARA A PRÓXIMA QUESTÃO (ou finalizar)
    # ==================================================

    def avancar_questao(self):

        if self.indice < len(self.questoes) - 1:

            self.indice += 1

            self.carregar_questao_atual()

        else:

            self.finalizar_simulado()

    # ==================================================
    # FINALIZAR SIMULADO
    # ==================================================

    def finalizar_simulado(self):

        self.parar_cronometro()

        acertos = 0
        erros = 0

        while self.resumo_layout.count():

            filho = self.resumo_layout.takeAt(0)

            if filho.widget():
                filho.widget().deleteLater()

        for dados in self.respostas.values():

            correta = dados["correta"]

            if correta:
                acertos += 1
            else:
                erros += 1

            linha = QFrame()

            linha.setObjectName("linhaResumo")

            linha_layout = QVBoxLayout()

            linha_layout.setContentsMargins(14, 10, 14, 10)

            linha_layout.setSpacing(4)

            linha.setLayout(linha_layout)

            cor = CORES["sucesso"] if correta else CORES["aviso"]

            simbolo = "✅" if correta else "❌"

            texto_pergunta = QLabel(
                f"{simbolo} {dados['pergunta'][:120]}"
            )

            texto_pergunta.setWordWrap(True)

            texto_pergunta.setStyleSheet(
                f"font-size:13px; color:{cor}; font-weight:600;"
            )

            linha_layout.addWidget(texto_pergunta)

            texto_resposta = QLabel(
                f"Sua resposta: {dados['resposta_usuario']}   |   "
                f"Correta: {dados['resposta_correta']}"
            )

            texto_resposta.setObjectName("textoSecundario")

            linha_layout.addWidget(texto_resposta)

            self.resumo_layout.addWidget(linha)

        total = acertos + erros

        percentual = round((acertos / total) * 100, 1) if total else 0

        self.lbl_nota.setText(
            f"✅ Acertos: {acertos}    ❌ Erros: {erros}    "
            f"🎯 Aproveitamento: {percentual}%"
        )

        self.mostrar_resultado()

    # ==================================================
    # ENCERRAR SIMULADO MANUALMENTE
    # ==================================================

    def encerrar_simulado(self):

        if not self.respostas:

            self.mostrar_configuracao()

            return

        resposta = QMessageBox.question(

            self,

            "Encerrar simulado",

            "Deseja encerrar o simulado agora e ver o resultado?",

            QMessageBox.Yes | QMessageBox.No

        )

        if resposta == QMessageBox.Yes:

            self.finalizar_simulado()

    # ==================================================
    # CRONÔMETRO DE PROVA
    # ==================================================

    def iniciar_cronometro(self, segundos_totais):

        self.modo_prova = True

        self.segundos_totais = segundos_totais

        self.segundos_restantes = segundos_totais

        self.pausado = False

        self.marcos_horas_notificados = set()

        self.notificado_30min = False

        self.notificado_15min = False

        self.botao_pausar.setEnabled(True)

        self.botao_pausar.setText("⏸ Pausar")

        self.lbl_toast.hide()

        self.painel_cronometro.show()

        self.atualizar_label_tempo()

        self.timer_prova.start(1000)

    def parar_cronometro(self):

        self.timer_prova.stop()

        self.modo_prova = False

        self.pausado = False

        self.painel_cronometro.hide()

        self.lbl_toast.hide()

    def tick_cronometro(self):

        if self.pausado:
            return

        self.segundos_restantes -= 1

        if self.segundos_restantes <= 0:

            self.segundos_restantes = 0

            self.atualizar_label_tempo()

            self.timer_prova.stop()

            self.tempo_esgotado()

            return

        self.atualizar_label_tempo()

        self.checar_marcos_tempo()

    def atualizar_label_tempo(self):

        self.lbl_tempo_restante.setText(
            f"⏱ {self.formatar_tempo(self.segundos_restantes)}"
        )

    def formatar_tempo(self, segundos):

        h = segundos // 3600

        m = (segundos % 3600) // 60

        s = segundos % 60

        if h > 0:

            return f"{h}h {m:02d}min {s:02d}s"

        return f"{m}min {s:02d}s"

    def checar_marcos_tempo(self):

        decorrido = self.segundos_totais - self.segundos_restantes

        horas_decorridas = decorrido // 3600

        if (

            horas_decorridas > 0
            and horas_decorridas not in self.marcos_horas_notificados

        ):

            self.marcos_horas_notificados.add(horas_decorridas)

            self.mostrar_toast(
                f"⏱ Já se passou {horas_decorridas}h de prova — "
                f"restam {self.formatar_tempo(self.segundos_restantes)}."
            )

            return

        if self.segundos_restantes <= 1800 and not self.notificado_30min:

            self.notificado_30min = True

            self.mostrar_toast("⏱ Atenção: restam 30 minutos de prova!")

            return

        if self.segundos_restantes <= 900 and not self.notificado_15min:

            self.notificado_15min = True

            self.mostrar_toast("⏱ Atenção: restam 15 minutos de prova!")

    def mostrar_toast(self, mensagem):

        self.lbl_toast.setStyleSheet(
            f"background-color:{CORES['primaria_fraca']};"
            f"color:{CORES['primaria']};"
            f"border-radius:8px; padding:8px; font-weight:600;"
        )

        self.lbl_toast.setText(mensagem)

        self.lbl_toast.show()

        QTimer.singleShot(5000, self.lbl_toast.hide)

    def tempo_esgotado(self):

        self.lbl_toast.setStyleSheet(
            f"background-color:{CORES['erro_fraco']};"
            f"color:{CORES['erro']};"
            f"border-radius:8px; padding:8px; font-weight:700;"
        )

        self.lbl_toast.setText("⏰ Acabou o tempo da prova!")

        self.lbl_toast.show()

        for radio in self.radios:
            radio.setEnabled(False)

        for tesoura in self.botoes_tesoura:
            tesoura.setEnabled(False)

        self.botao_responder.setEnabled(False)

        self.botao_avancar.setEnabled(False)

        self.botao_pausar.setEnabled(False)

        QMessageBox.information(

            self,

            "Tempo esgotado",

            "O tempo da prova acabou!\n\n"
            "Clique em \"Encerrar Simulado\" para ver seu resultado."

        )

    def alternar_pausa(self):

        self.pausado = not self.pausado

        if self.pausado:

            self._estava_habilitado_antes_pausa = (
                self.botao_responder.isEnabled()
            )

            self.botao_responder.setEnabled(False)

            for radio in self.radios:
                radio.setEnabled(False)

            for tesoura in self.botoes_tesoura:
                tesoura.setEnabled(False)

            self.botao_pausar.setText("▶ Retomar")

        else:

            if getattr(self, "_estava_habilitado_antes_pausa", False):

                self.botao_responder.setEnabled(True)

                for radio in self.radios:
                    radio.setEnabled(True)

                for tesoura in self.botoes_tesoura:
                    tesoura.setEnabled(True)

            self.botao_pausar.setText("⏸ Pausar")

    def reiniciar_cronometro(self):

        resposta = QMessageBox.question(

            self,

            "Reiniciar cronômetro",

            "Reiniciar o tempo da prova do zero?",

            QMessageBox.Yes | QMessageBox.No

        )

        if resposta != QMessageBox.Yes:

            return

        self.segundos_restantes = self.segundos_totais

        self.marcos_horas_notificados = set()

        self.notificado_30min = False

        self.notificado_15min = False

        self.pausado = False

        self.botao_pausar.setText("⏸ Pausar")

        self.botao_pausar.setEnabled(True)

        self.lbl_toast.hide()

        for radio in self.radios:
            if radio.isVisible():
                radio.setEnabled(True)

        for tesoura in self.botoes_tesoura:
            if tesoura.isVisible():
                tesoura.setEnabled(True)

        if not self.botao_avancar.isEnabled():

            self.botao_responder.setEnabled(True)

        self.botao_avancar.setEnabled(True)

        self.atualizar_label_tempo()

        if not self.timer_prova.isActive():

            self.timer_prova.start(1000)