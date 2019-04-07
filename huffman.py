import random
import time
"""
CSCI-665: LAB Assignment 2
Author: Srushti Kotak (sk7735)
"""


def generate_input(filename, linecount):
    """
    creates a random text file for input
    :param filename: name of the text file to be generated
    :param linecount: number of lines
    :return: None
    """
    nouns = ("crow", "khaleesi", "maester", "pyromancer", "raven", "valyrian", "warg")
    verbs = ("eats", "fights", "jumps", "flys", "thinks", "tolerates")
    adv = ("slowly.", "dutifully.", "foolishly.", "sadly.", "occasionally.", "rapidly.")
    adj = ("hot", "icy", "wet", "clueless", "madly", "odd", "stupid")

    all = [nouns, verbs, adj, adv]

    with open(filename, 'w') as f:
        for i in range(linecount):
            f.writelines([' '.join([random.choice(i) for i in all]), '\n'])


def estimated_frequency(input_string):
    """
    This function creates 2 lists having estimated frequency of each character
    and a list of characters in input string.
    :param input_string: input text data in string
    :return: lists of frequency of characters and only characters
    """
    freq_characters = []
    list_ch = []
    estimates = {"a": 8.167, "b": 1.492, "c": 2.782, "d": 4.253, "e": 12.702, "f": 2.228, "g": 2.015, "h": 6.094,
                 "i": 6.966, "j": 0.153, "k": 0.772, "l": 4.025, "m": 2.406, "n": 6.749, "o": 7.507, "p": 1.929,
                 "q": 0.095, "r": 5.987, "s": 6.327, "t": 9.056, "u": 2.758, "v": 0.978, "w": 2.360, "x": 0.150,
                 "y": 1.974, "z": 0.074, "\n": 5.012, ".": 4.210, " ": 10.650}
    for ch in input_string:
        if ch not in freq_characters:
            freq = estimates[ch] * len(input_string) / 100
            freq_characters.append(freq)
            freq_characters.append(ch)
            list_ch.append(ch)
    return freq_characters, list_ch


def frequency(input_string):
    """
    This function creates 2 lists having actual frequency of each character
    and a list of characters in input string.
    :param input_string: input text data in string
    :return: lists of frequency of characters and only characters
    """
    freq_characters = []
    list_ch = []
    for ch in input_string:
        if ch not in freq_characters:
            list_ch.append(ch)
            freq = input_string.count(ch)
            freq_characters.append(freq)
            freq_characters.append(ch)
    return freq_characters, list_ch


def generate_nodes(freq_characters):
    """
    This function generates nodes for the huffman tree and then calls the merge function
    which builds the huffman tree
    :param freq_characters: list of frequency of each character
    :return: huffman tree
    """
    nodes = []
    while len(freq_characters) > 0:
        nodes.append(freq_characters[0:2])
        freq_characters = freq_characters[2:]
    nodes.sort()
    huffman_tree = []
    huffman_tree.append(nodes)
    huffman_tree = merge(nodes, huffman_tree)
    return huffman_tree


def merge(nodes, huffman_tree):
    """
    This function merges nodes from bottom to top and builds the tree
    :param nodes: list of nodes
    :param huffman_tree: tree
    :return: huffman tree
    """
    index = 0
    updated_node = []
    if len(nodes) > 1:
        nodes.sort()
        nodes[index].append("0")
        nodes[index+1].append("1")
        join_1 = (nodes[index][0] + nodes[index + 1][0])
        join_2 = (nodes[index][1] + nodes[index + 1][1])
        updated_node.append(join_1)
        updated_node.append(join_2)
        newnodes = []
        newnodes.append(updated_node)
        newnodes = newnodes + nodes[2:]
        nodes = newnodes
        huffman_tree.append(nodes)
        merge(nodes, huffman_tree)
    return huffman_tree


def create_huffman_list(huffman_tree):
    """
    creates a list of huffman tree
    :param huffman_tree:
    :return: list
    """
    huffman_tree.sort(reverse=True)
    checklist = []
    for level in huffman_tree:
        for node in level:
            if node not in checklist:
                checklist.append(node)
            else:
                level.remove(node)
    return checklist


def encode(list_ch, input_string, checklist):
    """
    Converts the huffman nodes to a binary codes
    And creates a inary string of the input string
    :param list_ch: list of characters in input
    :param input_string: input string
    :param checklist: huffman list
    :return: encoded binary string
    """
    binary_codes = []
    if len(list_ch) == 1:
        charater_code = [list_ch[0], "0"]
        binary_codes.append(charater_code*len(input_string))
    else:
        for letter in list_ch:
            chcode = ""
            for node in checklist:
                if len(node) > 2 and letter in node[1]:
                    chcode = chcode + node[2]
            charater_code = [letter, chcode]
            binary_codes.append(charater_code)
    bitstring = ''
    for i in input_string:
        for j in binary_codes:
            if i in j:
                bitstring = bitstring + j[1]
    binary = (bin(int(bitstring, base=2)))
    return binary, bitstring, binary_codes


def decode(binary_string, binary_codes):
    """
    Decodes the binary string to actual text
    :param binary_string: encoded binary string
    :param binary_codes: codes with nodes
    :return: decoded string
    """
    decoded_string = ''
    code = ''
    for b in binary_string:
        code = code + b
        index = 0
        for ch in binary_codes:
            if code == ch[1]:
                decoded_string = decoded_string + binary_codes[index][0]
                code = ""
            index = index + 1
    return decoded_string


def main():
        print("Select an option. \n1. Select the input text file ")
        print("2. Generate the input text file ")
        n = int(input())
        if n == 1:
            filename = input("Enter the file name : ")
            input_string = ''
            lines = 0
            with open(filename, 'r') as f:
                for line in f:
                    lines += 1
                    line = line.lower()
                    input_string = input_string + line
        else:
            lines = random.choice([5000, 2000, 1000, 500, 100, 50])
            generate_input("input.txt", lines)
            filename = "input.txt"
            input_string = ''

            with open(filename, 'r') as f:
                for line in f:
                    input_string = input_string + line

        print("Input file --> input.txt ( Number of lines : ", lines, ")")

        before_time = time.time()
        freq_characters, list_ch = frequency(input_string)
        huffman_tree = generate_nodes(freq_characters)
        checklist = create_huffman_list(huffman_tree)
        binary, bitstring, binary_codes = encode(list_ch, input_string, checklist)
        decoded_string = decode(bitstring, binary_codes)

        # records time after sorting
        after_time = time.time()

        compression_time = (after_time - before_time)

        with open("decoded_input_1.txt", "w") as f:
            f.write(decoded_string)
        print("\n------------ Output with actual count of characters ------------")
        print("Uncompressed file size = ", len(input_string) * 7, "bits \n")
        print("Output file --> decoded_input_1.txt\n")
        print("Compressed file size = ", len(binary)-2, "bits \n")
        compression_ratio = (len(input_string) * 7)/(len(binary)-2)
        print("Compression ratio = (Uncompressed file size)/(Compressed file size)\n\t\t\t\t\t = ",
              round(compression_ratio, 4), ": 1")
        compression_percentage = 100 - ((len(binary) - 2) / (len(input_string) * 7)*100)
        print("Compression percentage = 100 - ((Compressed file size)/(Uncompressed file size)*100)\n\t\t\t\t\t\t = ",
              compression_percentage, "%")
        print("Time taken : ", compression_time)

        with open("results_1.txt", "a") as f:
            f.write(str(lines) + " " + str(len(input_string) * 7) + " " + str(compression_percentage)
            + " " + str(compression_ratio) + " " + str(compression_time) + "\n")

        before_time = time.time()
        estimate_freq_characters, list_ch = estimated_frequency(input_string)
        huffman_tree = generate_nodes(estimate_freq_characters)
        checklist = create_huffman_list(huffman_tree)
        binary, bitstring, binary_codes = encode(list_ch, input_string, checklist)
        decoded_string = decode(bitstring, binary_codes)
        # records time after sorting
        after_time = time.time()

        compression_time = (after_time - before_time)

        with open("decoded_input_2.txt", "w") as f:
            f.write(decoded_string)

        print("\n------------ Output with estimated count of characters ------------")
        print("Uncompressed file size = ", len(input_string) * 7, "bits \n")
        print("Output file --> decoded_input_2.txt\n")
        print("Compressed file size = ", len(binary) - 2, "bits \n")
        compression_ratio = (len(input_string) * 7) / (len(binary) - 2)
        print("Compression ratio = (Uncompressed file size)/(Compressed file size)\n\t\t\t\t\t = ",
              round(compression_ratio, 4), ": 1")
        compression_percentage = 100- ((len(binary) - 2) / (len(input_string) * 7) * 100)
        print("Compression percentage = 100 - ((Compressed file size)/(Uncompressed file size)*100)\n\t\t\t\t\t\t = ",
              compression_percentage, "%")
        print("Time taken : ", compression_time)

        with open("results_2.txt", "a") as f:
            f.write(str(lines) + " " + str(len(input_string) * 7) + " " + str(compression_percentage)
                    + " " + str(compression_ratio) + " " + str(compression_time) + "\n")


if __name__ == '__main__':
    main()
