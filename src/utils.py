import sqlalchemy

from src.entities.params import PipelineParams


def get_sql_connection(params: PipelineParams):  
    database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(params.sql_params.username, params.sql_params.password, 
                                                      params.sql_params.ip, params.sql_params.database))
    return database_connection
