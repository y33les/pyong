# Special values

import e

class KlongSpecialValue:
    name = ""

    def __init__(self):
        self.name = ""
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self,x):
        if isinstance(x,KlongSpecialValue):
            return type(self)==type(x)
        else:
            raise e.KlongTypeError("equal: type error:\n  ["+str(self)+" "+str(x)+"]")

    def __lt__(self,x):
        pass

    def __gt__(self,x):
        pass

class KlongUndefined(KlongSpecialValue):

    def __init__(self):
        self.name = ":undefined"

    def __lt__(self,x):
        if isinstance(x,KlongSpecialValue):
            if isinstance(x,KlongUndefined):
                return False
            elif isinstance(x,KlongEOF):
                return False
            else:
                raise Exception("Unimplemented special Klong value; please notify @y33les")
        else:
            raise e.KlongTypeError("less: type error:\n  ["+str(self)+" "+str(x)+"]")

    def __gt__(self,x):
        if isinstance(x,KlongSpecialValue):
            if isinstance(x,KlongUndefined):
                return False
            elif isinstance(x,KlongEOF):
                return True
            else:
                raise Exception("Unimplemented special Klong value; please notify @y33les")
        else:
            raise e.KlongTypeError("less: type error:\n  ["+str(self)+" "+str(x)+"]")

class KlongEOF(KlongSpecialValue):

    def __init__(self):
        self.name = ":eof"

    def __lt__(self,x):
        if isinstance(x,KlongSpecialValue):
            if isinstance(x,KlongUndefined):
                return True
            elif isinstance(x,KlongEOF):
                return False
            else:
                raise Exception("Unimplemented special Klong value; please notify @y33les")
        else:
            raise e.KlongTypeError("more: type error:\n  ["+str(self)+" "+str(x)+"]")

    def __gt__(self,x):
        if isinstance(x,KlongSpecialValue):
            if isinstance(x,KlongUndefined):
                return False
            elif isinstance(x,KlongEOF):
                return False
            else:
                raise Exception("Unimplemented special Klong value; please notify @y33les")
        else:
            raise e.KlongTypeError("more: type error:\n  ["+str(self)+" "+str(x)+"]")
