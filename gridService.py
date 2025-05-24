# Copyright (c) 2024 Preponderous Software
# MIT License

import logging
from typing import List, Optional
import requests
from requests.exceptions import HTTPError
from grid import Grid

logger = logging.getLogger(__name__)

class GridService:
    def __init__(self, base_url: str):
        """Initialize GridService with base URL.

        Args:
            base_url (str): Base URL of the service
        """
        self.base_url = f"{base_url}/api/v1/grids"

    def get_all_grids(self) -> List[Grid]:
        """Get all grids.

        Returns:
            List[Grid]: List of all grids

        Raises:
            RuntimeError: If there is an error fetching the grids
        """
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            return [Grid(**grid) for grid in response.json()]
        except Exception as e:
            logger.error(f"Error getting all grids: {str(e)}")
            raise RuntimeError("Failed to fetch all grids") from e

    def get_grid_by_id(self, grid_id: int) -> Optional[Grid]:
        """Get grid by ID.

        Args:
            grid_id (int): ID of the grid to fetch

        Returns:
            Optional[Grid]: Grid if found, None if not found

        Raises:
            RuntimeError: If there is an error fetching the grid
        """
        try:
            response = requests.get(f"{self.base_url}/{grid_id}")
            response.raise_for_status()
            return Grid(**response.json())
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            logger.error(f"Error getting grid by id {grid_id}: {str(e)}")
            raise RuntimeError(f"Failed to fetch grid by id: {grid_id}") from e
        except Exception as e:
            logger.error(f"Error getting grid by id {grid_id}: {str(e)}")
            raise RuntimeError(f"Failed to fetch grid by id: {grid_id}") from e

    def get_grids_in_environment(self, environment_id: int) -> List[Grid]:
        """Get all grids in an environment.

        Args:
            environment_id (int): ID of the environment

        Returns:
            List[Grid]: List of grids in the environment

        Raises:
            RuntimeError: If there is an error fetching the grids
        """
        try:
            response = requests.get(f"{self.base_url}/environment/{environment_id}")
            response.raise_for_status()
            return [Grid(**grid) for grid in response.json()]
        except Exception as e:
            logger.error(f"Error getting grids in environment {environment_id}: {str(e)}")
            raise RuntimeError(f"Failed to fetch grids in environment: {environment_id}") from e

    def get_grid_of_entity(self, entity_id: int) -> Optional[Grid]:
        """Get grid of an entity.

        Args:
            entity_id (int): ID of the entity

        Returns:
            Optional[Grid]: Grid if found, None if not found

        Raises:
            RuntimeError: If there is an error fetching the grid
        """
        try:
            response = requests.get(f"{self.base_url}/entity/{entity_id}")
            response.raise_for_status()
            return Grid(**response.json())
        except HTTPError as e:
            if e.response.status_code == 404:
                return None
            logger.error(f"Error getting grid for entity {entity_id}: {str(e)}")
            raise RuntimeError(f"Failed to fetch grid for entity: {entity_id}") from e
        except Exception as e:
            logger.error(f"Error getting grid for entity {entity_id}: {str(e)}")
            raise RuntimeError(f"Failed to fetch grid for entity: {entity_id}") from e