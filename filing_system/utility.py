from contextlib import contextmanager


@contextmanager
def manage_pwd(path: str):
    orignal_working_directory = os.getpwd()

    if not os.path.exists(path):
        raise ValueError

    if not os.isdir(path):
        raise ValueError

    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(orignal_working_directory)