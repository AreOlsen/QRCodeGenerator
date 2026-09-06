from logic.error_correction import generate_error_correction


def string_to_data(content_string:str)->list[int]:
    '''
    Function that returns string in pure bits.
    '''

    bit_list = []
    for character in content_string:
        for x in f'{ord(character):08b}':
            bit_list.append(int(x))
    return bit_list



def get_core_bit_list(content_string:str)->list[int]:
    '''
    The core bit list of a string,
    this includes meta data about the string,
    as well as the pure data of the string (string_to_data
    '''

    #Bit list initialization with modus.
    bit_list = [0,1,0,0]

    # Add length of string to bit_list.
    string_length = len(content_string)
    for x in f'{string_length:08b}':
        bit_list.append(int(x))

    # Add content string in pure bit format.
    bit_list.extend(string_to_data(content_string))

    #Add terminator of string.
    bit_list.extend([0]*4)

    return bit_list



def pad_bit_list(core_bit_list:list[int],pad_to_bytes:int)->None:
    '''
    Function that pads a bit list to a certain length of bytes (pad_to_bytes).
    '''

    #Bits to pad
    bits_to_pad = 8*pad_to_bytes-len(core_bit_list)

    #Padding
    padding_1=[1, 1, 1, 0, 1, 1, 0, 0]
    padding_2=[0, 0, 0, 1, 0, 0, 0, 1]
    padding=padding_1+padding_2

    #Add padding destructively.
    core_bit_list += [padding[x%len(padding)] for x in range(bits_to_pad)]



def string_to_bit_list(content_string:str, qr_layout:dict)->tuple[list[int],int]:
    '''
    Function that takes a string, and the current QR version.
    And outputs a bit list containg the padded core bit list of the string, and the error code for the string.
    '''

    core_bit_list = get_core_bit_list(content_string)
    error_bytes = qr_layout["error_correction_bytes"]
    bytes_capacity = qr_layout["byte_capacity"]

    # Get best possible error version.
    error_level = ""
    for level, byte in error_bytes.items():
        # If level with data can be stored.
        if  byte+len(core_bit_list)/8<=bytes_capacity:
            error_level=level
    if error_level=="":
        raise Exception("Altfor mykje data i QR-koden! \n Umogleg å ha både feilretting og data.")

    # Eventual padding.
    pad_to_bytes = bytes_capacity-error_bytes[error_level]
    pad_bit_list(core_bit_list,pad_to_bytes)

    # Adding error correction.
    bit_list = generate_error_correction(core_bit_list, error_level)

    return (bit_list, error_level)
