from ninja import Router

treino_router = Router()

@treino_router.get("alunos/")
def criar_aluno(request):
    return {"message": "Aluno criado"}