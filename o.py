# Operators
# Each operator's docstring is taken directly from klong-ref.txt
# (see https://t3x.org/klong/klong-ref.txt.html)

import e
import operator as op
from functools import reduce

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
    """
    !a                                                   [Enumerate]

    Create a list of integers from 0 to a-1. !0 gives [].

    Examples: !0   -->  []
              !1   -->  [0]
              !10  -->  [0 1 2 3 4 5 6 7 8 9]

    N.B.: The original Klong reference specifies that !1 --> [1], but
          this does not reflect the behaviour of the official Klong
          interpreter, which returns [0].  It is therefore assumed to
          be an error, and pyong instead recreates the interpreter's
          behaviour (i.e. that !1 --> [0]).
    """
    if not(isinstance(x,int)):
        raise e.KlongTypeError("enumerate: type error:\n  enumerate takes an int, but you provided a " + type(x).__name__)
    if x<0:
        raise e.KlongDomainError("enumerate: domain error\n  enumerate only accepts non-negative integers, but you provided " + str(x))
    return tuple(range(x))

def kExpandWhere(x):
    """
    &a                                                [Expand/Where]

    Expand "a" to a list of subsequent integers X, starting at 0,
    where each XI is included aI times. When "a" is zero or an
    empty list, return nil. When "a" is a positive integer, return
    a list of that many zeros.

    In combination with predicates this function is also called
    Where, since it compresses a list of boolean values to indices,
    e.g.:

     [1 2 3 4 5]=[0 2 0 4 5]  -->  [0 1 0 1 1]
    &[1 2 3 4 5]=[0 2 0 4 5]  -->  [1 3 4]

    Examples:           &0  -->   []
                        &5  -->   [0 0 0 0 0]
                  &[1 2 3]  -->   [0 1 1 2 2 2]
              &[0 1 0 1 0]  -->   [1 3]
    """
    if isinstance(x,int): # expand (int)
        if x<0:
            raise e.KlongRangeError("expand/where: range error: " + str(x))
        return (0,)*x
    elif isinstance(x,tuple):
        if not(all(map(lambda i: isinstance(i,int),x))):
            raise e.KlongTypeError("expand/where: type error:\n  expand/where takes an int vector, but your arg looks like (" + "".join(map(lambda i: type(i).__name__ + ", ",x))[:-2] + ")")
        if not(all(map(lambda i: i>=0,x))):
            raise e.KlongRangeError("expand/where: range error: " + str(tuple([i for i in x if i<0])))
        if all(map(lambda i: i==0 or i==1,x)): # where
            return tuple([i for i in range(len(x)) if x[i]])
        else: # expand (vector)
            return tuple(reduce(op.add,[(n,)*x[n] for n in range(len(x))]))
    else:
        raise e.KlongTypeError("expand/where: type error:\n  expand/where takes an int or an int vector, but you provided a " + type(x).__name__)

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
    """
    -a                                                      [Negate]

    Return 0-a; "a" must be a number.

    "-" is an atomic operator.

    Examples:    -1  -->  -1
              -1.23  -->  -1.23
    """
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
    s = False
    if isinstance(x,str):
        s = True
        x = tuple(x)
    if not(isinstance(y,tuple)):
        raise e.KlongTypeError("amend: type error:\n  amend takes a vector on the right, but you provided a " + type(y).__name__)
    if not(all(map(lambda i: isinstance(i,int),y[1:]))):
        raise e.KlongTypeError("amend: type error:\n  amend's right arg must be a vector in which every element but the first must be an integer, but your right arg looks like (" + "".join(map(lambda i: type(i).__name__ + ", ",y))[:-2] + ")")
    # TODO: implement it!!
    if s:
        out = tuple(map(lambda t: "".join(t),out)) # collapse back into strings
    return out

def kAmendInDepth(x,y):
    # TODO
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
    # TODO
    pass

def kDivide(x,y):
    """
    a%b                                                     [Divide]

    Return the quotient of "a" and "b". The result is always a real
    number, even if the result has a fractional part of 0.

    "%" is an atomic operator.

    Examples: 10%2  -->  5.0
              10%8  -->  1.25
    """
    return float(x)/float(y)

def kDrop(x,y):
    """
    a_b                                                       [Drop]

    When "b" is a list or string, drop "a" elements or characters
    from it, returning the remaining list. Dropping more elements
    than contained in "b" will yield the empty list/string. A
    negative value for "a" will drop elements from the end of "b".

    When "b" is a dictionary, remove the entry with the key "a" from
    it. Dictionary removal is in situ, i.e. the dictionary will be
    modified. Other objects will be copied.

    Examples: 3_[1 2 3 4 5]  -->  [4 5]
              (-3)_"abcdef"  -->  "abc"
                 17_[1 2 3]  -->  []
                   (-5)_"x"  -->  ""
                      0_[1]  -->  [1]

    N.B. Although the Klong documentation above specifies that
         dictionaries are modified in situ, this is not yet the case
         in pyong, which simply returns a new dictionary with the
         specified keys dropped.
    """
    s = False
    if not(isinstance(y,dict)):
        if not(isinstance(x,int)):
            raise e.KlongTypeError("drop: type error:\n  drop takes an int on the left, but you provided a " + type(x).__name__)
        if not(isinstance(y,tuple) or isinstance(y,str)):
            raise e.KlongTypeError("cut: type error:\n  cut takes a vector, a string or a dictionary on the right, but you provided a " + type(y).__name__)
        if isinstance(y,str):
            s = True
            y = tuple(y)
        out = ()
        if x>=0:
            out = y[x:]
        else:
            if abs(x)>=len(y):
                pass
            else:
                out = y[:x]
        if s:
            out = "".join(out) # collapse back into a string
        return out
    else:
        # TODO: In the Klong reference, it says that dictionaries get modified in situ
        y.pop(x)
        return y

def kEqual(x,y):
    """
    a=b                                                      [Equal]

    Return 1, if "a" and "b" are equal, otherwise return 0.

    Numbers are equal, if they have the same value.
    Characters are equal, if (#a)=#b.
    Strings and symbols are equal, if they contain the same
    characters in the same positions.

    "=" is an atomic operator. In particular it means that it
    cannot compare lists, but only elements of lists. Use "~"
    (Match) to compare lists.

    Real numbers should not be compared with "=". Use "~" instead.

    Examples:             1=1  -->  1
                  "foo"="foo"  -->  1
                    :foo=:foo  -->  1
                      0cx=0cx  -->  1
              [1 2 3]=[1 4 3]  -->  [1 0 1]
    """
    return int(x==y)

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
    """
    a-b                                                      [Minus]

    Subtract "b" from "a" and return the result. "a" and "b" must be
    numbers.

    "-" is an atomic operator.

    Examples:  12-3  -->  9
              12--3  -->  15
              1-0.3  -->  0.7
    """
    return x-y

def kMore(x,y):
    pass

def kPlus(x,y):
    """
    a+b                                                       [Plus]

    Add "b" to "a" and return the result. "a" and "b" must both be
    numbers.

    Dyadic "+" is an atomic operator.

    Examples:  12+3  -->  15
              12+-3  -->  9
              1+0.3  -->  1.3
    """
    return x+y

def kPower(x,y):
    """
    a^b                                                      [Power]

    Compute "a" to the power of "b" and return the result. Both "a"
    and "b" must be numbers. The result of a^b cannot be a complex
    number.

    Dyadic "^" is an atomic operator.

    Examples:   2^0  -->  1
                2^1  -->  2
                2^8  -->  256
               2^-5  -->  0.03125
              0.3^3  -->  0.027
              2^0.5  -->  1.41421356237309504
    """
    return x**y

def kReshape(x,y):
    pass

def kRemainder(x,y):
    """
    a!b                                                  [Remainder]

    Return the truncated division remainder of "a" and "b". Both
    "a" and "b" must be integers.

    Formally, a = (b*a:%b) + a!b .

    Dyadic "!" is an atomic operator.

    Examples:    7!5  -->  2
                7!-5  -->  2
              (-7)!5  --> -2
               -7!-5  --> -2
    """
    if x>=0:
        if y>=0:
            return x%y
        else:
            return x%-y
    else:
        if y>=0:
            return -((-x)%y)
        else:
            return x%y

def kRotate(x,y):
    pass

def kSplit(x,y):
    pass

def kTake(x,y):
    pass

def kTimes(x,y):
    """
    a*b                                                      [Times]

    Return "a" multiplied by "b". "a" and "b" must both be numbers.

    Dyadic "*" is an atomic operator.

    Examples:   3*4  -->  12
               3*-4  -->  -12
              0.3*7  -->  2.1
    """
    return x*y
