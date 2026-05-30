
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


# =========================
# CONEXÃO COM BANCO
# =========================

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="mydb"
    )


# =========================
# CRIAR TABELAS
# =========================

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    # CLIENTES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(50),
            telefone VARCHAR(20),
            cpf VARCHAR(14),
            data_nascimento DATE,
            bairro VARCHAR(50),
            rua VARCHAR(100),
            numero_casa VARCHAR(10),
            cidade VARCHAR(50),
            estado VARCHAR(2),
            cep VARCHAR(9),
            complemento VARCHAR(100)
        )
    """)

    # SERVIÇOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            valor DECIMAL(10,2)
        )
    """)
    # PAGAMENTOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagamentos (
        id_pagamento INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(30)
    )
""")

    # AGENDAMENTOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT,
            id_servico INT,
            id_pagamento INT,
            data_hora DATETIME,

            FOREIGN KEY (id_cliente)
            REFERENCES clientes(id_cliente)
            ON DELETE CASCADE,

            FOREIGN KEY (id_servico)
            REFERENCES servicos(id)
            ON DELETE CASCADE,
            
            FOREIGN KEY (id_pagamento)
            REFERENCES pagamentos(id_pagamento)
            ON DELETE CASCADE
        )
    """)

    conexao.commit()
    conexao.close()


# =========================
# HOME (LISTAR TUDO)
# =========================

@app.route("/")
def home():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    cursor.execute("SELECT * FROM servicos")
    servicos = cursor.fetchall()

    cursor.execute("SELECT * FROM pagamentos")
    pagamentos = cursor.fetchall()

    cursor.execute("""
        SELECT
            agendamentos.id_agendamento,
            clientes.nome,
            servicos.nome,
            agendamentos.data_hora
        FROM agendamentos
        JOIN clientes
            ON agendamentos.id_cliente = clientes.id_cliente
        JOIN servicos
            ON agendamentos.id_servico = servicos.id
    """)

    agendamentos = cursor.fetchall()

    conexao.close()

    return render_template(
        "index.html",
        clientes=clientes,
        servicos=servicos,
        pagamentos=pagamentos,
        agendamentos=agendamentos
    )


# =========================
# CLIENTES
# =========================

@app.route("/cliente", methods=["POST"])
def cliente():

    nome = request.form["nome"]
    telefone = request.form["telefone"]
    cpf = request.form["cpf"]
    data_nascimento = request.form["data_nascimento"]
    bairro = request.form["bairro"]
    rua = request.form["rua"]
    numero_casa = request.form["numero_casa"]
    cidade = request.form["cidade"]
    estado = request.form["estado"]
    cep = request.form["cep"]
    complemento = request.form["complemento"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO clientes (
            nome,
            telefone,
            cpf,
            data_nascimento,
            bairro,
            rua,
            numero_casa,
            cidade,
            estado,
            cep,
            complemento
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        nome,
        telefone,
        cpf,
        data_nascimento,
        bairro,
        rua,
        numero_casa,
        cidade,
        estado,
        cep,
        complemento
    ))

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/delete_cliente/<int:id>")
def delete_cliente(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM clientes WHERE id_cliente=%s",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/update_cliente/<int:id>", methods=["POST"])
def update_cliente(id):

    nome = request.form["nome"]
    telefone = request.form["telefone"]
    cpf = request.form["cpf"]
    data_nascimento = request.form["data_nascimento"]
    bairro = request.form["bairro"]
    rua = request.form["rua"]
    numero_casa = request.form["numero_casa"]
    cidade = request.form["cidade"]
    estado = request.form["estado"]
    cep = request.form["cep"]
    complemento = request.form["complemento"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE clientes SET
            nome=%s,
            telefone=%s,
            cpf=%s,
            data_nascimento=%s,
            bairro=%s,
            rua=%s,
            numero_casa=%s,
            cidade=%s,
            estado=%s,
            cep=%s,
            complemento=%s
        WHERE id_cliente=%s
    """, (
        nome,
        telefone,
        cpf,
        data_nascimento,
        bairro,
        rua,
        numero_casa,
        cidade,
        estado,
        cep,
        complemento,
        id
    ))

    conexao.commit()
    conexao.close()

    return redirect("/")


# =========================
# SERVIÇOS
# =========================

@app.route("/servico", methods=["POST"])
def servico():

    nome = request.form["nome"]
    valor = request.form["valor"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO servicos (nome, valor) VALUES (%s, %s)",
        (nome, valor)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/delete_servico/<int:id>")
def delete_servico(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM servicos WHERE id=%s",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/update_servico/<int:id>", methods=["POST"])
def update_servico(id):

    nome = request.form["nome"]
    valor = request.form["valor"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE servicos SET nome=%s, valor=%s WHERE id=%s",
        (nome, valor, id)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")

# =========================
# PAGAMENTOS
# =========================


@app.route("/pagamento", methods=["POST"])
def pagamento():

    nome = request.form["nome"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO pagamentos (nome) VALUES (%s)",
        (nome,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/delete_pagamento/<int:id>")
def delete_pagamento(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM pagamentos WHERE id_pagamento=%s",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/update_pagamento/<int:id>", methods=["POST"])
def update_pagamento(id):

    nome = request.form["nome"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE pagamentos SET nome=%s WHERE id_pagamento=%s",
        (nome, id)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")
# =========================
# AGENDAMENTOS
# =========================


@app.route("/agendar", methods=["POST"])
def agendar():

    id_cliente = request.form["id_cliente"]
    id_servico = request.form["id_servico"]
    id_pagamento = request.form["id_pagamento"]
    data_hora = request.form["data_hora"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO agendamentos (
            id_cliente,
            id_servico,
            id_pagamento,
            data_hora
        )
        VALUES (%s, %s, %s, %s)
    """, (
        id_cliente,
        id_servico,
        id_pagamento,
        data_hora
    ))

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/delete_agendamento/<int:id>")
def delete_agendamento(id):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM agendamentos WHERE id_agendamento=%s",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/update_agendamento/<int:id>", methods=["POST"])
def update_agendamento(id):

    id_cliente = request.form["id_cliente"]
    id_servico = request.form["id_servico"]
    id_pagamento = request.form["id_pagamento"]
    data_hora = request.form["data_hora"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        UPDATE agendamentos
        SET
            id_cliente=%s,
            id_servico=%s,
            id_pagamento=%s,
            data_hora=%s
        WHERE id_agendamento=%s
    """, (
        id_cliente,
        id_servico,
        id_pagamento,
        data_hora,
        id
    ))

    conexao.commit()
    conexao.close()

    return redirect("/")


# =========================
# START DO SERVIDOR
# =========================

if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)
