import marshmallow.validate
from dataclasses import dataclass, field


@dataclass()
class FeatureParams:
    some_param: str
