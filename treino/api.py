from ninja import Router
from ninja.errors import HttpError
from typing import List
from treino.schemas import AlunoSchema
from treino.models import Aluno

treino_router = Router()

@treino_router.post("alunos/", response={200: AlunoSchema, 400: str}, description="Cadastrar um aluno")
def criar_aluno(request, aluno_schema: AlunoSchema):
    nome = aluno_schema.dict()['nome']
    email = aluno_schema.dict()['email']
    faixa = aluno_schema.dict()['faixa']
    data_nascimento = aluno_schema.dict()['data_nascimento']

    if Aluno.objects.filter(email=email).exists():
        raise HttpError(400, "Email já cadastrado")

    aluno = Aluno(
        nome=nome,
        email=email,
        faixa=faixa,
        data_nascimento=data_nascimento
    )

    aluno.save()

    return aluno

@treino_router.get("alunos/", response={200: List[AlunoSchema]}, description="Listar todos os alunos")
def listar_alunos(request):
    alunos = Aluno.objects.all()
    return alunos