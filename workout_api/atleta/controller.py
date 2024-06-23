from fastapi import APIRouter, Body, HTTPException, status
from datetime import datetime, timezone
from uuid import uuid4
from pydantic import UUID4
from sqlalchemy.future import select

from workout_api.base.dependencies import DatabaseDependency
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate

from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()


# POST
@router.post(
    "/",
    summary="Criar um Novo Atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...),
):
    # Campo Categoria
    categoria_name = atleta_in.categoria.nome
    categoria = (
        await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_name))
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {categoria_name} não foi encontrada.",
        )

    # Campo Centro Treinamento
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    centro_treinamento = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O Centro de Treinamento {centro_treinamento_nome} não foi encontrado.",
        )

    # Campos Gerais - Atleta
    try:
        atleta_out = AtletaOut(
            id=uuid4(),
            created_at=datetime.now(timezone.utc),
            **atleta_in.model_dump(),
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um Erro ao inserir dados no banco",
        )

    return atleta_out


# GET ALL
@router.get(
    "/",
    summary="Consultar todos os Atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def get(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (
        (await db_session.execute(select(AtletaOut))).scalars().all()
    )

    return [AtletaOut.model_validate(atleta) for atleta in atletas]


# GET BY ID
@router.get(
    "/{id}",
    summary="Consultar um Atleta pelo Id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_id(id: UUID4, db_session: DatabaseDependency) -> list[AtletaOut]:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )

    return atleta


# PATCH
@router.patch(
    "/",
    summary="Editar um Atleta pelo Id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdate = Body(...),
) -> AtletaOut:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta

# DELETE
@router.delete(
    "/{id}",
    summary="Deletar um Atleta pelo Id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta não encontrado no id: {id}",
        )
        
    await db_session.delete(atleta)
    await db_session.commit()