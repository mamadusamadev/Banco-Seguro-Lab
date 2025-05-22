from flask import Flask, request, render_template, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = "vulnlabsecret"


# Credenciais vulneráveis
USUARIO = "admin"
SENHA = "123456"

# Dados simulados
CLIENTES = [
    {"id": 1001, "nome": "João Silva", "cpf": "123.456.789-00", "conta": "12345-6", "saldo": 5678.90},
    {"id": 1002, "nome": "Maria Souza", "cpf": "987.654.321-00", "conta": "54321-6", "saldo": 12345.67},
    {"id": 1003, "nome": "Carlos Oliveira", "cpf": "456.789.123-00", "conta": "67890-1", "saldo": 789.12}
]

TRANSACOES = [
    {"id": 1, "origem": "12345-6", "destino": "54321-6", "valor": 500.00, 
     "data": "2023-05-01", "status": "Concluído", "descricao": "Transferência mensal"},
    {"id": 2, "origem": "54321-6", "destino": "67890-1", "valor": 200.00, 
     "data": "2023-05-02", "status": "Concluído", "descricao": "Pagamento de serviço"},
    {"id": 3, "origem": "67890-1", "destino": "12345-6", "valor": 100.00, 
     "data": "2023-05-03", "status": "Pendente", "descricao": "Reembolso"},
    {"id": 4, "origem": "12345-6", "destino": "98765-4", "valor": 1500.00, 
     "data": "2023-05-04", "status": "Concluído", "descricao": "Investimento"},
    {"id": 5, "origem": "54321-6", "destino": "12345-6", "valor": 300.00, 
     "data": "2023-05-05", "status": "Cancelado", "descricao": "Transferência erro"}
]



@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        usuario = request.form.get("username")
        senha = request.form.get("password")


        if usuario == USUARIO and senha == SENHA:
            session["usuario"] = usuario
            return redirect("/admin")
        else:
            erro = "Usuário ou senha inválidos."

    return render_template("login.html", erro=erro)





@app.route("/admin")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", usuario=session["usuario"])

@app.route("/admin/clientes")
def clientes():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    search = request.args.get("search", "").lower()
    if search:
        clientes_filtrados = [c for c in CLIENTES if search in c["nome"].lower()]
    else:
        clientes_filtrados = CLIENTES
    
    return render_template("clientes.html", 
                         usuario=session["usuario"], 
                         clientes=clientes_filtrados)

@app.route("/admin/clientes/novo")
def novo_cliente():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("novo_cliente.html", usuario=session["usuario"])

@app.route("/admin/transacoes")
def transacoes():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("transacoes.html", 
                         usuario=session["usuario"], 
                         transacoes=TRANSACOES)

@app.route("/admin/config")
def config():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("config.html", usuario=session["usuario"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    # Simulação de SQL Injection vulnerável
    if "' OR '1'='1" in query:
        flash("Todos os registros retornados (vulnerabilidade explorada!)", "erro")
        return render_template("search.html", results=CLIENTES, query=query)
    else:
        results = [c for c in CLIENTES if query.lower() in c["nome"].lower()]
        return render_template("search.html", results=results, query=query)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)