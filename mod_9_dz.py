users = {}
def input_error(func):
    def wrapper(*args):
        try:
            pass
        except KeyError:
            pass
        except ValueError:
            pass
        except IndexError:
            pass
