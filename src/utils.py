import pymysql

from src.entities.params import PipelineParams


def get_sql_connection(params: PipelineParams):  
    connection = pymysql.connect(host=params.sql_params.ip,
                                 user=params.sql_params.username,
                                 password=params.sql_params.password,
                                 database=params.sql_params.database)
    return connection
