from datetime import datetime
from typing import List, Optional

from backend.model.basic_model import BasicModel
from backend.utility.encrypt_helper import encrypt_plaintext_password
from backend.utility.error_helper import BusinessError
from backend.utility.string_helper import generate_random_string, is_blank


class MasterUserEm(BasicModel):
    username: str
    password: str
    salt: Optional[str]
    is_active: bool = True
    last_login_at: Optional[datetime]

    @classmethod
    def create_new_user(cls, username: str, password: str):
        data = cls(username=username, password=password)
        data.random_salt()
        data.encrypt_password()
        return data

    def random_salt(self):
        self.salt = generate_random_string()

    def encrypt_password(self):
        if self.salt is None:
            self.random_salt()

        self.password = encrypt_plaintext_password(self.password, self.salt)

    def check_password(self, input_password: str) -> bool:
        """
        :return: `True` is passed
        """
        if self.salt is None:
            raise BusinessError("User password salt not found.")
        input_password = encrypt_plaintext_password(input_password, self.salt)
        return input_password == self.password


class MasterUserRegisterEm(MasterUserEm):
    password_confirm: str

    def check_password2(self) -> bool:
        """
        :return: `True` is passed.
        """
        if is_blank(self.password):
            raise BusinessError("`password` can not be blank.")
        if is_blank(self.password_confirm):
            raise BusinessError("`password2` can not be blank.")
        return self.password == self.password_confirm


class MasterUserManageEm(MasterUserEm):
    password: str = None
    new_password: Optional[str]
    new_password_confirm: Optional[str]

    organization_id: str = None
    role_id_list: List[str]

    def check_new_password(self) -> bool:
        """:return: True if need update password, raise when validate failed."""
        if not self.new_password:
            return False
        if not self.new_password_confirm:
            raise BusinessError('重置密码时重复密码不得为空')
        if not self.new_password == self.new_password_confirm:
            raise BusinessError('两次密码不匹配')

        self.password = self.new_password
        self.encrypt_password()

        return True
