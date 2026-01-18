"""
SQL Query converter untuk compatibility antara SQLite dan PostgreSQL
"""

def convert_sql_for_postgres(sql, params=None):
    """Convert SQLite SQL syntax ke PostgreSQL"""
    # Replace ? placeholder dengan %s
    converted_sql = sql.replace("?", "%s")
    
    # Replace SQLite strftime dengan PostgreSQL to_char
    # strftime('%m', column) -> to_char(column, 'MM')
    # strftime('%Y', column) -> to_char(column, 'YYYY')
    # strftime('%m-%Y', column) -> to_char(column, 'MM-YYYY')
    import re
    
    # Handle strftime patterns
    converted_sql = re.sub(r"strftime\('%m',\s*(\w+)\)", r"to_char(\1, 'MM')", converted_sql)
    converted_sql = re.sub(r"strftime\('%Y',\s*(\w+)\)", r"to_char(\1, 'YYYY')", converted_sql)
    converted_sql = re.sub(r"strftime\('%m-%Y',\s*(\w+)\)", r"to_char(\1, 'MM-YYYY')", converted_sql)
    converted_sql = re.sub(r"strftime\('%d',\s*(\w+)\)", r"to_char(\1, 'DD')", converted_sql)
    
    # Replace DATE('now') with CURRENT_DATE
    converted_sql = converted_sql.replace("DATE('now')", "CURRENT_DATE")
    converted_sql = converted_sql.replace("date('now')", "CURRENT_DATE")
    
    # Replace CASE WHEN expressions (keep as-is, they're compatible)
    # But replace SQLite date functions inside CASE
    converted_sql = re.sub(r"strftime\('%Y-%m-%d',\s*datetime\('now'\)\)", "CURRENT_DATE::text", converted_sql)
    
    return converted_sql, params

