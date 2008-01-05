# Copyright(c) 2006, James Le Cuirot <chewi@aura-online.co.uk>
# Copyright(c) 2004, Karl Trygve Kalleberg <karltk@gentoo.org>
# Copyright(c) 2004, Gentoo Foundation
#
# Licensed under the GNU General Public License, v2
#
# $Header: $

import sys

class ParseError:
    def __init__(self, error):
        self.error = error

class NodeIter:
    def __init__(self, node):
        self._node = node
        self._index = 0
    def next(self):
        self._index += 1
        if self._index >= len(self._node._kids):
            raise StopIteration
        return self._node._kids[self._index]
        
class Node:
    def __init__(self, name = None, value = None):
        self.name = name
        self.value = value
        self._kids = []
    
    def __iter__(self):
        return NodeIter(self)
    
    def add_kid(self, kid):
        for x in self._kids:
            if x.name == kid.name:
                return
            
        self._kids.append(kid)
    
    def _dump_kids(self, indent, ous):
        for x in self._kids:
            x.dump(indent + 1)
    
    """
    Dump self as text to stream.
    """
    def dump(self, indent = 0, ous = sys.stdout):
        if self.name:
            ous.write((" " * indent) + self.name + " = " + self.value + "\n")
        
        self._dump_kids(indent, ous)
    
    """
    Output self as text to stream using the given format.
    """
    def output(self, before, between, after, wrap = None, indent = "", ous = sys.stdout):       
        if self.name:
            outval = self.value
        
            if wrap != None:
                outval = outval.replace(wrap, wrap + "\n" + indent)
            
            ous.write(before + self.name + between + outval + after + "\n")
        
        for x in self._kids:
            x.output(before, between, after, wrap, indent, ous)

    """
    Returns a lists of all the node names.
    """
    def node_names(self):
        names = []
        
        if self.name:
            names.append(self.name)
        
        for x in self._kids:
            names.extend(x.node_names())
        
        return names

    """
    Find a given node name in a tree.
    
    @param tree - the tree to search in
    @param nodename - the name of the node to search for
    
    @return reference to the found node, if any
    """
    def find_node(self, nodename):
        if self.name == nodename:
            return self

        else:
            for x in self._kids:
                y = x.find_node(nodename)
                
                if y != None:
                    return y
        
        return None

# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 nowrap:
