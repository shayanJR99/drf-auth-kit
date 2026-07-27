class ChangePasswordService:
    @staticmethod
    def execute(user, new_password: str):
        user.set_password(new_password)
        user.save()
        return user