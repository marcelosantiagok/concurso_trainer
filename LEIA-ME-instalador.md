# Empacotamento do Concurso Trainer

O projeto inspecionado usa `main.py` como ponto de entrada. Os módulos Python ficam juntos na raiz e os recursos visuais são `icone.ico` e `icone.png`.

Dependências identificadas:

- PySide6 — interface gráfica Qt;
- ReportLab — geração de PDFs;
- pypdf — leitura e extração de texto dos PDFs;
- PyMuPDF (`fitz`) — visualização e seleção de trechos de PDF;
- SQLite — incluído na biblioteca padrão do Python.

## Arquivos deste pacote

- `ConcursoTrainer.spec`: configuração PyInstaller em modo pasta (`onedir`), com os ícones e módulos de PDF;
- `ConcursoTrainer.iss`: script Inno Setup para gerar o instalador com atalhos;
- `requirements-build.txt`: dependências para a máquina que fará o build.

Copie esses três arquivos para a pasta do projeto (`E:\Projetos\concurso_trainer_atualizado\concurso_trainer`). O `.spec` referencia essa localização do projeto explicitamente.

## Gerar o programa e o instalador

Na máquina de build, instale Python 3.11 ou 3.12 de 64 bits, depois abra o PowerShell na pasta do projeto e rode:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-build.txt
pyinstaller --clean --noconfirm ConcursoTrainer.spec
```

Instale o Inno Setup 6 nessa máquina. Abra `ConcursoTrainer.iss` no Inno Setup e clique em **Compile**. O instalador será criado em `installer\ConcursoTrainer-Setup.exe`. O computador de destino não precisa ter Python: o PyInstaller inclui o runtime e as bibliotecas.

Antes de distribuir, teste a pasta `dist\ConcursoTrainer` em um Windows limpo e depois teste o instalador em outra conta ou computador. O build deve ser feito no Windows para produzir um executável Windows.

## Ajuste de dados necessário para distribuição segura

O `database.py` atual define `CAMINHO_BANCO = "concurso.db"`, relativo ao diretório de trabalho. O instalador proposto é por usuário e instala em `%LOCALAPPDATA%\Programs`, o que costuma permitir gravação, mas isso mistura o banco do usuário com os arquivos do aplicativo e pode perder dados ao desinstalar/reinstalar ou ao atualizar.

Antes de distribuir amplamente, altere o código para gravar o banco em uma pasta de dados do usuário, por exemplo `%APPDATA%\Concurso Trainer\concurso.db`, criando o diretório quando necessário. Se já houver `concurso.db` na pasta do projeto, planeje copiar/migrar esse banco para o novo local para preservar questões existentes. Faça backup antes de qualquer migração.

Não foi gerado um EXE neste ambiente: a pasta do projeto foi disponibilizada somente para leitura, e a compilação final depende de instalar as dependências e o Inno Setup na máquina Windows de build.
