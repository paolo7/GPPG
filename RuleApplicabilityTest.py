from RuleApplicability import *

extended_debug_print = True
allTestsPassed = True
tests = 0
testsfailed = 0

def test(passed):
    global tests, testsfailed
    tests += 1
    print("\nTest n. " + str(tests))
    print("TEST pass: " + str(passed))
    if not passed:
        testsfailed += 1
    return passed

def test_rule_applicability(graphpattern,rules,rule,expected):
    global tests, testsfailed
    tests += 1
    applicable = is_rule_applicable(graphpattern,rules,rule)
    print("\n\nGiven schema: ")
    debug_print_graph_pattern(graphpattern)
    print("and set of rules: ")
    for r in rules:
        print("-rule: ")
        debug_print_graph_pattern(r[0])
        print("  ==>")
        debug_print_graph_pattern(r[1])
    print("\nthe RULE: ")
    debug_print_graph_pattern(rule[0])
    print("==>")
    debug_print_graph_pattern(rule[1])
    if (applicable):
        print("is applicable")
    else:
        print("is NOT applicable")
    passed =  applicable == expected
    if passed:
        print("(as expected)")
    if not passed:
        print("(NOT as expected)")
        testsfailed += 1
    return passed

def test1():
  print("\nTEST SET 1\n")
  graphpattern = {
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO_Danger")}),
        hashabledict({"s": variable(2), "p": newURI("observedProperty"), "o": newURI("WorkerTag")}),
        hashabledict({"s": variable(3), "p": newURI("hasFeatureOfInterest"), "o": newURI("TunnelA")}),
        hashabledict({"s": variable(4), "p": newURI("hasResult"), "o": variable(5)}),
    }
  expected_graphpattern = {
        hashabledict({"s": newURI("TunnelA"), "p": newURI("type"), "o": newURI("GeofencingViolatedTunnel")}),
        hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO_Danger")}),
        hashabledict({"s": variable(2), "p": newURI("observedProperty"), "o": newURI("WorkerTag")}),
        hashabledict({"s": variable(3), "p": newURI("hasFeatureOfInterest"), "o": newURI("TunnelA")}),
        hashabledict({"s": variable(4), "p": newURI("hasResult"), "o": variable(5)}),
        hashabledict({"s": newURI("TunnelA"), "p": newURI("type"), "o": newURI("OffLimitArea")}),
    }
  # the set of rules
  rule1 = (
          {  # Precondition:
              hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("WorkerTag")}),
              hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
              hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(3)}),
              hashabledict({"s": variable(2), "p": newURI("type"), "o": newURI("OffLimitArea")}),
          },  # ==>
          {  # Consequent
              hashabledict({"s": variable(2), "p": newURI("type"), "o": newURI("GeofencingViolatedTunnel")}),
          }
      )
  rule2 = (
          { # Precondition:
            hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO_Danger")}),
            hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
            hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": Literal('1')}),
          }, # ==>
          { # Consequent
            hashabledict({"s": variable(2), "p": newURI("type"), "o": newURI("OffLimitArea")}),
          }
      )
  rules = [rule1,rule2]
  expanded = expand_rules(graphpattern, rules, extended_debug_print)
  correct = graph_pattern_equality(expanded,expected_graphpattern)
  test(correct)
  test_rule_applicability(graphpattern, rules, rule1,True)
  test_rule_applicability(graphpattern, rules, rule2,True)
  test_rule_applicability(graphpattern, [rule1], rule1, False)
  return correct

def test2():
  print("\nTEST SET 2\n")
  graphpattern = {
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
    }
  expected_graphpattern = {
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
      hashabledict({"s": variable(1), "p": newURI("geoFencingActive"), "o": Literal("1")}),
      hashabledict({"s": variable(1), "p": newURI("securityLevelAlertLoc"), "o": Literal("DX02")}),
      hashabledict({"s": variable(1), "p": newURI("securityLevelAlertLoc"), "o": Literal("DX01")}),
    }
  # the set of rules
  rule1 = (
          {  # Precondition:
              hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
              hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
              hashabledict({"s": variable(2), "p": newURI("isIndoor"), "o": newURI("yes")}),
              hashabledict({"s": variable(2), "p": newURI("humanConcentration"), "o": variable(3)}),
              hashabledict({"s": variable(3), "p": newURI("locTag"), "o": variable(5)}),
              hashabledict({"s": variable(3), "p": newURI("securityLevel"), "o": Literal("5")}),
              hashabledict({"s": variable(4), "p": newURI("securityLevel"), "o": Literal("4")}),
              hashabledict({"s": variable(4), "p": newURI("locTag"), "o": Literal("DX02")}),
          },  # ==>
          {  # Consequent
              hashabledict({"s": variable(2), "p": newURI("geoFencingActive"), "o": Literal("1")}),
              hashabledict({"s": variable(2), "p": newURI("securityLevelAlertLoc"), "o": variable(5)}),
          }
      )
  rules = [rule1]
  expanded = expand_rules(graphpattern, rules, extended_debug_print)
  correct = graph_pattern_equality(expanded,expected_graphpattern)
  test(correct)
  test_rule_applicability(graphpattern, rules, rule1,True)
  return correct


def test3():
  print("\nTEST SET 3\n")
  graphpattern = {
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
    }
  expected_graphpattern = {
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
    }
  # the set of rules
  # this rule should not be applicable because DX03 is not in the original schema
  rule1 = (
          {  # Precondition:
              hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
              hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(2)}),
              hashabledict({"s": variable(2), "p": newURI("isIndoor"), "o": newURI("yes")}),
              hashabledict({"s": variable(2), "p": newURI("humanConcentration"), "o": variable(3)}),
              hashabledict({"s": variable(3), "p": newURI("locTag"), "o": variable(5)}),
              hashabledict({"s": variable(3), "p": newURI("securityLevel"), "o": Literal("5")}),
              hashabledict({"s": variable(4), "p": newURI("securityLevel"), "o": Literal("4")}),
              hashabledict({"s": variable(4), "p": newURI("locTag"), "o": Literal("DX03")}),
          },  # ==>
          {  # Consequent
              hashabledict({"s": variable(2), "p": newURI("geoFencingActive"), "o": Literal("1")}),
              hashabledict({"s": variable(2), "p": newURI("securityLevelAlertLoc"), "o": variable(5)}),
          }
      )
  rules = [rule1]
  expanded = expand_rules(graphpattern, rules, extended_debug_print)
  correct = graph_pattern_equality(expanded,expected_graphpattern)
  test(correct)
  test_rule_applicability(graphpattern, rules, rule1,False)
  return correct


def test4():
  print("\nTEST SET 4\n")
  graphpattern = {
      hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
      hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("MineElevator")}),
      hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
      hashabledict({"s": variable(1), "p": newURI("type"), "o": newURI("MonitoringCentre")}),
    }
  expected_graphpattern = {
      hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
      hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("MineElevator")}),
      hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
      hashabledict({"s": variable(1), "p": newURI("type"), "o": newURI("MonitoringCentre")}),
      hashabledict({"s": newURI("MineElevator"), "p": newURI("hasCO2level"), "o": variable(4)}),
      hashabledict({"s": newURI("MineElevator"), "p": newURI("hasTemperature"), "o": variable(4)}),
      hashabledict({"s": newURI("MineElevator"), "p": newURI("hasFireRisk"), "o": Literal("High")}),
      hashabledict({"s": newURI("MineElevator"), "p": newURI("evacuationNeeded"), "o": Literal("1")}),
    }
  # the set of rules
  rule1 = (
          {  # Precondition:
              hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO2")}),
              hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
              hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
          },  # ==>
          {  # Consequent
              hashabledict({"s": variable(3), "p": newURI("hasCO2level"), "o": variable(4)}),
          }
      )
  rule2 = (
      {  # Precondition:
          hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("Temperature")}),
          hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
          hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(3), "p": newURI("hasTemperature"), "o": variable(4)}),
      }
  )
  rule3 = (
      {  # Precondition:
          hashabledict({"s": variable(1), "p": newURI("hasCO2level"), "o": variable(4)}),
          hashabledict({"s": variable(1), "p": newURI("hasTemperature"), "o": variable(4)}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(1), "p": newURI("hasFireRisk"), "o": Literal("High")}),
      }
  )
  rule4 = (
      {  # Precondition:
          hashabledict({"s": variable(1), "p": newURI("hasCO2level"), "o": variable(4)}),
          hashabledict({"s": variable(1), "p": newURI("hasTemperature"), "o": variable(4)}),
          hashabledict({"s": variable(1), "p": newURI("type"), "o": newURI("MonitoringCentre")}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(1), "p": newURI("evacuationNeeded"), "o": Literal("1")}),
      }
  )
  rule5 = (
      {  # Precondition:
          hashabledict({"s": newURI("CentreA1"), "p": newURI("hasCO2level"), "o": variable(4)}),
          hashabledict({"s": newURI("CentreA1"), "p": newURI("hasTemperature"), "o": variable(4)}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(1), "p": newURI("evacuationNeeded"), "o": Literal("1")}),
      }
  )
  rules = [rule1,rule2,rule3,rule4,rule5]
  expanded = expand_rules(graphpattern, rules, extended_debug_print)
  correct = graph_pattern_equality(expanded,expected_graphpattern)
  test(correct)
  test_rule_applicability(graphpattern, rules, rule1,True)
  test_rule_applicability(graphpattern, rules, rule2, True)
  test_rule_applicability(graphpattern, rules, rule3, True)
  test_rule_applicability(graphpattern, rules, rule4, True)
  test_rule_applicability(graphpattern, rules, rule5, False)
  return correct

def test5():
  print("\nTEST SET 5\n")
  graphpattern = {
      hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
      hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("MineElevator")}),
      hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
    }
  expected_graphpattern = {
      hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
      hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("MineElevator")}),
      hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
    }
  # the set of rules
  rule1 = (
          {  # Precondition:
              hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("CO")}),
              hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": newURI("TunnelEntrance")}),
              hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
          },  # ==>
          {  # Consequent
              hashabledict({"s": variable(3), "p": newURI("hasCOlevel"), "o": variable(4)}),
          }
      )
  rule2 = (
      {  # Precondition:
          hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
          hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
          hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
      }
  )
  rules = [rule1,rule2]
  expanded = expand_rules(graphpattern, rules, extended_debug_print)
  correct = graph_pattern_equality(expanded,expected_graphpattern)
  test(correct)
  test_rule_applicability(graphpattern, rules, rule1,False)
  test_rule_applicability(graphpattern, rules, rule2, True)
  return correct

def test6():
  print("\nTEST SET 6\n")
  graphpattern = {
      hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
      hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
      hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
      hashabledict({"s": variable(1), "p": newURI("type"), "o": newURI("Room")}),
      hashabledict({"s": variable(1), "p": newURI("type"), "o": newURI("Human")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room1")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room2")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room3")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room4")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room5")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room6")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room7")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room8")}),
      hashabledict({"s": newURI("room8"), "p": newURI("type"), "o": newURI("humanSafeRoom")}),
      hashabledict({"s": newURI("room6"), "p": newURI("type"), "o": newURI("humanSafeRoom")}),
      hashabledict({"s": newURI("room5"), "p": newURI("type"), "o": newURI("humanSafeRoom")}),
    }
  expected_graphpattern = {
      hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": variable(2)}),
      hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
      hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
      hashabledict({"s": variable(1), "p": newURI("type"), "o": newURI("Room")}),
      hashabledict({"s": variable(1), "p": newURI("type"), "o": newURI("Human")}),
      hashabledict({"s": variable(3), "p": newURI("hasMethanelevel"), "o": variable(4)}),
      hashabledict({"s": variable(3), "p": newURI("hasRoomMethanelevel"), "o": variable(4)}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room1")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room2")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room3")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room4")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room5")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room6")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room7")}),
      hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": newURI("room8")}),
      hashabledict({"s": newURI("room8"), "p": newURI("type"), "o": newURI("humanSafeRoom")}),
      hashabledict({"s": newURI("room6"), "p": newURI("type"), "o": newURI("humanSafeRoom")}),
      hashabledict({"s": newURI("room5"), "p": newURI("type"), "o": newURI("humanSafeRoom")}),
      hashabledict({"s": newURI("room1"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room2"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room3"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room4"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room5"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room6"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room7"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room8"), "p": newURI("containsHuman"), "o": variable(3)}),
      hashabledict({"s": newURI("room8"), "p": newURI("RequiredAction"), "o": newURI("RestoreSafety")}),
      hashabledict({"s": newURI("room6"), "p": newURI("RequiredAction"), "o": newURI("RestoreSafety")}),
      hashabledict({"s": newURI("room5"), "p": newURI("RequiredAction"), "o": newURI("RestoreSafety")}),
      hashabledict({"s": newURI("room1"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room2"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room3"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room4"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room5"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room6"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room7"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room8"), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      hashabledict({"s": newURI("room8"), "p": newURI("hasAlertLevel"), "o": newURI("HighAlert")}),
      hashabledict({"s": newURI("room6"), "p": newURI("hasAlertLevel"), "o": newURI("HighAlert")}),
      hashabledict({"s": newURI("room5"), "p": newURI("hasAlertLevel"), "o": newURI("HighAlert")}),
      hashabledict({"s": newURI("Mine"), "p": newURI("RequiredAction"), "o": newURI("FullEvacuation")}),
    }
  # the set of rules


  rule6 = (
      {  # Precondition:
          hashabledict({"s": variable(3), "p": newURI("containsHuman"), "o": newURI("SafetyManager")}),
          hashabledict({"s": variable(3), "p": newURI("hasAlertLevel"), "o": newURI("HighAlert")}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": newURI("Mine"), "p": newURI("RequiredAction"), "o": newURI("FullEvacuation")}),
      }
  )
  rule5 = (
      {  # Precondition:
          hashabledict({"s": variable(3), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
          hashabledict({"s": variable(3), "p": newURI("RequiredAction"), "o": newURI("RestoreSafety")}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(3), "p": newURI("hasAlertLevel"), "o": newURI("HighAlert")}),
      }
  )
  rule4 = (
      {  # Precondition:
          hashabledict({"s": variable(3), "p": newURI("containsHuman"), "o": variable(1)}),
          hashabledict({"s": variable(3), "p": newURI("hasRoomMethanelevel"), "o": variable(4)}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(3), "p": newURI("RequiredAction"), "o": newURI("SendEmergencyRescue")}),
      }
  )
  rule0 = (
      {  # Precondition:
          hashabledict({"s": variable(1), "p": newURI("hasLocation"), "o": variable(3)}),
          hashabledict({"s": variable(3), "p": newURI("hasRoomMethanelevel"), "o": variable(4)}),
          hashabledict({"s": variable(3), "p": newURI("type"), "o": newURI("humanSafeRoom")}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(3), "p": newURI("RequiredAction"), "o": newURI("RestoreSafety")}),
      }
  )
  rule1 = (
      {  # Precondition:
          hashabledict({"s": variable(3), "p": newURI("hasMethanelevel"), "o": variable(4)}),
          hashabledict({"s": variable(3), "p": newURI("type"), "o": newURI("Room")}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(3), "p": newURI("hasRoomMethanelevel"), "o": variable(4)}),
      }
  )
  rule2 = (
          {  # Precondition:
              hashabledict({"s": variable(1), "p": newURI("observedProperty"), "o": newURI("Methane")}),
              hashabledict({"s": variable(1), "p": newURI("hasFeatureOfInterest"), "o": variable(3)}),
              hashabledict({"s": variable(1), "p": newURI("hasResult"), "o": variable(4)}),
          },  # ==>
          {  # Consequent
              hashabledict({"s": variable(3), "p": newURI("hasMethanelevel"), "o": variable(4)}),
          }
      )
  rule3 = (
      {  # Precondition:
          hashabledict({"s": variable(3), "p": newURI("hasLocation"), "o": variable(4)}),
          hashabledict({"s": variable(4), "p": newURI("type"), "o": newURI("Room")}),
          hashabledict({"s": variable(3), "p": newURI("type"), "o": newURI("Human")}),
      },  # ==>
      {  # Consequent
          hashabledict({"s": variable(4), "p": newURI("containsHuman"), "o": variable(3)}),
      }
  )

  rules = [rule1,rule2,rule3,rule4,rule5,rule6,rule0]
  expanded = expand_rules(graphpattern, rules, extended_debug_print)
  correct = graph_pattern_equality(expanded,expected_graphpattern)
  test(correct)
  test_rule_applicability(graphpattern, rules, rule1,True)
  test_rule_applicability(graphpattern, rules, rule2, True)
  test_rule_applicability(graphpattern, rules, rule3, True)
  test_rule_applicability(graphpattern, rules, rule4, True)
  test_rule_applicability(graphpattern, rules, rule5, True)
  test_rule_applicability(graphpattern, rules, rule6, True)
  test_rule_applicability(graphpattern, rules, rule0, True)
  return correct

allTestsPassed = allTestsPassed & test1() & test2() & test3() & test4() & test5() & test6()

# Print of the test results

print("\nTests: "+str(tests-testsfailed)+"/"+str(tests))
print("\nAll tests passed - "+str(allTestsPassed))