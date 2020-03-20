SQLALCHEMY_DATABASE_URI = "postgres://postgres:root@127.0.0.1/smart"
# SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
#

SQLALCHEMY_ENGINE_OPTIONS = {
    "max_overflow": 15,
    "pool_pre_ping": True,
    "pool_recycle": 10 * 10,
    "pool_size": 30,
}
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = [
    "access",
    "refresh",
]
