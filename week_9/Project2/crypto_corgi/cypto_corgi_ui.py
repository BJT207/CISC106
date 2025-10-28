from drafter import *
from crypto_tools import encrypt_text, decrypt_text, hash_text
from dataclasses import dataclass
from bakery import assert_equal


ROTATION = 4
BASE = 31
HASH_SIZE = 10**9


@dataclass
class State:
    """
    The current state of the Crypto Corgi application.
    
    Attributes:
        message (str): The latest saved encrypted or decrypted text. After
            encrypting, this should be set to the encrypted text. After
            decrypting, this should be set to the decrypted text (but only if
            it was decrypted successfully).
        latest_hash (str): The latest saved hash. After encrypting, this should be
            set to the hash of the original message. After decrypting, this should
            be unchanged.
        status (str): A string message to display to the user, with information
            about the latest encryption and decryption attempt.
    """
    message: str
    latest_hash: str
    status: str


@route
def index(state: State):
    '''
    Consumes the current State and produces the actual Page content, including the current status message,
    two input boxes, and two buttons.
    
    Args:
        state (State): state of the drafter ui
        
    Returns:
        Page: current status message, two input boxes, and two buttons.
    '''
    return Page(state, [
        Header("Crypto Corgi"),
        state.status,
        "Message:",
        TextBox("given_message", state.message),
        Button("Encrypt", "encrypt"),
        "Hash:",
        TextBox("latest_hash", state.latest_hash),
        Button("Decrypt", "decrypt"),
        ])

@route
def encrypt(state: State, given_message: str):
    '''
    Consumes the current State and the message to encrypt. Modifies the state to
    contain the encrypted message and the hash of the message, then returns the
    main index page using the modified state
    
    Args:
        state (State): state of the drafter ui
        given_message (str): the message to be encrypted
    Returns:
        index: returns the index page with the newly updates state
    '''
    state.message = encrypt_text(given_message,ROTATION)
    state.latest_hash = str(hash_text(given_message, BASE, HASH_SIZE))
    state.status = "Message encrypted and hashed!"
    return index(state)


@route
def decrypt(state: State, given_message: str, latest_hash: str):
    '''
    Consumes the current State and the message to encrypt. Decrypts
    the message and checks it against the hash. If the hash dosen't
    match or is empty, returns an index with the state.status modified
    to display a failed to decrypt message. if it does match, the
    index is returned with a modified state including the decrypted message,
    a status saying the message was sucesfully decrypted, and a cleared hash
    
    Args:
        state (State): state of the drafter ui
        given_message (str): the message to be encrypted
    Returns:
        index: returns the index page with the newly updates state
    '''
    decrypted_message = decrypt_text(given_message, ROTATION)
    decrypted_hash = hash_text(decrypted_message, BASE, HASH_SIZE)
    if not latest_hash:
        state.status = "Decryption failed: Hash mismatch!"
    elif int(latest_hash) != decrypted_hash:
        state.status = "Decryption failed: Hash mismatch!"
    else:
        state.message = decrypted_message
        state.latest_hash = ""
        state.status = "Message decrypted successfully!"
    return index(state)

# Initial version of index page
assert_equal(index(State("", "", "Write your message below")),
             Page(State("", "", "Write your message below"), [
                 Header("Crypto Corgi"),
                 "Write your message below",
                 "Message:",
                 TextBox("given_message", ""),
                 Button("Encrypt", "encrypt"),
                 "Hash:", 
                 TextBox("latest_hash", ""),
                 Button("Decrypt", "decrypt"),
             ]))
# Loading index with content
assert_equal(index(State("Test", "1000", "Write your message below")),
             Page(State("Test", "1000", "Write your message below"), [
                 Header("Crypto Corgi"),
                 "Write your message below",
                 "Message:", TextBox("given_message", "Test"),
                 Button("Encrypt", "encrypt"),
                 "Hash:", TextBox("latest_hash", "1000"),
                 Button("Decrypt", "decrypt"),
             ]))
# Encrypt a message
assert_equal(
    encrypt(State("", "", ""), "Hello world!"),
    Page(
        State("Lipps$~{svph%~", "533815340", "Message encrypted and hashed!"),
        [
            Header("Crypto Corgi"),
            "Message encrypted and hashed!",
            "Message:",
            TextBox("given_message", "Lipps$~{svph%~"),
            Button("Encrypt", "encrypt"),
            "Hash:",
            TextBox("latest_hash", "533815340"),
            Button("Decrypt", "decrypt"),
        ],
    ),
)
# Successful decryption
assert_equal(
    decrypt(State("", "", ""), "Lipps$~{svph%~", "533815340"),
    Page(
        State("Hello world!", "", "Message decrypted successfully!"),
        [
            Header("Crypto Corgi"),
            "Message decrypted successfully!",
            "Message:",
            TextBox("given_message", "Hello world!"),
            Button("Encrypt", "encrypt"),
            "Hash:",
            TextBox("latest_hash", ""),
            Button("Decrypt", "decrypt"),
        ],
    ),
)
# Unsuccessful decryption
assert_equal(
    decrypt(State("The original message", "", ""), "Hello world!", "533815340"),
    Page(State("The original message", "", "Decryption failed: Hash mismatch!"), [
        Header("Crypto Corgi"),
        "Decryption failed: Hash mismatch!",
        "Message:",
        TextBox("given_message", "The original message"),
        Button("Encrypt", "encrypt"),
        "Hash:",
        TextBox("latest_hash", ""),
        Button("Decrypt", "decrypt"),
    ]),
)


# Comment out this line to skip running the actual server.
start_server(State("", "", ""))