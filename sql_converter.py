"""
SQL Query converter untuk compatibility antara SQLite dan PostgreSQL
"""

def convert_sql_for_postgres(sql, params=None):
    """Convert SQLite SQL syntax ke PostgreSQL"""
    # Replace ? placeholder dengan %s
    converted_sql = sql.replace("?", "%s")
    
    # Replace SQLite functions ke PostgreSQL equivalents
    converted_sql = converted_sql.replace("strftime", "to_char")
    converted_sql = converted_sql.replace("DATE('now')", "CURRENT_DATE")
    converted_sql = converted_sql.replace("date('now')", "CURRENT_DATE")
    
    return converted_sql, params
