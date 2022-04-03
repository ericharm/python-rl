from functools import reduce

class CollisionController:

  def __init__(self, level):
    self.level = level

  def handle_collisions(self, entities):
    pairs = self.get_colliding_pairs(entities)
    for pair in pairs:
      self.dispatch_collision_actions(pair)

  def get_colliding_pairs(self, entities):
    pairs = reduce(lambda accum, entity: self.accumulate_colliding_entities(accum, entity, entities), entities, [])
    return map(lambda pair: CollidingPair(pair[0], pair[1]), pairs)

  def accumulate_colliding_entities(self, accum, entity, entities):
    for collider in entity.colliding_entities(entities):
      if [collider, entity] not in accum:
        accum.append([entity, collider])
    return accum

  def dispatch_collision_actions(self, pair):
    if pair.has_control_categories('zap', 'shootable'):
      for entity in pair:
        entity.pluck(self.level)


class CollidingPair (list):

  def __init__(self, entity_a, entity_b):
    list.__init__(self)
    self.extend([entity_a, entity_b])
    self.first = entity_a
    self.second = entity_b

  def has_control_categories(self, category_a, category_b):
    return ((category_a in self.first.categories and category_b in self.second.categories)
    or (category_b in self.first.categories and category_a in self.second.categories))

  def get_collider_by_category(self, category):
    return reduce(lambda a, b: a if category in a.categories else b, self)
