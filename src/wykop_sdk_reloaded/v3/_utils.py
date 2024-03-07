import functools


def auth_user_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]

        self.auth.check_user_authentication()

        return func(*args, **kwargs)
    return wrapper
