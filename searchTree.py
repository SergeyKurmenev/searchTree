class SearchTree:

    def __init__(self, value=None):
        if value is None:
            self.baseNode = None
        else:
            self.baseNode = Node(value)

    def insert(self, value):
        if self.baseNode is not None:
            self.baseNode.insert(value)
        else:
            self.baseNode = Node(value)

    def find(self, value):
        if self.baseNode is not None:
            return self.baseNode.find(value)
        else:
            return None

    def delete(self, value):
        if self.baseNode is not None:
            if self.baseNode.value is value:
                # удаление baseNode
                if not self.baseNode.has_children():
                    self.baseNode = None
                elif self.baseNode.has_one_child():
                    if self.baseNode.left is not None:
                        self.baseNode = self.baseNode.left
                    else:
                        self.baseNode = self.baseNode.right
                else:
                    self.baseNode = self.baseNode.delete(value)
            else:
                self.baseNode.delete(value)

    def traverse(self):
        if self.baseNode is not None:
            self.baseNode.traverse()
        else:
            print('Empty')


class Node:

    def __init__(self, value, parent=None, left=None, right=None):
        self.parent = parent
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return '{}'.format(self.value)

    def insert(self, new_value):
        if self.value is not new_value:
            if new_value > self.value:
                if self.right is not None:
                    self.right.insert(new_value)
                else:
                    self.right = Node(new_value, self)
            elif new_value < self.value:
                if self.left is not None:
                    self.left.insert(new_value)
                else:
                    self.left = Node(new_value, self)
        else:
            print(new_value, "already in tree")

    def find(self, searching_value):
        result = None

        if self.value is searching_value:
            result = self
        else:
            if searching_value > self.value:
                if self.right is not None:
                    result = self.right.find(searching_value)
            else:
                if self.left is not None:
                    result = self.left.find(searching_value)

        return result

    def traverse(self):
        if self.left is not None:
            self.left.traverse()
        print(self.value)
        if self.right is not None:
            self.right.traverse()

    def delete(self, value_for_delete):

        node_for_delete = self.find(value_for_delete)

        if node_for_delete is not None:

            # удаление крайнего элемента(без child элементов)
            if not node_for_delete.has_children():

                if node_for_delete.is_left():
                    node_for_delete.parent.left = None
                else:
                    node_for_delete.parent.right = None

            # удаление элемена, имеющего 1 child элемент
            elif node_for_delete.has_one_child():

                if node_for_delete.is_left():

                    if node_for_delete.left is not None:
                        node_for_delete.parent.left, node_for_delete.left.parent = \
                            node_for_delete.left, node_for_delete.parent
                    else:
                        node_for_delete.parent.left, node_for_delete.right.parent = \
                            node_for_delete.right, node_for_delete.parent
                else:
                    if node_for_delete.left is not None:
                        node_for_delete.parent.right, node_for_delete.left.parent = \
                            node_for_delete.left, node_for_delete.parent
                    else:
                        node_for_delete.parent.right, node_for_delete.right.parent = \
                            node_for_delete.right, node_for_delete.parent

            # удаление элемента, имеющего оба child элемента
            else:
                # элемент, которым будет заменён удаляемый
                node_for_replace = node_for_delete.find_min_above()

                # ближайший элемент, который больше чем удаляемый - оказался его right child
                if node_for_delete.right is node_for_replace:
                    node_for_replace.left = node_for_delete.left
                    node_for_delete.left.parent = node_for_replace
                    if node_for_delete.parent is None:
                        # если удалялся baseNode - возвращается replace элемент для установки в кач-ве baseNode
                        node_for_replace.parent = None
                        return node_for_replace
                    else:
                        # если удалялся не baseNode
                        if node_for_delete.is_left():
                            node_for_delete.parent.left = node_for_replace
                            node_for_replace.parent = node_for_delete.parent
                        else:
                            node_for_delete.parent.right = node_for_replace
                            node_for_replace.parent = node_for_delete.parent

                else:
                    if node_for_replace.right is not None:
                        # если у replace елемента есть right child - отвязывается от replace элемента и привязывается
                        # к replace.parent - в роли left child
                        node_for_replace.parent.left = node_for_replace.right
                        node_for_replace.right.parent = node_for_replace.parent

                    # left и right от delete элемента переходят к replace элементу
                    node_for_replace.left, node_for_replace.right = \
                        node_for_delete.left, node_for_delete.right
                    node_for_delete.left.parent, node_for_delete.right.parent = \
                        node_for_replace, node_for_replace

                    if node_for_delete.parent is None:
                        # если удалялся baseNode - возвращается replace элемент для установки в кач-ве baseNode
                        node_for_replace.parent = None
                        return node_for_replace
                    else:
                        # иначе replace привязывается к delete.parent
                        if node_for_delete.is_left():
                            node_for_delete.parent.left = node_for_replace
                        else:
                            node_for_delete.parent.right = node_for_replace

    def find_min_above(self):
        min_above = self.right
        while min_above.left is not None:
            min_above = min_above.left
        return min_above

    def has_one_child(self):
        return ((self.left is not None) and (self.right is None)) or ((self.left is None) and (self.right is not None))

    def is_left(self):
        return self.parent.left is self

    def has_children(self):
        return self.left or self.right is not None
