import marshmallow.validate
from dataclasses import dataclass, field


@dataclass()
class DataParams:
    raw_data_path: str
    train_data_path: str 
    test_data_path: str
    n_samples: int = field(default=100, metadata={"validate": marshmallow.validate.Range(min=1)})
    n_features: int = field(default=10, metadata={"validate": marshmallow.validate.Range(min=1)})
    test_size: float = field(default=0.3, metadata={"validate": marshmallow.validate.Range(min=0.0)})
    