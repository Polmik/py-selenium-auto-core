from __future__ import annotations

import os


class EnvironmentConfiguration:
    """Environment variables reader"""

    @staticmethod
    def get_variable(env_key: str) -> str | None:
        """Gets value of environment variable by key

        Args:
            env_key (str): Environment variable key

        Returns:
            Value of environment variable
        """
        variables = (
            os.environ.get(env_key),
            os.environ.get(env_key.lower()),
            os.environ.get(env_key.upper()),
        )
        if variables.count(None) == len(variables):
            return None
        return next(var for var in variables if var is not None)
