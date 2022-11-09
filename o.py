# Operators
# Each operator's docstring is taken directly from klong-ref.txt
# (see https://t3x.org/klong/klong-ref.txt.html)

import e

# Monads
def kAtom(x):
    """
    @a                                                        [Atom]

    @ returns 1, if "a" is an atom and otherwise 0. All objects
    except for non-empty lists and non-empty strings are atoms.

    Examples:      @""  -->  1
                   @[]  -->  1
                  @123  -->  1
              @[1 2 3]  -->  0
    """
    return not(isinstance(x,tuple) or isinstance(x,str)) or x==() or x==""

def kChar(x):
    """
    :#a                                                       [Char]

    Return the character at the code point "a".

    Monadic :# is an atomic operator.

    Examples: :#64  -->  0cA
              :#10  -->  :"newline character"
    """
    if not(isinstance(x,int)):
        raise e.KlongTypeError("char: type error:\n  char takes an int, but you provided a " + type(x).__name__)
    else:
        return chr(x)

def kEnumerate(x):
    pass

def kExpandWhere(x):
    pass

def kFirst(x):
    pass

def kFloor(x):
    pass

def kFormat(x):
    pass

def kGradeDown(x):
    pass

def kGradeUp(x):
    pass

def kGroup(x):
    pass

def kList(x):
    pass

def kNegate(x):
    if isinstance(x,tuple):
        return tuple(map(kNegate,x)) # FIXME: is this right for klong?
    else:
        return -x

def kNot(x):
    pass

def kRange(x):
    pass

def kReciprocal(x):
    pass

def kReverse(x):
    pass

def kShape(x):
    pass

def kSize(x):
    pass

def kTranspose(x):
    pass

def kUndefined(x):
    pass

# Dyads
def kAmend(x,y):
    """
    a:=b                                                     [Amend]

    "a" must be a list or string and "b" must be a list where the
    first element can have any type and the remaining elements must
    be integers. It returns a new object of a's type where a@b2
    through a@bN are replaced by b1. When "a" is a string, b1 must
    be a character or a string. The first element of "a" has an
    index of 0.

    When both "a" and b1 are strings, Amend replaces each substring
    of "a" starting at b2..bN by b1. Note that no index b2..bN must
    be larger than #a or a range error will occur. When b1 is
    replaced at a position past (#a)-#b1, the amended string will
    grow by the required amount. For instance:

    "aa":="bc",1 --> "abc".

    Examples:    "-----":=0cx,[1 3]  -->  "-x-x-"
                       [1 2 3]:=0,1  -->  [1 0 3]
              "-------":="xx",[1 4]  -->  "-xx-xx-"
                     "abc":="def",3  -->  "abcdef"
    """
    out="" # TODO: remove; this was just to temporarily suppress an error while testing cut
    s = False
    if isinstance(x,str):
        s = True
        x = tuple(x)
    if not(isinstance(y,tuple)):
        raise e.KlongTypeError("amend: type error:\n  amend takes a vector on the right, but you provided a " + type(y).__name__)
    if not(all(map(lambda i: isinstance(i,int),y[1:]))):
        raise e.KlongTypeError("amend: type error:\n  amend's right arg must be a vector in which every element but the first must be an integer, but your right arg looks like (" + "".join(map(lambda i: type(i).__name__ + ", ",y))[:-2] + ")")
    if s:
        out = tuple(map(lambda t: "".join(t),out)) # collapse back into strings
    return out

def kAmendInDepth(x,y):
    pass

def kCut(x,y):
    """
    a:_b                                                       [Cut]

    Cut the list "b" before the elements at positions given in "a".
    "a" must be an integer or a list of integers. When it is a list
    of integers, its elements must be in monotonically increasing
    order. :_ returns a new list containing consecutive segments of
    "b". 

    When "a" is zero or #b or contains two subsequent equal indices,
    nil (or an empty string if "b" is a string) will be inserted.

    Examples:      2:_[1 2 3 4]  -->  [[1 2] [3 4]]
              [2 3 5]:_"abcdef"  -->  ["ab" "c" "de" "f"]
                         0:_[1]  -->  [[] [1]]
                       3:_"abc"  -->  ["abc" ""]
                   [1 1]:_[1 2]  -->  [[1] [] [2]]
    """
    if not(isinstance(y,tuple) or isinstance(y,str)):
        raise e.KlongTypeError("cut: type error:\n  cut takes a vector or string on the right, but you provided a " + type(y).__name__)
    s = False
    if isinstance(y,str):
        s = True
        y = tuple(y)
    if isinstance(x,int):
        if x<0:
            raise e.KlongRangeError("cut: range error: " + str(x))
        elif x==0:
            out = ((),y)
        elif x==len(y):
            out = (y,())
        elif x>len(y):
            raise e.KlongLengthError("cut: length error: " + str(x))
        else:
            out = (y[0:x],y[x:])
        if s:
            out = tuple(map(lambda t: "".join(t),out)) # collapse back into strings
        return out
    elif isinstance(x,tuple):
        # This would all be a lot nicer in Python 3.10, which has match, but we're on 3.8
        if x==():
            out = (y,)
        elif len(x)==1:
            out = kCut(x[0],y)
        else:
            # range error if not monotonically increasing
            # insert empty list if duplicate indices
            if not(all(map(lambda i: isinstance(i,int),x))):
                raise e.KlongTypeError("cut: type error:\n  cut takes an int or an int vector on the left, but you've provided a tuple of (" + "".join(map(lambda i: type(i).__name__ + ", ",x))[:-2] + ")")
            if not(all(map(lambda t: t[0]<=t[1],zip((0,)+x[:-1],x)))): # check monotonically increasing
                raise e.KlongRangeError("cut: range error: " + str(x))
            else:
                out = tuple(map(lambda t: y[t[0]:t[1]],zip((0,)+x,x+(None,))))
        if s:
            out = tuple(map(lambda t: "".join(t),out)) # collapse back into strings
        return out
    else:
        raise e.KlongTypeError("cut: type error:\n  cut takes an int or an int vector on the left, but you provided a " + type(x).__name__)

def kDefine(x,y):
    pass

def kDivide(x,y):
    pass

def kDrop(x,y):
    pass

def kEqual(x,y):
    pass

def kFind(x,y):
    pass

def kForm(x,y):
    pass

def kFormat2(x,y):
    pass

def kIndexApply(x,y):
    pass

def kIndexInDepth(x,y):
    pass

def kIntegerDivide(x,y):
    pass

def kJoin(x,y):
    pass

def kLess(x,y):
    pass

def kMatch(x,y):
    pass

def kMaxOr(x,y):
    pass

def kMinAnd(x,y):
    pass

def kMinus(x,y):
    return x-y

def kMore(x,y):
    pass

def kPlus(x,y):
    pass

def kPower(x,y):
    pass

def kReshape(x,y):
    pass

def kRemainder(x,y):
    pass

def kRotate(x,y):
    pass

def kSplit(x,y):
    pass

def kTake(x,y):
    pass

def kTimes(x,y):
    pass
