from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params
from src.auth.auth import is_super_user


def get_user_roles_by_company(company_id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user(cur=cur)
        if super_admin:
            sql = ''' select * from app_user_role where company = %s''' \
                if company_id is not None else '''select * from app_user_role'''
            params = (company_id,) if company_id else ()
        else:
            sql = ''' select * from app_user_role where company = %s'''
            params = (company,)
        data = query_db(cur, sql, params)
        return data


def get_user_role(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user(cur=cur)
        if super_admin:
            sql = ''' select * from app_user_role where id = %s''' \
                if id is not None else '''select * from app_user_role'''
            params = (id,) if id else ()
        else:
            sql = ''' select * from app_user_role where company = %s''' \
                if id is not None else '''select * from app_user_role where company = %s and id = %s'''
            params = (company, id,) if id else (company,)
        data = query_db(cur, sql, params)
        return data

def create_user_role(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f"""insert into app_user_role {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
            conn.commit()
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating user role: {str(ex.args[0])}")


def delete_user_role(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from app_user_role where id = %s"""
            cur.execute(sql, (id,))
            sql = 'delete from role_priv_crs where user_role = %s'
            cur.execute(sql, (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while deleting user role: {str(ex.args[0])}")


def update_user_role(data, id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            if len(data) == 0:
                return
            params, values = parse_update_params(data)
            sql = f"""update app_user_role set {params} where id = %s""".replace("'", "")
            cur.execute(sql, values + (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating user role: {str(ex.args[0])}")


def delete_user_roles(ids):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from app_user_role where id in %s"""
            cur.execute(sql, (tuple(ids),))
            sql = 'delete from role_priv_crs where user_role in %s'
            cur.execute(sql, (tuple(ids),))
    except Exception as ex:
        raise Exception(f"Error while deleting user roles: {str(ex.args[0])}")
