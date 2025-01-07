from main import app, db
from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import (
    generate_password_hash as hash,
    check_password_hash as check_hash,
)
from modelos import Funcionario

@app.route('/')
def index():
    return render_template(
        "index.html",
        titulo="Grupo Tria - Analise de fechamento",
        h2titulo="[nome da funcionarioa]",
    )

@app.route("/dados_funcionario")
def dados_funcionario():
    """:Descrição:
    Cria a página de cadastro contendo toda as informações necessarias de um usuário.

    :Retorno:
    Renderiza a página de cadastro com um formulário referente a `funcionario`
    """
    id = request.args.get("id")
    if id:
        user = Funcionario.query.get(id)
        return render_template(
            "dados_funcionario.html",
            titulo="Grupo Tria - funcionario",
            h2titulo="Novo funcionario",
            tem_user=1,
            user=user,
        )
    else:
        return render_template(
            "dados_funcionario.html",
            titulo="Grupo Tria - funcionario",
            h2titulo="Novo funcionario",
            tem_user=0,
        )

@app.route("/cadastro_funcionario", methods=["POST"])
def cadastro_funcionario():
    if session["funcao"] == "adm":
            nome = request.form["nome"]
            funcao = request.form["funcao"]
            senha = request.form["senha"]
            confirmar = request.form["senhaConfirmar"]

            funcionario_nome_repetido = Funcionario.query.filter(
                Funcionario.nome.ilike(f"{nome}")
            ).first()
            if funcionario_nome_repetido == None:
                if senha == confirmar:
                    senha = hash(senha).decode("utf-8")
                    novo_func = Funcionario(nome=nome, funcao=funcao, senha=senha)

                    db.session.add(novo_func)
                    db.session.commit()

                    flash("Novo funcionario :^D", "alert alert-success")
                    return redirect(url_for("tabela_funcionario"))

                else:
                    flash("As senhas não são as mesmas ಠ_ಠ", "alert alert-danger")
                    return redirect(url_for("dados_funcionario"))
            else:
                flash(f"O nome {nome} já está em uso", "alert alert-danger")
                return redirect(url_for("tabela_funcionario"))
    else:
        return redirect(url_for("index"))
    
@app.route("/editar_funcionario", methods=["POST"])
def editar_funcionario():
    """:Descrição:
    Recebe as informações de `/dados_funcionario` via `POST` para efetuar alguma alteração em um usuário específico.
    O acesso é restrito a usuários com função "adm" na sessão.

    :Parâmetros:
    - `id` (obrigatório): id para localizar o usuário no banco;
    - `nome` (obrigatório): nome que identifica o usúario;
    - `funcao` (obrigatório): Função que determina os pontos de acesso do sistema;
    - `senha` (opcional): Senha para iniciar a sessão;
    - `senhaAntiga` (opcional): Senha atual para fazer a alteração na senha;

    :Comportamento:
    1. Através do `id`, efetua a busca do `Funcionario` para dar início a alteração de dados;
    2. Verifica se o nome recebido pelo formulário não está repetido no banco:
    - Se estiver repetido, redireciona para `/tabela_funcionario` exibindo uma mensagem indicando que o nome já está em uso;
    - Caso contrário, continua com o processo.
    3. Efetua a alteração de `nome`, `funcao`;
    4. A senha só pode ser alterada se com a validação da antiga senha:
    - Se a senha antiga for igual a senha antes da alteração, criptografa a senha nova e insere a informação
    - Caso contrário, apenas exiba uma mensagem dizendo que a senha não foi alterada.
    5. Após as alterações, exibe a mensagem informando que a alteração foi concluída.

    :Retorno:
    - redireciona a página principal se não for um usuário válido;
    - redirecione a `/tabela_funcionario` indicando a mensagem de sucesso ou algum erro.
    """

    if session["funcao"] == "adm":
        id = request.form["id"]
        nome = request.form["nome"]
        funcao = request.form["funcao"]
        senha = request.form["senha"]
        senhaAntiga = request.form["senhaConfirmar"]

        usuario = Funcionario.query.get(id)

        usuario_nome_repetido = Funcionario.query.filter(
            Funcionario.nome.ilike(f"{nome}")
        ).first()

        if usuario_nome_repetido == None or usuario_nome_repetido.id == usuario.id:
            usuario.nome = nome
            usuario.funcao = funcao

            msg = "Alteração concluída"

            if senha:
                if check_hash(usuario.senha, senhaAntiga) and len(senhaAntiga) >= 8:
                    usuario.senha = hash(senha).decode("utf-8")
                    msg = msg + " (senha alterada!)"
                else:
                    flash(
                        "Não foi possível fazer alteração na senha, pois a senha antiga não está correta ou muito curta",
                        "alert alert-warning",
                    )
            db.session.commit()
            flash(msg, "alert alert-success")
        else:
            flash(
                f"Não é possível fazer a alteração do nome pois o {nome} já está em uso",
                "alert alert-danger",
            )

        return redirect(url_for("tabela_funcionario"))

    else:
        return redirect(url_for("index"))
    
@app.route("/deletar_funcionario", methods=["GET"])
def deletar_funcionario():
    """:Descrição:
    Recebe as informações de via `GET` para efetuar a exclusão de um usuário específico.
    O acesso é restrito a usuários com função "adm" na sessão.

    :Comportamento:
    1. Através do `id`, efetua a busca do `Usuario` para tentar fazer a exclusão de dados;
    2. Tente efetuar a exclusão:
    - Se a exclusão for possível, exibe uma mensagem indicando a exclusão;
    - caso contrário, exibe a mensagem indicando a falha.

    :Retorno:
    - redireciona a página principal se não for um usuário válido;
    - redirecione a `/tabela_usuario` indicando a mensagem de sucesso ou algum erro.
    """
    if session["funcao"] == "adm":
        id = request.args.get("id", type=int)

        user = Funcionario.query.get(id)

        try:
            db.session.delete(user)
            db.session.commit()
            flash("O usuário foi removido", "alert alert-success")
        except:
            flash(
                "Não é possível remover o usuario\n(registro do usuário está presente em auditoria)",
                "alert alert-danger",
            )

        return redirect(url_for("tabela_funcionario"))
    else:
        return redirect(url_for("index"))

@app.route("/tabela_funcionario")
def tabela_funcionario():
    """:Descrição:
    Cria a página onde contém a tabela de todos os funcionários ordenados pelo nome.

    :Retorno:
    Renderiza a página `/tabela_funcionario` juntamente com uma tabela dos funcionários em ordem alfabética.
    """
    lista_usuario = Funcionario.query.order_by(Funcionario.nome).all()
    return render_template(
        "tabela_funcionario.html",
        titulo="Grupo Tria - Usuarios",
        h2titulo="Tabela dos usuarios",
        lista_usuario=lista_usuario,
    )

@app.route("/login")
def login():
    """:Descrição: Cria a página de login com um formulário em branco, esperando argumentos como nome e senha

    :Retorno:
    Renderiza a página de `/login`
    """
    return render_template("login.html", titulo="Grupo Tria - Logar", h2titulo="Logar")


@app.route("/logar", methods=["POST"])
def logar():
    """:Descrição: Recebe as informações de `/login` via `POST`, para validar as informações e efetuar o login
    do usuário

    :Comportamento:
    1. Através do nome do usuário, busca o primeiro resultado da `Querry`;
    2. Verifica se a `Querry` obteve algum resultado;
    3. Se houver o resultado da `Querry`, verifica se `funcionario.senha` é igual a `senha` através da função
    check_password_hash (renomeada para check_hash());
    4. Se as senhas coincidirem, exibe uma mensagem de autenticação e insira os dados de `Usario`:
    - `session["id"] = funcionario.id`
    - `session["nome"] = funcionario.nome`
    - `session["funcao"] = funcionario.funcao`
    5. Se não houver resultado na `Querry` ou as senhas não se coincide, retorna a página inicial com uma mensagem
    indicando a falha ao autenticar;

    :Retorno:
    Renderiza a página de `/login`
    """
    senha = request.form["senha"]
    nome = request.form["nome"]

    funcionario = Funcionario.query.filter(Funcionario.nome.ilike(f"{nome}")).first()

    if funcionario and check_hash(funcionario.senha, senha):
        session["id"] = funcionario.id
        session["nome"] = funcionario.nome
        session["funcao"] = funcionario.funcao
        flash(
            f"A sessão foi iniciada\nBem vindo(a) {session['nome']} (ᵔᴥᵔ)",
            "alert alert-success",
        )
    else:
        flash(
            "Falha ao autenticar (⇀‸↼‶)",
            "alert alert-warning",
        )
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    """:Descrição: Limpe os dados da sessão atual

    :Comportamento:
    1. Dados retirados são:
    - `session["id"] = None`
    - `session["nome"] = None`
    - `session["funcao"] = None`;

    :Retorno:
    Renderiza a página de `/login`
    """
    session["id"] = None
    session["nome"] = None
    session["funcao"] = None

    flash(f"A sessão foi encerrada", "alert alert-warning")

    return redirect(url_for("index"))