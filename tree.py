# author: Anya Zhang
# date: 11/12/22
# file: tree.py implements a binary tree and expression tree ADT
# input: root of tree
# output: binary tree/expression tree ADT, evaluates expression tree

from stack import Stack

class BinaryTree:
    def __init__(self,rootObj=None):
        self.key = str(rootObj)
        self.leftChild = None
        self.rightChild = None

    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t

    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t

    def getRightChild(self):
        return self.rightChild

    def getLeftChild(self):
        return self.leftChild

    def setRootVal(self,obj):
        self.key = obj

    def getRootVal(self):
        return self.key

    def __str__(self):
        s = f"{self.key}"
        s += '('
        if self.leftChild != None:
            s += str(self.leftChild)
        s += ')('
        if self.rightChild != None:
            s += str(self.rightChild)
        s += ')'
        return s



class ExpTree(BinaryTree):

    def make_tree(postfix):
        stack = Stack()
        for i in postfix:
            # if number, push
            if i.replace('.', '', 1).isdigit():
                stack.push(i)
            # if operator, first pop becomes its rightChild, second pop becomes its leftChild
            elif i in "+-*/^":
                rightChild = stack.pop()
                leftChild = stack.pop()
                tree = ExpTree(i)
                # if item popped is already a tree, don't insert
                if type(rightChild) == ExpTree:
                    tree.rightChild = rightChild
                else:
                    tree.insertRight(rightChild)
                if type(leftChild) == ExpTree:
                    tree.leftChild = leftChild
                else:
                    tree.insertLeft(leftChild)
                # push tree with operator root back onto the stack
                stack.push(tree)
        # pop and return final stack value, the root node
        return stack.pop()
    

    @staticmethod
    def preorder(tree):
        s = ''
        if tree != []:
            s += tree.getRootVal()
            if tree.getLeftChild() != None:
                s += ExpTree.preorder(tree.getLeftChild())
            if tree.getRightChild() != None:
                s += ExpTree.preorder(tree.getRightChild())
        return s


    @staticmethod
    def inorder(tree):
        s = ''
        if tree != []: 
            if tree.getLeftChild() != None:
                s += '('
                s += ExpTree.inorder(tree.getLeftChild())
            s += tree.getRootVal()
            if tree.getRightChild() != None:
                s += ExpTree.inorder(tree.getRightChild())
                s += ')'
        return s


    @staticmethod  
    def postorder(tree):
        s = ''
        if tree != []:
            if tree.getLeftChild() != None:
                s += ExpTree.postorder(tree.getLeftChild()) 
            if tree.getRightChild() != None:
                s += ExpTree.postorder(tree.getRightChild())
            s += tree.getRootVal()
        return s


    # Source: https://www.geeksforgeeks.org/evaluation-of-expression-tree/
    def evaluate(tree):
        root = tree.getRootVal()
        # empty tree
        if root == None:
            return 0
        # leaf, base case
        if tree.getLeftChild() == None and tree.getRightChild() == None:
            return float(root)
    
        # evaluate left subtree recursively
        left_sum = ExpTree.evaluate(tree.getLeftChild())
        # evaluate right subtree recursively
        right_sum = ExpTree.evaluate(tree.getRightChild())
    
        if root == '+':
            return left_sum + right_sum
        elif root == '-':
            return left_sum - right_sum
        elif root == '*':
            return left_sum * right_sum
        elif root == '/':
            return left_sum / right_sum
        elif root == '^':
            return left_sum ** right_sum
        
            
    def __str__(self):
        return ExpTree.inorder(self)
   


# a driver for testing BinaryTree and ExpTree
if __name__ == '__main__':
    # test a BinaryTree
    r = BinaryTree('a')
    assert r.getRootVal() == 'a'
    assert r.getLeftChild()== None
    assert r.getRightChild()== None
    assert str(r) == 'a()()'
    
    r.insertLeft('b')
    assert r.getLeftChild().getRootVal() == 'b'
    assert str(r) == 'a(b()())()'
    
    r.insertRight('c')
    assert r.getRightChild().getRootVal() == 'c'
    assert str(r) == 'a(b()())(c()())'
    
    r.getLeftChild().insertLeft('d')
    r.getLeftChild().insertRight('e')
    r.getRightChild().insertLeft('f')
    assert str(r) == 'a(b(d()())(e()()))(c(f()())())'

    assert str(r.getRightChild()) == 'c(f()())()'
    assert r.getRightChild().getLeftChild().getRootVal() == 'f'

    
    # test an ExpTree
    postfix = '5 2 3 * +'.split()
    tree = ExpTree.make_tree(postfix)
    # print(str(tree))
    # print(ExpTree.inorder(tree))
    # print(ExpTree.postorder(tree))
    # print(ExpTree.preorder(tree))
    # print(ExpTree.evaluate(tree))
    assert str(tree) == '(5+(2*3))'
    assert ExpTree.inorder(tree) == '(5+(2*3))'
    assert ExpTree.postorder(tree) == '523*+'
    assert ExpTree.preorder(tree) == '+5*23'
    assert ExpTree.evaluate(tree) == 11.0

    postfix = '5 2 + 3 *'.split()
    tree = ExpTree.make_tree(postfix)
    # print(str(tree))
    # print(ExpTree.inorder(tree))
    # print(ExpTree.postorder(tree))
    # print(ExpTree.preorder(tree))
    # print(ExpTree.evaluate(tree))
    assert str(tree) == '((5+2)*3)'
    assert ExpTree.inorder(tree) == '((5+2)*3)'
    assert ExpTree.postorder(tree) == '52+3*'
    assert ExpTree.preorder(tree) == '*+523'
    assert ExpTree.evaluate(tree) == 21.0

    print("Everything works correctly!")

    postfix = '1.3 2.7 + 2.02 0.02 - 1 + 6.5 + *'.split()
    #print(postfix)
    tree = ExpTree.make_tree(postfix)
    #print(str(tree))
    #print(ExpTree.evaluate(tree))