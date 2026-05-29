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
        password="root",
        database="mydb"
    )


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    # TABELA CLIENTES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            numero VARCHAR(20)
        )
    """)

    # TABELA SERVIÇOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100),
            valor DECIMAL(10,2)
        )
    """)

    # TABELA AGENDAMENTOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cliente_id INT,
            servico_id INT,
            data_agendamento DATETIME,

            FOREIGN KEY (cliente_id)
            REFERENCES clientes(id)
            ON DELETE CASCADE,

            FOREIGN KEY (servico_id)
            REFERENCES servicos(id)
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

    cursor.execute("""
        SELECT agendamentos.id, clientes.nome, servicos.nome, agendamentos.data_agendamento
        FROM agendamentos
        JOIN clientes ON agendamentos.cliente_id = clientes.id
        JOIN servicos ON agendamentos.servico_id = servicos.id
    """)
    agendamentos = cursor.fetchall()

    conexao.close()

    return render_template(
        "index.html",
        clientes=clientes,
        servicos=servicos,
        agendamentos=agendamentos
    )

# =========================
# CLIENTES
# =========================


@app.route("/cliente", methods=["POST"])
def cliente():
    nome = request.form["nome"]
    numero = request.form["numero"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO clientes (nome, numero) VALUES (%s, %s)",
        (nome, numero)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/delete_cliente/<int:id>")
def delete_cliente(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/update_cliente/<int:id>", methods=["POST"])
def update_cliente(id):
    nome = request.form["nome"]
    numero = request.form["numero"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE clientes SET nome=%s, numero=%s WHERE id=%s",
        (nome, numero, id)
    )

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

    cursor.execute("DELETE FROM servicos WHERE id=%s", (id,))
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
# AGENDAMENTOS
# =========================


@app.route("/agendar", methods=["POST"])
def agendar():
    cliente_id = request.form["cliente_id"]
    servico_id = request.form["servico_id"]
    data = request.form["data"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO agendamentos (cliente_id, servico_id, data_agendamento) VALUES (%s, %s, %s)",
        (cliente_id, servico_id, data)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/delete_agendamento/<int:id>")
def delete_agendamento(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM agendamentos WHERE id=%s", (id,))
    conexao.commit()
    conexao.close()

    return redirect("/")


@app.route("/update_agendamento/<int:id>", methods=["POST"])
def update_agendamento(id):
    cliente_id = request.form["cliente_id"]
    servico_id = request.form["servico_id"]
    data = request.form["data"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE agendamentos SET cliente_id=%s, servico_id=%s, data_agendamento=%s WHERE id=%s",
        (cliente_id, servico_id, data, id)
    )

    conexao.commit()
    conexao.close()

    return redirect("/")


# =========================
# START DO SERVIDOR
# =========================
if __name__ == "__main__":
    criar_tabelas()
    app.run(debug=True)
