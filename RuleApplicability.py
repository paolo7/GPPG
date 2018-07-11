from GPPGimplementation import *

# A rule is a tuple with two elements. The first is the graph pattern of the precondition.
# The second is the graph pattern of the consequent. The variables in the consequent need
# to be a subset of the variables in the precondition graph.

def expand_rules(graphpattern, rules, test_print=False):
    if test_print:
        print("Rule expansion started: initial state of the graph pattern:")
        debug_print_graph_pattern(graphpattern)
    changed = True
    size = len(graphpattern)
    while(changed):
        changed = False
        for rule in rules:
            mappings = GPPG(rule[0], graphpattern)
            expansion = instantiate_consequent(rule[1], mappings)
            for pattern1 in expansion:
                already_existing = False
                for pattern2 in graphpattern:
                    if triple_pattern_equality(pattern1,pattern2):
                        already_existing = True
                if not already_existing:
                    graphpattern = graphpattern | {pattern1}
        if len(graphpattern) > size:
            if test_print:
                print("\nRule inference iteration finished. Number of new triple patterns: "+str(len(graphpattern)-size))
                debug_print_graph_pattern(graphpattern)
            size = len(graphpattern)
            changed = True
    if test_print:
        print("\nAll rule inference iteration finished.")
    return graphpattern

def is_rule_applicable(graphpattern, rules, rule):
    expanded_graphpattern = expand_rules(graphpattern, rules)
    return len(GPPG(rule[0], expanded_graphpattern)) > 0

def instantiate_consequent(consequent, mappings):
    expansion = set()
    for mapping in mappings:
      for triple_pattern in consequent:
        subject = triple_pattern["s"]
        if isinstance(triple_pattern["s"], variable):
          subject = mapping["v"+str(triple_pattern["s"].num)]
        if isinstance(subject, URIRef) and subject.toPython() == URILAMBDA.toPython():
          # variables in variable independent graph patterns represent "any value" and therefore it does not matter
          # which variable is chosen, as long as we guarantee that it is not reused in the same triple pattern
          subject = variable(1)
        predicate = triple_pattern["p"]
        if isinstance(triple_pattern["p"], variable):
            predicate = mapping["v" + str(triple_pattern["p"].num)]
        if isinstance(predicate, URIRef) and predicate.toPython() == URILAMBDA.toPython():
          predicate = variable(2)
        object = triple_pattern["o"]
        if isinstance(triple_pattern["o"], variable):
            object = mapping["v" + str(triple_pattern["o"].num)]
        if isinstance(object, URIRef) and object.toPython() == URILAMBDA.toPython():
            object = variable(3)
        expansion.add(hashabledict({"s": subject, "p": predicate, "o": object}))
    return expansion

def debug_print_graph_pattern(graphpattern):
    print("    GRAPH PATTERN:")
    for triplepattern in graphpattern:
        print("      " + str(triplepattern["s"]) + " " + str(triplepattern["p"]) + " " + str(triplepattern["o"]))

def triple_pattern_equality(pattern1, pattern2):
    for index in {"s","p","o"}:
        if type(pattern1) != type(pattern2):
            return False
        if not (isinstance(pattern1[index], variable) or isinstance(pattern2[index], variable)):
            if pattern1[index].toPython() != pattern2[index].toPython():
                return False
    return True

def graph_pattern_equality(graph1, graph2):
    if len(graph1) != len(graph2):
        return False
    for pattern1 in graph1:
        equal_found = False
        for pattern2 in graph2:
            if triple_pattern_equality(pattern1, pattern2):
                equal_found = True
        if not equal_found:
            return False
    return True