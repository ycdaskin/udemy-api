from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params

def update_privilege(data, id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            params, values = parse_update_params(data)
            sql = f"""update privileges set {params} where id = %s""".replace("'", "")
            cur.execute(sql, values + (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating privilege: {str(ex.args[0])}")


def get_privileges(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = "select * from privileges where id = %s" if id else "select * from privileges"
        params = (id,) if id else ()
        data = query_db(cur, sql, params)
        return data


def create_privilege(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f"""insert into privileges {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
            conn.commit()
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating privilege: {str(ex.args[0])}")


def delete_privilege(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from privileges where id = %s"""
            cur.execute(sql, (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while deleting privilege: {str(ex.args[0])}")
