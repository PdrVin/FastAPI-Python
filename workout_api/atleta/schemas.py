from pydantic import Field, PositiveFloat
from typing import Annotated

from workout_api.base.schemas import BaseSchema, OutMixin
from workout_api.categoria.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta


class Atleta(BaseSchema):
    # Campos
    nome: Annotated[
        str, Field(description="Nome do Atleta", example="Joao", max_length=50)
    ]
    cpf: Annotated[
        str, Field(description="CPF do Atleta", example="12345678901", max_length=11)
    ]
    idade: Annotated[
        int, Field(description="Idade do Atleta", example="25")
    ]
    peso: Annotated[
        PositiveFloat, Field(description="Peso do Atleta", example="75.5")
    ]
    altura: Annotated[
        PositiveFloat, Field(description="Altura do Atleta", example="1.80")
    ]
    sexo: Annotated[
        str, Field(description="Sexo do Atleta", example="M", max_length=1)
    ]
    categoria: Annotated[
        CategoriaIn, Field(description="Categoria do Atleta")
    ]
    centro_treinamento: Annotated[
        CentroTreinamentoAtleta, Field(description="Centro de Treinamento do Atleta")
    ]


class AtletaIn(Atleta):
    pass


class AtletaOut(AtletaIn, OutMixin):
    pass