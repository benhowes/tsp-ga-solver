from math import sqrt
from unittest.mock import patch, mock_open
from io import StringIO

import pytest

from solver.map_utils import Point, Route, load_map

class TestPoint():

    def test_invalid_coords(self):
        with pytest.raises(ValueError):
            Point("name", 12, "not a number")

    def test_valid_point(self):
        p = Point("name", 12.2, 3.14)
        assert p.id == "name"
        assert p.x == 12.2
        assert p.y == 3.14

    @pytest.mark.parametrize("a,b,dist", (
        ((0,1), (0,0), 1),
        ((1,1), (0,0), sqrt(2)),
        ((0,1), (0,1), 0),
        ((0,10), (0,0), 10),
    ))
    def test_distance_method(self, a, b, dist):
        point_a = Point("a", *a)
        point_b = Point("b", *b)

        assert point_a.distance(point_b) == pytest.approx(dist)

    def test_distance_invalid_other(self):
        point = Point("a", 1, 2)
        with pytest.raises(TypeError):
            point.distance("Timbuktu")

    @pytest.mark.parametrize("a,b,eq", (
        (("a",0,1), ("a",0,0), False),
        (("a",1,1), ("a",0,0), False),
        (("b",0,1), ("a",0,1), False),
        (("a",0,10), ("b",0,0), False),
        (("a",0,0), ("a",0,0), True),
        (("b",10,10), ("b",10,10), True),
    ))
    def test_eq(self, a, b, eq):
        point_a = Point(*a)
        point_b = Point(*b)
        assert (point_a == point_b) == eq

class TestRoute():

    def test_add_invalid(self):
        p = "Bart Simpson"
        r = Route()
        with pytest.raises(TypeError):
            r.add(p)

    def test_add_valid_point(self):
        p = Point("a", 1, 2)
        r = Route()
        r.add(p)
        assert len(r) == 1

    def test_add_duplicate_point(self):
        p = Point("a", 1, 2)
        r = Route()
        r.add(p)
        r.add(p)
        assert len(r) == 1

    def test_pop_index(self):
        p = Point("a", 1, 2)
        p2 = Point("b", 1, 2)
        r = Route()
        r.add(p, p2)

        assert len(r) == 2
        r.pop(0)
        assert len(r) == 1
        assert r[0].id == "b"

    def test_distance_no_points(self):
        r = Route()
        with pytest.raises(ValueError):
            r.total_distance

    def test_distance_one_point(self):
        r = Route()
        p = Point("a", 1, 2)
        r.add(p)
        with pytest.raises(ValueError):
            r.total_distance

    def test_total_distance(self):
        r = Route()
        p = Point("a", 0, 0)
        p2 = Point("b", 0, 2)
        r.add(p, p2)
        assert r.total_distance == pytest.approx(2)

        p3 = Point("c", 2, 2)
        r.add(p3)
        assert r.total_distance == pytest.approx(4)

    def test_shuffle(self):
        r = Route()
        p = Point("a", 0, 0)
        p2 = Point("b", 0, 2)
        p3 = Point("c", 2, 2)
        r.add(p, p2, p3)
        r2 = r.shuffle()

        assert r is not r2
        assert len(r) == len(r2)

    def test_repr(self):
        """Asserts that the id's of the points all appear"""
        p = Point("aaa", 1, 2)
        p2 = Point("bbb", 3, 4)
        p3 = Point("ccc", 5, 6)
        r = Route()
        r.add(p, p2, p3)

        rep = r.__repr__()
        assert p.id in rep
        assert p2.id in rep
        assert p3.id in rep

class TestLoadMap():

    def get_f_open(self, input_file):
        """
            This implements the __iter__ method which the normal mock
            does not implement.

            Sourced from: https://github.com/gsauthof/utility/blob/6489c7215dac341be4e40e5348e64d69461766dd/user-installed.py#L176-L179
        """
        f_open = mock_open(read_data=input_file)
        f_open.return_value.__iter__ = lambda self: iter(self.readline, "")
        return f_open

    def test_valid_map(self):
        """
        Asserts that the test file `input_file` decodes to what we expect
        """
        input_file = "index,x_coord,y_coord\n1,0,0\n2,0,1\n"

        p = Point("1", 0, 0)
        p2 = Point("2", 0, 1)
        expected_route = Route()
        expected_route.add(p, p2)

        with patch("solver.map_utils.open", self.get_f_open(input_file),
                        create=True) as file:
            route = load_map("mock_file")

        # Note - this does rely on hashing/eq working on points
        assert route == expected_route

    def test_invalid_map(self):
        """
        Asserts that the test file `input_file` decodes to what we expect
        """
        input_file = "index,x_coord,y_coord\n1,cheese,0\n2,0,1\n"

        with patch("solver.map_utils.open", self.get_f_open(input_file),
                        create=True) as file:
            with pytest.raises(ValueError):
                route = load_map("mock_file")

