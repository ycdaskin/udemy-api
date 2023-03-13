from src.resources.dbops import get_connection, query_db, group_by, parse_params, parse_update_params
from src.auth.auth import is_super_user


def update_company(data, id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            params, values = parse_update_params(data)
            sql = f"""update company set {params} where id = %s""".replace("'", "")
            cur.execute(sql, values + (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while updating company: {str(ex.args[0])}")


def get_companies(id=None):
    with get_connection() as conn:
        cur = conn.cursor()
        request_user, company, super_admin = is_super_user()
        if super_admin:
            sql = "select * from company where id = %s" if id else "select * from company"
            params = (id,) if id else ()
        else:
            if id and id != company:
                return []
            sql = "select * from company where id = %s "
            params = (company,)
        data = query_db(cur, sql, params)
        return data


def create_company(data):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            columns, values, placeholders = parse_params(data, auto_id_column="id")
            sql = f"""insert into company {columns} values {placeholders}""".replace("'", "")
            cur.execute(sql, values)
            conn.commit()
            return values[0]
    except Exception as ex:
        raise Exception(f"Error while creating company: {str(ex.args[0])}")


def delete_company(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from company where id = %s"""
            cur.execute(sql, (id,))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while deleting company: {str(ex.args[0])}")


def delete_companies(ids):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = f"""delete from company where id in %s"""
            cur.execute(sql, (tuple(ids),))
            conn.commit()
    except Exception as ex:
        raise Exception(f"Error while deleting companies: {str(ex.args[0])}")


def get_company_details(id):
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            sql = '''select * from company where id = %s'''
            company = query_db(cur, sql, (id,))[0]
            return company
    except Exception as ex:
        raise Exception(f"Error while getting company details: {str(ex.args[0])}")