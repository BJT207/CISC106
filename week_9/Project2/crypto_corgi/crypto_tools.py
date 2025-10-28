from bakery import assert_equal

def rotate_char_code(char_code: int, rotation: int) -> int:
    '''
    Takes in a printable ASCII character's code
    and cypher shifts it by a given rotation
    
    Args:
        char (int): a two or three code for a printable ASCII character
        rotation (int): a int representing the number of characters
            the user wishes to spin around the cypher
    Returns:
        (int): a int representing the resulting shifted character code
    '''
    return (char_code + rotation - 32) % 94 + 32

assert_equal(rotate_char_code(34,5),39)
assert_equal(rotate_char_code(125,5),36)
assert_equal(rotate_char_code(100,5),105)

def string_to_list(phrase: str) -> list[str]:
    '''
    Takes in a string and parses it into a list
    
    Args:
        phrase (str): a string to be split into a list
        
    Returns:
        (list[str]): the list containing all the characters in the phrase
    '''
    returnList = []
    for character in phrase:
        returnList.append(character)
    return returnList

assert_equal(string_to_list("testing"),['t','e','s','t','i','n','g'])
assert_equal(string_to_list(""),[])
assert_equal(string_to_list("Stop"),["S","t","o","p"])

def list_to_string(phrase: list[str]) -> str:
    '''
    Takes in a list and parses it into a string
    
    Args:
        (list[str]): the list containing all the characters in the phrase
    Returns:
        (str): a string of charcters
    '''
    returnString = ""
    for character in phrase:
        returnString += character
    return returnString
assert_equal(list_to_string(["G","","2"]),"G2")
assert_equal(list_to_string(["H","e","l",'l','o']),"Hello")
assert_equal(list_to_string([]),"")

def encrypt_text(message:str, rotation_ammount:int) -> str:
    '''
    Takes in a string and encrypts it using a
    caesar sypher by a rotation ammount
    
    Args:
        phrase (str): a string to be encripted
        rotation_ammount (int): the number of shifts on the caesar cypher
    Returns:
        str: the string containing the encrypted phrase
    '''
    message_list = string_to_list(message)
    encriptedChars = []
    for character in message_list:
        charInt = rotate_char_code(ord(character), rotation_ammount)
        encriptedChars.append(chr(charInt))
        if charInt < 48:
            encriptedChars.append("~")
    return list_to_string(encriptedChars)

assert_equal(encrypt_text("2", -30), "r")
assert_equal(encrypt_text("Hello", 29), "e$~+~+~.~")    
assert_equal(encrypt_text("Dragons!", 10), "N|kqyx}+~")    

def decrypt_text(message: str, rotation_ammount:int) -> str:    
    '''
    Takes in a string and decripts it using a
    caesar sypher by a rotation ammount
    
    Args:
        phrase (str): a string to be decrypted
        rotation_ammount (int): the number of shifts on the caesar cypher
    Returns:
        str: the string containing the decrypted phrase
    '''
    messageList = string_to_list(message)
    decriptedChars = []
    for character in messageList:
        if not (character == "~"):
            charInt = rotate_char_code(ord(character), -rotation_ammount)
            decriptedChars.append(chr(charInt))
    return list_to_string(decriptedChars)

assert_equal(decrypt_text("r", -30), "2")
assert_equal(decrypt_text("e$~+~+~.~", 29), "Hello")    
assert_equal(decrypt_text("N|kqyx}+~", 10), "Dragons!")

def hash_text(message:str, base:int, hash_size:int) -> int:
    """
    Takes in a message to be hased, a base for the hash, and the hash_size
    and hashes the string
    
    Args:
        message (str): the string to be hashed
        base (int): the base value for the hash
        hash_size (int): lenght of the hash
        
    Returns:
        str: hashed string
    """
    hashSum = 0
    messageList = string_to_list(message)
    for i, character in enumerate(messageList):
        hashSum += (i + base) ** ord(character)
    return hashSum % hash_size
    
assert_equal(hash_text("Test", 13, 150),16)
assert_equal(hash_text("western", 55, 100000),55540)
assert_equal(hash_text("doge", 7393, 1223),1025)

def main():
    """
    Provides a command line interface for executing encryptions and decryptions
    
    Args:
    
    Results:
    
    """
    userAction = input("Type your desired opperation here (encrypt or decrypt): ")
    if userAction.lower() == "encrypt":
        message = input("Type your message here: ")
        print("Encrypted message: " + encrypt_text(message,43))
        print("Message hash is: " + str(hash_text(message, 31, 1000000000)))
    elif userAction.lower() == "decrypt":
        encrypted_message = input("Type your encrypted message here: ")
        user_hash = input("Type your verification hash here: ")
        message = decrypt_text(encrypted_message,43)
        message_hash = hash_text(message, 31, 1000000000)
        if int(user_hash) == message_hash:
            print("The decrypted message is: " + message )
        else:
            print("The hash checker encountered an error!")
            print("The user provided hash dosen't match the decrypted string's hash")
            print("Be careful, the message may have been tampered with!")
            print("The decrypted message is: " + message )
    else:
        print("The user input was irregular resulting in an error. The program will now stop")