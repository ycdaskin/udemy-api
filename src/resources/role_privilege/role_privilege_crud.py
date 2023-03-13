from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params
from src.auth.auth import is_super_user


def get_role_privileges():
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user()
        if super_admin:
            sql = '''select * from app_user_role'''
            params = ()
        else:
            sql = '''select * from app_user_role where company = %s'''
            params = (company,)
        user_roles = query_db(cur, sql, params)
        sql = '''select p.id, p.name, p.description from role_priv_crs rpc
        left join privileges p on p.id = rpc.priv 
        where user_role = %s'''
        for user_role in user_roles:
            privileges = query_db(cur, sql, (user_role["id"],))
            user_role["privileges"] = privileges
        return user_roles


def create_role_privilege(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            role_id = data["role_id"]
            privilege_ids = data["privilege_ids"]
            sql = 'delete from role_priv_crs where user_role = %s'
            cur.execute(sql, (role_id,))
            sql = 'insert into role_priv_crs values (%s, %s)'
            for priv_id in privilege_ids:
                cur.execute(sql, (role_id, priv_id,))
    except Exception as ex:
        raise Exception(f"Error while creating role-privilege relation: {str(ex.args[0])}")


def update_role_privilege(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            role_id = data["role_id"]
            privilege_ids = data["privilege_ids"]
            cur.execute('delete from role_priv_crs where user_role = %s', (role_id,))
            sql = 'insert into role_priv_crs values (%s, %s)'
            for priv_id in privilege_ids:
                cur.execute(sql, (role_id, priv_id,))
    except Exception as ex:
        raise Exception(f"Error while updating role-privilege relation: {str(ex.args[0])}")


def delete_role_privilege(role_id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute('delete from role_priv_crs where user_role = %s', (role_id,))
    except Exception as ex:
        raise Exception(f"Error while deleting role-privilege relation: {str(ex.args[0])}")






