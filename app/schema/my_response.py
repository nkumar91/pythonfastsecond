from pydantic import BaseModel,Generic,TypeVar,Optional
T = TypeVar("T")

class MyResonse(BaseModel,Generic[T]):
    model_config = {"exclude_none" : True}
    success:bool
    status_code:int = 200
    message:str
    data:Optional[T] = None
    error:Optional[T] = None
