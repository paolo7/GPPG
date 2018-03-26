import rdflib
from rdflib import URIRef, BNode, Literal
import logging
logging.basicConfig(level=logging.ERROR)

URILAMBDA = URIRef("http://example.org/LAMBDA")
URILAMBDAl = "<"+URILAMBDA+">"

printquery = False

def GPPG(querypattern, graphpattern):
    g = createSandboxGraph(graphpattern)
    q = createExpandedQuery(querypattern)
    qres = g.query(q)
    return delta(qres, querypattern)


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
            if isinstance(value, Literal) and var in noliteralvariables:
                valid = False
            mapping["v"+str(var.num)] = value
        if valid:
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

# Test function below:

def test(querypattern, graphpattern, expected):
    print("\nQUERY PATTERN:")
    for triplepattern in querypattern:
        print("  "+str(triplepattern["s"])+" "+str(triplepattern["p"])+" "+str(triplepattern["o"]))
    print("GRAPH PATTERN:")
    for triplepattern in graphpattern:
        print("  " + str(triplepattern["s"]) + " " + str(triplepattern["p"]) + " " + str(triplepattern["o"]))
    if printquery : print("QUERY:\n"+createExpandedQuery(querypattern))
    mappings = GPPG(querypattern,graphpattern)
    print("MAPPINGS:")
    if len(expected) > 0:
        for mapping in mappings:
            print("  mapping:")
            for var in mapping:
              print("    "+var+" --> "+mapping[var])
    else:
        print("  NONE")
    print("Expected MAPPINGS:")
    if len(expected) > 0:
        for mapping in expected:
            print("  mapping:")
            for var in mapping:
                print("    " + var + " --> " + mapping[var])
    else:
        print("  NONE")

    allEqual = True
    if len(mappings) != len(expected):
        allEqual = False
    for mapping in mappings:
        oneEqual = False
        for emapping in expected:
            equal = True
            if not len(mapping) == len(emapping):
                equal = False
            for var in mapping:
                if (not var in emapping) or mapping[var] != emapping[var]:
                    equal = False
            if equal: oneEqual = True
        if not oneEqual:
            allEqual = False
    print("TEST "+str(allEqual))
    return allEqual

# Test script below:
# If a pattern shouldn't match, the 'expected' set should be empty
# If a pattern without variables matches, the 'expected' set should have a single empty dictionary inside
# If a pattern with variable matches, the 'expected' set should contain all the expected mappings
# Each expected mapping should be represented as a dictionary with variables as keys

allTestsPassed = True

allTestsPassed = allTestsPassed and test(
        {
            hashabledict({"s":variable(1),"p":newURI("b"),"o":Literal('text')})
        } ,
        {
            hashabledict({"s":newURI("a"),"p":variable(1),"o":Literal('text')}),
            hashabledict({"s":newURI("a"),"p":newURI("b"),"o":Literal('text')})
        } ,
        {
            hashabledict({"v1": newURI("a")})
        }
    )

allTestsPassed = allTestsPassed and test(
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": newURI("c")})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": newURI("c")})
    },
    {
        hashabledict({"v1": URILAMBDA})
    }
)

allTestsPassed = allTestsPassed and test(
    {
        hashabledict({"s": variable(1), "p": newURI("c"), "o": newURI("c")})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": newURI("c")})
    },
    {

    }
)

allTestsPassed = allTestsPassed and test(
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": Literal('text')})
    },
    {

    }
)

allTestsPassed = allTestsPassed and test(
    {
        hashabledict({"s": variable(2), "p": newURI("b"), "o": variable(2)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": newURI("d")})
    },
    {
        hashabledict({"v2": newURI("d")})
    }
)

allTestsPassed = allTestsPassed and test(
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal('text')})
    },
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal('text')})
    },
    {
        hashabledict({})
    }
)

allTestsPassed = allTestsPassed and test(
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal('text')})
    },
    {
        hashabledict({"s": newURI("b"), "p": newURI("b"), "o": Literal('text')})
    },
    {
        hashabledict({})
    }
)

allTestsPassed = allTestsPassed and test(
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal('text')})
    },
    {
        hashabledict({"s": newURI("b"), "p": newURI("b"), "o": Literal('text')})
    },
    {
        hashabledict({})
    }
)

print("\nAll tests passed? "+str(allTestsPassed))