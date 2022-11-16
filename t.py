# Tests
# Tests largely derived from the examples in klong-ref.txt
# (see https://t3x.org/klong/klong-ref.txt.html)

import e
from o import *

# TODO: amend
# TODO: amend-in-depth

# Atom
print("Atom:\t\t",end="")
assert kAtom("")
assert kAtom(())
assert kAtom(123)
assert not(kAtom((1,2,3)))
print("PASS")

# Char
print("Char:\t\t",end="")
assert kChar(64)=="@"
try:
    kChar("a")
except e.KlongTypeError:
    pass
print("PASS")

# Cut
print("Cut:\t\t",end="")
try:
    kCut(2,2)
except e.KlongTypeError:
    pass
try:
    kCut(-1,(3,4,5,6))
except e.KlongRangeError:
    pass
assert kCut(0,(3,4,5,6)) == ((),(3,4,5,6))
assert kCut(2,(3,4,5,6)) == ((3,4),(5,6))
assert kCut(4,(3,4,5,6)) == ((3,4,5,6),())
try:
    kCut(5,(3,4,5,6))
except e.KlongLengthError:
    pass
assert kCut((),(3,4,5,6)) == ((3,4,5,6),)
assert kCut((2,),(3,4,5,6)) == kCut(2,(3,4,5,6))
try:
    kCut((2,"foo",3),(3,4,5,6))
except e.KlongTypeError:
    pass
try:
    kCut((3,2),(3,4,5,6))
except e.KlongRangeError:
    pass
assert kCut((2,4),(2,4,6,8,10,12)) == ((2,4),(6,8),(10,12))
assert kCut((2,2,4),(2,4,6,8,10,12)) == ((2,4),(),(6,8),(10,12))
assert kCut((0,2,4),(3,4,5,6)) == ((),(3,4),(5,6),())
try:
    kCut(-1,"foobar")
except e.KlongRangeError:
    pass
assert kCut(0,"foobar") == ("","foobar")
assert kCut(2,"foobar") == ("fo","obar")
assert kCut(6,"foobar") == ("foobar","")
try:
    kCut(7,"foobar")
except e.KlongLengthError:
    pass
assert kCut((),"foobar") == ("foobar",)
assert kCut((2,),"foobar") == kCut(2,"foobar")
try:
    kCut((2,"foo",3),"foobar")
except e.KlongTypeError:
    pass
try:
    kCut((3,2),"foobar")
except e.KlongRangeError:
    pass
assert kCut((2,4),"foobar") == ("fo","ob","ar")
assert kCut((2,2,4),"foobar") == ("fo","","ob","ar")
assert kCut((0,2,6),"foobar") == ("","fo","obar","")
print("PASS")

# TODO: define

# Divide
print("Divide:\t\t",end="")
assert kDivide(4,2)==2.0
assert isinstance(kDivide(4,2),float)
assert kDivide(3,2)==1.5
print("PASS")

# Drop
print("Drop:\t\t",end="")
assert kDrop(3,(1,2,3,4,5))==(4,5)
assert kDrop(-3,(1,2,3,4,5))==(1,2)
assert kDrop(2,"foobar")=="obar"
assert kDrop(-2,"foobar")=="foob"
assert kDrop(10,(1,2,3,4,5))==()
assert kDrop(10,"foobar")==""
assert kDrop(-10,(1,2,3,4,5))==()
assert kDrop(-10,"foobar")==""
assert kDrop(0,(1,2,3,4,5))==(1,2,3,4,5)
assert kDrop(0,"foobar")=="foobar"
assert kDrop("b",{"a":1,"b":2,"c":3})=={"a":1,"c":3}
assert kDrop((2,3),{(1,2):"a",(2,3):"b",(3,4):"c"})=={(1,2):"a",(3,4):"c"}
try:
    kDrop("foo",(1,2,3,4,5))
except e.KlongTypeError:
    pass
try:
    kDrop(2,8)
except e.KlongTypeError:
    pass
# TODO: once in-situ dictionary drop is implemented, make sure it works
print("PASS")

# Enumerate
print("Enumerate:\t",end="")
assert kEnumerate(0)==()
assert kEnumerate(1)==(0,)
assert kEnumerate(10)==(0,1,2,3,4,5,6,7,8,9)
try:
    kEnumerate(-10)
except e.KlongDomainError:
    pass
try:
    kEnumerate("foobar")
except e.KlongTypeError:
    pass
try:
    kEnumerate(2.5)
except e.KlongTypeError:
    pass
try:
    kEnumerate((2,4,6,8))
except e.KlongTypeError:
    pass
print("PASS")

# Equal
print("Equal:\t\t",end="")
assert kEqual(2,2)
assert not(kEqual(2,4))
assert kEqual(2.5,2.5)
assert not(kEqual(2.5,2.6))
assert kEqual(2,2.0)
assert not(kEqual(2,2.1))
assert kEqual("foo","foo")
assert not(kEqual("foo","bar"))
# TODO: character-string equality?
# TODO: equality of symbols, once implemented
# TODO: vectors, i.e. [1 2 3]=[1 4 3] --> [1 0 1]
print("PASS")

# Expand/Where
print("Expand/Where:\t",end="")
assert kExpandWhere(0)==()
assert kExpandWhere(5)==(0,0,0,0,0)
assert kExpandWhere((1,2,3))==(0,1,1,2,2,2)
assert kExpandWhere((0,1,0,1,0))==(1,3)
assert kExpandWhere((0,))==()
assert kExpandWhere((1,))==(0,)
assert kExpandWhere((2,0,4))==(0,0,2,2,2,2)
try:
    kExpandWhere(-2)
except e.KlongRangeError:
    pass
try:
    kExpandWhere((1,2,-3,4,-5,6,7,8))
except e.KlongRangeError:
    pass
try:
    kExpandWhere("foobar")
except e.KlongTypeError:
    pass
print("PASS")




# Minus
print("Minus:\t\t",end="")
assert kMinus(2,3)==-1
assert kMinus(3,2)==1
print("PASS")




# Negate
print("Negate:\t\t",end="")
assert kNegate(2)==-2
assert kNegate(-2)==2
assert kNegate(0)==0
print("PASS")




# Plus
print("Plus:\t\t",end="")
assert kPlus(2,3)==5
assert kPlus(3,2)==5
print("PASS")




# Power
print("Power:\t\t",end="")
assert kPower(2,3)==8
assert kPower(3,2)==9
print("PASS")



# Remainder
print("Remainder:\t",end="")
assert kRemainder(7,5)==2
assert kRemainder(7,-5)==2
assert kRemainder(-7,5)==-2
assert kRemainder(-7,-5)==-2
try:
    kRemainder(7,0)
except ZeroDivisionError:
    pass
print("PASS")




# Times
print("Times:\t\t",end="")
assert kTimes(2,3)==6
assert kTimes(3,2)==6
print("PASS")
