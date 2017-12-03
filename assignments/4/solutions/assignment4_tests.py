#!/usr/bin/env python

from assignment4 import *
import copy

print("TESTING...")
print("Checking with normal well formatted input...")

try:
	test = Pedigree()
	test.load_people("ryan_pedigree.txt")
	test.load_variants("test_variants.txt")
	print("Normal input works!")
except BaseException as error:
	print("FAILED: Couldn't run with standard input.")
	print(error)

print("Checking with malformed people DB input..")
print("\nduplicated person")
try:
	test = Pedigree()
	test.load_people("ryan_pedigree_dupperson.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nnonDAG")
try:
	test = Pedigree()
	test.load_people("ryan_pedigree_nonDAG.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nparents not in set")
try:
	test = Pedigree()
	test.load_people("ryan_pedigree_parentsnotinset.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nselfloop")
try:
	test = Pedigree()
	test.load_people("ryan_pedigree_selfloop.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nwrong gender")
try:
	test = Pedigree()
	test.load_people("ryan_pedigree_wronggender.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("")
print("All people DB tests passed.")
print("Checking variants DB tests...")

test = Pedigree()
test.load_people("ryan_pedigree.txt")

print("\nalt allele wrong")
try:
	test2 = copy.deepcopy(test)
	test2.load_variants("test_variants_altimproper.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nref allele wrong")
try:
	test2 = copy.deepcopy(test)
	test2.load_variants("test_variants_refimproper.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nimproper chrom")
try:
	test2 = copy.deepcopy(test)
	test2.load_variants("test_variants_improperchrom.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nperson not in db")
try:
	test2 = copy.deepcopy(test)
	test2.load_variants("test_variants_personnotindataset.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nredundant position")
try:
	test2 = copy.deepcopy(test)
	test2.load_variants("test_variants_redundantpos.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("\nvariant out of range")
try:
	test2 = copy.deepcopy(test)
	test2.load_variants("test_variants_varoutofrange.txt")
	raise Exception("TEST FAILED")
except AssertionError as msg:
	print("caught exception %s" % str(msg).replace("\t",""))

print("")
print("ALL TESTS PASSED :D")