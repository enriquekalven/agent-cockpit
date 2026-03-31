import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider

code = """
import asyncio
def my_func():
    pass
"""

class DecoratorTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (PositionProvider,)
    def __init__(self, target_line, decorator_str):
        self.target_line = target_line
        self.decorator_str = decorator_str
        self.found = False

    def _apply_decorator(self, original_node, updated_node):
        if getattr(self, 'found', False):
            return updated_node
        pos = self.get_metadata(PositionProvider, original_node)
        if pos and pos.start.line == self.target_line:
            self.found = True
            dummy = cst.parse_module(f"{self.decorator_str}\\ndef dummy_f(): pass")
            new_dec = dummy.body[0].decorators[0]
            if any(d.decorator == new_dec.decorator for d in updated_node.decorators):
                return updated_node # avoid double
            new_decorators = list(updated_node.decorators)
            new_decorators.insert(0, new_dec)
            return updated_node.with_changes(decorators=new_decorators)
        return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        return self._apply_decorator(original_node, updated_node)

    def leave_AsyncFunctionDef(self, original_node, updated_node):
        return self._apply_decorator(original_node, updated_node)

module = cst.parse_module(code)
wrapper = MetadataWrapper(module)
trans = DecoratorTransformer(3, "@cockpit_reflection")
res = wrapper.visit(trans)
print(res.code)
