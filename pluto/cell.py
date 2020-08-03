import ast
from .variable_access import VariableAccess


class Cell:
    def __init__(self, code=''):
        self.code = code
    

    @property
    def code(self):
        return self._code
    

    @code.setter
    def code(self, value):
        self._code = value
        for mode in ['eval', 'exec']:
            try:
                parsed = ast.parse(self.code, filename=self.filename, mode=mode)
            except SyntaxError as err:
                syntax_error = err
            else:
                self.mode = mode
                self.compiled = compile(self.code, filename=self.filename, mode=mode)
                self.variable_access = VariableAccess.from_ast(parsed)
                return
        
        self.mode = 'error'
        self.compiled = None
        self.variable_access = VariableAccess(reads=[], writes=[])
        self.output = syntax_error


    def run(self, workspace):
        if self.mode == 'error':
            return
        elif self.mode == 'eval':
            self.output = eval(self.compiled, workspace)
        elif self.mode == 'exec':
            exec(self.compiled, workspace)
            del workspace['__builtins__']
            self.output = VariableValues.from_workspace(workspace, self.variable_access.writes)
    

    @property
    def filename(self):
        return f'Pluto cell'
    

    def __repr__(self):
        return f'{self.code}'



class VariableValues(dict):
    @classmethod
    def from_workspace(cls, workspace, variable_names):
        return cls({var: workspace[var] for var in variable_names})


    def __repr__(self):
        return '\n'.join(f'{var} = {value}' for var, value in self.items())