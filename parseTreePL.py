#!/usr/bin/python

#-------------------------------------------------------------------------------------------#
# Author: Kinzang Chhogyal
# Email: kindrix@gmail.com
#
#Module to check if a given sentence is a well formed forumal (wff) of propostional logic
#The program is based on the idea of using difference lists used for DCG in Prolog (It may be used in in other languages as well.) More information can 
#be found at http://www.learnprolognow.org/lpnpage.php?pagetype=html&pageid=lpn-htmlse28.

#The following are the wff rules that I've used:

# formula : atom
# formula : ~ formula
# formula : (formula   operator  formula)
# operator : {&, |, ->, <->} 
# atom: a, c, d, ...z

#Examples of valid and invalid formulas:
# a : valid
# ~b : valid
# ~(c): invalid
# ~(c & d) : valid
# (c & d :invalid
# ((c & d ) -> (b & ( e -> f)) ) : valid

#-------------------------------------------------------------------------------------------#


#return list of chars and also remove spaces
def stringToCharList(exp):
	charList = []
	for char in exp:
		if (not(char == ' ')):
			charList.append(char)
	return charList


# recursive definition of a wff

def consume_formula(symList, depth, parseTree):
	#symListCopy = list(symList)
	#print 'current list:', symList

	#cosume an atom
	#formula: atom

	is_atom, symList, atom = consume_atom(symList)
	if is_atom:
		parseTree.append((depth, atom))
		return 1, symList, depth


	#consume negation followed by formula
	#formula: ~ formula

	is_negation, symList, negation = consume_negation(symList)
	if is_negation:
		parseTree.append((depth, negation))
		is_formula, symList, depth = consume_formula(symList, depth + 1, parseTree)
		if is_formula:			
			return 1, symList, depth


	#consume an opening bracket followed by a formula, operator and a closing bracket
	#formula: (formula operator formula)

	is_open_bracket, symList = consume_open_bracket(symList)
	if is_open_bracket:
		currentDepth = depth
		is_formula, symList, leftDepth = consume_formula(symList, depth + 1, parseTree)
		if is_formula:
			is_operator, symList, operator = consume_operator(symList)
			if is_operator:
				parseTree.append((currentDepth, operator))
				is_formula, symList, rightDepth = consume_formula(symList, currentDepth + 1, parseTree)
				if is_formula:
					is_closing_bracket, symList = consume_closing_bracket(symList)
					if is_closing_bracket:
						if (leftDepth > rightDepth):
							depth =  leftDepth
						else:
							depth = rightDepth
						return 1, symList, depth
	# 				else:
	# 					return 0, symList
	# 			else:
	# 				return 0, symList
	# 		else:
	# 			return 0, symList
	# 	else:
	# 		return 0, symList
	# else:
	# 	return 0, symList

	
	#all rules fails
	return 0, symList, depth


# consume an atom and return remaining list

def consume_atom(symList):
	if (len(symList) == 0):
		return 0, symList, None
	if ( symList[0].isalpha() ):
		atom = symList[0]
		symList.remove(symList[0])
		return 1, symList, atom
	return 0, symList, None

# consume negation symbol and return remaining list

def consume_negation(symList):
	if (len(symList) == 0):
		return 0, symList, None
	if ( symList[0] == '~' ):
		negation = symList[0]
		symList.remove(symList[0])
		return 1, symList, negation
	return 0, symList, None


# consume an open bracket '(' and return remaining list

def consume_open_bracket(symList):
	if (len(symList) == 0):
		return 0, symList
	if ( symList[0] == '(' ):
		symList.remove(symList[0])
		return 1, symList
	return 0, symList

# consume closing bracket ')' and  return remaining list

def consume_closing_bracket(symList):
	if (len(symList) == 0):
		return 0, symList
	if (symList[0] == ')' ):
		symList.remove(symList[0])
		return 1, symList
	return 0, symList

# consume an operator and return remaining list

def consume_operator(symList):
	if (len(symList) == 0):
		return 0, symList, None
	#and, or
	if ( symList[0] in ['&', '|']  ):
		operator = symList[0]
		symList.remove(symList[0])
		return 1, symList, operator
	#implication
	elif (symList[0] == '-' and symList[1] == '>'):
		operator = symList[0] + symList[1]
		symList.remove(symList[0])
		symList.remove(symList[0])
		return 1, symList, operator
	#biconditional
	elif (symList[0] == '<' and symList[1] == '-' and symList[2] == '>'):
		operator = symList[0] + symList[1] + symList[3]
		symList.remove(symList[0])
		symList.remove(symList[0])
		symList.remove(symList[0])
		return 1, symList, operator
	return 0, symList, None


#main function to check if formula is valid
#returns 1 if valid , 0 otherwise

def checkValidFormula(symList):
	startDepth = 0
	parseTree = []
	is_formula, symList, depth = consume_formula(symList, startDepth, parseTree)
	print 'Final after consumption:', symList
	if (is_formula and len(symList) == 0):
		print "Depth is: ", depth
		print "Parse Tree: \n", parseTree
		return 1
	return 0

#program execution starts here

exp = raw_input('Enter sentence:')
#exp = 'a & b'
expList = stringToCharList(exp)
print '\nChecking expression: %s ' %exp
print 'List representation: %s' % expList

if checkValidFormula(expList):
	print('valid')
else:
	print('invalid')



