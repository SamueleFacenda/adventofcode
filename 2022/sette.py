max_size = 100000

class Element(object):
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
    def get_size(self):
        return 0
    def get_parent(self):
        return self.parent

class File(Element):
    def __init__(self, name, size, parent=None):
        Element.__init__(self, name, parent)
        self.size = size
    def get_size(self):
        return self.size

class Directory(Element):
    def __init__(self, name, parent=None):
        Element.__init__(self, name, parent)
        self.elements = []
        self.size = None
    def add_element(self, element):
        self.elements.append(element)
        self.size = None
    def get_size(self):
        if self.size is not None:
            return self.size
        size = 0
        for element in self.elements:
            size += element.get_size()
        self.size = size
        return size
    def add_to_list(self, list):
        if self.get_size() <= max_size:
            list.append(self)
        for child in self.elements:
            if isinstance(child, Directory):
                child.add_to_list(list)
    def get_son_by_name(self, name):
        for child in self.elements:
            if child.name == name:
                return child
        print('error: son not found', name)
        return None

nome_home = 'samu_home_not_exist_in_challenge_12940124'

home = Directory(nome_home)
current_dir = home

with open('input','r') as f:
    for line in f.readlines():
        if line.startswith('$ ls'):
            continue
        if line.startswith('$ cd'):
            goto = line.split()[2]
            if goto == '..':
                current_dir = current_dir.get_parent()
            elif goto == '/':
                current_dir = home
            else:
                current_dir = current_dir.get_son_by_name(goto)

        else:
            size, name = line.split()
            if size == 'dir':
                new_dir = Directory(name, current_dir)
                current_dir.add_element(new_dir)
            else:
                new_file = File(name, int(size), current_dir)
                current_dir.add_element(new_file)

smaller_than_max = []
home.add_to_list(smaller_than_max)

sum = 0
for dir in smaller_than_max:
    if dir.name != nome_home:
        sum += dir.get_size()
print(smaller_than_max)
print(sum)