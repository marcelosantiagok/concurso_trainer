import sqlite3
import json
import csv
import shutil
import os

from datetime import datetime, timedelta


CAMINHO_BANCO = "concurso.db"


# ==========================================================
# INTERVALOS DE REVISÃO ESPAÇADA (ESTILO ANKI)
# ==========================================================
# nivel -> quantos dias até a próxima revisão
# Acerto sobe de nível (intervalo maior).
# Erro volta para o nível 1 (revisão amanhã).

INTERVALOS_REVISAO = {
    1: 1,
    2: 2,
    3: 4,
    4: 7,
    5: 15,
    6: 30,
    7: 60,
}

NIVEL_MAXIMO = 7



def conectar():

    conexao = sqlite3.connect(
        CAMINHO_BANCO
    )

    conexao.row_factory = sqlite3.Row

    return conexao

# ==========================================================
# CRIAR TABELAS DO SISTEMA
# ==========================================================

def criar_tabelas():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questoes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        categoria TEXT NOT NULL,

        subcategoria TEXT,

        pergunta TEXT NOT NULL,

        tipo TEXT DEFAULT 'MULTIPLA',

        alternativa_a TEXT,
        alternativa_b TEXT,
        alternativa_c TEXT,
        alternativa_d TEXT,
        alternativa_e TEXT,

        resposta TEXT NOT NULL,

        comentario TEXT,

        banca TEXT,

        ano INTEGER,

        dificuldade TEXT DEFAULT 'NORMAL',

        data_cadastro TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        questao_id INTEGER,

        resposta_usuario TEXT,

        resultado TEXT,

        data_estudo TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estatisticas(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        questao_id INTEGER UNIQUE,

        tentativas INTEGER DEFAULT 0,

        acertos INTEGER DEFAULT 0,

        erros INTEGER DEFAULT 0,

        ultimo_estudo TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        chave TEXT UNIQUE,

        valor TEXT

    )
    """)

    conexao.commit()
    conexao.close()

    migrar_colunas_revisao()


# ==========================================================
# MIGRAÇÃO: COLUNAS DO SISTEMA DE REVISÃO ESPAÇADA
# ==========================================================
# Adiciona nivel/sequencia/ultima_revisao/proxima_revisao
# na tabela questoes caso ainda não existam, sem apagar
# nenhum dado já cadastrado. Seguro rodar toda vez que o
# programa inicia.

def migrar_colunas_revisao():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("PRAGMA table_info(questoes)")

    colunas_existentes = [
        linha["name"] for linha in cursor.fetchall()
    ]

    colunas_novas = {
        "nivel": "INTEGER DEFAULT 1",
        "sequencia": "INTEGER DEFAULT 0",
        "ultima_revisao": "TEXT",
        "proxima_revisao": "TEXT",
    }

    for nome, tipo in colunas_novas.items():

        if nome not in colunas_existentes:

            cursor.execute(
                f"ALTER TABLE questoes ADD COLUMN {nome} {tipo}"
            )

    conexao.commit()

    conexao.close()


def inserir_questao(

        categoria,

        subcategoria,

        pergunta,

        tipo,

        alternativa_a,

        alternativa_b,

        alternativa_c,

        alternativa_d,

        alternativa_e,

        resposta,

        comentario,

        banca=None,

        ano=None,

        dificuldade="NORMAL"

):


    conexao = conectar()

    cursor = conexao.cursor()



    data = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )



    cursor.execute("""
    
    INSERT INTO questoes
    (

        categoria,

        subcategoria,

        pergunta,

        tipo,


        alternativa_a,

        alternativa_b,

        alternativa_c,

        alternativa_d,

        alternativa_e,


        resposta,

        comentario,


        banca,

        ano,

        dificuldade,


        data_cadastro

    )


    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """,

    (

        categoria,

        subcategoria,

        pergunta,

        tipo,


        alternativa_a,

        alternativa_b,

        alternativa_c,

        alternativa_d,

        alternativa_e,


        resposta,

        comentario,


        banca,

        ano,

        dificuldade,


        data

    ))



    conexao.commit()


    id_questao = cursor.lastrowid


    conexao.close()


    return id_questao





# ==========================================================
# BUSCAR ÚLTIMA QUESTÃO CADASTRADA
# ==========================================================

def buscar_ultima_questao():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    ORDER BY id DESC

    LIMIT 1

    """)



    resultado = cursor.fetchone()



    conexao.close()


    return resultado





# ==========================================================
# BUSCAR QUESTÃO POR ID
# ==========================================================

def buscar_questao_por_id(
        id_questao
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    WHERE id = ?

    """,

    (

        id_questao,

    ))



    resultado = cursor.fetchone()



    conexao.close()


    return resultado





# ==========================================================
# BUSCAR TODAS AS QUESTÕES
# ==========================================================

def buscar_todas_questoes():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    ORDER BY id DESC

    """)



    resultado = cursor.fetchall()



    conexao.close()


    return resultado





# ==========================================================
# COMPATIBILIDADE COM VERSÕES ANTERIORES
# ==========================================================

def listar_questoes():

    return buscar_todas_questoes()





# ==========================================================
# ATUALIZAR QUESTÃO
# ==========================================================

def atualizar_questao(

        id_questao,

        categoria,

        subcategoria,

        pergunta,

        tipo,

        alternativa_a,

        alternativa_b,

        alternativa_c,

        alternativa_d,

        alternativa_e,

        resposta,

        comentario,

        banca=None,

        ano=None,

        dificuldade="NORMAL"

):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    UPDATE questoes

    SET


        categoria = ?,

        subcategoria = ?,

        pergunta = ?,

        tipo = ?,


        alternativa_a = ?,

        alternativa_b = ?,

        alternativa_c = ?,

        alternativa_d = ?,

        alternativa_e = ?,


        resposta = ?,

        comentario = ?,


        banca = ?,

        ano = ?,

        dificuldade = ?


    WHERE id = ?

    """,

    (

        categoria,

        subcategoria,

        pergunta,

        tipo,


        alternativa_a,

        alternativa_b,

        alternativa_c,

        alternativa_d,

        alternativa_e,


        resposta,

        comentario,


        banca,

        ano,

        dificuldade,


        id_questao

    ))



    conexao.commit()


    conexao.close()





# ==========================================================
# EXCLUIR QUESTÃO
# ==========================================================

def excluir_questao(
        id_questao
):


    conexao = conectar()

    cursor = conexao.cursor()



    # remove histórico

    cursor.execute("""
    
    DELETE FROM historico

    WHERE questao_id = ?

    """,

    (

        id_questao,

    ))



    # remove estatística

    cursor.execute("""
    
    DELETE FROM estatisticas

    WHERE questao_id = ?

    """,

    (

        id_questao,

    ))



    # remove questão

    cursor.execute("""
    
    DELETE FROM questoes

    WHERE id = ?

    """,

    (

        id_questao,

    ))



    conexao.commit()


    conexao.close()
    
# ==========================================================
# PESQUISAR QUESTÕES
# ==========================================================

def pesquisar_questoes(texto):


    conexao = conectar()

    cursor = conexao.cursor()



    busca = f"%{texto}%"



    cursor.execute("""
    
    SELECT *

    FROM questoes

    WHERE

        pergunta LIKE ?

        OR categoria LIKE ?

        OR subcategoria LIKE ?

        OR banca LIKE ?

        OR dificuldade LIKE ?

    ORDER BY id DESC

    """,

    (

        busca,

        busca,

        busca,

        busca,

        busca

    ))



    resultado = cursor.fetchall()



    conexao.close()


    return resultado





# ==========================================================
# BUSCAR POR CATEGORIA
# ==========================================================

def buscar_por_categoria(
        categoria
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    WHERE categoria = ?

    ORDER BY id DESC

    """,

    (

        categoria,

    ))



    resultado = cursor.fetchall()



    conexao.close()


    return resultado





# ==========================================================
# BUSCAR POR SUBCATEGORIA
# ==========================================================

def buscar_por_subcategoria(
        subcategoria
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    WHERE subcategoria = ?

    ORDER BY id DESC

    """,

    (

        subcategoria,

    ))



    resultado = cursor.fetchall()



    conexao.close()


    return resultado





# ==========================================================
# BUSCAR POR BANCA
# ==========================================================

def buscar_por_banca(
        banca
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    WHERE banca = ?

    ORDER BY id DESC

    """,

    (

        banca,

    ))



    resultado = cursor.fetchall()



    conexao.close()


    return resultado





# ==========================================================
# BUSCAR POR DIFICULDADE
# ==========================================================

def buscar_por_dificuldade(
        dificuldade
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    WHERE dificuldade = ?

    ORDER BY id DESC

    """,

    (

        dificuldade,

    ))



    resultado = cursor.fetchall()



    conexao.close()


    return resultado





# ==========================================================
# BUSCAR POR ANO
# ==========================================================

def buscar_por_ano(
        ano
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    WHERE ano = ?

    ORDER BY id DESC

    """,

    (

        ano,

    ))



    resultado = cursor.fetchall()



    conexao.close()


    return resultado





# ==========================================================
# LISTAR CATEGORIAS
# ==========================================================

def buscar_categorias():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT DISTINCT categoria

    FROM questoes

    WHERE categoria IS NOT NULL

    AND categoria <> ''

    ORDER BY categoria

    """)



    resultado = cursor.fetchall()



    conexao.close()



    return [

        item["categoria"]

        for item in resultado

    ]





# ==========================================================
# LISTAR SUBCATEGORIAS
# ==========================================================

def buscar_subcategorias(
        categoria=None
):


    conexao = conectar()

    cursor = conexao.cursor()



    if categoria:


        cursor.execute("""
        
        SELECT DISTINCT subcategoria

        FROM questoes

        WHERE categoria = ?

        AND subcategoria IS NOT NULL

        AND subcategoria <> ''

        ORDER BY subcategoria

        """,

        (

            categoria,

        ))


    else:


        cursor.execute("""
        
        SELECT DISTINCT subcategoria

        FROM questoes

        WHERE subcategoria IS NOT NULL

        AND subcategoria <> ''

        ORDER BY subcategoria

        """)



    resultado = cursor.fetchall()



    conexao.close()



    return [

        item["subcategoria"]

        for item in resultado

    ]






# ==========================================================
# LISTAR BANCAS
# ==========================================================

def buscar_bancas():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""

    SELECT DISTINCT banca

    FROM questoes

    WHERE banca IS NOT NULL

    AND banca <> ''

    ORDER BY banca

    """)

    resultado = cursor.fetchall()

    conexao.close()

    return [
        item["banca"]
        for item in resultado
    ]


# ==========================================================
# LISTAR ANOS
# ==========================================================

def buscar_anos():

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""

    SELECT DISTINCT ano

    FROM questoes

    WHERE ano IS NOT NULL

    AND ano <> 0

    ORDER BY ano DESC

    """)

    resultado = cursor.fetchall()

    conexao.close()

    return [
        item["ano"]
        for item in resultado
    ]


# ==========================================================
# CONTAR QUESTÕES
# ==========================================================

def contar_questoes():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT COUNT(*) total

    FROM questoes

    """)



    resultado = cursor.fetchone()



    conexao.close()



    return resultado["total"]

# ==========================================================
# BUSCAR QUESTÃO PARA ESTUDO
# ==========================================================

def buscar_questao_estudo(

        categoria=None,

        dificuldade=None,

        banca=None,

        ano=None

):

    conexao = conectar()

    cursor = conexao.cursor()

    hoje = datetime.now().strftime("%Y-%m-%d")

    filtros = ""

    parametros = []

    if categoria:

        filtros += " AND categoria = ? "

        parametros.append(categoria)

    if dificuldade:

        filtros += " AND dificuldade = ? "

        parametros.append(dificuldade)

    if banca:

        filtros += " AND banca = ? "

        parametros.append(banca)

    if ano:

        filtros += " AND ano = ? "

        parametros.append(ano)

    # --------------------------------------
    # 1ª tentativa: questão atrasada na revisão
    # (proxima_revisao vazia = nunca estudada,
    # conta como atrasada também)
    # --------------------------------------

    consulta_atrasadas = f"""

        SELECT *

        FROM questoes

        WHERE (proxima_revisao IS NULL OR proxima_revisao <= ?)

        {filtros}

        ORDER BY

            CASE WHEN proxima_revisao IS NULL THEN 0 ELSE 1 END,

            proxima_revisao ASC

        LIMIT 1

    """

    cursor.execute(

        consulta_atrasadas,

        [hoje] + parametros

    )

    questao = cursor.fetchone()

    # --------------------------------------
    # 2ª tentativa: nada atrasado no momento,
    # então pega a questão com revisão mais
    # próxima de vencer (evita tela vazia)
    # --------------------------------------

    if questao is None:

        consulta_futuras = f"""

            SELECT *

            FROM questoes

            WHERE 1=1

            {filtros}

            ORDER BY

                CASE WHEN proxima_revisao IS NULL THEN 0 ELSE 1 END,

                proxima_revisao ASC

            LIMIT 1

        """

        cursor.execute(

            consulta_futuras,

            parametros

        )

        questao = cursor.fetchone()

    conexao.close()

    return questao





# ==========================================================
# BUSCAR QUESTÕES PARA SIMULADO
# ==========================================================

def buscar_questoes_quantidade(

        quantidade,

        categoria=None,

        dificuldade=None,

        banca=None,

        ano=None

):


    conexao = conectar()

    cursor = conexao.cursor()



    consulta = """

    SELECT *

    FROM questoes

    WHERE 1=1

    """



    parametros = []



    if categoria:


        consulta += """

        AND categoria = ?

        """


        parametros.append(
            categoria
        )



    if dificuldade:


        consulta += """

        AND dificuldade = ?

        """


        parametros.append(
            dificuldade
        )



    if banca:


        consulta += """

        AND banca = ?

        """


        parametros.append(
            banca
        )



    if ano:


        consulta += """

        AND ano = ?

        """


        parametros.append(
            ano
        )



    consulta += """

    ORDER BY RANDOM()

    LIMIT ?

    """



    parametros.append(
        quantidade
    )



    cursor.execute(

        consulta,

        parametros

    )



    resultado = cursor.fetchall()



    conexao.close()



    return resultado





# ==========================================================
# REGISTRAR RESULTADO DO ESTUDO
# ==========================================================

def registrar_resultado(

        questao_id,

        resposta_usuario,

        resultado

):


    conexao = conectar()

    cursor = conexao.cursor()



    data = datetime.now().strftime(

        "%d/%m/%Y %H:%M"

    )



    # --------------------------------------
    # SALVAR HISTÓRICO
    # --------------------------------------


    cursor.execute("""

    INSERT INTO historico

    (

        questao_id,

        resposta_usuario,

        resultado,

        data_estudo

    )


    VALUES (?,?,?,?)

    """,

    (

        questao_id,

        resposta_usuario,

        resultado,

        data

    ))





    # --------------------------------------
    # VERIFICAR ESTATÍSTICA EXISTENTE
    # --------------------------------------


    cursor.execute("""

    SELECT *

    FROM estatisticas

    WHERE questao_id = ?

    """,

    (

        questao_id,

    ))



    existente = cursor.fetchone()





    if existente:


        cursor.execute("""

        UPDATE estatisticas

        SET


            tentativas = tentativas + 1,


            acertos = acertos + ?,


            erros = erros + ?,


            ultimo_estudo = ?


        WHERE questao_id = ?

        """,

        (

            1 if resultado == "ACERTO" else 0,


            1 if resultado == "ERRO" else 0,


            data,


            questao_id

        ))



    else:


        cursor.execute("""

        INSERT INTO estatisticas

        (

            questao_id,

            tentativas,

            acertos,

            erros,

            ultimo_estudo

        )


        VALUES (?,?,?,?,?)

        """,

        (

            questao_id,


            1,


            1 if resultado == "ACERTO" else 0,


            1 if resultado == "ERRO" else 0,


            data

        ))






    # --------------------------------------
    # ATUALIZAR SISTEMA DE REVISAO ESPACADA
    # (nivel, sequencia, proxima_revisao)
    # --------------------------------------

    cursor.execute("""

    SELECT nivel, sequencia

    FROM questoes

    WHERE id = ?

    """,

    (
        questao_id,
    ))

    linha_questao = cursor.fetchone()

    nivel_atual = (
        linha_questao["nivel"]
        if linha_questao and linha_questao["nivel"]
        else 1
    )

    sequencia_atual = (
        linha_questao["sequencia"]
        if linha_questao and linha_questao["sequencia"]
        else 0
    )

    if resultado == "ACERTO":

        novo_nivel = min(nivel_atual + 1, NIVEL_MAXIMO)

        nova_sequencia = sequencia_atual + 1

    else:

        novo_nivel = 1

        nova_sequencia = 0

    dias_intervalo = INTERVALOS_REVISAO.get(novo_nivel, 1)

    agora = datetime.now()

    ultima_revisao = agora.strftime("%Y-%m-%d")

    proxima_revisao = (
        agora + timedelta(days=dias_intervalo)
    ).strftime("%Y-%m-%d")

    cursor.execute("""

    UPDATE questoes

    SET

        nivel = ?,

        sequencia = ?,

        ultima_revisao = ?,

        proxima_revisao = ?

    WHERE id = ?

    """,

    (
        novo_nivel,
        nova_sequencia,
        ultima_revisao,
        proxima_revisao,
        questao_id
    ))

    conexao.commit()

    conexao.close()





# ==========================================================
# BUSCAR HISTÓRICO DE UMA QUESTÃO
# ==========================================================

def buscar_historico_questao(

        questao_id

):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""

    SELECT *

    FROM historico

    WHERE questao_id = ?

    ORDER BY id DESC

    """,

    (

        questao_id,

    ))



    resultado = cursor.fetchall()



    conexao.close()



    return resultado

# ==========================================================
# BUSCAR ESTATÍSTICAS GERAIS
# ==========================================================

def buscar_estatisticas():


    conexao = conectar()

    cursor = conexao.cursor()


    dados = {}



    # --------------------------------------
    # TOTAL DE QUESTÕES
    # --------------------------------------

    cursor.execute("""
    
    SELECT COUNT(*) total

    FROM questoes

    """)


    dados["total_questoes"] = cursor.fetchone()["total"]




    # --------------------------------------
    # TOTAL DE TENTATIVAS
    # --------------------------------------

    cursor.execute("""
    
    SELECT SUM(tentativas) total

    FROM estatisticas

    """)


    resultado = cursor.fetchone()["total"]


    dados["tentativas"] = resultado or 0




    # --------------------------------------
    # TOTAL DE ACERTOS
    # --------------------------------------

    cursor.execute("""
    
    SELECT SUM(acertos) total

    FROM estatisticas

    """)


    resultado = cursor.fetchone()["total"]


    dados["acertos"] = resultado or 0




    # --------------------------------------
    # TOTAL DE ERROS
    # --------------------------------------

    cursor.execute("""
    
    SELECT SUM(erros) total

    FROM estatisticas

    """)


    resultado = cursor.fetchone()["total"]


    dados["erros"] = resultado or 0





    # --------------------------------------
    # PERCENTUAL
    # --------------------------------------

    if dados["tentativas"] > 0:


        dados["percentual"] = round(

            (

                dados["acertos"]

                /

                dados["tentativas"]

            )

            *

            100,

            2

        )


    else:


        dados["percentual"] = 0




    conexao.close()


    return dados





# ==========================================================
# ESTATÍSTICAS POR CATEGORIA
# ==========================================================

def buscar_estatisticas_categoria():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT


        q.categoria,


        COUNT(h.id) AS tentativas,


        SUM(

            CASE

            WHEN h.resultado = 'ACERTO'

            THEN 1

            ELSE 0

            END

        ) AS acertos,


        SUM(

            CASE

            WHEN h.resultado = 'ERRO'

            THEN 1

            ELSE 0

            END

        ) AS erros



    FROM questoes q


    LEFT JOIN historico h


    ON q.id = h.questao_id



    GROUP BY q.categoria



    ORDER BY acertos DESC


    """)



    resultado = cursor.fetchall()



    conexao.close()



    return resultado





# ==========================================================
# BUSCAR HISTÓRICO COMPLETO
# ==========================================================

def buscar_historico():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT


        h.id,


        h.questao_id,


        h.resposta_usuario,


        h.resultado,


        h.data_estudo,


        q.pergunta,


        q.categoria



    FROM historico h



    INNER JOIN questoes q


    ON q.id = h.questao_id



    ORDER BY h.id DESC


    """)



    resultado = cursor.fetchall()



    conexao.close()



    return resultado





# ==========================================================
# BUSCAR ÚLTIMOS ESTUDOS
# ==========================================================

def buscar_ultimos_estudos(

        limite=20

):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT


        h.*,


        q.pergunta,


        q.categoria



    FROM historico h



    INNER JOIN questoes q


    ON q.id = h.questao_id



    ORDER BY h.id DESC



    LIMIT ?

    """,

    (

        limite,

    ))



    resultado = cursor.fetchall()



    conexao.close()



    return resultado





# ==========================================================
# RESETAR ESTATÍSTICAS
# ==========================================================

def resetar_estatisticas():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    DELETE FROM historico

    """)



    cursor.execute("""
    
    DELETE FROM estatisticas

    """)



    cursor.execute("""

    UPDATE questoes

    SET

        nivel = 1,

        sequencia = 0,

        ultima_revisao = NULL,

        proxima_revisao = NULL

    """)



    conexao.commit()



    conexao.close()


# ==========================================================
# CRIAR CONFIGURAÇÕES PADRÃO
# ==========================================================

def criar_configuracoes_padrao():


    conexao = conectar()

    cursor = conexao.cursor()



    configuracoes = [

        (
            "versao",
            "2.0"
        ),

        (
            "data_criacao",
            datetime.now().strftime(
                "%d/%m/%Y"
            )
        ),

        (
            "nome_programa",
            "Concurso Trainer"
        )

    ]



    for chave, valor in configuracoes:


        cursor.execute("""
        
        INSERT OR IGNORE INTO configuracoes

        (

            chave,

            valor

        )

        VALUES (?,?)

        """,

        (

            chave,

            valor

        ))



    conexao.commit()

    conexao.close()





# ==========================================================
# BUSCAR CONFIGURAÇÃO
# ==========================================================

def buscar_configuracao(
        chave
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT valor

    FROM configuracoes

    WHERE chave = ?

    """,

    (

        chave,

    ))



    resultado = cursor.fetchone()



    conexao.close()



    if resultado:

        return resultado["valor"]


    return None





# ==========================================================
# CRIAR BACKUP DO BANCO
# ==========================================================

def criar_backup(
        caminho_destino=None
):

    if not os.path.exists(CAMINHO_BANCO):
        raise Exception("Banco de dados não encontrado.")

    if caminho_destino is None:

        pasta_backups = "Backups"

        os.makedirs(pasta_backups, exist_ok=True)

        data = datetime.now().strftime("%d-%m-%Y_%H-%M")

        caminho_destino = os.path.join(
            pasta_backups,
            f"backup_concurso_{data}.db"
        )

    shutil.copy(

        CAMINHO_BANCO,

        caminho_destino

    )

    return caminho_destino



# ==========================================================
# RESTAURAR BACKUP
# ==========================================================

def restaurar_backup(
        caminho_backup
):


    if os.path.exists(caminho_backup):


        shutil.copy(

            caminho_backup,

            CAMINHO_BANCO

        )





# ==========================================================
# EXPORTAR JSON
# ==========================================================

def exportar_json(
        caminho
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    """)



    questoes = cursor.fetchall()



    dados = []



    for questao in questoes:


        dados.append(

            dict(questao)

        )



    with open(

        caminho,

        "w",

        encoding="utf-8"

    ) as arquivo:


        json.dump(

            dados,

            arquivo,

            ensure_ascii=False,

            indent=4

        )



    conexao.close()





# ==========================================================
# IMPORTAR JSON
# ==========================================================

def importar_json(
        caminho
):


    with open(

        caminho,

        "r",

        encoding="utf-8"

    ) as arquivo:


        dados = json.load(
            arquivo
        )



    conexao = conectar()

    cursor = conexao.cursor()



    for item in dados:


        cursor.execute("""
        
        INSERT INTO questoes

        (

            categoria,

            subcategoria,

            pergunta,

            tipo,

            alternativa_a,

            alternativa_b,

            alternativa_c,

            alternativa_d,

            alternativa_e,

            resposta,

            comentario,

            banca,

            ano,

            dificuldade,

            data_cadastro

        )


        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

            item.get("categoria"),

            item.get("subcategoria"),

            item.get("pergunta"),

            item.get("tipo"),

            item.get("alternativa_a"),

            item.get("alternativa_b"),

            item.get("alternativa_c"),

            item.get("alternativa_d"),

            item.get("alternativa_e"),

            item.get("resposta"),

            item.get("comentario"),

            item.get("banca"),

            item.get("ano"),

            item.get("dificuldade"),

            item.get("data_cadastro")

        ))



    conexao.commit()

    conexao.close()





# ==========================================================
# EXPORTAR CSV
# ==========================================================

def exportar_csv(
        caminho
):


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute("""
    
    SELECT *

    FROM questoes

    """)



    dados = cursor.fetchall()



    conexao.close()



    if not dados:

        return



    colunas = dados[0].keys()



    with open(

        caminho,

        "w",

        newline="",

        encoding="utf-8-sig"

    ) as arquivo:


        escritor = csv.writer(
            arquivo
        )



        escritor.writerow(
            colunas
        )



        for linha in dados:


            escritor.writerow(

                [

                    linha[coluna]

                    for coluna in colunas

                ]

            )





# ==========================================================
# LIMPAR BANCO COMPLETO
# ==========================================================

def limpar_banco():


    conexao = conectar()

    cursor = conexao.cursor()



    cursor.execute(
        "DELETE FROM historico"
    )


    cursor.execute(
        "DELETE FROM estatisticas"
    )


    cursor.execute(
        "DELETE FROM questoes"
    )



    conexao.commit()

    conexao.close()





# ==========================================================
# INICIALIZAÇÃO COMPLETA DO SISTEMA
# ==========================================================

def iniciar_sistema():


    inicializar()

    criar_configuracoes_padrao()



# ==========================================================
# INICIALIZAÇÃO DO SISTEMA
# ==========================================================

def inicializar():

    criar_tabelas()

    criar_configuracoes_padrao()