"""
docs: https://docs.ponyorm.org/
"""
from os import urandom

from .models import *
from hashlib import pbkdf2_hmac
import binascii

SALT = "QCIGSDwfnTOaoF1MFkzFZfFzbAhmlrnU"

# ==============================================================================
# ===== CONTROLLER =====

# ==============================================================================
# ADMIN FUNCS

def hash_admin(email, pwd):
    dk = pbkdf2_hmac(hash_name='sha256',
                     password=bytes("%s ---- %s" % (email, pwd), 'utf-8'),
                     salt=SALT,
                     iterations=100000)
    return str(binascii.hexlify(dk), encoding="utf-8")


def is_admin(login, pwd):
    return is_hash_admin(hash_admin(login, pwd))


@db_session
def is_hash_admin(h):
    return h and exists(h == a.hash for a in Admin)


@db_session
def get_admin_by_email(email: str) -> Admin:
    return select(a for a in Admin if a.email == email).first()


@db_session
def get_admin_by_hash(hash: str) -> Admin:
    return select(a for a in Admin if a.hash == hash).first()


@db_session
def get_admin_by_id(id: int) -> Admin:
    return select(a for a in Admin if a.id == id).first()


@db_session
def get_admin(email_hash_id):
    return select(a for a in Admin if email_hash_id in (a.email, a.hash, a.id)).first()


@db_session
def create_admin(email: str, password: str, name: str = "") -> Admin or None:
    if not password:
        return None
    h = hash_admin(email, password)
    admin = get_admin_by_hash(h)

    if not admin and not select(a.email == email for a in Admin).first():
            return Admin(email=email, hash=h, name=name or email.split("@")[0])
    else:
        return admin


@db_session
def del_admin(email_hash_id):
    a = get_admin(email_hash_id)
    if a:
        a.delete()
        return True
    return False


@db_session
def edit_admin_password(email_hash_id, password: str):
    a = get_admin(email_hash_id)
    a.hash = hash_admin(a.email, password)
    return a


@db_session
def edit_admin_data(admin: Admin, name: str = None, email: str = None, password: str = None, **kwargs) -> Admin:
    if name:
        admin.name = name
    if email:
        admin.email = email
    if password:
        admin.hash = hash_admin(admin.email, password)
    return admin


@db_session
def get_settings(key, default={}):
    s = select(s for s in Settings if s.key == key).first()
    return s.value if s else default


@db_session
def get_all_settings():
    return dict(select((s.key, s.value) for s in Settings))


@db_session
def update_settings(key: str, value: dict):
    s = select(s for s in Settings if s.key == key).first()
    # print("GET", s)
    if s:
        s.value.update(value)
    else:
        with db_session:
            s = Settings(key=key, value=value)
        # print("ELSE", s)
    return s


# ===== END CONTROLLER =====


if __name__ == '__main__':
    with db_session:
        Admin.select().show()
        """
        print(create_admin("jag-k58@ya.ru", "PASSWORD"))
        print()
        Admin.select().show()
        print(edit_admin_password("jag-k58@ya.ru", "PASSwORD"))
        print()
        Admin.select().show()
        print()
        Admin.select().show()
        """
