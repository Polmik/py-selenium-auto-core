import os


class EnvironmentConfiguration:

    @staticmethod
    def get_variable(env_key: str):
        variables = (
            os.environ.get(env_key),
            os.environ.get(env_key.lower()),
            os.environ.get(env_key.upper()),
        )
        if variables.count(None) == len(variables):
            return None
        return next(var for var in variables if var is not None)
