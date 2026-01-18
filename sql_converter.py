"""
SQL Query converter untuk compatibility antara SQLite dan PostgreSQL
"""

def convert_sql_for_postgres(sql, params=None):
    """Convert SQLite SQL syntax ke PostgreSQL"""
    import re
    
    # Only replace ? with %s if params exist and are non-empty
    if params:
        converted_sql = sql.replace("?", "%s")
    else:
        converted_sql = sql
        # If no params but query has ?, remove them (they're inline literals)
        # Actually, don't remove - just leave as-is since there are no params
        # The query shouldn't have ? if there are no params
    
    # Replace SQLite IFNULL dengan PostgreSQL COALESCE
    converted_sql = re.sub(r"IFNULL\(", "COALESCE(", converted_sql, flags=re.IGNORECASE)
    
    # Replace SQLite GROUP_CONCAT dengan PostgreSQL string_agg
    # GROUP_CONCAT(expr) -> string_agg(expr, ', ')
    # GROUP_CONCAT(DISTINCT expr) -> string_agg(DISTINCT expr, ', ')
    converted_sql = re.sub(
        r"GROUP_CONCAT\(DISTINCT\s+([^)]+)\)", 
        r"string_agg(DISTINCT \1, ', ')", 
        converted_sql, 
        flags=re.IGNORECASE
    )
    converted_sql = re.sub(
        r"GROUP_CONCAT\(([^)]+)\)", 
        r"string_agg(\1, ', ')", 
        converted_sql, 
        flags=re.IGNORECASE
    )
    
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

