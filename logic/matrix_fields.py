def set_fixed_fields(matrix:list[int],qr_layout:dict)->None:
    '''
    Destructive function that applies the fixed fields to the QR code matrix.
    Fixed fields are used for better tracking of the QR code.
    '''
    for position in qr_layout["fixed_positions"]["zeros"]:
        matrix[position[0]][position[1]]=0

    for position in qr_layout["fixed_positions"]["ones"]:
        matrix[position[0]][position[1]]=1


def set_meta_fields(matrix:list[int], err_corr:str, mask_no:int, qr_layout:dict):
    '''
    Destructive function that sets the meta fields for the QR code.
    Meta fields are used to tell the receiving device meta info about the QR code.
    Such as which QR code version is used.
    '''

    bit_pattern = qr_layout["meta_patterns"][err_corr][mask_no]

    # First meta pattern.
    for index, position in enumerate(qr_layout["meta_positions"]["first"]):
        matrix[position[0]][position[1]]=bit_pattern[index]

    # Second meta pattern.
    for index, position in enumerate(qr_layout["meta_positions"]["second"]):
        matrix[position[0]][position[1]]=bit_pattern[index]
        