import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import database

from main_window import MainWindow

from styles import STYLESHEET

# ==========================================
# ÍCONE DO APLICATIVO
# ==========================================
# Caminho absoluto (baseado na pasta deste arquivo) para
# funcionar independente de onde o programa é executado.
# Prioriza o .ico (multi-resolução, ideal para Windows/
# taskbar/atalho) e cai para o .png caso o .ico não exista.

PASTA_BASE = os.path.dirname(os.path.abspath(__file__))

CAMINHO_ICONE_ICO = os.path.join(PASTA_BASE, "icone.ico")

CAMINHO_ICONE_PNG = os.path.join(PASTA_BASE, "icone.png")

CAMINHO_ICONE = (
    CAMINHO_ICONE_ICO
    if os.path.exists(CAMINHO_ICONE_ICO)
    else CAMINHO_ICONE_PNG
)

# ==========================================
# CRIAR BANCO
# ==========================================

database.inicializar()

# ==========================================
# INICIAR PROGRAMA
# ==========================================

app = QApplication(sys.argv)

# "Fusion" garante que o QSS (bordas arredondadas, cores
# de foco, etc.) seja respeitado de forma consistente —
# alguns estilos nativos do Windows ignoram parte do QSS.
app.setStyle("Fusion")

app.setStyleSheet(STYLESHEET)

icone_app = None

if os.path.exists(CAMINHO_ICONE):

    icone_app = QIcon(CAMINHO_ICONE)

    app.setWindowIcon(icone_app)

janela = MainWindow()

if icone_app is not None:

    janela.setWindowIcon(icone_app)

janela.resize(1200, 700)
janela.setMinimumSize(1000, 650)

janela.show()

sys.exit(app.exec())