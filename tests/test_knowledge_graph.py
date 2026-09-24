from seh_knowledge_graph import KnowledgeEntity, KnowledgeGraph, Relation


def test_graph():
    graph = KnowledgeGraph()
    graph.add_entity(KnowledgeEntity("skill-1", "Skill"))
    graph.add_relation(Relation("skill-1", "rule-1", "uses"))
    assert "skill-1" in graph.entities
    assert len(graph.relations) == 1
