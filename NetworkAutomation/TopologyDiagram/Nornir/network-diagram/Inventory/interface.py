from typing import Optional


class Interface:
    def __init__(self, name: str, device_name: Optional[str] = None) -> None:
        self.name = name
        self.device_name = self.device_name
    
    def __repr__(self) -> str:
        return {
            f"{self.__class__.__qualname__}("
            f"name={self.name!r}, "
            f"device_name={self.device_name!r})"
        }
    
    def __str__(self) -> str:
        return f"{self.device_name} {self.name}"
    
    def __lt__(self) -> bool:
        return (self.device_name, self.name) < (other.device_name, other.name)



Link(Interface('gig1', 'R1'), Interface('gig1', 'R2'))
Link(Interface('gig1', 'R2'), Interface('gig1', 'R1'))