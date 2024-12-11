import os

from langchain_neo4j import Neo4jGraph

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
    enhanced_schema=True,
)
graph.refresh_schema()


def get_neo4j_schema():
    return graph.schema


def query_neo4j(query: str):
    return graph.query(query)


def refresh_neo4j_schema():
    graph.refresh_schema()
