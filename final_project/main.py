from dataclasses import dataclass
from PIL import Image as PIL_Image  #This is a different Image than the drafter Image.
from drafter import *
from decoder import get_encoded_message, get_color_values
from encoder import hide_bits, message_to_binary,prepend_header
from bakery import assert_equal

#Classes
class EmptyableFile():
    '''
    Used for the File upload system
    Allows for an empty file to be processed by Drafter
    without automaticaly triggering a 500 server error.
    Assigns value as either a bytes value or a None value
    for the user to process manualy.
    Uses class over dataclass for type flexability when assigning self.value
    '''
    def __init__(self, value):   
        try:
            self.value = bytes(value.file.read()) 
        except:
            self.value = None
        value.file.close()

#Dataclasses
@dataclass
class State:
    '''
    The drafter State. Stores all the core information to be transfered across pages
    
    Args:
        image (PIL_Image): The image that will either have information encoded into it or be decoded
        info list[str]: a list of strings used to project error messages if the image that is uploaded
                        is either invalid or incorrectly named by the user
        encoding (bool): used by the decode_encode_settings function to determine if the encode fields
                        need to be shown or the decode feilds need to be shown
        modified_image (PIL_Image): the image that gets modified to store the encrypted data. Separated
                        from image to allow for the user to change what message they have in a given channel
                        before they download the image
        message_lengths (tupple): used to store information about the encrypted message length so that only the
                        effected pixels have to be restored to their origional format when re-encrypting or clearing
                        a channel
        file_name (str): the user given name of the file 
    '''
    image: PIL_Image = None
    info: list[str] = field(default_factory=lambda: ["Select a 'png' file."])
    encoding: bool = True
    modified_image: PIL_Image = None
    message_lengths: tuple = (0,0,0)
    file_name:str = ''

#Routes
@route
def index(state: State) -> Page:
    '''
    Used to allow user to select an image for encryption/decription
    
    Args:
        state (State): the drafter state
        
    Returns:
        Page: a page containing the upload form for the image and a field for the filename
    '''
    state.message_lengths = (0,0,0)
    state.modified_image = None
    state.image = None
    state.file_name=''
    page_content = []
    for message_line in state.info:
        page_content.append(message_line)
    page_content += [FileUpload("new_image", accept="image/png"),
                     "Write a name for your image Here:",
                     TextBox("file_name"),
        Button("Display", image_verification_handler)]
    return Page(state, page_content)


@route
def image_verification_handler(state : State, new_image:EmptyableFile, file_name: str) -> Page:
    '''
        Used to verify that an actual image was uploaded and named before attempting to
        diplay anything. (Prevents 500 Internal Server Error) If an image is not
        found, modifies the state.info to include an error message and returns the index page
        
        Args:
            state (State): the drafter state object
            image (EmptyableFile): used to store the uploaded image data [or lack of data]
            file_name (str): a string representing the name of the file
        Returns:
            Page: returns a page to the user depending on if the uploaded photo and filename are valid
    '''
    image_info = new_image.value
    if image_info:
        if verify_file_name(file_name):
            state.info = ["Select a 'png' file."]
            state.file_name = file_name
            return display_new_image(state, image_info)
        state.info = ["The provided image name was invalid",
                      "Image names may contain A-Z, a-z, 1-9, '-', '.', and '_'",
                      "Additionaly, the image may not start or end with '.'",
                      "Please try again.",
                      "Select a 'png' file."]
        return index(state)
    state.info = ["An image was either not uploaded or incorrectly formated",
                      "Please try again.",
                      "Select a 'png' file."]
    return index(state)

@route
def display_new_image(state : State, new_image: bytes) -> Page:
    # open the file and assign to State field
    state.image = PIL_Image.open(io.BytesIO(new_image)).convert('RGB')
    state.modified_image = state.image.copy()
    return display_image(state)

@route
def display_image(state : State) -> Page:
    # open the file and assign to State field
    return Page(state, [
        Image(state.image),
        Button("Decode", decode_page),
        Button("Encode", encode_page),
        Button("Back", index)
        ])

@route
def decode_page(state : State) -> Page:
    state.encoding = False
    return decode_encode_settings(state)

@route
def encode_page(state : State) -> Page:
    state.encoding = True
    return decode_encode_settings(state)

@route
def decoded(state: State, color_channel: str) -> Page:
    message = get_encoded_message(get_color_values(state.image, color_to_channel_ID(color_channel)))
    if message:
        return Page(state, [
            "The hidden message is:",
            '“'+message+'”',
            Button("Return to Selection Screen",display_image),
            Button("New Image",index)
            ])
    return Page(state, [
            "Sorry, there is no hidden message here",
            Button("Return to Selection Screen",display_image),
            Button("New Image",index)
            ])
@route
def encode_image(state:State, message:str, color_channel: str) -> Page:
    color_channel_id = color_to_channel_ID(color_channel)
    binary_message = message_to_binary(prepend_header(message))
    
    #if there has already been a message encoded into the channel, removes it before adding the new one
    if color_channel_id == 0:
        if not state.message_lengths[0] == 0:
            state.modified_image = reset_bits(state.image, state.modified_image, 0, state.message_lengths[0])
        state.message_lengths = (len(binary_message),state.message_lengths[1],state.message_lengths[2])
    elif color_channel_id == 1:
        if not state.message_lengths[1] == 0:
            state.modified_image = reset_bits(state.image, state.modified_image, 1, state.message_lengths[1])
        state.message_lengths = (state.message_lengths[0],len(binary_message),state.message_lengths[2])
    else:
        if not state.message_lengths[2] == 0:
            state.modified_image = reset_bits(state.image, state.modified_image, 2, state.message_lengths[2])
        state.message_lengths = (state.message_lengths[0],state.message_lengths[1],len(binary_message))
    # if the message is empty, checks if there is any messages at all and if not, sets the modified image back to none to prevent
    #download from poping up in the encode page
    if message:    
        state.modified_image = hide_bits(state.modified_image, binary_message, color_channel_id)
    else:
        if state.message_lengths == (0,0,0):
            state.modified_image = state.image.copy()
    return encode_page(state)

#Functions
def color_to_channel_ID(color_channel:str) -> int:
    '''
    Consumes a string of either 'Red', 'Green', or 'Blue' and returns the accompaning channel id of 0, 1, or 2
    
    Args:
        color_channel (str): the color chanel name to be converted to ID
    
    Returns:
        int: an int representing the id of the color channel provided
    '''
    
    if color_channel == "Red":
        return 0
    elif color_channel == "Green":
        return 1
    else:
        return 2
assert_equal(color_to_channel_ID("Red"), 0)
assert_equal(color_to_channel_ID("Green"), 1)
assert_equal(color_to_channel_ID("Blue"), 2)

def decode_encode_settings(state : State) -> Page:
    '''
    Consumes the state object and returns a page with varied elements based on whether or not its the encode or decode page.
    This was done since the two pages share a good number of common elements
    
    Args:
        state (State): the state of the Drafter instance
    
    Returns:
        Page: a page element for the encode or decode page
    '''
    
    pageItems = [Image(state.image),
                 "Color Channel:",
                 SelectBox("color_channel",["Red","Green","Blue"], "Green")
                 ]
    if state.encoding:
        pageItems += [
            "Message To Encode:",
            TextBox("message"),
            Button("Encode", encode_image)
            ]
        if not state.message_lengths == (0,0,0):
            pageItems.append(Download("Download", state.file_name+"_encrypted", state.modified_image))
    else:
        pageItems.append(Button("Decode", decoded))
    pageItems.append(Button("Back", display_image))
    
    return Page(state, pageItems)

def reset_bits(original_image:PIL_Image, image:PIL_Image, color:int, num_of_bits:int) -> PIL_Image:
    '''
    Used to reset the color channel of a modified image before it is rewritten
    
    Args:
        original_image (PIL_Image): the image that has already been modified
        image (PIL_Image): the origional image to reference
        color: the color channel to clear encode the data from (0=>red, 1=>green, 2=>blue)
        num_of_bits (int): the number of bits that need to be cleared

    Returns:
        PIL_Image: the modified image with all the data stripped from the provided channel
    '''
    width, length = image.size
    width_current = 0
    length_current = 0
    for bit in range(num_of_bits):
        red_old, green_old, blue_old = original_image.getpixel((width_current, length_current))
        red, green, blue = image.getpixel((width_current, length_current))
        if color == 0:
            red = red_old
        elif color == 1:
            green = green_old
        else:
            blue = blue_old
        image.putpixel((width_current, length_current), (red, green, blue))
        if length_current >= length:
            width_current += 1
            length_current = 0
        else:
            length_current += 1
    return image

def verify_file_name(fileName:str) -> bool:
    '''
    Takes in a file name and returns a bool stating if it is or isnt
    
    Args:
        file_name (str): the file name to be validated
        
    Returns:
        bool: if the file name is valid or not
    '''
    validCharList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                     'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                     '1','2','3','4','5','6','7','8','9','-', '_', '.']
                     
    nameIsValid = True
    fileNameLength = len(fileName)
    if fileNameLength > 0 and fileNameLength <= 50:
        if (fileName[0] == '.') or (fileName[-1] == '.'): 
            nameIsValid = False
        else:
            for letter in fileName:
                if not (letter in validCharList):
                    nameIsValid = False
    else:
        nameIsValid = False
    return nameIsValid

assert_equal(verify_file_name('test'), True)
assert_equal(verify_file_name('.test'), False)
assert_equal(verify_file_name('%test'), False)
assert_equal(verify_file_name(''), False)

#Route Assert Equal Statements:


start_server(State())