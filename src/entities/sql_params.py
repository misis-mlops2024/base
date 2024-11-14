from dataclasses import dataclass


@dataclass()
class SQLParams:
      username: str
      password: str
      database: str
      ip: str
    