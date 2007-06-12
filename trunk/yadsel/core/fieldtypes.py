"""
** not yet documented **
@author Marinho Brandao
@creation 2007-05-24
"""

class FieldType(object):
    name = None
    default = None
    required = True
    references = None
    primary_key = False
    domain = None
    collation = None

    def __init__(self, **kwargs):
        [setattr(self, k, kwargs[k]) for k in kwargs]

        if self.references:
            self.references.references_from = self.name

    def to_script(self, only_attrs=False):
        """
        Generates a Python script with the sintax to create this object
        
        @author Marinho Brandao
        @creation 2007-06-06
        """
        ret = ""

        if self.default: ret += "default=%s, " % self.default
        if not self.required: ret += "required=%s, " % self.required
        if self.references: ret += "references=%s, " % self.references.to_script()
        if self.primary_key: ret += "primary_key=%s, " % self.primary_key

        if not only_attrs:
            ret = "%s = %s(%s)" %( self.name, self.__class__.__name__, ret )

        return ret

class Integer(FieldType):
    autoincrement = False

class SmallInt(FieldType):
    pass

class Varchar(FieldType):
    length = None

    def __init__(self, length=None, **kwargs):
        super(Varchar, self).__init__(**kwargs)
        
        self.length = length or self.length

    def to_script(self, only_attrs=False):
        """
        Generates a Python script with the sintax to create this object
        
        @author Marinho Brandao
        @creation 2007-06-06
        """
        attrs = super(Varchar, self).to_script(True)
        if attrs: attrs = ", " + attrs
        ret = "%s = %s(%d%s)" %( self.name, self.__class__.__name__, self.length, attrs )

        return ret

class Char(FieldType):
    length = None

    def __init__(self, length=None, **kwargs):
        super(Char, self).__init__(**kwargs)
        
        self.length = length or self.length

    def to_script(self, only_attrs=False):
        """
        Generates a Python script with the sintax to create this object
        
        @author Marinho Brandao
        @creation 2007-06-06
        """
        attrs = super(Char, self).to_script(True)
        if attrs: attrs = ", " + attrs
        ret = "%s = %s(%d%s)" %( self.name, self.__class__.__name__, self.length, attrs )

        return ret

class Timestamp(FieldType):
    pass

class DateTime(FieldType):
    pass

class Date(FieldType):
    pass

class Time(FieldType):
    pass

class Text(FieldType):
    segment_size = None

class Blob(FieldType):
    segment_size = None

class Boolean(FieldType):
    pass

class Decimal(FieldType):
    length = None
    digits = None

    def __init__(self, length=None, digits=None, **kwargs):
        super(Decimal, self).__init__(**kwargs)

        self.length = length or self.length
        self.digits = digits or self.digits

    def to_script(self, only_attrs=False):
        """
        Generates a Python script with the sintax to create this object
        
        @author Marinho Brandao
        @creation 2007-06-06
        """
        attrs = super(Decimal, self).to_script(True)
        if attrs: attrs = ", " + attrs
        ret = "%s = %s(%d, %d%s)" %( self.name, self.__class__.__name__, self.length, self.digits, attrs )

        return ret

class Numeric(Decimal):
    pass

class Float(FieldType):
    pass

class Domain(FieldType):
    """
    This class will be receive another resource in future, when
    will have a domains list from where will be referenced domain
    cited here but declared on previous versions

    @author Marinho Brandao
    @creation 2007-06-05
    """
    domain_name = None

    def __init__(self, domain_name, **kwargs):
        super(Domain, self).__init__(**kwargs)
        
        self.domain_name = domain_name

