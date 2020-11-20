"""
"""

from dataclasses import field

from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter

from lupa import LuaRuntime

@Component()
class LuaScript:
    """
    """

    script_file: str = None
    script_globals: dict = field(default_factory=dict)
    script_storage: dict = field(default_factory=dict)

    script_runtime: object = None
    script_object: object = None

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

        script = entity[LuaScript]
        create_func = script.create_runtime if script.create_runtime else self._default_create_runtime
        assert callable(create_func), 'LuaScript create_runtime is not a valid callable'

        script.script_runtime = create_func(entity)
        if script.configure_runtime and callable(script.configure_runtime):
            script.configure_runtime(script.script_runtime)

        assert script.script_file != None, 'No script file is assigned to LuaScript'
        with open(script.script_file, 'r') as f:
            script_contents = f.read()
        script_func = script.script_runtime.eval(script_contents)
        script.script_object = script_func(script)

        script_globals = script.script_runtime.globals()
        for key, val in script.script_globals.items():
            script_globals[key] = val

    def update(self, entities_by_filter):
        """
        """

        for entity in entities_by_filter['script']:
            has_update = self._script_has_function(entity, 'update')
            if not has_update:
                continue

            self._call_function_from_script(entity, 'update', entity)

    def exit_filter_script(self, entity):
        """
        """

    def _script_has_function(self, entity, func_name):
        """
        """

        script = entity[LuaScript]
        try:
            return script.script_object[func_name] != None
        except Exception:
            return False
 
    def _call_function_from_script(self, entity, func_name, *args):
        """
        """

        script = entity[LuaScript]
        func = script.script_object[func_name]
        return func(script.script_object, *args)

    def _default_create_runtime(self, entity):
        """
        """

        runtime = LuaRuntime(unpack_returned_tuples=True)
        return runtime