from pluto.cell import Cell
from pluto.variable_access import VariableAccess



class TestCell:
    def test_variable_access(self):
        cell = Cell(code='x = y')
        assert cell.variable_access == VariableAccess(reads=['y'], writes=['x'])


    def test_expression(self):
        cell = Cell(code='[11 + 12, 3]')
        cell.run({})
        assert cell.output == [23, 3]


    def test_assignments(self):
        cell = Cell(code='x = 11\ny = 12')
        cell.run({})
        assert cell.output['x'] == 11
        assert cell.output['y'] == 12


    def test_dependent_internal(self):
        cell = Cell(code='x = 11\ny = x + 1')
        cell.run({})
        assert cell.output['x'] == 11
        assert cell.output['y'] == 12


    def test_dependent_external(self):
        cell = Cell(code='x = 11\ny = x + z')
        cell.run({'z': 7})
        assert cell.output['x'] == 11
        assert cell.output['y'] == 18
        assert 'z' not in cell.output


    def test_workspace_change(self):
        workspace = {'z': 7}
        cell = Cell(code='x = 11\ny = x + z')
        cell.run(workspace=workspace)
        assert cell.output['x'] == 11
        assert cell.output['y'] == 18
        assert 'z' not in cell.output
        assert set(workspace.keys()) == {'x', 'y', 'z'}
        assert workspace['x'] == 11
        assert workspace['y'] == 18
        assert workspace['z'] == 7


    def test_syntax_error(self):
        cell = Cell(code='x = +')
        cell.run({})
        assert isinstance(cell.output, SyntaxError)


    def test_depend(self):
        a = Cell(code='a_var = b_var - 11')
        b = Cell(code='b_var = 3')
        assert a.depends_on(b)

        a.code = 'a_var = c_var + 12'
        assert not a.depends_on(b)


    def test_depend_self(self):
        a = Cell(code='x = 11\nx = x + 1')
        assert not a.depends_on(a)
    

    def test_error_run(self):
        workspace = {}
        cell = Cell(code='x = 1 / 0')
        cell.run(workspace=workspace)
        assert isinstance(cell.output, ArithmeticError)
        assert workspace == {}