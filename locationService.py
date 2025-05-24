from typing import List, Optional
import logging
import requests
from dataclasses import dataclass
from location import Location

# Exception classes
class NotFoundException(Exception):
    pass

class ServiceException(Exception):
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause

# Service configuration
@dataclass
class ServiceConfig:
    viron_host: str
    viron_port: int

# Location Service
class LocationService:
    def __init__(self, service_config: ServiceConfig):
        self.logger = logging.getLogger(__name__)
        self.base_url = f"{service_config.viron_host}:{service_config.viron_port}/api/v1/locations"

    def get_all_locations(self) -> List[Location]:
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error getting locations: {str(e)}")
            raise ServiceException("Error getting locations", e)

    def get_location_by_id(self, id: int) -> Location:
        try:
            response = requests.get(f"{self.base_url}/{id}")
            if response.status_code == 404:
                raise NotFoundException(f"Location not found with id: {id}")
            response.raise_for_status()
            return response.json()
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error getting location by id {id}: {str(e)}")
            raise ServiceException(f"Error getting location by id: {id}", e)

    def get_locations_in_environment(self, environment_id: int) -> List[Location]:
        try:
            response = requests.get(f"{self.base_url}/environment/{environment_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error getting locations in environment {environment_id}: {str(e)}")
            raise ServiceException(f"Error getting locations in environment: {environment_id}", e)

    def get_locations_in_grid(self, grid_id: int) -> List[Location]:
        try:
            response = requests.get(f"{self.base_url}/grid/{grid_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error getting locations in grid {grid_id}: {str(e)}")
            raise ServiceException(f"Error getting locations in grid: {grid_id}", e)

    def get_location_of_entity(self, entity_id: int) -> Location:
        try:
            response = requests.get(f"{self.base_url}/entity/{entity_id}")
            if response.status_code == 404:
                raise NotFoundException(f"Location not found for entity: {entity_id}")
            response.raise_for_status()
            return response.json()
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error getting location of entity {entity_id}: {str(e)}")
            raise ServiceException(f"Error getting location of entity: {entity_id}", e)

    def add_entity_to_location(self, entity_id: int, location_id: int) -> None:
        try:
            response = requests.put(f"{self.base_url}/{location_id}/entity/{entity_id}")
            if response.status_code == 404:
                raise NotFoundException("Location or entity not found")
            response.raise_for_status()
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error adding entity {entity_id} to location {location_id}: {str(e)}")
            raise ServiceException("Error adding entity to location", e)

    def remove_entity_from_location(self, entity_id: int, location_id: int) -> None:
        try:
            response = requests.delete(f"{self.base_url}/{location_id}/entity/{entity_id}")
            if response.status_code == 404:
                raise NotFoundException("Location or entity not found")
            response.raise_for_status()
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error removing entity {entity_id} from location {location_id}: {str(e)}")
            raise ServiceException("Error removing entity from location", e)

    def remove_entity_from_current_location(self, entity_id: int) -> None:
        try:
            response = requests.delete(f"{self.base_url}/entity/{entity_id}")
            if response.status_code == 404:
                raise NotFoundException("Entity not found")
            response.raise_for_status()
        except NotFoundException as e:
            raise e
        except Exception as e:
            self.logger.error(f"Error removing entity {entity_id} from current location: {str(e)}")
            raise ServiceException("Error removing entity from current location", e)