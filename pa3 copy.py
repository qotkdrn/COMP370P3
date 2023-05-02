# Name: pa3.py
# Author(s):
# Date:
# Description:

class InvalidExpression(Exception):
	pass

class Node:
	def __init__(self, value=None, left_child=None, right_child=None):
		self.value = value
		self.left_child = left_child
		self.right_child = right_child


class RegEx:
	def __init__(self, filename):
		""" 
		Initializes a RegEx object from the specifications
		in the file whose name is filename.
		"""
		f = open(filename, 'r')
		self.precedence_dict = {'*' : 3, '~' : 2, '|' : 1}
		self.alphabet = [ch for ch in f.readline().strip("\n\t \r")]
		self.terminals = self.alphabet.copy()
		self.terminals.append('N') #null set
		self.terminals.append('e') #empty string
		self.regex = f.readline().strip("\n\t \r")
		self.operators = ['|', '*', '~']

		operand_stack = []
		operator_stack = []

		regex_copy = self.get_cleaned_regex(self.regex)
		print(self.get_cleaned_regex(self.regex))
		while len(regex_copy) > 0:
			ch = regex_copy[0]
			if ch != " ":
				print(ch)
				if ch in self.terminals:
					operand_stack.append(Node(value=ch))
				elif ch == "(":
					operator_stack.append(ch)
				elif ch == ")":
					while operator_stack[-1] != "(":
						temp_tree = self.get_subtree(operator_stack, operand_stack)
						operand_stack.append(temp_tree)
						if len(operator_stack) == 0:
							raise InvalidExpression
					operator_stack.pop()
				else:
					if ch in self.operators:
						if len(operator_stack) > 0:
							if self.is_ge_precedence(operator_stack[-1], ch):
								temp_tree = self.get_subtree(operator_stack, operand_stack)
								operator_stack.append(ch)
								operand_stack.append(temp_tree)
							else:
								operator_stack.append(ch)
						else:
							operator_stack.append(ch)
			regex_copy = regex_copy[1:]

		try:
			while len(operator_stack) > 0:
				temp_tree = self.get_subtree(operator_stack, operand_stack)
				operand_stack.append(temp_tree)
		except:
			raise InvalidExpression

		if len(operand_stack) > 1:
			raise InvalidExpression
		
		self.syntax_tree = operand_stack.pop()

		print(self.print_syntax_tree(self.syntax_tree))

		self.state_name_counter = 1 #used in the naming of states

		nfa_tuple = self.get_nfa_from_ast(self.syntax_tree)

		start_states = nfa_tuple[0]
		accept_states = nfa_tuple[1]
		transitions = nfa_tuple[2]

		print(start_states)
		print(accept_states)
		print(transitions)


	def is_ge_precedence(self, op1, op2):
		if op1 in ['(', ')']:
			return False
		return self.precedence_dict[op1] >= self.precedence_dict[op2]

	def print_syntax_tree(self, syntax_tree):
		if syntax_tree.left_child == None:
			return str(syntax_tree.value)
		elif syntax_tree.right_child == None:
			return "(" + self.print_syntax_tree(syntax_tree.left_child) + "<-" + str(syntax_tree.value) + ")"
		else:
			return "(" + self.print_syntax_tree(syntax_tree.left_child) + "<-" + str(syntax_tree.value) + "->" + self.print_syntax_tree(syntax_tree.right_child) + ")" 
			
	def print_stack(self, stack):
		for item in stack:
			if type(item) == Node:
				print(item.value)
			else:
				print(item)
	
	def get_cleaned_regex(self, regex):
		starters = [')', '*'] + self.terminals
		enders = ['('] + self.terminals
		new_regex = ""
		for ch in regex:
			if ch != " ":
				new_regex += ch

		i = 0
		while i < len(new_regex) - 1:
			ch = new_regex[i]
			next_symbol = new_regex[i+1]
			if ch in starters and next_symbol in enders:
				new_regex = new_regex[:i+1] + "~" + new_regex[i+1:]
			i += 1
		return new_regex

	def get_subtree(self, operator_stack, operand_stack):
		temp_tree = None
		if operator_stack[-1] in ['|', '~']: #binary operators
			rc = operand_stack.pop()
			if type(rc) != Node:
				rc = Node(value=rc)
			lc = operand_stack.pop()
			if type(lc) != Node:
				lc = Node(value=lc)
			value = operator_stack.pop()
			if type(value) == Node:
				value = value.value #good
			temp_tree = Node(value=value, left_child=lc, right_child=rc)
		elif operator_stack[-1] == '*': #unary operators
			lc = operand_stack.pop()
			if type(lc) != Node:
				lc = Node(value=lc)
			value = operator_stack.pop()
			if type(value) == Node:
				value = value.value #good
			temp_tree = Node(value=value, left_child=lc)
		else:
			raise InvalidExpression
		return temp_tree

	def get_nfa_from_ast(self, ast):
		if ast.left_child == None and ast.right_child == None:
			return self.get_leaf_nfa(ast)
		elif ast.right_child == None:
			return self.get_unary_nfa(self.get_nfa_from_ast(ast.left_child))	
		else:
			return self.get_binary_nfa(ast.value, self.get_nfa_from_ast(ast.left_child), self.get_nfa_from_ast(ast.right_child))

	def get_leaf_nfa(self, ast):
		if ast.value == 'e':
			start_states = [str(self.state_name_counter)]
			accept_states = [str(self.state_name_counter)]
			self.state_name_counter += 1
			transitions = {}
			return (start_states, accept_states, transitions)
		elif ast.value == 'N':
			start_states = [str(self.state_name_counter)]
			accept_states = []
			self.state_name_counter += 1
			transitions = {}
			return (start_states, accept_states, transitions)
		else:
			start_states = [str(self.state_name_counter)]
			self.state_name_counter += 1
			accept_states = [str(self.state_name_counter)]
			self.state_name_counter += 1
			transitions = {start_states[0] : {ast.value : accept_states}}
			return (start_states, accept_states, transitions)

	def get_unary_nfa(self, nfa_tuple):
		start_states = nfa_tuple[0]
		accept_states = nfa_tuple[1]
		transitions = nfa_tuple[2]
		for accept_state in accept_states:
			if accept_state not in transitions.keys():
				transitions[accept_state] = {}
			transitions[accept_state] = {'e' : start_states}

		return (start_states, accept_states, transitions)

	def get_binary_nfa(self, operator, nfa_tuple1, nfa_tuple2):
		start_states1 = nfa_tuple1[0]
		accept_states1 = nfa_tuple1[1]
		transitions1 = nfa_tuple1[2]
		start_states2 = nfa_tuple2[0]
		accept_states2 = nfa_tuple2[1]
		transitions2 = nfa_tuple2[2]
		if operator == "|":
			new_start_states = [self.state_name_counter]
			self.state_name_counter += 1
			new_accept_states = accept_states1 + accept_states2

			new_transitions = {**transitions1, **transitions2} #merge dictionaries
			new_transitions[new_start_states[0]] = {}

			prev_start_states = start_states1 + start_states2
			new_transitions[new_start_states[0]]['e'] = prev_start_states
			return (new_start_states, new_accept_states, new_transitions)
		elif operator == "~":
			new_start_states = start_states1
			new_accept_states = accept_states2
			new_transitions = {**transitions1, **transitions2} #merge dictionaries
			for accept_state in accept_states1:
				if accept_state not in new_transitions.keys():
					new_transitions[accept_state] = {}
				new_transitions[accept_state]['e'] = start_states2
			return (new_start_states, new_accept_states, new_transitions)
		else:
			raise InvalidExpression


		


	def simulate(self, str):
		"""
		Returns True if the string str is in the language of
		the "self" regular expression.
		"""
		pass  # replace this with your code
	
	# you will likely add other methods to this class

# you can add other classes here, including DFA and NFA (modified to suit
# the needs of this project).

tester = RegEx("regextest.txt")

