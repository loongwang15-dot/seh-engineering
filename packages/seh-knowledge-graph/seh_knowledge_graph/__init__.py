from dataclasses import dataclass, field


@dataclass
class KnowledgeEntity:
    id: str
    type: str
    metadata: dict = field(default_factory=dict)


@dataclass
class Relation:
    from_id: str
    to_id: str
    relation: str


class KnowledgeGraph:
    def __init__(self) -> None:
        self.entities: dict[str, KnowledgeEntity] = {}
        self.relations: list[Relation] = []

    def add_entity(self, entity: KnowledgeEntity) -> None:
        self.entities[entity.id] = entity

    def add_relation(self, relation: Relation) -> None:
        self.relations.append(relation)
