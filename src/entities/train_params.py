import marshmallow.validate
from dataclasses import dataclass, field


@dataclass()
class TrainParams:
    n_estimators: int = field(default=50, metadata={"validate": marshmallow.validate.Range(min=0)})
