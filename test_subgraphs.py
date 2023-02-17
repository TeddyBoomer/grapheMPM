import pytest
import re
from grapheMPM import GrapheMPM

@pytest.fixture
def MPM_showlevel_data():
    p = {"A": "", "B": "", "C": "A", "D": "AB", "E":"B",
         "F":"DE", "G": "E", "H":"CF", "I":"FG", "J": "HI"}
    w = {"A": 7, "B": 3, "C": 4, "D": 2, "E": 8,
         "F": 6, "G": 5, "H": 7, "I": 5, "J": 3}
    G = GrapheMPM(pred=p, pond=w, show_level=True)
    G.earliestdate()
    G.makeGraphviz()
    return G

@pytest.fixture
def subgraph_attrs(MPM_showlevel_data):
    A = re.compile("subgraph cluster_[0-9]+ {\n(.*)$", flags=re.M)
    return A.search(MPM_showlevel_data.gv.source)

def test_subgraph_rank(subgraph_attrs):
    # on vérifie le contenu de la 1ere ligne du 1er cluster
    assert subgraph_attrs
    assert "rank=same" in subgraph_attrs.group(1)

def test_showlevel_on(MPM_showlevel_data):
    assert isinstance(MPM_showlevel_data.gv.render("test_sl_on"), str)

def test_showlevel_off(MPM_showlevel_data):
    MPM_showlevel_data.show_level=False
    MPM_showlevel_data.earliestdate()
    MPM_showlevel_data.makeGraphviz()
    assert isinstance(MPM_showlevel_data.gv.render("test_sl_off"), str)


# def test_subgraph_rank(MPM_showlevel_data):
#     # on vérifie le contenu de la 1ere ligne du 1er cluster
#     A = re.compile("subgraph cluster_\d+ \{\n(.*)$", flags=re.M)
#     a = A.search(MPM.showlevel_data.gv.source)
#     assert "rank=same" in a.group(1)
