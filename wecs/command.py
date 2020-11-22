"""
"""

from dataclasses import field

from wecs.core import Component, System, UID, NoSuchUID, and_filter
from wecs.mechanics import clock

@Component()
class Command:
    """
    """

    command: str = None
    arguments: dict = field(default_factory=dict)


@Component()
class DelayedCommand(Command):
    """
    """

    delay: float = 0
    start_time: float = 0


class CommandHandler:
    """
    """

    def __init__(self):
        assert hasattr(self, 'entity_filters'), 'CommandHandler can only be used with WECS systems'
        self.entity_filters['command'] = and_filter(Command)

    def update(self, entities_by_filter):
        """
        """

        for entity in entities_by_filter['command']:
            command = entity[Command]
            command_name = entity.command

            if self._has_command(command_name):
                continue

            command_handler = self._get_command_handler(command_name)
            command_handler(**command.arguments)

    def _get_command_handler_name(self, command):
        """
        """

        return 'accept_%s' % command

    def _has_command(self, command):
        """
        """

        return hasattr(self, self._get_command_handler_name(command))
    
    def _get_command_handler(self, command):
        """
        """

        if not self._has_command(command):
            return None

        return getattr(self, self._get_command_handler_name(command))

class DelayedCommandManager(System):
    """
    """

    entity_filters = {
        'delayed': and_filter(DelayedCommand),
        'clock': and_filter(clock.Clock)
    }

    def update(self, entities_by_filter):
        """
        """

class CommandDisposal(Syste):
    """
    """

    entity_filters = {
        'command': and_filter(Command)
    }

    def update(self, entities_by_filter):
        """
        """

        for entity in entities_by_filter['command']:
            entity.remove_component(Command)

            if len(entity.get_components()) == 0:
                entity.world.destroy_entity(entity)