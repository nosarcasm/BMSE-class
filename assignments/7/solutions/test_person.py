#!/usr/bin/env python

""" Test Person

:Authors: Ryan Neff <ryan.neff@icahn.mssm.edu>, Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-12
:Copyright: 2017, Arthur Goldberg
:License: MIT
"""
import unittest

from person import Person, Gender, PersonError


class TestGender(unittest.TestCase):

    def test_gender(self):
        self.assertEqual(Gender().get_gender('Male'), Gender.MALE)
        self.assertEqual(Gender().get_gender('female'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('FEMALE'), Gender.FEMALE)
        self.assertEqual(Gender().get_gender('NA'), Gender.UNKNOWN)

        with self.assertRaises(PersonError) as context:
            Gender().get_gender('---')
        self.assertIn('Illegal gender', str(context.exception))


class TestPerson(unittest.TestCase):

    def setUp(self):
        # create a few Persons
        self.child = Person('kid', 'NA')
        self.mom = Person('mom', 'f')
        self.dad = Person('dad', 'm')

        self.generations = 4
        self.people = people = []
        self.root_child = Person('root_child', Gender.UNKNOWN)
        people.append(self.root_child)

        def add_parents(child, depth, max_depth):
            if depth+1 < max_depth:
                dad = Person(child.name + '_dad', Gender.MALE)
                mom = Person(child.name + '_mom', Gender.FEMALE)
                people.append(dad)
                people.append(mom)
                child.set_father(dad)
                child.set_mother(mom)
                add_parents(dad, depth+1, max_depth)
                add_parents(mom, depth+1, max_depth)
        add_parents(self.root_child, 0, self.generations)
        self.head_father = self.root_child.father.father.father

    def test_set_mother(self):
        self.child.set_mother(self.mom)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)
    
    def test_set_mother_error(self):
        self.mom.gender = Gender.MALE
        with self.assertRaises(PersonError) as context:
            self.child.set_mother(self.mom)
        self.assertIn('is not female', str(context.exception))

    def test_set_father(self):
        self.child.set_father(self.dad)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)
    
    def test_set_father_error(self):
        self.dad.gender = Gender.FEMALE
        with self.assertRaises(PersonError) as context:
            self.child.set_father(self.dad)
        self.assertIn('is not male', str(context.exception))

    def test_add_child(self):
        self.assertNotIn(self.child, self.mom.children)
        #FIXED BUG from unittests: we need to set the gender of the child too, right?
        self.child.gender = Gender.MALE
        self.mom.add_child(self.child)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)

        self.assertNotIn(self.child, self.dad.children)
        #FIXED BUG from unittests: we need to set the gender of the child too, right? 
        #  might as well check both genders
        self.child.gender = Gender.FEMALE
        self.dad.add_child(self.child)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)

    def test_add_child_error(self):
        #FIXED BUG from unittests: we need to set the gender of the child too, right? 
        self.dad.gender = Gender.UNKNOWN
        self.child.gender = Gender.MALE
        with self.assertRaises(PersonError) as context:
            self.dad.add_child(self.child)
        self.assertIn('cannot add child', str(context.exception))
        self.assertIn('with unknown gender of parent', str(context.exception))

        #adding more tests to cover all possible cases - father set on top of father
        self.dad.gender = Gender.MALE
        self.dad.add_child(self.child)
        with self.assertRaises(PersonError) as context:
            self.dad.add_child(self.child)
        self.assertIn("already has father", str(context.exception))

        #adding more tests to cover all possible cases - mother set on top of mother
        self.mom.add_child(self.child)
        with self.assertRaises(PersonError) as context:
            self.mom.add_child(self.child)
        self.assertIn("already has mother", str(context.exception))

        #adding more tests to cover all possible cases - check for loops or impossibilities in graph
        self.root_child.gender = Gender.MALE

        #adding more tests to cover all possible cases - check for loops or impossibilities in graph
        with self.assertRaises(PersonError) as context:
            self.root_child.add_child(self.head_father)
        self.assertIn("is an ancestor of person", str(context.exception))

    def test_remove_father(self):
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotIn(self.child, self.dad.children)

    def test_remove_mother(self):
        self.child.set_mother(self.mom)
        self.child.remove_mother()
        #FIXED BUG from unittests: it's self.mom, not self.mother for our test cases
        self.assertNotIn(self.child, self.mom.children)

    def test_remove_father_error(self):
        #FIXED BUG from unittests: self.child doesn't initially have any parents set
        with self.assertRaises(PersonError) as context:
            self.child.remove_father()
        self.assertIn('father not set', str(context.exception))

        self.child.set_father(self.dad)
        self.dad.children.remove(self.child)
        with self.assertRaises(PersonError) as context:
            self.child.remove_father()
        self.assertIn('father named', str(context.exception))
        self.assertIn('does not have person named', str(context.exception))
        self.assertIn('in children', str(context.exception))

    def test_remove_mother_error(self):
        with self.assertRaises(PersonError) as context:
            self.child.remove_mother()
        self.assertIn('mother not set', str(context.exception))

        self.child.set_mother(self.mom)
        self.mom.children.remove(self.child)
        with self.assertRaises(PersonError) as context:
            self.child.remove_mother()
        self.assertIn('mother named', str(context.exception))
        self.assertIn('does not have person named', str(context.exception))
        self.assertIn('in children', str(context.exception))

    def test_get_persons_name(self):
        self.assertEqual(Person.get_persons_name(self.mom),"mom")
        self.assertEqual(Person.get_persons_name(None),"NA")

    def test_grandparents(self):
        grandparents_names = set([Person.get_persons_name(i) for i in self.root_child.grandparents()])
        true_grandparents = {'root_child_mom_mom', 'root_child_dad_mom', 
                                'root_child_mom_dad', 'root_child_dad_dad'}
        self.assertEqual(grandparents_names,true_grandparents)

    def test_all_grandparents(self):
        all_grandparents_names = set([Person.get_persons_name(i) for i in self.root_child.all_grandparents()])
        #FIXED BUG: all grandparents returns all grandparents + great-grands, etc...
        true_all_grandparents = {'root_child_dad_mom_dad', 'root_child_dad_dad_dad', 'root_child_dad_mom_mom', 
                            'root_child_mom_dad_dad', 'root_child_mom_dad_mom', 'root_child_mom_mom_dad', 
                            'root_child_mom_mom_mom', 'root_child_dad_dad_mom',
                            'root_child_mom_mom', 'root_child_dad_mom', 
                            'root_child_mom_dad', 'root_child_dad_dad'}
        self.assertEqual(all_grandparents_names,true_all_grandparents)

    def test_all_ancestors(self):
        all_ancestors = set([Person.get_persons_name(i) for i in self.root_child.all_ancestors()])
        true_all_ancestors = {'root_child_mom_dad', 'root_child_mom_dad_mom', 'root_child_mom_mom', 
                            'root_child_dad_dad_dad', 'root_child_dad_mom', 'root_child_mom', 'root_child_mom_dad_dad', 
                            'root_child_dad_mom_dad', 'root_child_dad_dad', 'root_child_mom_mom_mom', 
                            'root_child_dad_mom_mom', 'root_child_dad', 'root_child_mom_mom_dad', 
                            'root_child_dad_dad_mom'}
        self.assertEqual(all_ancestors, true_all_ancestors)

    def test_parents(self):
        parents = set([Person.get_persons_name(i) for i in self.root_child.parents()])
        true_parents = {'root_child_dad', 'root_child_mom'}
        self.assertEqual(parents, true_parents)

    def test_ancestors(self):
        '''ancestors code has already been 100% covered 
        in other unittests (multiple levels and depths)'''
        pass

    def test_ancestors_error(self):
        with self.assertRaises(PersonError) as context:
            self.root_child.ancestors(min_depth=2,max_depth=1)
        self.assertIn('max_depth (1) cannot be less than min_depth (2)', str(context.exception))

    def test_descendants(self):
        all_descendants = set([Person.get_persons_name(i) 
                              for i in self.head_father.descendants(min_depth=1,max_depth=float('inf'))])
        true_descendants = {'root_child_dad_dad', 'root_child_dad', 'root_child'}
        self.assertEqual(all_descendants, true_descendants)

    def test_descendants_error(self):
        with self.assertRaises(PersonError) as context:
            self.head_father.descendants(min_depth=2,max_depth=1)
        self.assertIn('max_depth (1) cannot be less than min_depth (2)', str(context.exception))

if __name__ == '__main__':
    unittest.main()