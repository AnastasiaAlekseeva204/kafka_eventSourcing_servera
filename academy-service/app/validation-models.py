from typing import Annotated, List, Optional
from pydantic import BaseModel, Field, ConfigDict


LastNameType = Annotated[str, Field(min_length=1)]
FirstNameType = Annotated[str, Field(min_length=1)]
MiddleNameType = Annotated[str, Field(min_length=1)]
GenderType = bool
AgeType = Annotated[int, Field(ge=1)]
IdType = Annotated[int, Field(gt=0)]



class StudentBase(BaseModel):
    last_name: LastNameType
    first_name: FirstNameType
    middle_name: MiddleNameType
    gender: GenderType
    age: AgeType

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    last_name: Optional[LastNameType] = None
    first_name: Optional[FirstNameType] = None
    middle_name: Optional[MiddleNameType] = None
    gender: Optional[GenderType] = None
    age: Optional[AgeType] = None

class StudentOut(StudentBase):
    model_config = ConfigDict(from_attributes=True)
    id: IdType