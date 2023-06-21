class SchemaUtils:
    """
    A utility class for generating SQL statements for creating, altering, and deleting tables and schemas.
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def create_table(table_name: str, columns: list[str]) -> str:
        """
        Generate SQL statement for creating a table.

        Args:
            table_name (str): Name of the table.
            columns (list[str]): List of column definitions as strings.

        Returns:
            str: SQL statement for creating the table.
        """
        column_defs = ', '.join(columns)
        query = f"CREATE TABLE {table_name} ({column_defs})"
        return query

    @staticmethod
    def alter_table(table_name: str, column_name: str, new_data_type: str) -> str:
        """
        Generate SQL statement for altering a table's column data type.

        Args:
            table_name (str): Name of the table.
            column_name (str): Name of the column to be altered.
            new_data_type (str): New data type for the column.

        Returns:
            str: SQL statement for altering the table's column data type.
        """
        query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_data_type}"
        return query

    @staticmethod
    def drop_table(table_name: str) -> str:
        """
        Generate SQL statement for dropping a table.

        Args:
            table_name (str): Name of the table.

        Returns:
            str: SQL statement for dropping the table.
        """
        query = f"DROP TABLE IF EXISTS {table_name}"
        return query

    @staticmethod
    def create_schema(schema_name: str) -> str:
        """
        Generate SQL statement for creating a schema.

        Args:
            schema_name (str): Name of the schema.

        Returns:
            str: SQL statement for creating the schema.
        """
        query = f"CREATE SCHEMA {schema_name}"
        return query

    @staticmethod
    def drop_schema(schema_name: str) -> str:
        """
        Generate SQL statement for dropping a schema.

        Args:
            schema_name (str): Name of the schema.

        Returns:
            str: SQL statement for dropping the schema.
        """
        query = f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"
        return query
