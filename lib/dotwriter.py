#!/usr/bin/env python
#-*- coding:utf-8 -*-

import hashlib

class DotWriter:
    """ Formats a collection of Link objects as a Graphviz (Dot)
    graph.  Mostly, this means creating a node for each URL with a
    name which Graphviz will accept, and declaring links between those
    nodes.
    """

    def __init__ (self):
        self.node_alias = {}

    def _safe_alias(self, url, silent=False):
        """ Translate URLs into unique strings guaranteed to be safe as
        node names in the Graphviz language.  Currently, that's based
        on the md5 digest, in hexadecimal.
        """

        if url in self.node_alias:
            return self.node_alias[url]
        else:
            m = hashlib.md5()
            m.update(url)
            name = "N"+m.hexdigest()
            self.node_alias[url]=name
            if not silent:
                print "\t%s [label=\"%s\"];" % (name, url)    

            return name

    def asDot(self, links):
        """ Render a collection of Link objects as a Dot graph
        """

        print "digraph Crawl {"
        print "\t edge [K=0.2, len=0.1];"
        for l in links:            
            print "\t" + self._safe_alias(l.src) + " -> " + self._safe_alias(l.dst) + ";"
        print  "}"