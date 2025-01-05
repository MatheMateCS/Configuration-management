from z3 import *


deps = { 
    'LID': [['DP24', 'DP23'], ['M13']],
    'DP24': [['M12'], ['SD42'], ['LZ15']],
    'DP23': [['LZ14'], ['M13']],
    'LZ15': [['M12'], ['R12']],
    'M13': [['R11'], ['SD42']],
    'M12': [['SD41']]
}

elements = {}

for key in deps.keys():
    elements[key] = Bool(f'{key}')
    for package in deps[key]:
        for vers in package:
            if elements.get(vers) == None:
                elements[vers] = Bool(f'{vers}')
                
solver = Solver()

i_and = []
for premise in deps.keys():
    for package in deps[premise]:
        i_or = []
        for vers in package:
            i_or.append(Implies(elements[premise], elements[vers]))
        if (len(i_or) > 1) :
            i_and.append(Or(i_or))
        else:
            i_and.append(i_or[0])
            
solver.add(elements['LID'])
solver.add(And(i_and))

print(solver.check())
print(solver.model())