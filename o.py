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
    pass

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
    if not(isinstance(y,tuple)):
        raise e.KlongTypeError("cut: type error:\n  cut takes a list or string on the right, but you provided a " + type(y).__name__)
    if isinstance(x,int):
        if x<0:
            raise e.KlongRangeError("cut: range error: " + str(x))
        elif x==0:
            return ((),y)
        elif x==len(y):
            return (y,())
        elif x>len(y):
            raise e.KlongLengthError("cut: length error: " + str(x))
        else:
            return (y[0:x],y[x:])
    elif isinstance(x,tuple):
        # match x:
        # | x = (y[0:x],y[x+1:])
        # | x::xs = (kCut(x,y)[0], kCut(xs,kCut(x,y)[1]))
        # | () = ()
        # This would all be a lot nicer in Python 3.10, which has match, but we're on 3.8
        if x==():
            return (y,)
        elif len(x)==1:
            return kCut(x[0],y)
        else:
            # range error if not monotonically increasing
            # insert empty list if duplicate indices
            if not(all(map(lambda i: isinstance(i,int),x))):
                raise e.KlongTypeError("cut: type error:\n  cut takes an int or an int tuple on the left, but you've provided a tuple of (" + "".join(map(lambda i: type(i).__name__ + ", ",x)) + ")")
            if not(all(map(lambda t: t[0]<=t[1],zip((0,)+x[:-1],x)))): # check monotonically increasing
                raise e.KlongRangeError("cut: range error: " + str(x))
            else:
                return kCut(x[0],y)[0] + kCut(x[1:],kCut(x[0],y)[1])
    else:
        raise e.KlongTypeError("cut: type error:\n  cut takes an int or an int tuple on the left, but you provided a " + type(x).__name__)

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
