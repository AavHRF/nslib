class Nation:

    __slots__ = (
        "name",
    )

    @classmethod
    def from_dict(cls, dvals: dict):
        for key, value in dvals.items():
            try:
                setattr(cls, key, value)
            except AttributeError:
                pass

    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.__slots__}


class Region:

    @classmethod
    def from_dict(cls, dvals: dict):
        for key, value in dvals.items():
            try:
                setattr(cls, key, value)
            except AttributeError:
                pass

    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.__slots__}

