from PySide6.QtWidgets import (

    QMainWindow,

    QWidget,

    QHBoxLayout,

    QVBoxLayout,

    QPushButton,

    QButtonGroup,

    QStackedWidget,

    QLabel

)


from PySide6.QtCore import Qt


from cadastro_page import CadastroPage

from editar_page import EditarPage

from estudar_page import EstudarPage

from estatisticas_page import EstatisticasPage

from backup_page import BackupPage

from simulado_page import SimuladoPage

from contato_page import ContatoPage

from importar_pdf_page import ImportarPdfPage


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Concurso Trainer 2.0"
        )

        self.resize(1200, 700)

        self.criar_interface()

    # ==================================================
    # CRIAR INTERFACE PRINCIPAL
    # ==================================================

    def criar_interface(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout_principal = QHBoxLayout()

        layout_principal.setContentsMargins(0, 0, 0, 0)

        layout_principal.setSpacing(0)

        central.setLayout(layout_principal)

        layout_principal.addWidget(self.criar_menu_lateral())

        # =================================================
        # ÁREA DAS PÁGINAS
        # =================================================

        self.paginas = QStackedWidget()

        self.paginas.setObjectName("paginaCentral")

        layout_principal.addWidget(self.paginas, 1)

        # Criar páginas

        self.cadastro_page = CadastroPage()

        self.editar_page = EditarPage()

        self.estudar_page = EstudarPage()

        self.estatisticas_page = EstatisticasPage()

        self.backup_page = BackupPage()

        self.simulado_page = SimuladoPage()

        self.contato_page = ContatoPage()

        self.importar_pdf_page = ImportarPdfPage()

        for pagina in (
            self.cadastro_page,
            self.editar_page,
            self.estudar_page,
            self.estatisticas_page,
            self.backup_page,
            self.simulado_page,
            self.contato_page,
            self.importar_pdf_page,
        ):

            self.paginas.addWidget(pagina)

        # Marca o botão da primeira página como ativo
        self.botao_cadastro.setChecked(True)

    # ==================================================
    # CRIAR MENU LATERAL
    # ==================================================

    def criar_menu_lateral(self):

        sidebar = QWidget()

        sidebar.setObjectName("sidebar")

        sidebar.setFixedWidth(230)

        menu = QVBoxLayout()

        menu.setContentsMargins(14, 10, 14, 20)

        menu.setSpacing(4)

        sidebar.setLayout(menu)

        titulo = QLabel("📚  Concurso\nTrainer")

        titulo.setObjectName("tituloMenu")

        menu.addWidget(titulo)

        rotulo_menu = QLabel("MENU")

        rotulo_menu.setObjectName("tituloMenuApagado")

        menu.addWidget(rotulo_menu)

        self.grupo_menu = QButtonGroup(self)

        self.grupo_menu.setExclusive(True)

        botoes_config = [
            ("botao_cadastro", "➕  Cadastro"),
            ("botao_editar", "✏️  Editar"),
            ("botao_estudar", "📖  Estudar"),
            ("botao_simulado", "📝  Simulado"),
            ("botao_estatisticas", "📊  Estatísticas"),
            ("botao_importar_pdf", "📥  Importar PDF"),
            ("botao_backup", "💾  Backup"),
            ("botao_contato", "💙  Ajude o Projeto"),
        ]

        for atributo, texto in botoes_config:

            botao = QPushButton(texto)

            botao.setObjectName("botaoMenu")

            botao.setCheckable(True)

            botao.setMinimumHeight(42)

            setattr(self, atributo, botao)

            self.grupo_menu.addButton(botao)

            menu.addWidget(botao)

        menu.addStretch()

        rodape = QLabel("v2.0")

        rodape.setObjectName("tituloMenuApagado")

        rodape.setAlignment(Qt.AlignCenter)

        menu.addWidget(rodape)

        # Conectar botões à troca de página

        self.botao_cadastro.clicked.connect(
            lambda: self.trocar_pagina(self.cadastro_page, self.botao_cadastro)
        )

        self.botao_editar.clicked.connect(
            lambda: self.trocar_pagina(self.editar_page, self.botao_editar)
        )

        self.botao_estudar.clicked.connect(
            lambda: self.trocar_pagina(self.estudar_page, self.botao_estudar)
        )

        self.botao_simulado.clicked.connect(
            lambda: self.trocar_pagina(self.simulado_page, self.botao_simulado)
        )

        self.botao_estatisticas.clicked.connect(
            lambda: self.trocar_pagina(self.estatisticas_page, self.botao_estatisticas)
        )

        self.botao_backup.clicked.connect(
            lambda: self.trocar_pagina(self.backup_page, self.botao_backup)
        )

        self.botao_contato.clicked.connect(
            lambda: self.trocar_pagina(self.contato_page, self.botao_contato)
        )

        self.botao_importar_pdf.clicked.connect(
            lambda: self.trocar_pagina(
                self.importar_pdf_page, self.botao_importar_pdf
            )
        )

        return sidebar

    # ==================================================
    # TROCAR DE PÁGINA
    # ==================================================

    def trocar_pagina(self, pagina, botao):

        self.paginas.setCurrentWidget(pagina)

        botao.setChecked(True)

    # ==================================================
    # CRIAR BARRA SUPERIOR
    # ==================================================

    def criar_barra_superior(self):

        barra = QHBoxLayout()

        self.botao_pdf = QPushButton(
            "📄 Exportar PDF"
        )

        self.botao_pdf.clicked.connect(
            self.exportar_pdf
        )

        barra.addWidget(
            self.botao_pdf
        )

        barra.addStretch()

        return barra

    # ==================================================
    # EXPORTAR PDF
    # ==================================================

    def exportar_pdf(self):

        from PySide6.QtWidgets import (
            QFileDialog,
            QMessageBox
        )

        from gerador_pdf import criar_pdf

        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar PDF",
            "questoes_concurso.pdf",
            "Arquivo PDF (*.pdf)"
        )

        if caminho:

            sucesso = criar_pdf(caminho)

            if sucesso:

                QMessageBox.information(
                    self,
                    "Sucesso",
                    "PDF criado com sucesso!"
                )

            else:

                QMessageBox.critical(
                    self,
                    "Erro",
                    "Não foi possível gerar o PDF."
                )

    # ==================================================
    # ATUALIZAR TELAS
    # ==================================================

    def atualizar_telas(self):

        try:

            self.editar_page.carregar_lista()

        except Exception:

            pass

        try:

            self.estatisticas_page.atualizar_dados()

        except Exception:

            pass

    # ==================================================
    # MOSTRAR PRIMEIRA TELA
    # ==================================================

    def iniciar_programa(self):

        self.trocar_pagina(self.estudar_page, self.botao_estudar)

        self.atualizar_telas()