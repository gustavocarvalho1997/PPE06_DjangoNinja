from ninja import Router
from ninja.errors import HttpError
from typing import List
from treino.schemas import AlunoSchema, ProgressoAlunoSchema, AulaRealizadaSchema
from treino.models import Aluno, AulaConcluida
from treino.graduacao import calculate_lesson_to_upgrade, order_belt

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

@treino_router.get("/progresso_aluno/", response={200: ProgressoAlunoSchema, 404: str}, description="Verificar progresso do aluno")
def progresso_aluno(request, email_aluno: str):
    aluno = Aluno.objects.get(email=email_aluno)
    if not aluno:
        raise HttpError(404, "Aluno não encontrado")
    faixa_atual = aluno.get_faixa_display() # Retorna o valor da faixa, não a sigla
    n = order_belt.get(faixa_atual, 0) # Retorna o valor da faixa, se não existir retorna 0
    total_aulas_proxima_faixa = calculate_lesson_to_upgrade(n)
    total_aulas_concluidas_faixa = AulaConcluida.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count() 
    aulas_faltantes = total_aulas_proxima_faixa - total_aulas_concluidas_faixa

    return {
        "email": aluno.email,
        "nome": aluno.nome,
        "faixa": faixa_atual,
        "total_aulas": total_aulas_concluidas_faixa,
        "aulas_necessarias_para_proxima_faixa": aulas_faltantes
    }

@treino_router.post("/aula_realizada/", response={200: str, 400: str, 404: str}, description="Registrar aula realizada")
def aula_realizada(request, aula_realizada: AulaRealizadaSchema):
    qtd = aula_realizada.dict()['qtd']
    email_aluno = aula_realizada.dict()['email_aluno']

    if qtd <= 0:
        raise HttpError(400, "Quantidade de aulas inválida")
    
    aluno = Aluno.objects.get(email=email_aluno)

    if not aluno:
        raise HttpError(404, "Aluno não encontrado")
    
    for _ in range(0, qtd):
        ac = AulaConcluida(
            aluno=aluno,
            faixa_atual=aluno.faixa
        )
        ac.save()
    
    return 200, f"Aula marcada como realizada para o aluno {aluno.nome}"
