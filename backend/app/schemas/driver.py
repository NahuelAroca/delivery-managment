from pydantic import BaseModel


class DriverResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }