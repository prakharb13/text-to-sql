from utils import load_db, query_db


def get_answer(sql_query: str, db_path: str = "Chinook.db"):
    """
    Execute SQL query and return results.
    
    Args:
        sql_query: SQL query string to execute
        db_path: Path to the SQLite database
        
    Returns:
        List of dictionaries with results, or error string if failed
    """
    try:
        conn = load_db(db_path)
        results = query_db(conn, sql_query, return_as_df=False)
        conn.close()
        return results
    except Exception as e:
        return f"Error: {str(e)}"

