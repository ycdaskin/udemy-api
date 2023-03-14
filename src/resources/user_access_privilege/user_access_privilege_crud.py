from src.resources.dbops import get_connection, query_db, parse_params
from src.auth.auth import is_super_user


def get_user_access_privs():
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user(cur=cur)
        if super_admin:
            sql = '''select uap.*, u.name || ' ' || u.last_name as user_name, u.avatar, g.name as gate_name, 
                         g.id as gate_id, b.name as building_name 
                    from data.user_access_privs uap
                    left join data.access_point ap on ap.id = uap.access_point_id
                    left join data.gate g on g.id = ap.gate
                    left join data.building b on b.id = g.building
                    left join data.app_user u on u.id = uap.user_id
                    '''
            params = ()
        else:
            sql = '''select uap.*, u.name || ' ' || u.last_name as user_name, u.avatar, g.name as gate_name,
                         g.id as gate_id, b.name as building_name 
                    from data.user_access_privs uap
                    left join data.access_point ap on ap.id = uap.access_point_id
                    left join data.gate g on g.id = ap.gate
                    left join data.building b on b.id = g.building 
                    left join data.app_user u on u.id = uap.user_id where b.company = %s'''
            params = (company,)
        data = query_db(cur, sql, params)
        return data


def create_user_access_privs(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data)
            sql = f"""insert into user_access_privs {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
    except Exception as ex:
        raise Exception(f"Error while creating user access privileges: {str(ex.args[0])}")


def delete_access_privs_of_user(user_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from user_access_privs where user_id = %s"""
            cur.execute(sql, (tuple(user_id),))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while deleting companies: {str(ex.args[0])}")


def get_aceess_privs_by_user(user_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = '''select * from user_access_privs where user_id = %s'''
            company = query_db(cur, sql, (user_id,))
            return company
    except Exception as ex:
        raise Exception(f"Error while getting user access privileges: {str(ex.args[0])}")


def get_user_access_privs_by_gate(user_id, gate_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = '''select uap.*, ap.gate as gate_id, g.name as gate_name, g.building as building_id,
                     b.name as building_name
                  from data.user_access_privs uap
                  left join data.access_point ap on ap.id = uap.access_point_id
                  left join data.gate g on g.id = ap.gate
                  left join data.building b on g.building = b.id
                  where uap.user_id = %s and ap.gate = %s'''
            data = query_db(cur, sql, (user_id, gate_id,))
            return data
    except Exception as ex:
        raise Exception(f"Error while getting user access privileges: {str(ex.args[0])}")


def grant_user_access_privs_by_gate(user_id, gate_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = '''select id from access_point where gate = %s'''
            access_points = query_db(cur, sql, (gate_id,))
            sql = 'insert into user_access_privs values (%s, %s)'
            for access_point in access_points:
                cur.execute(sql, (user_id, access_point["id"]),)
    except Exception as ex:
        raise Exception(f"Error while granting user access privileges: {str(ex.args[0])}")


def revoke_user_access_privs_by_gate(user_id, gate_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = '''select id from access_point where gate = %s'''
            cur.execute(sql, (gate_id,))
            access_points = cur.fetchall()
            if len(access_points) > 0:
                access_points = [ap[0] for ap in access_points]
                sql = 'delete from user_access_privs where user_id = %s and access_point_id in %s'
                cur.execute(sql, user_id, tuple(access_points))
    except Exception as ex:
        raise Exception(f"Error while revoking user access privileges: {str(ex.args[0])}")


def revoke_user_access_privs_by_gate_multiple(data):
    '''
    çoklu şekilde kullanıcıların kapılardan geçiş yetkilerini kaldırır
    :param data: user_id, gate_id objeletinden oluşan array [{user_id, gate_id}]
    :return:
    '''
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            for record in data:
                user_id = record["user_id"]
                gate_id = record["gate_id"]
                sql = '''select id from access_point where gate = %s'''
                cur.execute(sql, (gate_id,))
                access_points = cur.fetchall()
                if len(access_points) > 0:
                    access_points = [ap[0] for ap in access_points]
                    sql = 'delete from user_access_privs where user_id = %s and access_point_id in %s'
                cur.execute(sql, (user_id, tuple(access_points),))
    except Exception as ex:
        raise Exception(f"Error while revoking user access privileges: {str(ex.args[0])}")


