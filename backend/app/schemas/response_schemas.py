from math import ceil
from typing import Any, Dict, Generic, Sequence, Union, Optional, TypeVar
from pydantic.generics import GenericModel


DataType = TypeVar("DataType")
T = TypeVar("T")


class ResponseBase(GenericModel, Generic[T]):
    message: str = ""
    meta: Dict = {}
    data: Optional[T]


class GetResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data got correctly"


class PostResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data created correctly"


class PutResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data updated correctly"


class DeleteResponseBase(ResponseBase[DataType], Generic[DataType]):
    message: str = "Data deleted correctly"


def create_response(
    data: Optional[DataType],
    message: Optional[str] = "",
    meta: Optional[Union[Dict, Any]] = {},
) -> Union[Dict[str, DataType], DataType]:
    # if isinstance(data, IResponsePage):
    #     data.message = "Data paginated correctly" if not message else message
    #     data.meta = meta
    #     return data
    body_response = {"data": data, "message": message, "meta": meta}

    # It returns a dictionary to avoid doble
    # validation https://github.com/tiangolo/fastapi/issues/3021
    return {k: v for k, v in body_response.items() if v is not None}