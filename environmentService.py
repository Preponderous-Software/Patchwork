
# Copyright (c) 2024 Preponderous Software
# MIT License

import requests
from environment import Environment

class EnvironmentService:
    def __init__(self, base_url):
        self.base_url = f"{base_url}/api/v1/environments"

    def get_all_environments(self) -> list[Environment]:
        response = requests.get(f"{self.base_url}")
        response.raise_for_status()
        return [Environment(**env) for env in response.json()]

    def get_environment_by_id(self, environment_id: int) -> Environment:
        response = requests.get(f"{self.base_url}/{environment_id}")
        response.raise_for_status()
        return Environment(**response.json())

    def get_environment_by_name(self, name: str) -> Environment:
        response = requests.get(f"{self.base_url}/name/{name}")
        response.raise_for_status()
        return Environment(**response.json())

    def get_environment_of_entity(self, entity_id: int) -> Environment:
        response = requests.get(f"{self.base_url}/entity/{entity_id}")
        response.raise_for_status()
        return Environment(**response.json())

    def create_environment(self, name: str, num_grids: int, grid_size: int) -> Environment:
        response = requests.post(f"{self.base_url}/{name}/{num_grids}/{grid_size}")
        response.raise_for_status()
        return Environment(**response.json())

    def delete_environment(self, environment_id: int) -> bool:
        response = requests.delete(f"{self.base_url}/{environment_id}")
        response.raise_for_status()
        return response.status_code == 200

    def update_environment_name(self, environment_id: int, name: str) -> bool:
        response = requests.patch(f"{self.base_url}/{environment_id}/name/{name}")
        response.raise_for_status()
        return response.status_code == 200