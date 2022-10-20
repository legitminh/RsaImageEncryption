class HuffmanTree:
    """
    Creates a huffman tree
    """

    def __init__(self, data: str, binary=False):
        # conversion is the dictionary that you can use to convert data into binary & vise versa
        self.conversion = {}

        # tree is a representation of the tree ([freq, val])
        self.tree = []
        if not binary:
            self.create_tree(data)

    def create_tree(self, data):
        # temp temporarily stores the chars and their frequencies (char: freq)
        temp = {}

        # getting the frequency
        for char in data:
            temp[char] = data.count(char)

        # transforing the info from temp into tree
        for char, freq in temp.items():
            self.tree.append([freq, char])

        # creating the branches
        while len(self.tree) > 1:  # while there is more than one branch

            # sorting tree by frequency
            self.tree.sort(key=lambda x: x[0])

            #
            n1 = self.tree.pop(0)
            n2 = self.tree.pop(0)

            # freq then the seperate branches
            self.tree.append([n1[0] + n2[0], [n1, n2]])
        # tree is now in [freq, branch] form

        # creating the coversion dictionary using recusion
        self.get_conversion(*self.tree)

    def get_conversion(self, branch, current_path=None):
        # just for initialization
        if current_path is None:
            current_path = ''

        # if the branch is just a value, then add it to the conversion dictionary with the path taken to get there
        if not isinstance(branch[1], list):
            self.conversion[current_path] = branch[1]
            return

        # getting the left and right branches of the tree
        self.get_conversion(branch[1][0], current_path + '0')
        self.get_conversion(branch[1][1], current_path + '1')

    def encode(self, data):
        out = ''
        conversion = {}
        for k, v in self.conversion.items():
            conversion[v] = k
        for char in data:
            out += conversion[char]
        return out

    def decode(self, data):
        out = ''
        path = ''
        for char in data:
            path += char
            if path in self.conversion:
                out += self.conversion[path]
                path = ''
        return out

    def binary_rep_of_tree(self):
        """
        The first byte serves as the length of the entire tree (in bytes)
        The next nyble is going to be the length of the path (in bits)
        The nyble following that is going to be the length of the item (in bits)
        Conversion table is stored like this:
        {'00110': '\\', '01101': 'x'}:
            Size     PathLen ItemLen Path   BinRep  Path   BinRep
            00000110 0110    0111    100110 1011100 101101 1111000
        """
        out = ''
        max_lens = [0, 0]
        for path, item in self.conversion.items():
            max_lens = [max(max_lens[0], len(path)+1), max(max_lens[1], len(bin(ord(item))[2:]))]

        #
        out += '0'*(4-len(bin(max_lens[0])[2:]))+bin(max_lens[0])[2:]
        out += '0'*(4-len(bin(max_lens[1])[2:]))+bin(max_lens[1])[2:]

        for path, item in self.conversion.items():
            out += '0'*(max_lens[0]-len(path)-1) + '1' + path
            n = len(bin(ord(item))[2:])
            out += '0'*(max_lens[1]-n) + bin(ord(item))[2:]
        return out+'0'*8

    def conv_bin_dict(self, binary):
        len_path = int(binary[0:4], 2)
        len_char = int(binary[4:8], 2)
        i = 8
        while binary[i:i+8] != '00000000':
            path = binary[i:i+len_path]
            path = path[path.find('1')+1:]
            i += len_path
            char = chr(int(binary[i:i+len_char], 2))
            i += len_char
            self.conversion[path] = char
        print(self.conversion)
        return self.decode(binary[i+8:])