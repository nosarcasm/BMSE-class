#!/usr/bin/env python

""" Person, with heredity and other characteristics
:Authors: Ryan Neff <ryan.neff@icahn.mssm.edu>, Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-11-16
:License: MIT
"""

''' From https://stackoverflow.com/questions/2825452/correct-approach-to-validate-attributes-of-an-instance-of-class

You can use Python properties to cleanly apply rules to each field separately, 
and enforce them even when client code tries to change the field:

class Spam(object):
    def __init__(self, description, value):
        self.description = description
        self.value = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, d):
        if not d: raise Exception("description cannot be empty")
        self._description = d

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if not (v > 0): raise Exception("value must be greater than zero")
        self._value = v

An exception will be thrown on any attempt to violate the rules, 
even in the __init__ function, in which case object construction will fail.

UPDATE: Sometime between 2010 and now, I learned about operator.attrgetter:

import operator

class Spam(object):
    def __init__(self, description, value):
        self.description = description
        self.value = value

    description = property(operator.attrgetter('_description'))

    @description.setter
    def description(self, d):
        if not d: raise Exception("description cannot be empty")
        self._description = d

    value = property(operator.attrgetter('_value'))

    @value.setter
    def value(self, v):
        if not (v > 0): raise Exception("value must be greater than zero")
        self._value = v
'''

class Pedigree(object):
    self.people = set()
    self.variants = set()

    def __init__(people=None,variants=None):
        self.people=people
        self.variants=variants

    ## TODO: Create class that loads person and variant data from files
    '''
        ::Functions::
        load_people(path)
            person name, gender, father name, mother name
            father and mother may be blank (missing)
            must check: unique person names, parents are in loaded data, genders OK
                reject those that fail, output nicely formatted error msgs
        load_variants(path)
            chrom, location, ref, alt, person
            must check:
                chrom name is valid
                    against hg38 = will be hard-coded for the homework
                nucleotide is on chrom (nucleotide position is valid and 0-based)
                variant nucleotide is valid (don't worry about the reference!)
                variant different than reference
                person is in the dataset ?
                    can check after the fact!!
        path is a .tsv
    '''

    #TODO
    def load_people(self.path):
        return None

    #TODO
    def load_variants(path):
        return None

class Variant(object):
	''' Variant
	Attributes:
		chrom (:obj:`str`): chromosome the variant is on
		pos (:obj:`int`): position that the variant is on the chromosome (0-indexed)
		ref (:obj:`str`): reference/null allele at that position
		alt (:obj:`str`): alternate/variant allele at that position
	'''

    ## TODO: Create a Variant class (represents single SNP)
    '''
        Each is stored with chrom, pos (ONLY ONE POSITION AS INT), ref, alt
        Variant __str__ -> string representation
    '''

	self._chrom_sizes = '''chr1	248956422
	chr2	242193529
	chr3	198295559
	chr4	190214555
	chr5	181538259
	chr6	170805979
	chr7	159345973
	chrX	156040895
	chr8	145138636
	chr9	138394717
	chr11	135086622
	chr10	133797422
	chr12	133275309
	chr13	114364328
	chr14	107043718
	chr15	101991189
	chr16	90338345
	chr17	83257441
	chr18	80373285
	chr20	64444167
	chr19	58617616
	chrY	57227415
	chr22	50818468
	chr21	46709983'''

    self._chrom_sizes = {c.split("\t")[0]:int(c.split("\t")[1]) for c in self._chrom_sizes.split("\n")}

    self.chrom = str()
    self.pos = int()
    self.ref = None
    self.alt = str()
    self.person = None

	def __init__(self,chrom,pos,alt,ref=None,person=None,sanity=True):
		if sanity:
            ## assertions to check input
			assert chrom in self._chrom_sizes.keys(), "chrom %s not found" % chrom
            assert isinstance(pos,int), "pos must be type int, got type %s" % type(pos)
            assert (pos>=0)&(pos<self._chrom_sizes[chrom]),"pos must be < chrom size, chrom %s is %d, pos is %d"%(chrom,self._chrom_sizes[chrom],pos)
            assert isinstance(alt,str), "alt allele must be type str, got type %s" % type(alt)
            assert length(alt)==1, "alt allele only supports SNPs at this time, got length %d" % length(alt)
            if ref!=None:
                assert isinstance(ref,str), "ref allele must be a string, got type %s" % type(ref)
                assert length(ref)==1, "ref allele only supports SNPs at this time, got length %d" % length(ref)            
            if person!=None:
                assert isinstance(person,Person), "person must be of Person() class, got type" % type(person)
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.person = person

    def __repr__(self):
        if ref!=None:
            return "<Variant at %s, %s:%d:%s->%s, belongs to:%s>" % (str(id(self)),self.chrom,self.pos,self.ref,self.alt,str(self.Person))
        else:
            return "<Variant at %s, %s:%d:??->%s, belongs to:%s>" % (str(id(self)),self.chrom,self.pos,self.alt,str(self.Person))

class Person(object):
    """ Person
    Attributes:
        name (:obj:`str`): a person's name
        gender (:obj:`str`): a person's gender
        mother (:obj:`Person`): a person's mother
        father (:obj:`Person`): a person's father
        children (:obj:`set` of `Person`): a person's children
        variants (:obj:`list` of :obj:`Variant`s, optional): variants associated with the person
    """

    self.name = str()
    self.gender = str()
    self.mother=None
    self.father=None
    self.variants=set()
    self.children = set()
    self._genders = {
        "M":"male","m":"male","male":"male",
        "F":"female","f":"female","female":"female"
        }

    def __init__(self, name, gender, mother=None, father=None, variants=None,children=None,sanity=True):
        """ Create a Person instance
        Create a new Person object, AKA a Person instance. This is used by the
        expression Person(). The parameters name and gender are required, while   other parameters are
        optional.
        Args:
             name (:obj:`str`): the person's name
             gender (:obj:`str`): the person's gender
             mother (:obj:`Person`, optional): the person's mother
             father (:obj:`Person`, optional): the person's father
             variants (:obj:`set` of :obj:`Variant`s, optional): variants associated with the person
             children (:obj:`set` of :obj:`Person`, optional): children associated with the person
        """
        if sanity:
            ## assertions to check input
            assert isinstance(name,str),"name must be type str, got type %s" % type(name)
            assert (len(name) > 0)&(len(name)<=255), "name must be between 1 and 255 characters"
            assert gender in self._genders.keys(),"gender must be one of %s" % str(self._genders.keys())
            if variants != None:
                assert isinstance(variants,list),"variants must be of type list, not type %s"%type(variants)
                for v in variants:
                    assert isinstance(v,Variant),"variants must each be of type Variant(), not type %s for variant %s"%(type(v),str(v))
            if mother != None:
                assert isinstance(mother,Person),"mother must be a Person(), not type %s"%type(mother)
                assert mother not in self.children,"mother must not also belong to Person's children, Person %s" % str(mother)
            if father != None:
                assert isinstance(father,Person),"father must be a Person(), not type %s"%type(mother)
                assert father not in self.children,"father must not also belong to Person's children, Person %s" % str(father)
            if children != None:
                assert isinstance(children,set),"children passed at init must be enclosed in a set, not type %s"%type(children)
                assert self.mother not in children,"attempt to set child equal to Person's mother, mother %s" % str(self.mother)
                assert self.father not in children,"attempt to set child equal to Person's father, father %s" % str(self.father)
                for a in children:
                    assert isinstance(a,Person),"child %s passed in children is not of type Person (got type %s)" % (str(a),type(a))
            if (mother != None)&(children != None):
                assert mother not in children,"attempt to set mother and child to same, Person %s"%str(mother)
                #TODO: do some recursive matching to make sure you have a DAG
            if (father != None)&(children != None):
                assert father not in children,"attempt to set father and child to same, Person %s"%str(father)
                #TODO: do some recursive matching to make sure you have a DAG
        self.name = name
        self.gender = self._genders[gender]
        self.set_mother(mother)
        self.set_father(father)
        self.children = children
        self.add_variants(variants)

    def __repr__(self):
    """ Provide a string representation of this person
    """
    return "<Person at {}, name: {}: gender {}; mother {}; father {}>".format(
        str(id(self)),
        self.name,
        self.gender,
        Person.get_persons_name(self.mother),
        Person.get_persons_name(self.father))

    # a method annotated with '@staticmethod' is a 'static method' that does not receive an
    # implicit first argument. Rather, it is called C.m(), where the class C identifies the
    # class in which the method is defined.

    @staticmethod
    def get_persons_name(person):
        """ Get a person's name; if the person is not known, return 'NA'
        Returns:
            :obj:`str`: the person's name, or 'NA' if they're not known
        """
        if person is None:
            return 'NA'
        return person.name

    # TODO: write 'set_father' and 'set_mother' methods that set a person's father or mother,
    # and adds the person to the father's or mother's children. Replace all statements below
    # that set a person's father or mother attribute with these methods.
    
    ##TODO
    def set_mother(self,mother):
        return None

    ##TODO
    def set_father(self,father):
        return None

    # TODO: remove the 'add_child' method and replace any statements that use it with a call to
    # 'set_father' or 'set_mother'

    ##TODO: REMOVE THIS###
    #def add_child(self, child):
    #   """ Add a child to this person's set of children
    #    Args:
    #         child (:obj:`Person`): a child of `self`
    #    """
    #    self.children.add(child)

    # TODO: write 'remove_father' and 'remove_mother' methods that removes a person's father or mother,
    # and removes the person from the father's or mother's children. Test these methods.

    #TODO
    def remove_mother(self):
        return None

    #TODO
    def remove_father(self):
        return None

    # TODO: add a data structure containing this person's variants, and methods that add a variant,
    # and list all variants

    #TODO
    def add_variant(self,variant):
        return None

    #TODO
    def add_variants(self,variants):
        return None

    #TODO
    def list_variants(self):
        return None

    # TODO: create a 'siblings' method that returns a person's siblings, and write a 'half_siblings'
    # method that returns a person's half-siblings.

    #TODO
    def siblings(self):
        return None

    #TODO
    def half_siblings(self):
        return None

    # TODO: EXTRA CREDIT: implement this descendents method, which has analogous semantics to the
    # ancestors method below. The implementation may use a while loop or be recursive. Use
    # your 'descendents' method to implement 'children', 'grand_children', and 'all_descendents'.

    # TODO: EXTRA CREDIT: can a cycle in the ancestry graph create an infinite loop?
    # if so, avoid this problem.

    def sons(self):
        """ Get this person's sons
        Returns:
            :obj:`list` of `Person`: the person's sons
        """
        sons = []
        for child in self.children:
            if child.gender == 'male':
                sons.append(child)
        return sons

    def grandparents_structured(self):
        ''' Provide this person's grandparents
        Returns:
            :obj:`tuple`: the person's grandparents, in a 4-tuple:
            (maternal grandmother, maternal grandfather, paternal grandmother, paternal grandfather)
            Missing individuals are identified by None.
        '''
        grandparents = []
        if self.mother:
            grandparents.extend([self.mother.mother, self.mother.father])
        else:
            grandparents.extend([None, None])
        if self.father:
            grandparents.extend([self.father.mother, self.father.father])
        else:
            grandparents.extend([None, None])
        return tuple(grandparents)

    def descendants(self, min_depth, max_depth=None):
        """ Return this person's descendants within a generational depth range
        Obtain descendants whose generational depth satisfies `min_depth` <= depth <= `max_depth`.
        E.g., this person's children would be obtained with `min_depth` = 1, and this person's
        grandchildren and great-grandchildren would be obtained with `min_depth` = 3 and
        `max_depth` = 3.
        Args:
            min_depth (:obj:`int`): the minimum depth of descendants which should be provided;
                this person's depth is 0, their children's depth is 1, etc.
            max_depth (:obj:`int`, optional): the minimum depth of descendants which should be
                provided; if `max_depth` is not provided, then `max_depth` == `min_depth` so that only
                descendants at depth == `min_depth` will be provided; a `max_depth` of infinity will
                obtain all descendants at depth >= `min_depth`.
        Returns:
            :obj:`set` of `Person`: this person's descendants
        Raises:
            :obj:`ValueError`: if `max_depth` < `min_depth`
        """
        pass

    def ancestors(self, min_depth, max_depth=None):
        """ Return this person's ancestors within a generational depth range
        Obtain ancestors whose generational depth satisfies `min_depth` <= depth <= `max_depth`. E.g.,
        a person's parents would be obtained with `min_depth` = 1, and this person's parents and
        grandparents would be obtained with `min_depth` = 1 and `max_depth` = 2.
        Args:
            min_depth (:obj:`int`): the minimum depth of ancestors which should be provided;
                this person's depth is 0, their parents' depth is 1, etc.
            max_depth (:obj:`int`, optional): the minimum depth of ancestors which should be
                provided; if `max_depth` is not provided, then `max_depth` == `min_depth` so that only
                ancestors at depth == `min_depth` will be provided; a `max_depth` of infinity will obtain
                all ancestors at depth >= `min_depth`.
        Returns:
            :obj:`set` of `Person`: this person's ancestors
        Raises:
            :obj:`ValueError`: if `max_depth` < `min_depth`
        """
        if max_depth is not None:
            if max_depth < min_depth:
                    raise ValueError("max_depth ({}) cannot be less than min_depth ({})".format(
                        max_depth, min_depth))
        else:
            # collect just one depth
            max_depth = min_depth
        collected_ancestors = set()
        return self._ancestors(collected_ancestors, min_depth, max_depth)

    def _ancestors(self, collected_ancestors, min_depth, max_depth):
        """ Obtain this person's ancestors who lie within the generational depth [min_depth, max_depth]
        This is a private, recursive method that recurses through the ancestry via parent references.
        Args:
            collected_ancestors (:obj:`set`): ancestors collected thus far by this method
            min_depth (:obj:`int`): see `ancestors()`
            max_depth (:obj:`int`): see `ancestors()`
        Returns:
            :obj:`set` of `Person`: this person's ancestors
        Raises:
            :obj:`ValueError`: if `max_depth` < `min_depth`
        """
        if min_depth <= 0:
            collected_ancestors.add(self)
        if 0 < max_depth:
            for parent in [self.mother, self.father]:
                if parent is not None:
                    parent._ancestors(collected_ancestors, min_depth-1, max_depth-1)
        return collected_ancestors

    def parents(self):
        ''' Provide this person's parents
        Returns:
            :obj:`set`: this person's known parents
        '''
        return self.ancestors(1)

    def grandparents(self):
        ''' Provide this person's known grandparents, by using ancestors()
        Returns:
            :obj:`set`: this person's known grandparents
        '''
        return self.ancestors(2)

    def great_grandparents(self):
        return self.ancestors(3)

    def all_grandparents(self):
        ''' Provide all of this person's known grandparents, from their parents' parents on back 
        Returns:
            :obj:`set`: all of this person's known grandparents
        '''
        return self.ancestors(2, max_depth=float('inf'))

    def all_ancestors(self):
        ''' Provide all of this person's known ancestors
        Returns:
            :obj:`set`: all of this person's known ancestors
        '''
        return self.ancestors(1, max_depth=float('inf'))