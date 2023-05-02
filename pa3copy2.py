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
			#regex_copy = regex_copy[1:]
			if ch != " ":
				print(ch)
				if ch in self.terminals:
					operand_stack.append(Node(value=ch))
				elif ch == "(":
					operator_stack.append(ch)
				elif ch == ")":
					while operator_stack[-1] != "(":
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
						operand_stack.append(temp_tree)
						if len(operator_stack) == 0:
							raise InvalidExpression
					operator_stack.pop()
				else:
					if ch in self.operators:
						if len(operator_stack) > 0:
							print("here")
							if self.is_ge_precedence(operator_stack[-1], ch):
								print("here2")
								print(operator_stack[-1])
								temp_tree = None
								if operator_stack[-1] in ['|', '~']: #binary operators
									print("here4")
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
									print("here3")
									lc = operand_stack.pop()
									if type(lc) != Node:
										lc = Node(value=lc)
									value = operator_stack.pop()
									if type(value) == Node:
										value = value.value #good
									temp_tree = Node(value=value, left_child=lc)
								else:
									raise InvalidExpression
								operator_stack.append(ch)
								operand_stack.append(temp_tree)
							else:
								operator_stack.append(ch)
						else:
							operator_stack.append(ch)
			regex_copy = regex_copy[1:]
			print("operands")
			self.print_stack(operand_stack)
			print("operators")
			self.print_stack(operator_stack)
			print("-----")

		try:
			while len(operator_stack) > 0:
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
				operand_stack.append(temp_tree)
		except:
			raise InvalidExpression

		#print("operand stack")
		#self.print_stack(operand_stack)
		if len(operand_stack) > 1:
			raise InvalidExpression
		
		self.syntax_tree = operand_stack.pop()

		print(self.print_syntax_tree(self.syntax_tree))


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

