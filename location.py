# Copyright (c) 2024 Preponderous Software
# MIT License

class Location:
    def __init__(self, location_id: int, x: int, y: int):
        self.location_id = location_id
        self.x = x
        self.y = y

    def get_location_id(self) -> int:
        return self.location_id

    def set_location_id(self, location_id: int):
        self.location_id = location_id

    def get_x(self) -> int:
        return self.x

    def set_x(self, x: int):
        self.x = x

    def get_y(self) -> int:
        return self.y

    def set_y(self, y: int):
        self.y = y

    def __str__(self) -> str:
        return f"Location{{location_id={self.location_id}, x={self.x}, y={self.y}}}"