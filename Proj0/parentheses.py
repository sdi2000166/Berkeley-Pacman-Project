class Stack:

    def __init__(self): # Initialization of the stack:
        self.stack = [] # The stack will be implemented by using a list.
        self.count = 0 # 'count' will represent the total items currently in the stack.

    def push(self, item): # This function adds a given item at the top of the stack.
        self.count += 1 # Increase the number of items in the stack by 1.
        newItem = [item] # Make a list that contains the new item.
        self.stack += newItem # Combine the new list with the previous list.

    def pop(self): # This function removes and returns the item at the top of the stack.
        poppedItem = self.stack[-1] # Save the item in 'poppedItem'.
        self.count -= 1 # Decrease the number of items in the stack by 1.
        newStack = [] # Make a new list, that will contain all the stack's items except the top-most one.
        for i in range(0, self.count): # 'self.count' has already been decreased, so there's no need to write range( 0, self.count - 1 )
            newStack += self.stack[i] # Copy the i-th item of the stack to the new list.
        self.stack = newStack # 'self.stack' now contains the new list, without the popped item.
        return poppedItem # Return the popped item.

    def empty(self): # This function checks if the stack is empty.
        if self.count > 0: # If there's at least one item in the stack:
            return False # The stack is not empty.
        return True # Otherwise, it is indeed empty.

        
def equal(str): # This function recieves a string that consists of (,),[,],{,} and checks if they are properly paired.
# It does not check if the string contains other character besides the ones mentioned above.
    
    stack = Stack() # Initialize a stack.

    for i in range(0, len(str)): # For every character in the string:
        if stack.empty(): # If the stack is empty: push the currect string character in the stack.
            stack.push(str[i])
        else: # If the stack is not empty, pop it.
            stackEnd = stack.pop()
            if (str[i] == ')' and stackEnd == '(') or (str[i] == ']' and stackEnd == '[') or (str[i] == '}' and stackEnd == '{'):
                # If the current character in the string is a closing parenthesis 
                # and the popped item of the stack is an opening parenthesis of the same type:
                continue # Move on.
            else: # Otherwise, push the popped item back in the stack, along with the current character in the string.
                stack.push(stackEnd)
                stack.push(str[i])

    if stack.empty(): # If the stack end up empty, then all the parentheses in the string were correctly paired up.
        print('The parentheses were paired correctly.')
        return True
    print('The parentheses were paired incorrectly.') # If the stack is not empty, then the parentheses were paired incorrectly.
    return False