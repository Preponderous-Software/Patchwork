import logging
from typing import List, Optional
import requests

from src.main.python.preponderous.viron.models.entity import Entity

logger = logging.getLogger(__name__)


class EntityServiceException(Exception):
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause


class EntityService:
    def __init__(self, viron_host: str, viron_port: int):
        """Initialize EntityService with host and port"""
        self.viron_host = viron_host
        self.viron_port = viron_port

    def get_base_url(self) -> str:
        """Get the base URL for the API"""
        return f"{self.viron_host}:{self.viron_port}/api/v1/entities"

    def get_all_entities(self) -> List[Entity]:
        try:
            response = requests.get(self.get_base_url())
            response.raise_for_status()
            data = response.json()
            return [Entity(**entity) for entity in data] if data else []
        except Exception as e:
            logger.error(f"Failed to fetch all entities: {str(e)}")
            raise EntityServiceException("Error retrieving entities", e)

    def get_entity_by_id(self, entity_id: int) -> Optional[Entity]:
        try:
            response = requests.get(f"{self.get_base_url()}/{entity_id}")
            response.raise_for_status()
            data = response.json()
            return Entity(**data) if data else None
        except Exception as e:
            logger.error(f"Failed to fetch entity with id {entity_id}: {str(e)}")
            raise EntityServiceException("Error retrieving entity", e)

    def get_entities_in_environment(self, environment_id: int) -> List[Entity]:
        try:
            response = requests.get(f"{self.get_base_url()}/environment/{environment_id}")
            response.raise_for_status()
            data = response.json()
            return [Entity(**entity) for entity in data] if data else []
        except Exception as e:
            logger.error(f"Failed to fetch entities in environment {environment_id}: {str(e)}")
            raise EntityServiceException("Error retrieving entities in environment", e)

    def get_entities_in_grid(self, grid_id: int) -> List[Entity]:
        try:
            response = requests.get(f"{self.get_base_url()}/grid/{grid_id}")
            response.raise_for_status()
            data = response.json()
            return [Entity(**entity) for entity in data] if data else []
        except Exception as e:
            logger.error(f"Failed to fetch entities in grid {grid_id}: {str(e)}")
            raise EntityServiceException("Error retrieving entities in grid", e)

    def get_entities_in_location(self, location_id: int) -> List[Entity]:
        try:
            response = requests.get(f"{self.get_base_url()}/location/{location_id}")
            response.raise_for_status()
            data = response.json()
            return [Entity(**entity) for entity in data] if data else []
        except Exception as e:
            logger.error(f"Failed to fetch entities in location {location_id}: {str(e)}")
            raise EntityServiceException("Error retrieving entities in location", e)

    def get_entities_not_in_any_location(self) -> List[Entity]:
        try:
            response = requests.get(f"{self.get_base_url()}/unassigned")
            response.raise_for_status()
            data = response.json()
            return [Entity(**entity) for entity in data] if data else []
        except Exception as e:
            logger.error(f"Failed to fetch unassigned entities: {str(e)}")
            raise EntityServiceException("Error retrieving unassigned entities", e)

    def create_entity(self, name: str) -> Entity:
        try:
            response = requests.post(f"{self.get_base_url()}/{name}")
            response.raise_for_status()
            data = response.json()
            if not data:
                raise EntityServiceException("Created entity response was null")
            return Entity(**data)
        except Exception as e:
            logger.error(f"Failed to create entity with name {name}: {str(e)}")
            raise EntityServiceException("Error creating entity", e)

    def delete_entity(self, entity_id: int) -> bool:
        try:
            response = requests.delete(f"{self.get_base_url()}/{entity_id}")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to delete entity {entity_id}: {str(e)}")
            raise EntityServiceException("Error deleting entity", e)

    def update_entity_name(self, entity_id: int, name: str) -> bool:
        try:
            response = requests.patch(f"{self.get_base_url()}/{entity_id}/name/{name}")
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Failed to update name for entity {entity_id}: {str(e)}")
            raise EntityServiceException("Error updating entity name", e)
