from utils.shared import get_redis_revoke_list
from flask import current_app


def init_jwt(jwt):
    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        revoked_list = get_redis_revoke_list()
        jti = decrypted_token["jti"]
        if jti in revoked_list:
            return True
        return False


def revoke_tokens(access_token_jti, refresh_token_jti):
    revoked_list = get_redis_revoke_list()
    access_token_expires = current_app.config["JWT_ACCESS_TOKEN_EXPIRES"]
    refresh_token_expires = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    revoked_list.set(access_token_jti, 1, access_token_expires)
    revoked_list.set(refresh_token_jti, 1, refresh_token_expires)
