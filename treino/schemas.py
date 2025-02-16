from ninja import ModelSchema, Schema
from treino.models import Aluno

class AlunoSchema(ModelSchema):
    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'faixa', 'data_nascimento']

class ProgressoAlunoSchema(Schema):
    email: str
    nome: str
    faixa: str
    total_aulas: int
    aulas_necessarias_para_proxima_faixa: int