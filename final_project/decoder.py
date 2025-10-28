from bakery import assert_equal
from PIL import Image as PIL_Image
import tkinter as tk
from tkinter import filedialog
import os


def even_or_odd_bit(num:int) -> str:
    '''
        Consumes an int and returns epresenting the color intensity value
        (0-255) and returns a '0' or '1' based on whether the color intensity
        value is odd or even.
        
        Args:
            num (int): a number representing the color intensity between 0 and 255
        
        Returns:
            str: string of either "0" or "1"
    '''
    
    if num % 2:
        return "1"
    return "0"

assert_equal(even_or_odd_bit(55),"1")
assert_equal(even_or_odd_bit(255),"1")
assert_equal(even_or_odd_bit(0),"0")
assert_equal(even_or_odd_bit(44),"0")

def decode_single_char(color_values: list[int]) -> str:
    '''
        Consumes a list of integers containing eight color intensities values
        return a string containing the corresponding ascii character
        
        Args:
            color_values (list[int]): a list of ints representing the color values
        
        Returns:
            str: a string containing a single ascii character
    '''
    byte_str = ''
    if len(color_values) == 8:
        for num in color_values:
            byte_str += even_or_odd_bit(num)
        return chr(int(byte_str, 2))
    return ''

assert_equal(decode_single_char([46, 47, 46, 46, 47, 44, 46, 44]),"H")
assert_equal(decode_single_char([44,45,45,44,44,45,45,44]),"f")
assert_equal(decode_single_char([44,44,55,55,44,55,44,55]),"5")
assert_equal(decode_single_char([44,44,55,44,44,44,44,55]),"!")

def decode_chars(color_values: list[int], char_count:int) -> str:
    '''
        Consumes a list of integers of color intensity values and
        an integer representing how many characters to decode.
        Returns a string containing the decoded characters
        
        Args:
            color_values (list[int]): a list containing the color intensity values
                from the image
            char_count (int): the number of characters to decode
        
        Returns:
            str: a string of the decoded message
    '''
    if len(color_values) == char_count*8:
        char_str = ''
        for char in range(char_count):
            char_str += decode_single_char(color_values[(8*char):(8*(char+1))])
        return char_str
    return None

assert_equal(decode_chars([],1),None)
assert_equal(decode_chars([46, 47, 46, 46, 47, 44, 46, 44],1),'H')
assert_equal(decode_chars([46, 47, 46, 46, 47, 44, 46, 44,44,45,45,44,44,45,45,44],2),'Hf')
assert_equal(decode_chars([46, 47, 46, 46, 47, 44, 46, 44,44,45,45,44,44,45,45,44,44,44,55,55,44,55,44,55],3),'Hf5')

colors = [22,22,23,23,22,22,23,22,26,26,27,27,26,27,26,27,2,42,43,43,44,44,40,42]

def get_message_length(colors:list[int], header_length:int) -> int:
    '''
    Consumes a list of color intensity values and an int representing how many characters
    are used in the header to represent the rest of the message's length. Returns the an
    int with number of characters that are in the rest of the hidden message
    
    Args:
        colors (list[int]): list of color intensity values between 0 and 255
        header_length (int): length of header
        
    Returns:
        int: number of characters stored in the image
    '''
    if len(colors) >= header_length*8:
        header_str = decode_chars(colors[0:header_length*8], header_length)
        if header_str.isdigit():
            return int(header_str)
    return 0

assert_equal(get_message_length([20, 254, 45, 95, 40, 90, 20, 40, 200, 254, 45,
                           95, 40, 95, 20, 45,220, 250, 45, 95, 48, 95, 24, 44], 3), 54)
assert_equal(get_message_length(colors,3),250)
assert_equal(get_message_length([44,44,55,55,44,55,44,44,44,44,55,55,44,44,55,44], 2), 42)

def get_encoded_message(colors: list[int]) -> str:
    '''
        Consumes a list of color intensities and returns the hidden message
    
        Args:
            colors (list[int]): a list of color value ints with the range of 0-255
        
        Returns:
            str: a string with the decoded message
    '''
    header_length = 3
    length = get_message_length(colors, header_length)
    starting_point = header_length*8
    ending_point = (length*8)+starting_point
    return decode_chars(colors[starting_point:ending_point], length)

encoded_message_test = [254, 254, 255, 255, 254, 254, 254, 254, 
                           254, 254, 255, 255, 254, 254, 254, 254, 
                           254, 254, 255, 255, 254, 254, 255, 254, 
                           254, 255, 254, 254, 255, 254, 254, 254, 
                           254, 255, 255, 254, 255, 254, 254, 255, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           254, 254, 254, 254, 254, 254, 254, 254, 
                           252]
assert_equal(get_encoded_message(encoded_message_test), "Hi" )

def get_color_values(image: PIL_Image, channel_index:int) -> list[int]:
    width, length = image.size
    color_list = []
    for x in range(width):
        for y in range(length):
            red, green, blue = image.getpixel((x,y))
            if not channel_index:
                color_list.append(red)
            elif channel_index == 1:
                color_list.append(green)
            else:
                color_list.append(blue)
    return color_list

def select_file() -> str:    
    '''
    This function asks user to select a local PNG file
      and returns the file name

    Args:
        None         
    Returns:
        str: the file name
    '''
    root = tk.Tk()
    root.withdraw()

    file_path = tk.filedialog.askopenfilename()

    while (file_path == "" or file_path[-4:] != ".png"):   
        print("Invalid file - must select a PNG file.")
        file_path = tk.filedialog.askopenfilename()

    file_name = os.path.basename(file_path)  #remove path 
    return file_name

file_name = select_file()    # allows user to pick an image file

image = PIL_Image.open(file_name).convert('RGB')  # get RGB Pillow Image format of the image file

# get the color intensity values where the message is hidden
# you must define get_color_values
green_vals = get_color_values(image, 1)  #use green channel
print("Message hidden in file: " , get_encoded_message(green_vals))