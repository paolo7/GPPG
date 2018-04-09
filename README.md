# Sample GPPG Implementation and Testing

## Overview

Graph Pattern evaluation over Pattern-constrained Graphs (GPPG) is the task of computing the set of all the possible results that can be obtained by evaluating a SPARQL query graph pattern `P` over an RDF graph that only contains triples that follow a certain pattern `P'`.

Both `P` and `P'` need to be basic conjunctive graph patterns (a set of triple patterns). Black nodes are not supported, and each triple in `P'` cannot have more than one occurrence of the same variable (e.g. triple `<?v1, :a, ?v1>` is not allowed in `P'`).

## Running the script

The script is written in Python 3, and it requires the `rdflib` library.<sup>1</sup>

### Test cases

The script contains a number of test cases that are automatically evaluated when the script is run. To remove them, delete all the lines after `# Algorithm finished, test script below:`. 

Sample results of the test cases [here](results.txt) (Python console output).

### Lambda URI

The code contains an arbitrarely chosen URI `URILAMBDA`. This URI can be changed to any other one, but it MUST NOT be one of the URIs that occur in `P` or `P1`.

---

<sup>1</sup> [https://github.com/RDFLib/rdflib](https://github.com/RDFLib/rdflib)
