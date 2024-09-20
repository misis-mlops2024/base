import marshmallow.validate
from dataclasses import dataclass, field


@dataclass()
class DataParams:
    test_size: float = field(default=0.2, metadata={"validate": marshmallow.validate.Range(min=0)})
