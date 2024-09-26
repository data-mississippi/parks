from dataclasses import dataclass, field


@dataclass
class Campsite:
    name: str
    district: str
    division_id: str
    dates: dict = field(default_factory=dict)

    def to_dict(self):
        return self.__dict__


@dataclass
class Subscription:
    email: str
    dates: list
    campsite: Campsite
