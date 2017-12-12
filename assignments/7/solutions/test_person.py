""" Test Person

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2017-12-09
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

        # TODO: uncomment these lines:: make a deep family history
        '''
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
        '''

    def test_set_mother(self):
        self.child.set_mother(self.mom)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)

    '''TODO: uncomment these lines!
    
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
        self.mom.add_child(self.child)
        self.assertEqual(self.child.mother, self.mom)
        self.assertIn(self.child, self.mom.children)

        self.assertNotIn(self.child, self.dad.children)
        self.dad.add_child(self.child)
        self.assertEqual(self.child.father, self.dad)
        self.assertIn(self.child, self.dad.children)

    def test_add_child_error(self):
        self.dad.gender = Gender.UNKNOWN
        with self.assertRaises(PersonError) as context:
            self.dad.add_child(self.child)
        self.assertIn('cannot add child', str(context.exception))
        self.assertIn('with unknown gender', str(context.exception))

    def test_remove_father(self):
        self.child.set_father(self.dad)
        self.child.remove_father()
        self.assertNotIn(self.child, self.dad.children)

    def test_remove_mother(self):
        self.child.set_mother(self.mom)
        self.child.remove_mother()
        self.assertNotIn(self.child, self.mother.children)

    def test_remove_father_error(self):
        pass

    def test_remove_mother_error(self):
        pass

    def test_get_persons_name(self):
        pass

    def test_grandparents(self):
        pass

    def test_all_grandparents(self):
        pass

    def test_all_ancestors(self):
        pass

    def test_ancestors(self):
        pass

    def test_ancestors_error(self):
        pass

    '''

    #TODO: 

if __name__ == '__main__':
    unittest.main()