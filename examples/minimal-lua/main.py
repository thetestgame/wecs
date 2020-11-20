from wecs.core import World, Component, System, and_filter, UID, NoSuchUID
from wecs import lua

@Component()
class Counter:
    value: int


@Component()
class Printer:
    printee: UID


class Print(System):
    entity_filters = {'prints': and_filter([Printer])}

    def update(self, entities_by_filter):
        for entity in entities_by_filter['prints']:
            reference = entity.get_component(Printer).printee
            # Maybe the reference doesn't point anywhere anymore?
            if reference is None:
                print("Empty reference.")
                return
            # Since those references are UIDs of entitites, not entitites
            # themselves, we'll need to resolve them. It may happen that a
            # referenced entity has been destroyed, so we'll need to handle that
            # case here as well.
            try:
                printed_entity = self.world.get_entity(reference)
            except NoSuchUID:
                print("Dangling reference.")
                return
            # But is it even counter anymore?
            if not printed_entity.has_component(Counter):
                print("Referenced entity is not a counter.")
                return
            # Okay, so the entity's printee is an existing entity that is a
            # Counter. We can actually print its value!
            print(printed_entity.get_component(Counter).value)


# Create our world and add our systems
world = World()
world.add_system(lua.LuaScriptSystem(), 0)
world.add_system(Print(), 1)
world.update()

entity = world.create_entity()
counter = Counter(value=0)
entity.add_component(counter)
entity.add_component(Printer(printee=entity._uid))
entity.add_component(lua.LuaScript(
    script_file='counter.lua',
    script_storage={'CounterComponent': counter}
))

# ...and see whether it works.
world.update()
# ...and if we make the entity a non-counter?
entity.remove_component(Counter)
world.update()

# ...and if there is no other entity?
world.destroy_entity(entity)
world.update()