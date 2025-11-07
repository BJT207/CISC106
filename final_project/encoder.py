from bakery import assert_equal
from PIL import Image as PIL_Image
import tkinter as tk
from tkinter import filedialog
import os

def prepend_header(message:str) -> str:
    """
    Prepends a three digit header to the message indicating the message length
    
    Args:
        message (str): a string containing the message you want to prepend
    
    Returns:
        str: a atring containing the prepended header and the message
    """
    message_len = len(message)
    if message_len <= 9:
        return "00" + str(message_len)+message
    elif message_len <= 99:
        return "0" + str(message_len)+message
    return str(message_len)+message

assert_equal(prepend_header("123456789"),"009123456789")
assert_equal(prepend_header(""),"000")
assert_equal(prepend_header("123456789012345678901"),"021123456789012345678901")
assert_equal(prepend_header("1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"),
             "1001234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890")

def message_to_binary(message:str) -> str:
    """
    Takes in a string and returns the binary string of the characters
    
    Args:
        message (str): the message to be converted to binary
    Returns:
        str: a binary string of "1"s and "0"s representing the message
    """
    binary_str = ''
    for char in message:
        binary_str += format(ord(char), '08b')
    return binary_str

assert_equal(message_to_binary("Hi"), "0100100001101001")
assert_equal(message_to_binary("058"),"001100000011010100111000")
assert_equal(message_to_binary("test"),"01110100011001010111001101110100")
assert_equal(message_to_binary("binary101"),"011000100110100101101110011000010111001001111001001100010011000000110001")

def new_color_value(original:int, bit:str) -> int:
    """
    Takes in a color int and makes sure it matches even or odd with the bit value.
    If need be, it modifies it by +-1 to create the match
    
    Args:
        original (int): the original value of the bit
        bit (str): the bit to be encoded
        
    Return:
        int: the bit modified value
    """
    if (original % 2) and (bit == "0"):
        return original - 1
    elif (not original % 2) and (bit == "1"):
        return original + 1
    return original

assert_equal(new_color_value(199,"1"),199)
assert_equal(new_color_value(120,"1"),121)
assert_equal(new_color_value(120,"0"),120)
assert_equal(new_color_value(199,"0"),198)

def hide_bits(image:PIL_Image, bits:str, color:int) ->PIL_Image:
    """
    Consumes an image and a string of bits and encodes the
    bits into one of the color channels in the photo
    
    Args:
        image (PIL_Image): the image to have data encoded into
        bits (str): the bits to be encoded into the image
        color (int): the color channel to encode the data into (0=>red, 1=>green, 2=>blue)
    Returns:
        PIL_Image: an image with the message encoded into it
    """
    modified_image = image.copy()
    width, length = modified_image.size
    width_current = 0
    length_current = 0
    for bit in bits:
        red, green, blue = modified_image.getpixel((width_current, length_current))
        if color == 0:
            red = new_color_value(red, bit)
        elif color == 1:
            green = new_color_value(green, bit)
        else:
            blue = new_color_value(blue, bit)
        modified_image.putpixel((width_current, length_current), (red, green, blue))
        if length_current >= length:
            width_current += 1
            length_current = 0
        else:
            length_current += 1
    return modified_image

# def get_message(max_length: int) -> str:
#     '''
#     Takes a max length of the message as an arg and the message using input once
#     it's length is less than the max length
#     
#     Args:
#         max_length (int): the maximum lenth of characters the message can be
#     Returns:
#         str: the message from the user
#     '''
#     message = input('Write your message here:')
#     while len(message) > max_length:
#         print('Message is to long, try again')
#         message = input('Write your message here:')
#     return message

# def select_file() -> str:    
#     '''
#     This function asks user to select a local PNG file
#       and returns the file name
# 
#     Args:
#         None         
#     Returns:
#         str: the file name
#     '''
#     root = tk.Tk()
#     root.withdraw()
# 
#     file_path = tk.filedialog.askopenfilename()
# 
#     while (file_path == "" or file_path[-4:] != ".png"):   
#         print("Invalid file - must select a PNG file.")
#         file_path = tk.filedialog.askopenfilename()
# 
#     file_name = os.path.basename(file_path)  #remove path 
#     return file_name

# file_name = select_file()    # allows user to pick an image file
# 
# image = PIL_Image.open(file_name).convert('RGB')  # get RGB Pillow Image format of the image file
# binary_string = message_to_binary(prepend_header(get_message(999)))
# 
# image = hide_bits(image, binary_string,1) # encode the message into the image
# 
# # save the updated image with a new file name  
# new_file_name = "1_" + file_name # format of 1 + old filename (1 represents green channel)  
# image.save(new_file_name, "PNG")
# print("Message hidden in file: ", new_file_name)