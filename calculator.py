# author: Anya Zhang
# date: 11/12/22
# file: calculator.py emulates a simple calculator that operates on non-negative float and integer numbers. 
# The program will ask the user to enter an arithmetic expression and output the result. 
# input: infix expression
# output: postfix expression and calculated answer 

from tree import ExpTree
from stack import Stack

def infix_to_postfix(infix):
    stack = Stack()
    postfix = ""
    priority = {'+':1, '-':1, '*':2, '/':2, '^':3} 
    i = 0

    while i < len(infix):
        char = infix[i]
        # if number: add to postfix
        if char.replace('.', '', 1).isdigit():
            # find end index of the number (if there are multiple digits)
            end_num = len(infix)
            for j in range(i, len(infix)):
                if infix[j] not in "1234567890.":
                    end_num = j
                    break
            num = infix[i:end_num]
            postfix += num + " "
            i += len(num) - 1

        # if open parenthesis: push to stack
        elif char == '(':
            stack.push(char)

        # Source: https://favtutor.com/blogs/infix-to-postfix-conversion
        # if operator: add to postfix if higher priority than operator at top of stack
        # if lower priority, pop operators from the stack until there operator at top has lower priority or the stack becomes empty
        elif char in priority.keys():
            while not stack.isEmpty() and stack.peek() != '(' and priority[char] <= priority[stack.peek()]:
                postfix += stack.pop() + " "
            stack.push(char)

        # if closed parenthesis: pop stack and add to postfix until open parenthesis is reached
        elif char == ')':
            while True:
                popped = stack.pop()
                if popped == '(':
                    break
                postfix += popped + " "
        
        i += 1
                
    # pop stack and add to the postfix 
    while not stack.isEmpty():
        postfix += stack.pop() + " "
    # remove extra space at end
    postfix = postfix[0:len(postfix)-1]
    return postfix


def calculate(infix):
    postfix = infix_to_postfix(infix)
    tree = ExpTree.make_tree(postfix.split())
    return ExpTree.evaluate(tree)


def main_menu():
    print("Welcome to Calculator Program!")
    while True:
        i = input("Please enter your expression here. To quit enter 'quit' or 'q':\n")
        if i == 'quit' or i == 'q':
            print("Goodbye!")
            break
        answer = calculate(i)
        print(answer)



# a driver to test calculate module
if __name__ == '__main__':

    # test infix_to_postfix function
    assert infix_to_postfix('(5+2)*3') == '5 2 + 3 *'
    assert infix_to_postfix('5+2*3') == '5 2 3 * +'

    # test calculate function
    assert calculate('(5+2)*3') == 21.0
    assert calculate('5+2*3') == 11.0
    #print(infix_to_postfix('((3^2-4)*(5-2))-(2^3+1)'))
    #print(calculate('((3^2-4)*(5-2))-(2^3+1)'))

    main_menu()