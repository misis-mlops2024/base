import marshmallow.validate
from dataclasses import dataclass, field


@dataclass()
class TrainParams:
    model_path: str
    metrics_path: str
    n_estimators: int = field(default=50, metadata={"validate": marshmallow.validate.Range(min=0)})
