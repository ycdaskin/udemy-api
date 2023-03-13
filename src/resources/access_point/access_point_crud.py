from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params
from src.auth.auth import is_super_user



def get_access_points(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user()
        if super_admin:
            sql = '''select ap.*, g.id as gate_id, g.name as gate_name, c.name as company_name from access_point ap 
            left join gate g on g.id = ap.gate
            left join company c on c.id = ap.company''' \
            if id is None else \
                '''select ap.*, g.id as gate_id, g.name as gate_name, c.name as company_name from access_point ap 
                left join gate g on g.id = ap.gate 
                left join company c on c.id = ap.company where ap.id = %s'''
            params = (id,) if id else ()
        else:
            sql = '''select ap.*, g.id as gate_id, g.name as gate_name, c.name as company_name from access_point ap 
            left join gate g on g.id = ap.gate 
            left join company c on c.id = ap.company where ap.id = %s and gate.company = %s''' \
            if id is not None else \
                '''select ap.*, g.id as gate_id, g.name as gate_name, c.name as company_name from access_point ap 
                left join gate g on g.id = ap.gate
                left join company c on c.id = ap.company where gate.company = %s'''
            params = (id, company,) if id else (company,)
        data = query_db(cur, sql, params)
        return data


def create_access_point(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = '''select b.company from gate g left join building b on g.building = b.id where g.id = %s'''
            cur.execute(sql, (data["gate"],))
            rows = cur.fetchall()
            if len(rows) > 0:
                company = rows[0][0]
                data["company"] = company
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f"""insert into access_point {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating access point: {str(ex.args[0])}")


def update_access_point(data, id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            params, values = parse_update_params(data)
            sql = f"""update access_point set {params} where id = %s""".replace("'", "")
            cur.execute(sql, values + (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating access point: {str(ex.args[0])}")


def delete_access_point(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from access_point where id = %s"""
            cur.execute(sql, (id,))
    except Exception as ex:
        raise Exception(f"Error while deleting access point: {str(ex.args[0])}")


def delete_access_points(ids):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from access_point where id in %s"""
            cur.execute(sql, (tuple(ids),))
    except Exception as ex:
        raise Exception(f"Error while deleting access points: {str(ex.args[0])}")