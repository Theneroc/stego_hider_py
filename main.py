import math
import os
import tkinter
from tkinter import filedialog

from PIL import Image


def part1():
    encode()

    decode()


def encode():
    print("Select a text file you wish to hide:")
    root = tkinter.Tk()
    root.withdraw()
    secret_path = filedialog.askopenfilename()
    print("Select a png cover file:")
    cover_path = filedialog.askopenfilename()
    root.destroy()

    secret_file = open(secret_path, 'r')  # get the secret file

    secret_content = secret_file.read()  # retrieve the content from the secret file

    secret_bits = ''.join(format(ord(char), '08b') for char in secret_content)  # convert the secret chars to bits of 8
    # each and concatenate them

    cover_image = Image.open(cover_path)  # retrieve the cover image

    cover_bytes = cover_image.tobytes()
    print("cover bytes: ", cover_bytes)
    print("secret_bits: ", secret_bits)
    cover_bytes_list = [byte for byte in cover_bytes]
    secret_bits_list = [int(bit) for bit in secret_bits]
    print("secret_bit_list", len(secret_bits_list))

    print("cover bytes: ", len(cover_bytes))
    ratio = len(cover_bytes) / len(
        secret_bits)  # get the ratio between a bit in the secret to the amount of bytes in the
    # cover file

    ratio = math.floor(ratio)  # if the ratio is for ex. 21.232:1 then it becomes 21:1

    j = 0
    for i in range(len(cover_bytes_list)):
        if i % ratio == 0 and (j < len(secret_bits_list)):
            if cover_bytes_list[i] % 2 == 0:
                if secret_bits_list[j] == 1:
                    cover_bytes_list[i] = cover_bytes_list[i]
                else:
                    cover_bytes_list[i] += 1
            if cover_bytes_list[i] % 2 != 0:
                if secret_bits_list[j] == 0:
                    cover_bytes_list[i] = cover_bytes_list[i]
                else:
                    cover_bytes_list[i] -= 1
            j += 1

    image_type = cover_image.format
    stego_name = "newstego_file." + image_type
    parent_dir = os.path.dirname(cover_path)

    cover_bytes = bytes(cover_bytes_list)
    print("after lsb: ", len(cover_bytes))
    stego_image = Image.frombytes(cover_image.mode, cover_image.size, cover_bytes)
    stego_path = os.path.join(parent_dir, stego_name)
    stego_image.save(stego_path)

    print("Steganography file created with key: ", ratio, len(secret_bits_list))


def decode():
    print("Select the stego file you wish to unfold:")

    root = tkinter.Tk()
    root.withdraw()
    stego_path = filedialog.askopenfilename()
    root.destroy()

    stego_image = Image.open(stego_path)  # retrieve the cover image

    stego_bytes = stego_image.tobytes()
    stego_bytes_list = [byte for byte in stego_bytes]
    secret_bit_list = []

    ratio = int(input("enter key: "))
    secret_length = int(input("enter secret length: "))
    j = 0
    for i in range(len(stego_bytes_list)):
        if i % ratio == 0 and j <= secret_length:
            if stego_bytes_list[i] % 2 == 0:
                secret_bit_list.append(1)
            else:
                secret_bit_list.append(0)

    secret_bit_string = ''.join(map(str, secret_bit_list))
    print(len(secret_bit_string))
    secret_bytes = [secret_bit_string[i:i + 8] for i in range(0, len(secret_bit_string), 8)]
    secret_chars = [chr(int(secret_byte, 2)) for secret_byte in secret_bytes]

    secret_msg = ''.join(secret_chars)
    print(secret_msg)
    print("Secret retrieved.")


def part2():
    [signature_content, directory] = create_hash()
    print(directory)

    with open(directory + '/signature.txt', 'w') as file:
        file.write(''.join(signature_content))

    part1()


def create_hash():
    print("Select a text file you wish to hash:")

    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()

    file = open(file_path, 'r')  # get the file

    file_content = file.read()  # retrieve the content from the file

    file_bits = ''.join(format(ord(char), '08b') for char in file_content)  # convert the chars to bits of 8
    # each and concatenate them

    file_bytes = [file_bits[i:i + 8] for i in range(0, len(file_bits), 8)]
    file_bytes = [int(bit, 2) for bit in file_bytes]

    countMap = {}
    firstPlace_Map = {}
    lastPlace_Map = {}

    for i, byte in enumerate(file_bytes):
        if byte in countMap:
            countMap[byte] += 1
        else:
            countMap[byte] = 1
            firstPlace_Map[byte] = i
        lastPlace_Map[byte] = i

    count_bit_string = ''.join(format(byte, '08b') + format(count, '08b') for byte, count in countMap.items())
    firstPlace_bit_string = ''.join(format(byte, '08b') + format(count, '08b') for byte, count in firstPlace_Map.items()
                                    )
    lastPlace_bit_string = ''.join(format(byte, '08b') + format(count, '08b') for byte, count in lastPlace_Map.items())

    countMap_8bit_list = [count_bit_string[i:i + 8] for i in range(0, len(count_bit_string), 8)]
    firstPlace_Map_8bit_list = [firstPlace_bit_string[i:i + 8] for i in range(0, len(firstPlace_bit_string), 8)]
    lastPlace_Map_8bit_list = [lastPlace_bit_string[i:i + 8] for i in range(0, len(lastPlace_bit_string), 8)]

    countMap_byte_list = [int(bit, 2) for bit in countMap_8bit_list]
    firstPlace_Map_byte_list = [int(bit, 2) for bit in firstPlace_Map_8bit_list]
    lastPlace_Map_byte_list = [int(bit, 2) for bit in lastPlace_Map_8bit_list]

    countMap_sum = 0
    firstPlace_Map_sum = 0
    lastPlace_Map_sum = 0

    for byte in countMap_byte_list:
        countMap_sum += byte

    for byte in firstPlace_Map_byte_list:
        firstPlace_Map_sum += byte

    for byte in lastPlace_Map_byte_list:
        lastPlace_Map_sum += byte

    countMap_sum = bin(countMap_sum)[2:]
    firstPlace_Map_sum = bin(firstPlace_Map_sum)[2:]
    lastPlace_Map_sum = bin(lastPlace_Map_sum)[2:]

    hashMap_sum = '{:032b}'.format(int(countMap_sum, 2))
    firstPlace_Map_sum = '{:032b}'.format(int(firstPlace_Map_sum, 2))
    lastPlace_Map_sum = '{:032b}'.format(int(lastPlace_Map_sum, 2))

    print(hashMap_sum)

    # firstPlace_ map sum will be reversed as a string and concatenated to count map sum
    reversed_firstPlace_Map_sum = firstPlace_Map_sum[::-1]
    print(reversed_firstPlace_Map_sum)

    signature_bits = countMap_sum + reversed_firstPlace_Map_sum + lastPlace_Map_sum

    signature = '{:096b}'.format(int(signature_bits, 2))
    signature_list = [bit for bit in signature]

    parent_directory = os.path.dirname(file_path)

    return [signature_list, parent_directory]


def test_collision(signature1, signature2):
    print(int(signature1) - int(signature2))


if __name__ == "__main__":
    part1()

    # part2()

    # 000000000000000000010001111110100111101100111000000000000000000000000000000000000010111010110000

    # 000000000000000000010001111110010111101100111000000000000000000000000000000000000010111010101110

    # test_collision("0000000000000000000100011111101001111011001110000000000000000000000000000000000000101"
    #                "11010110000",
    #                "0000000000000000000100011111100101111011001110000000000000000000000000000000000000101"
    #                "11010101110")