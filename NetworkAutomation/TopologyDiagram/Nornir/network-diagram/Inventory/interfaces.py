class interfaces:
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