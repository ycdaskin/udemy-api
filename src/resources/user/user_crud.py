from src.resources.dbops import get_connection, query_db, parse_params, parse_update_params
from src.auth.auth import is_super_user
from src.s3_storage.s3_utils import delete_file

def update_user(data, id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            params, values = parse_update_params(data)
            sql = f"""update app_user set {params} where id = %s""".replace("'", "")
            cur.execute(sql, values + (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating user: {str(ex.args[0])}")


def get_users(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user()
        if super_admin:
            sql = '''select u.id, u.name, last_name, user_name, company, u.phone, u.email, u.address, chief,
            u.is_active, avatar, id_number, u.area_code, c.name company_name from app_user u
            left join company c on c.id = u.company where u.id = %s''' \
                if id is not None else \
                '''select u.id, u.name, last_name, user_name, company, u.phone, u.email, u.address, chief,
                u.is_active, avatar, id_number, u.area_code, c.name company_name from app_user u
                left join company c on c.id = u.company'''
            params = (id,) if id else ()
        else:
            sql = '''select u.id, u.name, last_name, user_name, company, u.phone, u.email, u.address, chief,
            u.is_active, avatar, id_number, u.area_code, c.name company_name from app_user u
            left join company c on c.id = u.company where u.id = %s and u.company = %s''' \
                if id is not None else \
                '''select u.id, u.name, last_name, user_name, company, u.phone, u.email, u.address, chief,
                u.is_active, avatar, id_number, u.area_code, c.name company_name from app_user u
                left join company c on c.id = u.company where u.company = %s'''
            params = (id, company,) if id else (company,)
        data = query_db(cur, sql, params)
        for user in data:
            privs = get_user_privileges(user["id"], cur)
            user["privileges"] = privs
        return data





def get_user_privileges(user_id, cursor, name_only=True):
    cur = cursor
    sql = '''select * from user_privileges as up
    left join privileges as p
    on up.privilege = p.id
    where up.user_id = %s'''
    priv_data = query_db(cur, sql, (user_id,))
    sql = '''select p.* from role_priv_crs rpc
    left join privileges p on p.id = rpc.priv
    where rpc.user_role in (select role_id from user_role_rel urr where urr.user_id = %s)'''
    role_priv_data = query_db(cur, sql, (user_id,))
    priv_arr = [d["name"] for d in priv_data] if name_only else priv_data
    role_priv_arr = [d["name"] for d in role_priv_data] if name_only else role_priv_data
    return priv_arr + role_priv_arr




def create_user(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id", columns_to_encyript=["password"])
            sql = f"""insert into app_user {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
            if "avatar" not in data:
                avatar = f'''https://ui-avatars.com/api/?background=FFE88C&size=128&name={data["name"]}+{data["last_name"]}'''
                sql = '''update app_user set avatar = %s where id = %s'''
                cur.execute(sql, (avatar, values[0]))
            conn.commit()
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating user: {str(ex.args[0])}")



def delete_user(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            avatar_sql = 'select avatar from app_user where id = %s'
            cur.execute(avatar_sql, (id,))
            rows = cur.fetchall()
            if len(rows) > 0 and "s3" in rows[0][0]:
                try:
                    key = rows[0][0].split('/')[-1]
                    delete_file(key)
                except:
                    pass
            sql = 'delete from app_user where id = %s'
            cur.execute(sql, (id,))
            sql = 'delete from user_access_privs where user_id = %s'
            cur.execute(sql, (id,))
            sql = 'delete from user_access_privs where user_id = %s'
            cur.execute(sql, (id,))
    except Exception as ex:
        raise Exception(f"Error while deleting user: {str(ex.args[0])}")






def delete_users(ids):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = 'delete from app_user where id in %s'
            cur.execute(sql, (tuple(ids),))
            sql = 'delete from user_access_privs where user_id in %s'
            cur.execute(sql, (tuple(ids),))
            sql = 'delete from user_access_privs where user_id in %s'
            cur.execute(sql, (tuple(ids),))
    except Exception as ex:
        raise Exception(f"Error while deleting users: {str(ex.args[0])}")

def get_user_staff(id, cursor):
    '''
    kullanıcıya bağlı çalışanları getirir
    :param id:
    :return:
    '''
    sql = "select name, last_name, id, avatar from app_user where chief = %s"
    data = query_db(cursor, sql, (id,))
    return data



def get_user_details(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = '''select u.id, u.name, last_name, user_name, company, u.phone, u.email, u.address, chief,
            u.is_active, avatar, id_number, u.area_code, c.name company_name from app_user u
            left join company c on c.id = u.company where u.id = %s'''
            user = query_db(cur, sql, (id,))[0]
            privs = get_user_privileges(id, cur, name_only=False)
            user["privileges"] = privs
            staff = get_user_staff(id, cur)
            user["staff"] = staff
            return user
    except Exception as ex:
        raise Exception(f"Error while getting user details: {str(ex.args[0])}")
