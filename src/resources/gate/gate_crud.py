import uuid

from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params
from src.auth.auth import is_super_user



def get_gates(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user()
        if super_admin:
            sql = '''with gt as (
            select g.*, b.company as company_id, b.name as building_name from gate g 
            left join building b on b.id = g.building
            )
            select gt.*, c.name as company_name from gt
            left join company c on c.id = gt.company_id
            ''' if id is None else \
            '''with gt as (
            select g.*, b.company as company_id, b.name as building_name from gate g 
            left join building b on b.id = g.building
            )
            select gt.*, c.name as company_name from gt
            left join company c on c.id = gt.company_id 
            where gt.id = %s'''
            params = (id,) if id else ()
        else:
            sql = '''with gt as (
            select g.*, b.company as company_id, b.name as building_name from gate g 
            left join building b on b.id = g.building
            )
            select gt.*, c.name as company_name from gt
            left join company c on c.id = gt.company_id 
            where gt.company_id = %s
            ''' if id is not None else \
            '''with gt as (
            select g.*, b.company as company_id, b.name as building_name from gate g 
            left join building b on b.id = g.building
            )
            select gt.*, c.name as company_name from gt
            left join company c on c.id = gt.company_id 
            where gt.id = %s and gt.company_id = %s'''
            params = (id, company,) if id else (company,)
        data = query_db(cur, sql, params)
        return data


def get_gate_details(gate_id):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''with gt as (
              select g.*, b.company as company_id, b.name as building_name from gate g 
              left join building b on b.id = g.building
              )
              select gt.*, c.name as company_name from gt
              left join company c on c.id = gt.company_id
              where gt.id = %s'''
        data = query_db(cur, sql, (gate_id,))
        sql = 'select id, ip from access_point where gate = %s'
        access_points = query_db(cur, sql, (gate_id,))
        data[0]["access_points"] = access_points
        return data[0]


def create_gate(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f"""insert into gate {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
            gate_id = values[0]
            building = data["building"]
            create_default_access_point(cur, gate_id, building)
            return gate_id
    except Exception as ex:
        raise Exception(f"Error while creating gate: {str(ex.args[0])}")


def create_default_access_point(cursor, gate_id, building):
    access_point_id = str(uuid.uuid4())
    sql = 'select company from building where id = %s'
    cursor.execute(sql, (building,))
    company = cursor.fetchall()[0][0]
    sql = 'insert into access_point (id, gate, company) values (%s, %s, %s)'
    cursor.execute(sql, (access_point_id, gate_id, company,))


def update_gate(data, id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            params, values = parse_update_params(data)
            sql = f"""update gate set {params} where id = %s""".replace("'", "")
            cur.execute(sql, values + (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating gate: {str(ex.args[0])}")


def delete_gate(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from gate where id = %s"""
            cur.execute(sql, (id,))
            sql = 'delete from access_point where gate = %s'
            cur.execute(sql, (id,))
    except Exception as ex:
        raise Exception(f"Error while deleting building: {str(ex.args[0])}")


def delete_gates(ids):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from gate where id in %s"""
            cur.execute(sql, (tuple(ids),))
            sql = 'delete from access_point where gate in %s'
            cur.execute(sql, (tuple(ids),))
    except Exception as ex:
        raise Exception(f"Error while deleting gates: {str(ex.args[0])}")