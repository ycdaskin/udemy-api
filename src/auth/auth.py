import uuid

from src.crypto.crypto import Crypto
import datetime
import json
from flask import make_response, jsonify, request
from functools import wraps
from psycopg2 import pool as p
from contextlib import contextmanager
from random import randint

crypto = Crypto()

pool = p.ThreadedConnectionPool(
    5,
    20,
    host='ec2-54-73-22-169.eu-west-1.compute.amazonaws.com',
    database='dbm5rut493hudn',
    user='rmgicawsisxtnu',
    password="475be76867cdbaf3edd0ba958b34ada8fe238d49079893a5f6e6c41716702346",
    port=5432,
    options="-c search_path=dbo,auth"
)


@contextmanager
def get_connection():
    con = pool.getconn()
    try:
        yield con
        con.commit()
    finally:
        pool.putconn(con)


def generate_verification_code(n):
    return ''.join(["{}".format(randint(0, 9)) for num in range(0, n)])


def get_user_by_secret_key(secret_key, verification_code):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select user_id, verification_code from otp where id = %s'''
        cur.execute(sql, (secret_key,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return None
        if rows[0][1] != verification_code:
            return None
        return rows[0][0]


def delete_verification_code(secret_key):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = 'delete from otp where id = %s'
        cur.execute(sql, (secret_key,))



def get_secret_key_by_verification_code(verification_code):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select id, verification_code, expire_date from otp where verification_code = %s'''
        cur.execute(sql, (verification_code,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return None
        expire_date = datetime.datetime.fromisoformat(rows[0][2])
        now = datetime.datetime.now()
        if now > expire_date:
            cur.execute('''delete from otp where verification_code = %s''', (verification_code,))
            conn.commit()
            return None
        return rows[0][0]



def verification_code_valid(req):
    verification_code = req.headers.get("Verification-Code")
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select user_id, verification_code, expire_date from otp where verification_code: %s'''
        cur.execute(sql, (verification_code,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return False
        expire_date = datetime.datetime.fromisoformat(rows[0][2])
        now = datetime.datetime.now()
        if now > expire_date:
            cur.execute('''delete from otp where verification_code = %s''', (verification_code,))
            conn.commit()
            return False
        return True


def is_super_user():
    auth = request.headers.get("Authorization")
    token = auth.split(" ")[1]
    user, company = get_user_and_company(token)
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select * from data.user_privileges up 
        left join data.privileges p
        on up.privilege = p.id
        where p.name = 'superAdmin' and up.user_id = %s '''
        cur.execute(sql, (user,))
        return user, company, len(cur.fetchall()) > 0



def token_valid(req):
    auth = req.headers.get("Authorization")
    token = auth.split(" ")[1]
    with get_connection() as conn:
        cur = conn.cursor()
        sess_sql = '''select * from sess where token = %s'''
        cur.execute(sess_sql, (token,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return False
        token_str = crypto.decrypt(rows[0][2])
        token_obj = json.loads(token_str)
        created_at = token_obj["created_at"]
        validation_delta = token_obj["validation_delta"]
        validation_delta = parse_delta_string(validation_delta)
        creation_time = datetime.datetime.fromisoformat(created_at)
        now = datetime.datetime.now()
        diff = now - creation_time
        if diff > validation_delta:
            cur.execute('delete from sess where token = %s', (token,))
            conn.commit()
            return False
        return True


def refresh_token_valid(req):
    auth = req.headers.get("Authorization")
    refresh_token = auth.split(" ")[1]
    with get_connection() as conn:
        cur = conn.cursor()
        sess_sql = '''select * from sess where refresh_token = %s'''
        cur.execute(sess_sql, (refresh_token,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return False
        refresh_token_str = crypto.decrypt(rows[0][3])
        refresh_token_obj = json.loads(refresh_token_str)
        created_at = refresh_token_obj["created_at"]
        validation_delta = refresh_token_obj["validation_delta"]
        validation_delta = parse_delta_string(validation_delta)
        creation_time = datetime.datetime.fromisoformat(created_at)
        now = datetime.datetime.now()
        diff = now - creation_time
        related_token = rows[0][2]
        if diff > validation_delta or get_identity(related_token) != refresh_token_obj["identity"]: # token expire olmuşsa veya identity'si ilgili access_token identity ile aynı değilse
            cur.execute('delete from sess where refresh_token = %s', (refresh_token,))
            conn.commit()
            return False

        is_refresh = refresh_token_obj["is_refresh"]
        return is_refresh


def create_token(identity, company, validation_delta=datetime.timedelta(hours=24), for_mobile=False):
    token_object = {
        "identity": identity,
        "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "validation_delta": str(validation_delta),
        "for_mobile": for_mobile,
        "is_refresh": False,
        "company": company
    }
    str_obj = json.dumps(token_object)
    token = crypto.encrypt(str_obj)
    return token


def create_refresh_token(identity, company, related_token, validation_delta=datetime.timedelta(days=180)):
    refresh_token_object = {
        "identity": identity,
        "created_at": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "validation_delta": str(validation_delta),
        "related_token": related_token,
        "is_refresh": True,
        "company": company
    }
    str_obj = json.dumps(refresh_token_object)
    refresh_token = crypto.encrypt(str_obj)
    return refresh_token


def get_identity(token):
    token_str = crypto.decrypt(token)
    token_obj = json.loads(token_str)
    return token_obj["identity"]


def get_user_and_company(token):
    token_str = crypto.decrypt(token)
    token_obj = json.loads(token_str)
    return token_obj["identity"], token_obj["company"]


def parse_delta_string(delta_string):
    if "day" in delta_string:
        splitted = delta_string.split(' ')
        days = int(splitted[0])
        hmsms = splitted[2].split(':')
        hours = int(hmsms[0])
        minutes = int(hmsms[1])
        sms = hmsms[2].split('.')
        seconds = int(sms[0])
        milliseconds = int(sms[1]) if len(sms) == 2 else 0
    else:
        days = 0
        splitted = delta_string.split(':')
        hours = int(splitted[0])
        minutes = int(splitted[1])
        sms = splitted[2].split('.')
        seconds = int(sms[0])
        milliseconds = int(sms[1]) if len(sms) == 2 else 0
    return datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


def create_session(user, token, refresh_token):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''insert into sess values(%s, %s, %s, %s)'''
        params = (str(uuid.uuid4()), user, token, refresh_token,)
        cur.execute(sql, params)


def create_verification_code_record(user, verification_code, validation_range=datetime.timedelta(seconds=180)):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''insert into otp values (%s, %s, %s, %s)'''
        record_id = str(uuid.uuid4())
        expire_date = (datetime.datetime.now() + validation_range).strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(sql, (record_id, user, expire_date, verification_code,))



def update_session_by_refresh_token(token, refresh_token):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''update sess set token = %s where refresh_token = %s'''
        cur.execute(sql, (token, refresh_token,))


def kill_session(token):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''delete from sess where token = %s'''
        cur.execute(sql, (token,))
        conn.commit()


def kill_user_sessions(user):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''delete from sess where user = %s'''
        cur.execute(sql, (user,))
        conn.commit()


def kill_user_mobile_sessions(user):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select token from sess where user = %s'''
        cur.execute(sql, (user,))
        tokens = [r[0] for r in cur.fetchall()]
        for token in tokens:
            if is_mobile_session(token):
                sql = '''delete from sess where token = %s'''
                cur.execute(sql, (token,))
        conn.commit()


def kill_user_web_sessions(user):
    with get_connection() as conn:
        cur = conn.cursor()
        sql = '''select token from sess where user = %s'''
        cur.execute(sql, (user,))
        tokens = [r[0] for r in cur.fetchall()]
        for token in tokens:
            if not is_mobile_session(token):
                sql = '''delete from sess where token = %s'''
                cur.execute(sql, (token,))
        conn.commit()


def is_mobile_session(token):
    token_str = crypto.decrypt(token)
    token_obj = json.loads(token_str)
    return token_obj["is_mobile"]


def token_required(f):
    @wraps(f)
    def inner(*args, **kws):
        if not token_valid(request):
            return make_response(jsonify(
                msg="Invalid or expired token",
                status="fail"
            ), 401)
        return f(*args, **kws)
    return inner


def refresh_token_required(f):
    @wraps(f)
    def inner(*args, **kws):
        if not refresh_token_valid(request):
            return make_response(jsonify(
                msg="Invalid or expired refresh token",
                status="fail"
            ), 401)
        return f(*args, **kws)
    return inner


def verification_code_required(f):
    @wraps(f)
    def inner(*args, **kws):
        if not verification_code_valid(request):
            return make_response(jsonify(
                msg="Invalid or expired verification code",
                status="fail"
            ), 401)
        return f(*args, **kws)
    return inner



