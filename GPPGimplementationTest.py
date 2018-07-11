from GPPGimplementation import *

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