<p align="center">
  <img src="icone.png" alt="Concurso Trainer" width="150">
</p>

<h1 align="center">Concurso Trainer</h1>

<p align="center">
  Organize suas questões e estude para concursos no seu ritmo.
  <br>
  Gratuito para usar, sem anúncios e sem assinatura.
</p>

<p align="center">
  <img alt="Windows" src="https://img.shields.io/badge/Windows-64--bit-0078D4?logo=windows&logoColor=white">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white">
  <img alt="Interface" src="https://img.shields.io/badge/interface-PySide6-41CD52?logo=qt&logoColor=white">
  <img alt="Anúncios" src="https://img.shields.io/badge/anúncios-nenhum-brightgreen">
</p>

O **Concurso Trainer** é um aplicativo de estudos para quem está se preparando para concursos públicos. Em vez de depender de uma plataforma paga, você monta e organiza seu próprio banco de questões, pratica, acompanha seu desempenho e revisa os conteúdos no computador.

## Por que usar

- **Gratuito:** sem mensalidade ou cobrança para usar o programa.
- **Sem anúncios:** a interface não exibe propaganda.
- **Seu banco de questões:** cadastre questões que você já tem autorização para usar; o programa não vende nem fornece um banco de questões de terceiros.
- **Dados no seu computador:** questões e histórico são guardados localmente em SQLite; não é necessário criar conta.
- **Você decide o ritmo:** estude por disciplina, assunto, banca, ano e dificuldade, conforme os filtros disponíveis.

> O programa ajuda a organizar os estudos, mas não substitui edital, materiais oficiais nem a conferência das respostas e dos direitos de uso das questões.

## Recursos

- Cadastro, edição, pesquisa e organização de questões de múltipla escolha e de certo ou errado.
- Registro de categoria, subcategoria, banca, ano, dificuldade, resposta e comentário.
- Sessões de estudo com registro de respostas, acertos e erros.
- Revisão espaçada: questões acertadas avançam por intervalos de 1, 2, 4, 7, 15, 30 e 60 dias; erros retornam ao primeiro nível.
- Estatísticas gerais e por categoria, com histórico de estudos.
- Geração de simulados e exportação de questões para PDF.
- Importação de texto de PDFs de provas para uma tela de revisão antes de cadastrar as questões.
- Ferramenta visual beta para selecionar trechos de PDFs e preencher os campos manualmente.
- Backup do banco e importação/exportação de dados em JSON; exportação em CSV.

### Importação de PDF

A extração automática funciona melhor com PDFs que contêm texto selecionável. PDFs digitalizados como imagem podem exigir OCR, que não está incluído. A identificação de enunciados, alternativas e gabaritos usa padrões e deve ser revisada antes de salvar. A ferramenta de seleção visual está em desenvolvimento.

## Instalação no Windows

Baixe o instalador na área [Releases](https://github.com/marcelosantiagok/concurso_trainer/releases) quando uma versão estiver publicada. Execute `ConcursoTrainer-Setup.exe` e siga as instruções. A versão distribuída é de 64 bits e não exige Python instalado no computador de uso.

## Executar a partir do código-fonte

Requer Windows de 64 bits e Python instalado. No PowerShell, na pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-build.txt
python main.py
```

O aplicativo cria o banco `concurso.db` no diretório de execução se ele ainda não existir.

## Gerar o executável e o instalador

Na máquina de build, use Windows de 64 bits, instale o Python e o [Inno Setup 6](https://jrsoftware.org/isdl.php) e execute na pasta do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-build.txt
pyinstaller --clean --noconfirm ConcursoTrainer.spec
```

Depois, abra `ConcursoTrainer.iss` no Inno Setup e escolha **Compile**. O instalador será salvo em `installer\ConcursoTrainer-Setup.exe`.

## Estrutura de dados e backups

O banco SQLite guarda as questões e o histórico localmente. Use a função **Backup** no aplicativo e mantenha uma cópia dos arquivos exportados em outro local. Ao reinstalar ou trocar de computador, importe o backup para recuperar seus dados. Não compartilhe o banco se ele contiver informações que você queira manter privadas.

## Tecnologias

- Python
- PySide6 / Qt
- SQLite
- ReportLab
- pypdf
- PyMuPDF
- PyInstaller
- Inno Setup

## Licença

Este repositório ainda não contém um arquivo de licença. O programa é gratuito para uso, mas as condições para copiar, modificar ou redistribuir o código ainda precisam ser definidas pelo autor. As bibliotecas usadas têm licenças próprias.

## Contribuições e contato

Sugestões, correções e melhorias são bem-vindas por meio de [Issues](https://github.com/marcelosantiagok/concurso_trainer/issues) e Pull Requests. Ao contribuir, não envie bancos de questões, PDFs ou outros materiais protegidos por direitos autorais sem autorização.
