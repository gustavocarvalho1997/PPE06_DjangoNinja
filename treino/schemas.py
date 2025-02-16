from ninja import ModelSchema
from treino.models import Aluno

class AlunoSchema(ModelSchema):
    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'faixa', 'data_nascimento']