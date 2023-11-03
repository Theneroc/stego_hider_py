import cv2, numpy, tkinter, math, os
from PIL import Image
from tkinter import filedialog


def part1():
    encode()

    decode()


def encode():
    root = tkinter.Tk()
    root.withdraw()
    secret_path = filedialog.askopenfilename()
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
                    cover_bytes_list[i] += 1
                else:
                    cover_bytes_list[i] = cover_bytes_list[i]
            if cover_bytes_list[i] % 2 != 0:
                if secret_bits_list[j] == 0:
                    cover_bytes_list[i] -= 1
                else:
                    cover_bytes_list[i] = cover_bytes_list[i]
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
                secret_bit_list.append(0)
            else:
                secret_bit_list.append(1)

    secret_bit_string = ''.join(map(str, secret_bit_list))
    print(len(secret_bit_string))
    secret_bytes = [secret_bit_string[i:i + 8] for i in range(0, len(secret_bit_string), 8)]
    secret_chars = [chr(int(secret_byte, 2)) for secret_byte in secret_bytes]

    secret_msg = ''.join(secret_chars)
    print(secret_msg)
    print("Secret retrieved.")


def create_hash():
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()

    file = open(file_path, 'r')  # get the file

    file_content = file.read()  # retrieve the content from the file

    file_length = len(file_content)

    file_bits = ''.join(format(ord(char), '08b') for char in file_content)  # convert the chars to bits of 8
    # each and concatenate them

    file_bytes = [file_bits[i:i + 8] for i in range(0, len(file_bits), 8)]
    file_bytes = [int(bit, 2) for bit in file_bytes]
    # print("file_bits: ", file_bits)
    # print("file_bytes", file_bytes)
    # print("file length", file_length)

    countMap = {}
    placeMap = {}
    # oneCount = 0
    # zeroCount = 0
    #
    # for i in file_bits:
    #     if i == '1':
    #         oneCount += 1
    #     else:
    #         zeroCount += 1

    for i, byte in enumerate(file_bytes):
        if byte in countMap:
            countMap[byte] += 1
        else:
            countMap[byte] = 1
            placeMap[byte] = i

    count_bit_string = ''.join(format(byte, '08b') + format(count, '08b') for byte, count in countMap.items())
    place_bit_string = ''.join(format(byte, '08b') + format(count, '08b') for byte, count in placeMap.items())

    countMap_8bit_list = [count_bit_string[i:i + 8] for i in range(0, len(count_bit_string), 8)]
    placeMap_8bit_list = [place_bit_string[i:i + 8] for i in range(0, len(place_bit_string), 8)]

    countMap_byte_list = [int(bit, 2) for bit in countMap_8bit_list]
    placeMap_byte_list = [int(bit, 2) for bit in placeMap_8bit_list]

    countMap_sum = 0
    placeMap_sum = 0

    for byte in countMap_byte_list:
        countMap_sum += byte

    for byte in placeMap_byte_list:
        placeMap_sum += byte

    countMap_sum = bin(countMap_sum)[2:]
    placeMap_sum = bin(placeMap_sum)[2:]
    # zeroCount = bin(zeroCount)[2:]
    # oneCount = bin(oneCount)[2:]
    hashMap_sum = '{:032b}'.format(int(countMap_sum, 2))
    placeMap_sum = '{:032b}'.format(int(placeMap_sum, 2))
    # zeroCount = '{:0>32}'.format(zeroCount)
    # oneCount = '{:0>32}'.format(oneCount)

    print(hashMap_sum)
    # print(zeroCount)
    # print(oneCount)

    # place map sum will be reversed as a string and concatenated to count map sum
    reversed_placeMap_sum = placeMap_sum[::-1]
    print(reversed_placeMap_sum)

    signature_bits = countMap_sum + reversed_placeMap_sum

    signature = '{:064b}'.format(int(signature_bits, 2))

    print(signature)

if __name__ == "__main__":
    encode()

    decode()
