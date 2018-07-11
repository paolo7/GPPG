import rdflib
from rdflib import URIRef, BNode, Literal
import logging
logging.basicConfig(level=logging.ERROR)

URILAMBDA = URIRef("http://example.org/LAMBDA")
URILAMBDAl = "<"+URILAMBDA+">"

printquery = False

# querypattern must be a basic conjunctive graph pattern (a set of triple patterns)
# graphpattern must be a variable-independent basic conjunctive graph pattern (a set of triple
# patterns such that no triple contains more than once occurrence of the same variable)
def GPPG(querypattern, graphpattern):
    # verify that 'graphpattern' is variable-independent
    if not isVIGP(graphpattern):
        raise ValueError('ERROR. Graph patter `graphpattern` is not variable independent. One triple has a repeated variable')
    # compute GPPG, as the 'delta' filtering of the results of the evaluation
    # of the expansion of 'querypattern' over the sandbox graph derived by 'graphpattern'
    g = createSandboxGraph(graphpattern)
    q = createExpandedQuery(querypattern)
    return delta(g.query(q), querypattern)


def delta(qres, querypattern):
    variables = set()
    noliteralvariables = set()
    # discover all variables in the query pattern, and all variables which cannot have literal values
    for triplepattern in querypattern:
        if isinstance(triplepattern["s"], variable):
            variables.add(triplepattern["s"])
            noliteralvariables.add(triplepattern["s"])
        if isinstance(triplepattern["p"], variable):
            variables.add(triplepattern["p"])
            noliteralvariables.add(triplepattern["s"])
        if isinstance(triplepattern["o"], variable):
            variables.add(triplepattern["o"])
    mappings = []
    for row in qres:
        mapping = {}
        valid = True
        for var in variables:
            value = row["v"+str(var.num)]
            if value == None:
                valid = False
            if isinstance(value, Literal) and var in noliteralvariables:
                valid = False
            mapping["v"+str(var.num)] = value
        if valid and not mapping in mappings:
            mappings.append(mapping)
    return mappings

def createSandboxGraph(graphpattern):
    g = rdflib.Graph()
    for triplepattern in graphpattern:
        g.add( (triplepattern["s"] if not isinstance(triplepattern["s"], variable) else URILAMBDA,
                triplepattern["p"] if not isinstance(triplepattern["p"], variable) else URILAMBDA,
                triplepattern["o"] if not isinstance(triplepattern["o"], variable) else URILAMBDA ) );
    return g

def toSPARQLstring(node):
    if isinstance(node, variable):
        return "?v"+str(node.num)
    if isinstance(node, URIRef):
        return "<"+node+">"
    if isinstance(node, Literal):
        return "\"\"\"" + node + "\"\"\""

def createExpandedQuery(querypattern):
    query = """SELECT * WHERE {\n"""
    if not containsVariables(querypattern):
        query = """ASK {\n"""
    for triplepattern in querypattern:
        subject = toSPARQLstring(triplepattern["s"])
        predicate = toSPARQLstring(triplepattern["p"])
        object = toSPARQLstring(triplepattern["o"])
        query = query+"""  {\n"""
        query = query + """    { """ + subject + """ """ + predicate + """ """ + object + """ } UNION\n"""
        query = query + """    { """ + URILAMBDAl + """ """ + predicate + """ """ + object + """ } UNION\n"""
        query = query + """    { """ + subject + """ """ + URILAMBDAl + """ """ + object + """ } UNION\n"""
        query = query + """    { """ + subject + """ """ + predicate + """ """ + URILAMBDAl + """ } UNION\n"""
        query = query + """    { """ + URILAMBDAl + """ """ + URILAMBDAl + """ """ + object + """ } UNION\n"""
        query = query + """    { """ + URILAMBDAl + """ """ + predicate + """ """ + URILAMBDAl + """ } UNION\n"""
        query = query + """    { """ + subject + """ """ + URILAMBDAl + """ """ + URILAMBDAl + """ } UNION\n"""
        query = query + """    { """ + URILAMBDAl + """ """ + URILAMBDAl + """ """ + URILAMBDAl + """ }\n"""
        query = query + """  }\n"""
    return query+"}"

def containsVariables(querypattern):
    for triplepattern in querypattern:
        if isinstance(triplepattern["s"], variable) or isinstance(triplepattern["p"], variable) or isinstance(triplepattern["o"], variable):
            return True
    return False

def newURI(name):
    return URIRef("http://example.org/"+name)

class hashabledict(dict):
  def __key(self):
    return tuple((k,self[k]) for k in sorted(self))
  def __hash__(self):
    return hash(self.__key())
  def __eq__(self, other):
    return self.__key() == other.__key()

class variable():
    def __init__(self, num):
        self.num = num
    def __repr__(self):
        return "?v"+str(self.num)

def isVIGP(graphpattern):
    for triplepattern in graphpattern:
        variables = set()
        for element in triplepattern:
            if isinstance(triplepattern[str(element)], variable):
                if triplepattern[str(element)].num in variables:
                    return False
                variables.add(triplepattern[str(element)].num)
    return True