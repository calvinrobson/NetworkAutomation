from typing import List
from network_diagram.interface import Interface


class Link:
    def __init__(self, interfaces: List[Interface]) -> None:
        self.interface = sorted(interfaces)
    
    def __eq__(self, other) -> bool:
        return all(
            int1 == int2
            for int1, int2 in zip(self.interfaces, other.interfaces)
        )
    def __hash__(self) -> int
        return hash(tuple(self.interfaces))