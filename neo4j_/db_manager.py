import os
from typing import Any

from neo4j import GraphDatabase


class Neo4jDBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jDBManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.driver = None

    def open(self):
        if self.driver is None:
            self.driver = GraphDatabase.driver(os.getenv("NEO4J_URI"), auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")))

    def close(self):
        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def create_nodes(self, labels: list[str], properties: dict[str, Any]):
        if not labels or not properties:
            print(f'No labels or properties to create: {
                  labels} / {properties}')
            return

        self.open()

        flatten_labels = '&'.join(labels)
        flatten_properties = ','.join(
            f'{key}: ${key}' for key in properties.keys()
        )

        query = f'CREATE (:{flatten_labels} {{{flatten_properties}}})'
        print(f'trying query: {query} with {properties}')

        result = self.driver.execute_query(
            query,
            **properties,
            database_='neo4j'
        )

        print(f'Created {result.summary.counters.properties_set} properties '
              f'in {result.summary.result_available_after}ms.')

    def create_relationship(self):
        pass
