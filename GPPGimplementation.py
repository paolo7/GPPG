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

# Algorithm finished, test script below:
# Test function below:

tests = 0
testsfailed = 0

def test(querypattern, graphpattern, expected):
    global tests, testsfailed
    tests += 1
    print("\nTest n. " + str(tests))
    print("QUERY PATTERN:")
    for triplepattern in querypattern:
        print("  "+str(triplepattern["s"])+" "+str(triplepattern["p"])+" "+str(triplepattern["o"]))
    print("GRAPH PATTERN:")
    for triplepattern in graphpattern:
        print("  " + str(triplepattern["s"]) + " " + str(triplepattern["p"]) + " " + str(triplepattern["o"]))
    if printquery : print("QUERY:\n"+createExpandedQuery(querypattern))
    mappings = GPPG(querypattern,graphpattern)
    print("MAPPINGS Found:")
    if len(mappings) > 0:
        for mapping in mappings:
            print("    mapping:")
            for var in mapping:
              print("    "+var+" --> "+mapping[var])
    else:
        print("  NONE")
    print("MAPPINGS Expected:")
    if len(expected) > 0:
        for mapping in expected:
            print("    mapping:")
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
    print("TEST pass: "+str(allEqual))
    if not allEqual:
        testsfailed += 1
    return allEqual

# Test cases below:
# If a pattern shouldn't match, the 'expected' set should be empty
# If a pattern without variables matches, the 'expected' set should have a single empty dictionary inside
# If a pattern with variable matches, the 'expected' set should contain all the expected mappings
# Each expected mapping should be represented as a dictionary with variables as keys

allTestsPassed = True

allTestsPassed = allTestsPassed & test(
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

allTestsPassed = allTestsPassed & test(
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

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("c"), "o": newURI("c")})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": newURI("c")})
    },
    {

    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": Literal('text')})
    },
    {

    }
)

allTestsPassed = allTestsPassed & test(
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

allTestsPassed = allTestsPassed & test(
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

allTestsPassed = allTestsPassed & test(
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

allTestsPassed = allTestsPassed & test(
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

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal('text')})
    },
    {

    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": Literal('text')})
    },
    {

    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"v1": newURI("a")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(2)})
    },
    {
        hashabledict({"v1": URILAMBDA})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(2), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(2)})
    },
    {
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(2), "p": newURI("b"), "o": variable(1)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(2)})
    },
    {
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA})
    }
)

try:
    allTestsPassed = allTestsPassed & test(
        {
            hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal('text')})
        },
        {
            hashabledict({"s": variable(1), "p": newURI("b"), "o": variable(1)})
        },
        {
            hashabledict({})
        }
    )
    allTestsPassed = False
except ValueError as e:
    print('\nSuccessfully detected a graph pattern which is not a VIGP')



allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(2), "p": newURI("b"), "o": variable(1)}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": variable(2)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": Literal("k")}),
        hashabledict({"s": variable(2), "p": newURI("b"), "o": Literal("l")}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": Literal("k")})
    },
    {

    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": newURI("c")})
    },
    {
        hashabledict({"s": variable(1), "p": variable(2), "o": variable(3)})
    },
    {
        hashabledict()
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": variable(1), "o": variable(1)})
    },
    {
        hashabledict({"s": variable(1), "p": variable(2), "o": newURI("c")})
    },
    {
        hashabledict({"v1": newURI("c")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": variable(1), "o": variable(1)})
    },
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": newURI("c")})
    },
    {

    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": variable(2), "o": variable(3)})
    },
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": newURI("c")})
    },
    {
        hashabledict({"v1": newURI("a"), "v2": newURI("b"), "v3": newURI("c")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(2), "p": newURI("b"), "o": variable(1)}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": variable(2)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("b"), "o": Literal("k")}),
        hashabledict({"s": variable(2), "p": newURI("b"), "o": Literal("l")}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": newURI("b")})
    },
    {
        hashabledict({"v1": Literal("l"), "v2": newURI("b")}),
        hashabledict({"v1": Literal("k"), "v2": newURI("b")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": variable(1)}),
        hashabledict({"s": newURI("d"), "p": newURI("e"), "o": variable(1)})
    },
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal("l")}),
        hashabledict({"s": newURI("d"), "p": newURI("e"), "o": Literal("l")})
    },
    {
        hashabledict({"v1": Literal("l")})
    }
)


allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(2), "p": newURI("b"), "o": variable(1)}),
        hashabledict({"s": variable(2), "p": newURI("c"), "o": variable(1)})
    },
    {
        hashabledict({"s": newURI("a"), "p": newURI("b"), "o": Literal("l")}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": Literal("l")})
    },
    {
        hashabledict({"v1": Literal("l"), "v2": newURI("a")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(2), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(2), "p": newURI("humanConcentration"), "o": variable(3)}),
        hashabledict({"s": variable(3), "p": newURI("locTag"), "o": variable(4)}),
    },
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("NCO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("no")}),
        hashabledict({"s": variable(1), "p": newURI("humanConcentration"), "o": variable(2)}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": Literal("l")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX01")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX02")}),
    },
    {
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": URILAMBDA, "v4": Literal("DX01")}),
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": URILAMBDA, "v4": Literal("DX02")})
    }
)


allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(2), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(2), "p": newURI("humanConcentration"), "o": variable(3)}),
        hashabledict({"s": variable(3), "p": newURI("locTag"), "o": variable(4)}),
        hashabledict({"s": variable(3), "p": newURI("securityLevel"), "o": Literal("5")}),
    },
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("NCO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("no")}),
        hashabledict({"s": variable(1), "p": newURI("humanConcentration"), "o": variable(2)}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": Literal("l")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX01")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX02")}),
        hashabledict({"s": newURI("GM1"), "p": newURI("locTag"), "o": Literal("DX02")}),
        hashabledict({"s": newURI("GM1"), "p": newURI("securityLevel"), "o": Literal("5")}),
        hashabledict({"s": newURI("GM2"), "p": newURI("locTag"), "o": Literal("DX01")}),
        hashabledict({"s": newURI("GM2"), "p": newURI("securityLevel"), "o": Literal("4")}),
    },
    {
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": Literal("DX01")}),
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": Literal("DX02")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(2), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(2), "p": newURI("humanConcentration"), "o": variable(3)}),
        hashabledict({"s": variable(3), "p": newURI("locTag"), "o": variable(5)}),
        hashabledict({"s": variable(3), "p": newURI("securityLevel"), "o": Literal("5")}),
        hashabledict({"s": variable(4), "p": newURI("securityLevel"), "o": Literal("4")}),
        hashabledict({"s": variable(4), "p": newURI("locTag"), "o": Literal("DX02")}),
    },
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("NCO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("no")}),
        hashabledict({"s": variable(1), "p": newURI("humanConcentration"), "o": variable(2)}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": Literal("l")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX01")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX02")}),
        hashabledict({"s": newURI("GM1"), "p": newURI("locTag"), "o": Literal("DX02")}),
        hashabledict({"s": newURI("GM1"), "p": newURI("securityLevel"), "o": Literal("5")}),
        hashabledict({"s": newURI("GM2"), "p": newURI("locTag"), "o": Literal("DX01")}),
        hashabledict({"s": newURI("GM2"), "p": newURI("securityLevel"), "o": Literal("4")}),
    },
    {
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": newURI("GM2"), "v5": Literal("DX01")}),
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": newURI("GM2"), "v5": Literal("DX02")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(2), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(2), "p": newURI("humanConcentration"), "o": variable(3)}),
        hashabledict({"s": variable(3), "p": newURI("locTag"), "o": variable(5)}),
        hashabledict({"s": variable(3), "p": newURI("securityLevel"), "o": Literal("5")}),
        hashabledict({"s": variable(4), "p": newURI("securityLevel"), "o": Literal("4")}),
        hashabledict({"s": variable(4), "p": newURI("locTag"), "o": Literal("DX02")}),
    },
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("NCO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("yes")}),
        hashabledict({"s": variable(1), "p": newURI("isIndoor"), "o": newURI("no")}),
        hashabledict({"s": variable(1), "p": newURI("humanConcentration"), "o": variable(2)}),
        hashabledict({"s": newURI("a"), "p": newURI("c"), "o": Literal("l")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX01")}),
        hashabledict({"s": variable(1), "p": newURI("locTag"), "o": Literal("DX02")}),
        hashabledict({"s": newURI("GM1"), "p": newURI("securityLevel"), "o": variable(1)}),
        hashabledict({"s": newURI("GM1"), "p": newURI("locTag"), "o": Literal("DX02")}),
        hashabledict({"s": newURI("GM1"), "p": newURI("securityLevel"), "o": Literal("5")}),
        hashabledict({"s": newURI("GM2"), "p": newURI("locTag"), "o": Literal("DX01")}),
        hashabledict({"s": newURI("GM2"), "p": newURI("securityLevel"), "o": Literal("4")}),
    },
    {
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": newURI("GM2"), "v5": Literal("DX01")}),
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": newURI("GM2"), "v5": Literal("DX02")}),
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": newURI("GM1"), "v5": Literal("DX01")}),
        hashabledict({"v1": URILAMBDA, "v2": URILAMBDA, "v3": newURI("GM1"), "v4": newURI("GM1"), "v5": Literal("DX02")}),
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
        hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("MineElevator")}),
hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("MineCorridor")}),
        hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)})
    },
    {
        hashabledict({"v1": URILAMBDA, "v4": URILAMBDA, "v3": newURI("MineElevator")}),
        hashabledict({"v1": URILAMBDA, "v4": URILAMBDA, "v3": newURI("MineCorridor")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
        hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("MineElevator")}),
        hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)})
    },
    {
        hashabledict({"v1": URILAMBDA, "v4": URILAMBDA, "v3": newURI("MineElevator")})
    }
)

allTestsPassed = allTestsPassed & test(
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
        hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)})
    },
    {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("NO2")}),
        hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
        hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)})
    },
    {

    }
)

# Print of the test results

print("\nTests: "+str(tests-testsfailed)+"/"+str(tests))
print("\nAll tests passed - "+str(allTestsPassed))