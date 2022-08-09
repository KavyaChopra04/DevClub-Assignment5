from users.models import UserInfo
import logging


class MyAuthBackend(object):
    def authenticate(self, email, password):    
        try:
            user = UserInfo.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                return None
        except UserInfo.DoesNotExist:
            logging.getLogger("error_logger").error("user with login %s does not exists " % login)
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, email):
        try:
            user = UserModel.objects.get(sys_id=email)
            if user.is_active:
                return user
            return None
        except UserModel.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(email)d not found")
            return None
