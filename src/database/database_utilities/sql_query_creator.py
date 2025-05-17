from typing import Optional

from src.utilities.error_handler import ErrorHandler

def create_sql_query(filters: dict, parent=None) -> Optional[tuple]:
    try:
        if not filters:
            return None
        basic_filter = """SELECT mandatory.id FROM mandatory\n"""
        where_filter = []
        values = []
        for key in filters:
            if key != "mandatory":
                basic_filter += f"LEFT JOIN {key} ON mandatory.id = {key}.id\n"
            new_filter, value = filters[key]
            where_filter.append(new_filter)
            values.extend(value)
        final_where = " AND ".join(where_filter)
        final_filter = basic_filter + "WHERE " + final_where
        return final_filter, values
    except Exception as e:
        ErrorHandler.exception_handler(e, parent)
        return None