from typing import Optional
from fastapi import APIRouter, Body, HTTPException, Query, status
from datetime import datetime
from uuid import uuid4
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import LimitOffsetPage, paginate, add_pagination

from workout_api.base.dependencies import DatabaseDependency
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import (
    AtletaIn,
    AtletaOut,
    AtletaUpdate,
    AtletaResponse,
)

from workout_api.categoria.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()


# POST
@router.post(
    "/",
    summary="Criar Novo Atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...),
):
    # Campo Categoria
    categoria_nome = atleta_in.categoria.nome
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)
            )
        )
        .scalars()
        .first()
    )

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A categoria {categoria_nome} não foi encontrada.",
        )

    # Campo Centro Treinamento
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)
            )
        )
        .scalars()
        .first()
    )

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O centro de treinamento {centro_treinamento_nome} não foi encontrado.",
        )

    # Campos Gerais - Atleta
    try:
        atleta_out = AtletaOut(
            id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump()
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}",
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao inserir os dados no banco. {err}",
        )

    return atleta_out


# GET ALL
@router.get(
    "/",
    summary="Consultar todos os Atletas",
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[AtletaResponse],
)
async def get(
    db_session: DatabaseDependency,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> LimitOffsetPage[AtletaResponse]:
    atletas_query = await db_session.execute(select(AtletaModel).offset(offset).limit(limit))
    atletas: list[AtletaOut] = atletas_query.scalars().all()

    atletas_response = [
        AtletaResponse(
            nome=atleta.nome,
            categoria=CategoriaModel(nome=atleta.categoria.nome),
            centro_treinamento=CentroTreinamentoModel(nome=atleta.centro_treinamento.nome)
        )
        for atleta in atletas
    ]

    return paginate(atletas_response)


# GET BY ID
@router.get(
    "/{id}",
    summary="Consultar um Atleta pelo Id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_id(
    id: UUID4,
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
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

    return atleta


# PATCH
@router.patch(
    "/{id}",
    summary="Editar um Atleta pelo Id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: UUID4,
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdate = Body(...),
    nome: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
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
async def delete(
    id: UUID4,
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(None),
    cpf: Optional[str] = Query(None),
) -> None:
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

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail=f"Atleta com id ({id}) excluído com sucesso.",
    )

add_pagination(router)