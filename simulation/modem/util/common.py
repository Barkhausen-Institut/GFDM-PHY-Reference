
class FrozenBoundedClass(object):
    # TODO: This code is copied from another project, so it should be imported
    # TODO: Implement this as decoretor
    __is_frozen = False
    def __setattr__(self, key, value):
        if hasattr(self.__class__, "bounds"):
            bounds = getattr(self.__class__,"bounds")
            if key in bounds:
                if value > bounds[key][1] or value < bounds[key][0]:
                    raise ValueError (str(value)+" is out of bounds: ("+
                        str(bounds[key][0])+", "+str(bounds[key][1])+")" )
        if self.__is_frozen and not hasattr(self, key):
            raise TypeError( "%r is a frozen class" % self )
        object.__setattr__(self, key, value)

    def _freeze(self):
        self.__is_frozen = True
