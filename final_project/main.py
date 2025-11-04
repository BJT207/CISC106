from dataclasses import dataclass
from PIL import Image as PIL_Image  #This is a different Image than the drafter Image.
from drafter import *

class EmptyableFile():
    """
    Personal Additon to the File upload system
    Allows for an empty file to be processed by Drafter
    without automaticaly triggering a 500 server error by storing
    the raw data from .read() and them returning it as either a bytes
    value or a None value for the user to process manualy
    """
    def __init__(self, value):   
        try:
            self.value = bytes(value.file.read())
        except:
            self.value = None
    def return_info(self):
        return self.value

@dataclass
class State:
    image: PIL_Image
    message: list[str] = field(default_factory=lambda: ["Select a 'png' file."])

@route
def index(state: State) -> Page:
    """ Use FileUpload to allow user to select only png files """
    
    page_content = []
    for message_line in state.message:
        page_content.append(message_line)
    page_content += [ FileUpload("new_image", accept="image/png"),
        Button("Display", image_verification_handler)
        ]
    
    return Page(state, page_content)

@route
def image_verification_handler(state : State, new_image:EmptyableFile) -> Page:
    """
        Personal addition to the image upload system.
        Used to verify that an actual image was uploaded before attempting to
        diplay anything. (Prevents 500 Internal Server Error) If an image is not
        found, modifies the state.message and returns the index page
        
        Args:
            state (State): the drafter state object
            image (): a typeless var used to store the uploaded image data [or lack of]
        
        Returns:
            Page: returns a page to the user depend
    """
    image_info = new_image.return_info()
    if image_info: 
        return display_image(state, image_info)  
    state.message = ["An image was either not uploaded or incorrectly formated",
                      "Please try again.",
                      "Select a 'png' file."]
    return index(state)


@route
def display_image(state : State, new_image: bytes) -> Page:
    # open the file and assign to State field
    state.image = PIL_Image.open(io.BytesIO(new_image)).convert('RGB')
    state.message = ["Select a 'png' file."]
    return Page(state, [
        Image(state.image),
        Button("Back", index)
        ])

start_server(State(None))