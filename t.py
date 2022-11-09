# Tests
# Tests largely derived from the examples in klong-ref.txt
# (see https://t3x.org/klong/klong-ref.txt.html)

import e
from o import *

# TODO: amend
# TODO: amend-in-depth

# Atom
print("Atom:\t",end="")
assert kAtom("")
assert kAtom(())
assert kAtom(123)
assert not(kAtom((1,2,3)))
print("PASS")

# Char
print("Char:\t",end="")
assert kChar(64)=="@"
try:
    kChar("a")
except e.KlongTypeError:
    pass
print("PASS")

# Cut
print("Cut:\t",end="")
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
