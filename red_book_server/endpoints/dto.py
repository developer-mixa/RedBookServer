from typing import Optional
from dataclasses import dataclass

@dataclass
class RedBookLocationDTO:
    longitude: float
    latitude: float

@dataclass
class RedBookItemDTO:
    name: str
    description: str
    count: int
    image: bytes
    category_id: int
    location: Optional[RedBookLocationDTO] = None

    @staticmethod
    def from_json(json: dict):
        location = json.get('location')
        return RedBookItemDTO(
            json['name'],
            json['description'],
            json['count'],
            json['image'],
            json['category_id'],
            RedBookLocationDTO(location['longitude'], location['latitude']) if location else None
        )
