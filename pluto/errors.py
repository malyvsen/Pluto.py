class ReactivityError:
    '''Base class for all reactivity-related errors.'''



class MultipleReactivityErrors(ReactivityError):
    '''Multiple reactivity errors packaged into one, human-readable object.'''
    def __init__(self, errors):
        super().__init__()
        assert len(errors) > 0
        self.errors = errors
    

    @classmethod
    def pack(cls, errors):
        if len(errors) == 1:
            return errors[0]
        return cls(errors)
    

    def __repr__(self):
        return f'Multiple reactivity errors!\n' + '\n\n'.join(repr(error) for error in self.errors)



class NameConflictError(ReactivityError):
    '''An error which arises when multiple cells assign to the same variable.'''
    def __init__(self, errored_variable):
        super().__init__()
        self.errored_variable = errored_variable
    

    def __repr__(self):
        return f'The variable `{self.errored_variable}` is assigned to in multiple cells.'
    

    def __eq__(self, other):
        return self.errored_variable == other.errored_variable



class CycleError(ReactivityError):
    '''An error which arises when cells form a cycle.'''
    def __init__(self, cells_in_cycle):
        super().__init__()
        self.cells_in_cycle = cells_in_cycle
    

    def __repr__(self):
        return 'These cells form a cycle:\n' + '\n\n'.join(repr(cell) for cell in self.cells_in_cycle)
    

    def __eq__(self, other):
        return frozenset(self.cells_in_cycle) == frozenset(other.cells_in_cycle)
