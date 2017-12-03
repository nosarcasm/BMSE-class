#!/usr/bin/env python

""" Person, with heredity and other characteristics
:Authors: Ryan Neff <ryan.neff@icahn.mssm.edu>, Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-11-16
:License: MIT
"""

import pandas as pd
import networkx as nx

class Pedigree(object):
	''' Pedigree() Creates class that loads person and variant data from files
	::Functions::
	load_people(path)
		person name, gender, father name, mother name
		father and mother may be blank (missing)
		columns in the files are tab-separated (headers??)
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

	def __init__(self,people=None,variants=None,graph=None):
		"""A blank Pedigree object for loading people and variants"""
		self.people=people if people != None else dict()
		self.variants=variants if variants != None else set()
		self.graph=graph if graph != None else nx.DiGraph()

	def load_people(self,path,header=True):
		'''load_people() Takes a filename as input that includes the following 
		tab-separated columns in this order:
			1: person name (string 1-255 chars), title="name"
			2: person gender (one of <M,m,male,F,f,female>), title="gender"
			3: father's name (optional), title="father_name"
			4: mother's name (optional), title="mother_name"
		Denote presence of header with header=True.
		'''
		column_names = ["name","gender","father_name","mother_name"]
		assert isinstance(header,bool), "please denote header as True or False"
		peoplefile=None

		#load the input tsv into a pandas array
		if header:
			peoplefile = pd.read_table(path)
			assert set(column_names).issubset(set(peoplefile.columns)), """Column titles must include: name, gender, father_name, mother_name. 
		    You provided: %s""" % str(peoplefile.columns)
			peoplefile = peoplefile[column_names]
		else:
			peoplefile = pd.read_table(path,names=column_names,usecols=range(0,4),header=None)
		peoplefile["mother_name"] = peoplefile.apply(lambda x: 
										   x["mother_name"] if type(x["mother_name"])!=float else None,axis=1)
		peoplefile["father_name"] = peoplefile.apply(lambda x: 
										   x["father_name"] if type(x["father_name"])!=float else None,axis=1)

		# check that each person is represented in the database and that each person name is unique
		assert len(set(peoplefile["name"])) == len(peoplefile["name"]), "You have duplicate 'name's in your input."
		assert set(peoplefile["mother_name"]). \
			  union(set(peoplefile["father_name"])).difference(set([None])). \
			  issubset(set(peoplefile["name"])), """mothers and fathers must also have their own rows.
											   These parents are not represented: %s""" % (set(peoplefile["mother_name"]).
																							union(set(peoplefile["father_name"])).
																							difference(set(peoplefile["name"])))
		# check that graph is a DAG
		for ix,row in peoplefile.iterrows():
			pg.add_node(row["name"],{"gender":row["gender"]})
			if row["mother_name"] != None: self.graph.add_edge(row["mother_name"], row["name"])
			if row["father_name"] != None: self.graph.add_edge(row["father_name"], row["name"])
		assert nx.is_directed_acyclic_graph(self.graph), """You have an error in your pedigree.
		You did not provide a directed acyclic graph (pedigree is impossible)."""

		# validate each person using the Person generator
		peoplefile.set_index(peoplefile["name"],inplace=True) #make the input file indexable by row name which equals node name
		try:
			"""THOUGHTS: so for this to work, each person has to inherit from the mother (top part of the graph).
			we should store the graph representation as well.
			"""
			# create the people objects as nodes, don't worry about setting parents yet
			for ix,row in peoplefile.iterrows():
				self.people[row["name"]] = Person(name=row["name"],
											gender=row["gender"],
											mother=None,
											father=None
										   )
		except AssertionError as msg:
			print("ERROR:: line %d in %s :: %s"%(ix,path,msg))
			raise

		# traverse the graph from top to bottom to save time and to do this systematically
		for node in nx.topological_sort(self.graph): #this should return the top ancestor first
			parent = self.people[node] # get the person object
			first_order_descendents = self.graph.edge[node] #these are the children of that node
			if parent.gender == "female":
				for child in first_order_descendents:
					self.people[child].set_mother(parent)
			elif parent.gender == "male":
				for child in first_order_descendents:
					self.people[child].set_father(parent)

		return None

	def load_variants(self,path,header=True):
		"""load_variants() Takes a filename as input that includes the following 
		tab-separated columns in this order:
		1: chrom (the chromosome location, in "chr#" format)
		2: pos (a 0-based integer location)
		3: ref (optional, reference nucleotide)
		4: alt (a alternate nucleotide)
		5: person (the name of the person the variant is associated with)
		Denote presence of header with header=True.
		"""
		assert len(self.people) > 0, "you must load the people into the dataset first"

		column_names = ["chrom","pos","ref","alt","person"]
		assert isinstance(header,bool), "please denote header as True or False"
		variantfile=None

		if header:
			variantfile = pd.read_table(path)
			assert set(column_names).issubset(set(variantfile.columns)), """Column titles must include: "chrom","pos","ref","alt","person" 
		    You provided: %s""" % str(variantfile.columns)
			variantfile = variantfile[column_names]
		else:
			variantfile = pd.read_table(path,names=column_names,usecols=range(0,5),header=None)

		#replace NaN with None
		variantfile["person"] = variantfile.apply(lambda x: 
										   x["person"] if type(x["person"])!=float else None,axis=1)

		assert set(variantfile["person"]).difference(set([None])).issubset(self.people.keys()), """Variants in input include people not loaded in pedigree. 
		These people could not be found: %s""" % set(variantfile["person"]).difference(set([None])).difference(self.people.keys())

		assert any(variantfile.duplicated(subset=["chrom","pos","person"]))==False,"""Duplicate variants for each individual exist in the dataset.
		First example: %s""" % variantfile[variantfile.duplicated(subset=["chrom","pos","person"])].loc[0,]

		for ix,row in variantfile.iterrows():
			variant = Variant(row["chrom"],
			                          row["pos"],
			                          ref=row["ref"],
			                          alt=row["alt"],
			                          person=self.people[row["person"]])
			self.people[row["person"]].add_variant(variant)
			self.variants.add(variant)
		return None

class Variant(object):
	''' Variant
	Attributes:
		chrom (:obj:`str`): chromosome the variant is on
		pos (:obj:`int`): position that the variant is on the chromosome (0-indexed)
		ref (:obj:`str`): reference/null allele at that position
		alt (:obj:`str`): alternate/variant allele at that position
	'''

	_chrom_sizes = {'chr1': 248956422,
	 'chr10': 133797422,
	 'chr11': 135086622,
	 'chr12': 133275309,
	 'chr13': 114364328,
	 'chr14': 107043718,
	 'chr15': 101991189,
	 'chr16': 90338345,
	 'chr17': 83257441,
	 'chr18': 80373285,
	 'chr19': 58617616,
	 'chr2': 242193529,
	 'chr20': 64444167,
	 'chr21': 46709983,
	 'chr22': 50818468,
	 'chr3': 198295559,
	 'chr4': 190214555,
	 'chr5': 181538259,
	 'chr6': 170805979,
	 'chr7': 159345973,
	 'chr8': 145138636,
	 'chr9': 138394717,
	 'chrX': 156040895,
	 'chrY': 57227415}

	def __init__(self,chrom,pos,alt,ref=None,person=None,sanity=True):
		''' Creates a Variant class (represents single SNP)
		Each is stored with chrom, pos (ONLY ONE POSITION AS INT), ref, alt
		Variant __str__ -> string representation
		'''
		if sanity:
			## assertions to check input
			assert chrom in self._chrom_sizes.keys(), "chrom %s not found" % chrom
			assert isinstance(pos,int), "pos must be type int, got type %s" % type(pos)
			assert (pos>=0)&(pos<self._chrom_sizes[chrom]),"pos must be < chrom size, chrom %s is %d, pos is %d"%(chrom,self._chrom_sizes[chrom],pos)
			assert isinstance(alt,str), "alt allele must be type str, got type %s" % type(alt)
			assert len(alt)==1, "alt allele only supports SNPs at this time, got length %d" % len(alt)
			assert alt in ["A","C","T","G"], "alt allele must be in A,C,T,G"
			if ref!=None:
				assert isinstance(ref,str), "ref allele must be a string, got type %s" % type(ref)
				assert len(ref)==1, "ref allele only supports SNPs at this time, got length %d" % len(ref)
				assert ref in ["A","C","T","G"], "ref allele must be in A,C,T,G"          
			if person!=None:
				assert isinstance(person,Person), "person must be of Person() class, got type" % type(person)
		self.chrom = chrom
		self.pos = pos
		self.ref = ref.upper() if ref != None else None
		self.alt = alt.upper()
		self.person = person if person != None else None

	def __repr__(self):
		if self.ref!=None:
			return "<Variant at %s, %s:%d:%s->%s, belongs to:%s>" % (str(id(self)),self.chrom,self.pos,self.ref,self.alt,str(self.person))
		else:
			return "<Variant at %s, %s:%d:??->%s, belongs to:%s>" % (str(id(self)),self.chrom,self.pos,self.alt,str(self.person))

	def __str__(self):
		return self.__repr__()

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
	_genders = {
		"M":"male","m":"male","male":"male",
		"F":"female","f":"female","female":"female"
		}

	def __init__(self, name, gender,mother=None, father=None, variants=None, children=None, sanity=True):
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

		self.mother = None
		self.father = None
		self.set_mother(mother)
		self.set_father(father)
		self.children = children if children != None else set()

		self.variants = list()
		if variants != None: self.add_variants(variants) 

	def __repr__(self):
		""" Provide a string representation of this person
		"""
		return "<Person at {}: name: {}; gender: {}; mother {}; father {}>".format(
			str(id(self)),
			self.name,
			self.gender,
			Person.get_persons_name(self.mother),
			Person.get_persons_name(self.father))

	def __str__(self):
		return self.__repr__()

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

	def set_mother(self,mother):
		if mother != None:
			assert isinstance(mother, Person), "mother should be set to a Person object, not %s" % type(mother)
			if self.mother != None: self.mother.children.remove(self)
			mother.children.add(self)
			self.mother = mother

	def set_father(self,father):
		if father != None:
			assert isinstance(father, Person), "father should be set to a Person object, not %s" % type(father)
			if self.father != None: self.father.children.remove(self)
			father.children.add(self)
			self.father = father

	def remove_mother(self):
		self.mother.children.remove(self)
		self.mother = None
		return None

	def remove_father(self):
		self.father.children.remove(self)
		self.father = None
		return None

	def add_variant(self,variant):
		assert isinstance(variant,Variant), "input variant must be type Variant, not %s" % type(variant)
		variant.person = self
		variant_positions = [(v.chrom,v.pos) for v in self.variants if v != None]
		assert (variant.chrom, variant.pos) not in variant_positions, "variant already exists at %s:%d"%(variant.chrom,variant.pos) # sanity check
		self.variants.append(variant)
		return None

	def add_variants(self,variants):
		assert isinstance(variants,list),"variants must be a list"
		for v in variants:
			self.add_variant(v)
		return None

	def remove_variant(self,variant):
		assert isinstance(variant,Variant), "input variant must be type Variant, not %s" % type(variant)
		self.variant.person = None
		if variant in self.variants:
			self.variants.pop(variant)

	def list_variants(self):
		return list(self.variants)

	def siblings(self):
		mother_children = self.mother.children if self.mother else set()
		father_children = self.father.children if self.father else set()
		return mother_chldren.intersection(father_children)

	def half_siblings(self):
		mother_children = self.mother.children if self.mother else set()
		father_children = self.father.children if self.father else set()
		mother_half = mother_chldren.difference(father_children)
		father_half = father_children.difference(mother_children)
		return father_half.union(mother_half)

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

	def daughters(self):
		""" Get this person's daughters
		Returns:
			:obj:`list` of `Person`: the person's daughters
		"""
		daughters = []
		for child in self.children:
			if child.gender == 'female':
				daughters.append(child)
		return daughters

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

	def descendants(self, min_depth=1, max_depth=None):
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
		if max_depth is not None:
			if max_depth < min_depth:
					raise ValueError("max_depth ({}) cannot be less than min_depth ({})".format(
						max_depth, min_depth))
		else:
			max_depth = min_depth # just collect one

		collected_descendants = set()
		return self._descendants(collected_descendants, min_depth, max_depth)

	def _descendants(self, collected_descendants, min_depth, max_depth):
		""" Obtain this person's descendants who lie within the generational depth [min_depth, max_depth]
		This is a private, recursive method that recurses through the descendants via children references.
		Args:
			collected_descendants (:obj:`set`): descendants collected thus far by this method
			min_depth (:obj:`int`): see `descendants()`
			max_depth (:obj:`int`): see `descendants()`
		Returns:
			:obj:`set` of `Person`: this person's descendants
		Raises:
			:obj:`ValueError`: if `max_depth` < `min_depth`
		"""
		assert self not in collected_descendants, "the pedigree is not a DAG. self is descendant of self."
		if min_depth <= 0:
			collected_descendants.add(self)
		if 0 < max_depth:
			for child in self.children:
				child._descendants(collected_descendants, min_depth-1, max_depth-1)
		return collected_descendants

	def ancestors(self, min_depth=1, max_depth=None):
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
		assert self not in collected_ancestors, "the pedigree is not a DAG. self is ancestor of self."
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