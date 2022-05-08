from functools import reduce
from src.entity import Entity


class CollidingPair(list[Entity]):
    def __init__(self, entity_a: Entity, entity_b: Entity):
        list.__init__(self)
        self.extend([entity_a, entity_b])
        self.first = entity_a
        self.second = entity_b

    def has_control_categories(self, category_a: str, category_b: str) -> bool:
        return (
            category_a in self.first.categories and category_b in self.second.categories
        ) or (
            category_b in self.first.categories and category_a in self.second.categories
        )

    def get_collider_by_category(self, category: str) -> Entity:
        return reduce(lambda a, b: a if category in a.categories else b, self)


class CollisionDetector:
    def get_colliding_pairs(self, entities: list[Entity]) -> list[CollidingPair]:
        pairs: list[CollidingPair] = reduce(
            lambda accum, entity: self.accumulate_colliding_entities(
                accum, entity, entities
            ),
            entities,
            [],
        )
        return list(map(lambda pair: CollidingPair(pair[0], pair[1]), pairs))

    def accumulate_colliding_entities(
            self, accum: list[CollidingPair], entity: Entity, entities: list[Entity]
    ) -> list[CollidingPair]:
        for collider in entity.colliding_entities(entities):
            if [collider, entity] not in accum:
                accum.append(CollidingPair(entity, collider))
        return accum
