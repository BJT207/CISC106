from dataclasses import dataclass
from PIL import Image as PIL_Image  #This is a different Image than the drafter Image.
from drafter import *

@dataclass
class State:
    image: PIL_Image
    
@route
def index(state: State) -> Page:
    """ Use FileUpload to allow user to select only png files """
    return Page(state, [
        "Select a 'png' file.",       
        FileUpload("new_image", accept="image/png"),
        Button("Display", display_image)
        ])

@route
def display_image(state : State, new_image: bytes) -> Page:
    # open the file and assign to State field
    state.image = PIL_Image.open(io.BytesIO(new_image)).convert('RGB')

    return Page(state, [
        Image(state.image),
        Button("Back", index)
        ])

start_server(State(None))