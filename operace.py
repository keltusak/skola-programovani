import operator
import math
operation2 = {}
operation1 = {}

operation2["+"]=lambda a,b: a+b
operation2["-"]= operator.sub
operation2["*"]= operator.mul
operation2["/"]= operator.truediv
operation2["//"]= operator.floordiv
operation2["%"]= lambda a,b: a%b

operation1["sqrt"]=lambda a: math.sqrt(a)
operation1["V"]=lambda a: math.sqrt(a)
operation1["^"]=lambda a: a**2
operation1["d"]=math.degrees
operation1["r"]=math.radians
operation1["sin"]=lambda a: math.sin
operation1["cos"]=lambda a: math.cos
operation1["tg"]=lambda a: math.tg
operation1["tan"]=lambda a: math.tan
