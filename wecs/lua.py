"""
"""

from dataclasses import field

from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter

from lupa import LuaRuntime

@Component()
class LuaScript(Script):
    """
    """

    script_file: str = None
    script_globals: dict = {}

    script_runtime: object = field(default_factory=LuaRuntime)

    create_runtime: object = None
    configure_runtime: object = None

class LuaScriptSystem(System):
    """
    """

    entity_filters = {
        'script': and_filter(LuaScript)
    }

    def enter_filter_script(self, entity):
        """
        """

    def update(self, entities_by_filter):
        """
        """

    def exit_filter_script(self, entity):
        """
        """

    def _script_has_function(self, func_name):
        """
        """

    def _get_function_from_script(self, func_name):
        """
        """