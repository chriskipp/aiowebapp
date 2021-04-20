#!/usr/bin/env python3

# Install graphviz using pip3 (on archlinux):
#  $ sudo pip3 install graphviz

import graphviz as gv

def g2svg(g=None):
    g1 = gv.Graph(format="svg") # "svg" or "dot"
    g1.node('A')
    g1.node('B')
    g1.node('C')
    g1.edge('A', 'C')
    g1.edge('B', 'C')
    return g1.render()

svg = g2svg()
print(svg)
