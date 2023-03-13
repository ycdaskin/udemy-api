from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params
from src.auth.auth import is_super_user


def create_user_role_rel(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data)
            sql = f"""insert into user_role_rel {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
    except Exception as ex:
        raise Exception(f"Error while creating user-role relation: {str(ex.args[0])}")


def delete_user_role_rel(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            user_id = data["user_id"]
            role_id = data["role_id"]
            sql = "delete from user_role_rel where user_id = %s and role_id = %s"
            cur.execute(sql, (user_id, role_id,))
    except Exception as ex:
        raise Exception(f"Error while deleting user-role relation: {str(ex.args[0])}")



def delete_user_role_rel_multiple(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = "delete from user_role_rel where user_id = %s and role_id = %s"
            for d in data:
                user_id = d["user_id"]
                role_id = d["role_id"]
                cur.execute(sql, (user_id, role_id,))
    except Exception as ex:
        raise Exception(f"Error while deleting user-role relations: {str(ex.args[0])}")



def get_user_role_rel_details():
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            request_user, company, super_admin = is_super_user()
            if super_admin:
                sql = '''select urr.*, aur.name as role_name, aur.description as role_description,
                        au.name || ' ' || au.last_name as user_name, au.avatar
                        from data.user_role_rel urr
                        left join data.app_user_role aur on aur.id = urr.role_id
                        left join data.app_user au on au.id = urr.user_id'''
                params = ()
            else:
                sql = '''select urr.*, aur.name as role_name, aur.description as role_description,
                        au.name || ' ' || au.last_name as user_name, au.avatar
                        from data.user_role_rel urr
                        left join data.app_user_role aur on aur.id = urr.role_id
                        left join data.app_user au on au.id = urr.user_id where au.company = %s'''
                params = (company,)
            data = query_db(cur, sql, params)
            return data
    except Exception as ex:
        raise Exception(f"Error while deleting user-role relation: {str(ex.args[0])}")
