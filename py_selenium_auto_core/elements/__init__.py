from typing import Type, TypeVar


class A:

    def __init__(self, v):
        print(f"A: {v}")
        self.v = v

    def get_v(self):
        return self.v


class B(A):

    def __init__(self, v):
        v = v+1
        super().__init__(v)
        print(f"B: {v}")
        self.v = v

    def get_v1(self):
        return self.v


T = TypeVar("T", bound=A, covariant=True)

