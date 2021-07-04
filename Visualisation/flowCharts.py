from pyflowchart import *

st = StartNode('Play Solo Card')
cond0 = ConditionNode('Are we Bid winner?')
# -----------------------------
# A0 for bidwinner
bidWinner = SubroutineNode('Bid winner')
bidwinnerCondA1 = ConditionNode('Do we have the lead?')
YCondA2 = ConditionNode('Opposition still has trump & We hold trump')
YopA1 = OperationNode('Play highest Trump')
# A2
NcondA1 = ConditionNode('Do we have cards not trump?')
YopA3 = OperationNode('Play highest Rank')
opA3N = OperationNode('Play random card')
