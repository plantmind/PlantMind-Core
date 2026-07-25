"""
PlantMind Knowledge Graph Service
Version: 1.0
"""

from typing import Dict, List


class KnowledgeGraphService:
    """
    Manages industrial knowledge relationships.
    """

    def __init__(self):
        self.nodes = {}
        self.relationships = []

    def add_equipment(self, tag: str, equipment_type: str):
        self.nodes[tag] = {
            "tag": tag,
            "type": equipment_type
        }

    def add_relationship(self, source: str, target: str, relation: str):
        self.relationships.append({
            "source": source,
            "target": target,
            "relation": relation
        })

    def get_equipment(self, tag: str):
        return self.nodes.get(tag)

    def list_relationships(self):
        return self.relationships
