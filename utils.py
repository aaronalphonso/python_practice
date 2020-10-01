import time
from contextlib import contextmanager


@contextmanager
def timed_block(name):
    """Context manager to help time an arbitrary block of code

    @:param name: Just a name to be used in the print statement

    Usage:
        with timed_block("testing prints"):
            print("Hello")
            print("World")
    """
    start_time = time.time()
    try:
        yield
    except Exception as e:
        raise e
    finally:
        end_time = time.time()
        print("Block labelled {} completed execution in {:.6}ms".format(name, (end_time - start_time) * 1000))

