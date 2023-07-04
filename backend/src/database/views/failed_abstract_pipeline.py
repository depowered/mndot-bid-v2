from duckdb import DuckDBPyConnection

from src.database.tables import abstract_pipeline

__viewname__ = "failed_abstract_pipeline"


def create_or_replace_view(con: DuckDBPyConnection) -> None:
    query = f"""
        CREATE OR REPLACE VIEW {__viewname__} AS (
            SELECT * FROM {abstract_pipeline.tablename}
            WHERE 
                {abstract_pipeline.Stage.DOWNLOAD} = '{abstract_pipeline.Status.FAILED}' OR
                {abstract_pipeline.Stage.SPLIT} = '{abstract_pipeline.Status.FAILED}' OR
                {abstract_pipeline.Stage.CLEAN} = '{abstract_pipeline.Status.FAILED}' OR
                {abstract_pipeline.Stage.LOAD} = '{abstract_pipeline.Status.FAILED}'
        )"""
    con.execute(query)
