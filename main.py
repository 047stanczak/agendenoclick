from flask import Flask, render_template, request
from sqlalchemy import create_engine, insert, text
from services.models import Cliente, CadastroProfissional, HorariosDisponiveis
import os

app = Flask(__name__)

@app.route('/postCadastro', methods=['POST'])
def postCadastro():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    senha = request.form['senha']
    engine = create_engine('mysql+pymysql://sqlalchemy:masterkey@localhost:3306/agendanoclick')
    with engine.connect() as conn:
        conn.execute(insert(Cliente).values(nome=nome, email=email, telefone=telefone, senha=senha))
        conn.commit()
    return render_template('cadastro.html')

@app.route('/postCadastroProfissional', methods=['POST'])
def postCadastroProfissional():
    nome = request.form['nome']
    nomeEstabelecimento = request.form['nomeEstabelecimento']
    email = request.form['email']
    telefone = request.form['telefone']
    senha = request.form['senha']
    fotoPerfil = request.files['fotoPerfil']
    categoriaServico = request.form['categoriaServico']
    dia_semana = request.form.getlist('dias')
    horarioInicio = request.form['horarioInicio']
    horarioFim = request.form['horarioFim']

    UPLOAD_FOLDER = 'static/img/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if fotoPerfil:
        fotoPerfilPath = os.path.join(app.config['UPLOAD_FOLDER'], f"{nomeEstabelecimento}{os.path.splitext(fotoPerfil.filename)[1]}")
        fotoPerfil.save(fotoPerfilPath)
    
    engine = create_engine('mysql+pymysql://sqlalchemy:masterkey@localhost:3306/agendanoclick')
    with engine.connect() as conn:
        conn.execute(insert(CadastroProfissional).values(
            nome=nome, 
            nomeEstabelecimento=nomeEstabelecimento, 
            email=email, 
            telefone=telefone, 
            senha=senha, 
            fotoPerfil=fotoPerfilPath, 
            categoriaServico=categoriaServico
            ))
        query = text("SELECT profissionalID FROM CadastroProfissional WHERE nome = :nome")
        result = conn.execute(query, {'nome': nome}).fetchone()
        profissionalID = result[0]
        for dia in dia_semana:
            conn.execute(insert(HorariosDisponiveis).values(profissionalID=profissionalID, diaId=dia, horarioInicio=horarioInicio, horarioFim=horarioFim))
        conn.commit()
    return render_template('cadastroProfissional.html')

from services.routes import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)