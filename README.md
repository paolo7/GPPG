# GPPG Implementation and Rule Applicability - sample code and implementation

## Overview

Graph Pattern evaluation over Pattern-constrained Graphs (GPPG) is the task of computing the set of all the possible results that can be obtained by evaluating a SPARQL query graph pattern `P` over an RDF graph that only contains triples that follow a certain pattern `P'`.

Both `P` and `P'` need to be basic conjunctive graph patterns (a set of triple patterns). Black nodes are not supported, and each triple in `P'` cannot have more than one occurrence of the same variable (e.g. triple `<?v1, :a, ?v1>` is not allowed in `P'`).

GPPG can be used to determine the applicability of a rule on a dataset defined by a graph schema. It allows to predict the effect of the application of a rule, and therefore reason about the subsequent applicability of other rules.

The code provided allows both to detect rule applicability (the `is_rule_applicable` method) and to expand a graph schema with a set of inference rules (the `expand_rules` method).

## Running the scripts

The scripts are written in Python 3, and they requires the `rdflib` library.<sup>1</sup>

The `GPPGimplementation` script contains the algorithm to solve GPPG problems.

The `RuleApplicability` script contains the algorithm to expand a graph schema with a given set of rules using the GPPG solver algorithm.

### Test cases

The `GPPGimplementationTest` and `RuleApplicabilityTest` scripts contain a number of test cases that are automatically evaluated when the script is run.

Sample results of the test cases [here](results.txt) and [here](results2.txt) (Python console output).

### Lambda URI

The code contains an arbitrarely chosen URI `URILAMBDA`. This URI can be changed to any other one, but it MUST NOT be one of the URIs that occur in `P` or `P1`.

---

<sup>1</sup> [https://github.com/RDFLib/rdflib](https://github.com/RDFLib/rdflib)
