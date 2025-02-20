from sqlalchemy import create_engine, Column, Integer, String, Time, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    
    clienteID = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    telefone = Column(String(14), unique=True, nullable=False)
    senha = Column(String(20), nullable=False)

class CadastroProfissional(Base):
    __tablename__ = 'cadastroProfissional'
    
    ProfissionalID = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), nullable=False)
    nomeEstabelecimento = Column(String(40), nullable=False)
    email = Column(String(40), unique=True, nullable=False)
    telefone = Column(String(14), unique=True, nullable=False)
    senha = Column(String(20), nullable=False)
    fotoPerfil = Column(String(255))
    categoriaServico = Column(Enum(
        'BARBEIRO', 'CABELEREIRO', 'MANICURE/PEDICURE', 'ESTETICISTA', 
        'MASSAGISTA', 'DENTISTA', 'FISIOTERAPEUTA', 'PSICÓLOGA', 
        'NUTRICIONISTA', 'MECÂNICO', 'LAVAGEM DE CARROS', 
        'FUNILARIA E PINTURA', 'ELETRICISTA', 'ENCANADOR', 
        'PEDREIRO', 'PINTOR', 'VETERINÁRIO', 'BANHO E TOSA', 
        'ADESTRADOR', 'FOTÓGRAFO', 'TÉCNICO DE INFORMÁTICA'
    ))

class DiasSemana(Base):
    __tablename__ = 'diasSemana'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(10), nullable=False)

class HorariosDisponiveis(Base):
    __tablename__ = 'horarios_disponiveis'
    
    horarioID = Column(Integer, primary_key=True, autoincrement=True)
    profissionalID = Column(Integer, ForeignKey('cadastroProfissional.ProfissionalID'), nullable=False)
    diaId = Column(Integer, ForeignKey('diasSemana.id'), nullable=False)
    horarioInicio = Column(Time, nullable=False)
    horarioFim = Column(Time, nullable=False)

    profissional = relationship("CadastroProfissional", back_populates="horarios")
    dia = relationship("DiasSemana")

CadastroProfissional.horarios = relationship("HorariosDisponiveis", order_by=HorariosDisponiveis.horarioID, back_populates="profissional")