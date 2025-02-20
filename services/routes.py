from main import app, create_engine, text, request
from flask import render_template

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/confLogin', methods=['POST'])
def confLogin():
    email = request.form['email']
    senha = request.form['senha']
    engine = create_engine('mysql+pymysql://sqlalchemy:masterkey@localhost:3306/agendanoclick')
    with engine.connect() as conn:
        query_cliente = text('SELECT * FROM clientes WHERE email = :email AND senha = :senha')
        result_cliente = conn.execute(query_cliente, {'email':email, 'senha':senha}).fetchone()
        if not result_cliente:
            query_profissional = text('SELECT * FROM cadastroProfissional WHERE email = :email AND senha = :senha')
            result_profissional = conn.execute(query_profissional, {'email':email, 'senha':senha}).fetchone()
        if result_cliente:
            query_nome = text('SELECT nome FROM clientes WHERE email = :email')
            query_nomePag = conn.execute(query_nome, {'email':email}).fetchone()
            nomePag = query_nomePag[0]
            query_profissionais = text('''
                SELECT 
                    c.ProfissionalID,  # Adicione o prefixo 'c.'
                    nome, nomeEstabelecimento, email, telefone, fotoPerfil, categoriaServico,
                    h.diaId, h.horarioInicio, h.horarioFim
                FROM cadastroProfissional AS c
                LEFT JOIN horarios_disponiveis AS h ON c.ProfissionalID = h.profissionalID
            ''')
            profissionaisQuery = conn.execute(query_profissionais).fetchall()
            profissionais = {}
            for row in profissionaisQuery:
                profissional_id = row[0]
                if profissional_id not in profissionais:
                    profissionais[profissional_id] = {
                        'nome': row[1], 'nome_estabelecimento': row[2], 'email': row[3],
                        'telefone': row[4], 'foto_perfil': row[5], 'categoria_servico': row[6],
                        'dias_disponiveis': []
                    }
                profissionais[profissional_id]['dias_disponiveis'].append({
                    'dia_semana': row[7], 'horario_inicio': row[8], 'horario_fim': row[9]
                })
                print(profissionais)
            return render_template('profissionais.html', nomePag=nomePag, profissionais=profissionais)

        elif result_profissional:
            return render_template('homepage.html')
        else:
            return render_template('login.html', erro='Email ou senha incorretos')

@app.route('/cadastroProfissional')
def cadastroProfissional():
    categoriasPossiveis = ['BARBEIRO', 'CABELEREIRO', 'MANICURE/PEDICURE', 'ESTETICISTA','MASSAGISTA', 'DENTISTA', 'FISIOTERAPEUTA', 'PSICÓLOGA','NUTRICIONISTA', 'MECÂNICO', 'LAVAGEM DE CARROS', 'FUNILARIA E PINTURA','ELETRICISTA', 'ENCANADOR', 'PEDREIRO', 'PINTOR', 'VETERINÁRIO','BANHO E TOSA', 'ADESTRADOR', 'FOTÓGRAFO', 'TÉCNICO DE INFORMÁTICA']
    return render_template('cadastroProfissional.html', categorias=categoriasPossiveis)