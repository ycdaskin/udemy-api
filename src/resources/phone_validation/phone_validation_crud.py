from src.resources.dbops import get_connection, query_db
from src.auth.auth import create_verification_code_record, generate_verification_code
from messenger.PyMessenger import Email, Messenger


def validate_phone_number(data):
    with get_connection() as conn:
        cur = conn.cursor()
        area_code = data["area_code"]
        phone = data["phone"]
        phone = phone[len(area_code):]
        sql = '''select id, phone, email from app_user where phone = %s and area_code = %s'''
        result = query_db(cur, sql, (phone, area_code,))
        if len(result) == 0:
            return None
        user = result[0]["id"]
        verification_code = generate_verification_code(6)
        print(verification_code)
        create_verification_code_record(user, verification_code)
        # burada sms ile verification code'u kullanıcıya iletme adımı olacak
        email = result[0]["email"]
        inform_user_with_mail(email, verification_code)
        return user


def inform_user_with_mail(to, verification_code):
    subject = "Beasy Doğrulama Kodu"
    body = f"Şifre değiştirme doğrulama kodunuz\n{verification_code}"
    msg = Email(to, subject, body, is_HTML=False)
    my_messenger = Messenger("ycdaskingg@gmail.com", "wtoewdxbdwwccwkl")
    my_messenger.send_email(msg, one_time=True)

