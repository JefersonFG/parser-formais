# -*- coding: utf-8 -*-

from nose.tools import assert_equals
from src.importer import Importer


def test_import_from_file_1():
    importer = Importer()

    grammar = importer.import_from_file("test/test_importer_files/example_grammar_1.txt")

    assert_equals(grammar.__str__(), "G = ({S,Z,B,X,Y,A}, {a,b,u,v}, {S -> XYZ | A -> a | B -> b | "
                                     "X -> AXA | X -> BXB | X -> Z | X -> V | Y -> AYB | Y -> BYA | "
                                     "Y -> Z | Y -> V | Z -> Zu | Z -> Zv | Z -> V}, S)")


def test_import_from_file_2():
    importer = Importer()

    grammar = importer.import_from_file("test/test_importer_files/example_grammar_2.txt")

    assert_equals(grammar.__str__(), "G = ({N,VB,NP,DT,VP,S,PP,P}, "
                                     "{runs,barks,eats,chases,park,dog,cat,meat,the,a,in,with,at}, "
                                     "{S -> NPVP | S -> SS | NP -> dog | NP -> cat | NP -> meat | "
                                     "NP -> park | NP -> DTN | NP -> NPPP | N -> dog | N -> cat | "
                                     "N -> meat | N -> park | VP -> VBNP | VP -> VPPP | "
                                     "VP -> runs | VP -> barks | VP -> eats | VP -> chases | "
                                     "VB -> runs | VB -> barks | VB -> eats | VB -> chases | "
                                     "DT -> a | DT -> the | PP -> PNP | P -> in | P -> with | "
                                     "P -> at}, S)")
