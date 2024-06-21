from typing import Annotated
from pydantic import UUID4, Field
from workout_api.base.schemas import BaseSchema


class CategoriaIn(BaseSchema):
    nome: Annotated[
        str, Field(description="Nome da Categoria", example="Scale", max_length=10)
    ]


class CategoriaOut(BaseSchema):
    id: Annotated[UUID4, Field(description="Identificador da Categoria")]
