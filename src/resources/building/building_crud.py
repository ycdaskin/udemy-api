from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params
from src.auth.auth import is_super_user



def get_buildings(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user()
        if super_admin:
            sql = '''select * from building''' \
                if id is None else \
                '''select * from building where id = %s'''
            params = (id,) if id else ()
        else:
            sql = '''select * from building where id = %s and company = %s''' \
                if id is None else \
                '''select * from building where company = %s'''
            params = (id, company,) if id else (company,)
        data = query_db(cur, sql, params)
        return data


def create_building(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f"""insert into building {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating building: {str(ex.args[0])}")


def update_building(data, id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            params, values = parse_update_params(data)
            sql = f"""update building set {params} where id = %s""".replace("'", "")
            cur.execute(sql, values + (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating building: {str(ex.args[0])}")


def delete_building(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from building where id = %s"""
            cur.execute(sql, (id,))
    except Exception as ex:
        raise Exception(f"Error while deleting building: {str(ex.args[0])}")


def delete_buildings(ids):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from building where id in %s"""
            cur.execute(sql, (tuple(ids),))
    except Exception as ex:
        raise Exception(f"Error while deleting buildings: {str(ex.args[0])}")