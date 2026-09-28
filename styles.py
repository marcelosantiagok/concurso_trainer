# ==========================================================
# STYLES.PY
# ==========================================================
#
# Design system centralizado do Concurso Trainer.
#
# Uso em main.py:
#
#   from styles import STYLESHEET
#   app.setStyle("Fusion")
#   app.setStyleSheet(STYLESHEET)
#
# As páginas usam apenas objectName (ex.: setObjectName("card"))
# para "assinar" quais elementos recebem qual estilo — nada de
# CSS solto espalhado em cada página.
# ==========================================================


# ==========================================================
# PALETA DE CORES
# ==========================================================
# Paleta "acadêmica" discreta: navy profundo no menu lateral,
# azul-índigo como cor de ação, fundo neutro levemente frio.

CORES = {

    # Base
    "fundo_janela": "#F3F5F9",
    "fundo_card": "#FFFFFF",
    "fundo_alternativo": "#F7F8FB",

    # Menu lateral
    "sidebar": "#16213E",
    "sidebar_hover": "#22315C",
    "sidebar_texto": "#E7EAF3",
    "sidebar_texto_apagado": "#8A93B2",

    # Ação primária
    "primaria": "#3454D1",
    "primaria_hover": "#2A44AD",
    "primaria_fraca": "#E8ECFB",

    # Texto
    "texto": "#1E2433",
    "texto_secundario": "#5B6478",
    "texto_apagado": "#9AA2B5",

    # Bordas
    "borda": "#E1E4EC",
    "borda_forte": "#C7CCDA",

    # Semânticas
    "sucesso": "#1F9D63",
    "sucesso_fraco": "#E4F7EE",
    "erro": "#D64545",
    "erro_fraco": "#FBEAEA",
    "aviso": "#C98A1B",
    "aviso_fraco": "#FBF1DF",

}


# ==========================================================
# TIPOGRAFIA
# ==========================================================

FONTE_FAMILIA = "'Segoe UI', 'Calibri', Arial, sans-serif"

TAMANHO_BASE = "14px"
TAMANHO_TITULO = "26px"
TAMANHO_SUBTITULO = "17px"
TAMANHO_PEQUENO = "12px"


# ==========================================================
# FOLHA DE ESTILOS GLOBAL (QSS)
# ==========================================================
# Widgets "assinam" o estilo através de objectName, por ex.:
#
#   titulo.setObjectName("tituloPagina")
#   card.setObjectName("card")
#   botao.setObjectName("botaoPerigo")
#
# Nomes disponíveis:
#   Texto:    tituloPagina, subtituloPagina, textoSecundario,
#             textoDestaque, badge, campoRotulo
#   Cards:    card, cardQuestao, linhaResumo
#   Botões:   (padrão já é o primário) botaoSecundario,
#             botaoPerigo, botaoMenu
#   Menu:     sidebar, tituloMenu, tituloMenuApagado

STYLESHEET = f"""

QWidget {{
    font-family: {FONTE_FAMILIA};
    font-size: {TAMANHO_BASE};
    color: {CORES['texto']};
}}

QMainWindow, #paginaCentral {{
    background-color: {CORES['fundo_janela']};
}}

/* ---------------------------------------------------- */
/* TÍTULOS E TEXTOS                                      */
/* ---------------------------------------------------- */

QLabel#tituloPagina {{
    font-size: {TAMANHO_TITULO};
    font-weight: 600;
    color: {CORES['texto']};
    padding: 4px 0px 8px 0px;
}}

QLabel#subtituloPagina {{
    font-size: {TAMANHO_SUBTITULO};
    font-weight: 600;
    color: {CORES['texto']};
    padding-top: 6px;
}}

QLabel#textoSecundario {{
    font-size: 13px;
    color: {CORES['texto_secundario']};
}}

QLabel#textoDestaque {{
    font-size: 13px;
    font-weight: 600;
    color: {CORES['primaria']};
}}

QLabel#badge {{
    background-color: {CORES['primaria_fraca']};
    color: {CORES['primaria']};
    font-size: 12px;
    font-weight: 600;
    border-radius: 10px;
    padding: 4px 10px;
}}

QLabel#campoRotulo {{
    font-size: 13px;
    font-weight: 600;
    color: {CORES['texto_secundario']};
    padding-top: 6px;
}}

/* ---------------------------------------------------- */
/* CARDS / CONTAINERS                                    */
/* ---------------------------------------------------- */

QWidget#card, QFrame#card {{
    background-color: {CORES['fundo_card']};
    border: 1px solid {CORES['borda']};
    border-radius: 14px;
}}

QLabel#cardQuestao {{
    background-color: {CORES['fundo_card']};
    border: 1px solid {CORES['borda']};
    border-radius: 12px;
    padding: 20px;
    font-size: 17px;
}}

QFrame#linhaResumo {{
    background-color: {CORES['fundo_alternativo']};
    border: 1px solid {CORES['borda']};
    border-radius: 10px;
}}

/* ---------------------------------------------------- */
/* CAMPOS DE ENTRADA                                     */
/* ---------------------------------------------------- */

QLineEdit, QTextEdit, QComboBox, QSpinBox {{
    background-color: {CORES['fundo_card']};
    border: 1px solid {CORES['borda_forte']};
    border-radius: 8px;
    padding: 8px 10px;
    selection-background-color: {CORES['primaria']};
    selection-color: white;
}}

QLineEdit:focus, QTextEdit:focus,
QComboBox:focus, QSpinBox:focus {{
    border: 1.5px solid {CORES['primaria']};
}}

QLineEdit:disabled, QTextEdit:disabled {{
    background-color: {CORES['fundo_alternativo']};
    color: {CORES['texto_apagado']};
}}

QComboBox::drop-down {{
    border: none;
    width: 26px;
}}

QComboBox QAbstractItemView {{
    background-color: {CORES['fundo_card']};
    border: 1px solid {CORES['borda']};
    border-radius: 8px;
    selection-background-color: {CORES['primaria_fraca']};
    selection-color: {CORES['primaria']};
    outline: none;
    padding: 4px;
}}

QSpinBox::up-button, QSpinBox::down-button {{
    width: 18px;
    border: none;
}}

/* ---------------------------------------------------- */
/* BOTÕES                                                */
/* ---------------------------------------------------- */

QPushButton {{
    background-color: {CORES['primaria']};
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 18px;
    font-size: 14px;
    font-weight: 600;
}}

QPushButton:hover {{
    background-color: {CORES['primaria_hover']};
}}

QPushButton:pressed {{
    background-color: {CORES['primaria_hover']};
}}

QPushButton:disabled {{
    background-color: {CORES['borda_forte']};
    color: {CORES['fundo_card']};
}}

QPushButton#botaoSecundario {{
    background-color: {CORES['fundo_card']};
    color: {CORES['primaria']};
    border: 1.5px solid {CORES['primaria']};
}}

QPushButton#botaoSecundario:hover {{
    background-color: {CORES['primaria_fraca']};
}}

QPushButton#botaoPerigo {{
    background-color: {CORES['erro']};
}}

QPushButton#botaoPerigo:hover {{
    background-color: #B93636;
}}

/* ---------------------------------------------------- */
/* RADIO BUTTONS                                         */
/* ---------------------------------------------------- */

QRadioButton {{
    font-size: 15px;
    padding: 10px 8px;
    spacing: 10px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 1.5px solid {CORES['borda_forte']};
    background-color: {CORES['fundo_card']};
}}

QRadioButton::indicator:hover {{
    border: 1.5px solid {CORES['primaria']};
}}

QRadioButton::indicator:checked {{
    border: 1.5px solid {CORES['primaria']};
    background: qradialgradient(
        cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
        stop:0 {CORES['primaria']},
        stop:0.45 {CORES['primaria']},
        stop:0.55 {CORES['fundo_card']},
        stop:1 {CORES['fundo_card']}
    );
}}

/* ---------------------------------------------------- */
/* TABELAS E LISTAS                                      */
/* ---------------------------------------------------- */

QTableWidget {{
    background-color: {CORES['fundo_card']};
    border: 1px solid {CORES['borda']};
    border-radius: 10px;
    gridline-color: {CORES['borda']};
    alternate-background-color: {CORES['fundo_alternativo']};
}}

QTableWidget::item {{
    padding: 6px;
}}

QHeaderView::section {{
    background-color: {CORES['fundo_alternativo']};
    color: {CORES['texto_secundario']};
    font-weight: 600;
    padding: 8px;
    border: none;
    border-bottom: 1px solid {CORES['borda']};
}}

QListWidget {{
    background-color: {CORES['fundo_card']};
    border: 1px solid {CORES['borda']};
    border-radius: 10px;
    padding: 6px;
    outline: none;
}}

QListWidget::item {{
    padding: 10px 8px;
    border-radius: 8px;
    margin: 2px 0px;
}}

QListWidget::item:selected {{
    background-color: {CORES['primaria_fraca']};
    color: {CORES['primaria']};
}}

QListWidget::item:hover {{
    background-color: {CORES['fundo_alternativo']};
}}

/* ---------------------------------------------------- */
/* SCROLL AREA / SCROLLBAR                               */
/* ---------------------------------------------------- */

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background: {CORES['borda_forte']};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {CORES['texto_apagado']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* ---------------------------------------------------- */
/* MENU LATERAL                                          */
/* ---------------------------------------------------- */

QWidget#sidebar {{
    background-color: {CORES['sidebar']};
}}

QLabel#tituloMenu {{
    color: {CORES['sidebar_texto']};
    font-size: 18px;
    font-weight: 700;
    padding: 22px 10px 22px 10px;
}}

QLabel#tituloMenuApagado {{
    color: {CORES['sidebar_texto_apagado']};
    font-size: 11px;
    font-weight: 600;
    padding: 0px 14px 8px 14px;
}}

QPushButton#botaoMenu {{
    background-color: transparent;
    color: {CORES['sidebar_texto']};
    text-align: left;
    padding: 12px 16px;
    border-radius: 9px;
    font-size: 14px;
    font-weight: 500;
}}

QPushButton#botaoMenu:hover {{
    background-color: {CORES['sidebar_hover']};
}}

QPushButton#botaoMenu:checked {{
    background-color: {CORES['primaria']};
    color: white;
}}

/* ---------------------------------------------------- */
/* ALTERNATIVAS COM TESOURA (Estudar / Simulado)         */
/* ---------------------------------------------------- */

QFrame#linhaOpcao {{
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 10px;
}}

QPushButton#botaoTesoura {{
    background-color: transparent;
    color: {CORES['texto_secundario']};
    border: none;
    border-radius: 8px;
    padding: 4px;
    font-size: 15px;
    font-weight: 400;
    min-width: 28px;
    max-width: 28px;
}}

QPushButton#botaoTesoura:hover {{
    background-color: {CORES['fundo_alternativo']};
}}

QPushButton#botaoTesoura:checked {{
    background-color: {CORES['primaria_fraca']};
    color: {CORES['primaria']};
}}

/* ---------------------------------------------------- */
/* CHECKBOX                                              */
/* ---------------------------------------------------- */

QCheckBox {{
    spacing: 8px;
    padding: 4px 0px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1.5px solid {CORES['borda_forte']};
    background-color: {CORES['fundo_card']};
}}

QCheckBox::indicator:hover {{
    border: 1.5px solid {CORES['primaria']};
}}

QCheckBox::indicator:checked {{
    background-color: {CORES['primaria']};
    border: 1.5px solid {CORES['primaria']};
}}

/* ---------------------------------------------------- */
/* BARRA DE PROGRESSO (sessão de estudo)                 */
/* ---------------------------------------------------- */

QProgressBar {{
    border: 1px solid {CORES['borda']};
    border-radius: 8px;
    background-color: {CORES['fundo_alternativo']};
    text-align: center;
    color: {CORES['texto_secundario']};
    min-height: 10px;
    max-height: 10px;
}}

QProgressBar::chunk {{
    background-color: {CORES['primaria']};
    border-radius: 8px;
}}

/* ---------------------------------------------------- */
/* MENSAGENS / CAIXAS DE DIÁLOGO                         */
/* ---------------------------------------------------- */

QMessageBox {{
    background-color: {CORES['fundo_card']};
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}
"""