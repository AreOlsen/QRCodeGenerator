def get_next_pos(row:int, column:int, size:int)->tuple[int,int]:
    '''
    To iterate over the QR matrix for placing bits there are a few rules.
    There is one rule for even columned cells.
    And two for odd columned cells.
    '''

    # EVEN COLUMNED CELLS.
    if column%2==0:
        if column==0:
            return (row-1,column)
        return (row,column-1)

    # FIRST ODD COLUMNED CELLS RULE.
    elif column%4==1:
        if row==size-1:
            return (row,column-1)
        return (row+1,column+1)

    # SECOND ODD COLUMNED CELLS RULE.
    elif column%4==3:
        if row==0:
            return (row,column-1)
        return (row-1,column+1)



def bit_list_to_raw_matrix(bit_list:list[int], qr_layout:dict)->list[list[int]]:
    '''
        Turns a bit list into a raw QR code matrix,
        by iterating over the QR code positions using the get_next_pos function.
    '''

    # Initialize QR code matrix.
    matrix = [[0]*qr_layout["side_length"] for row in range(qr_layout["side_length"])]

    # Start in lower right corner.
    row = qr_layout["side_length"]-1
    column =  qr_layout["side_length"]-1

    # Go through all bits.
    for bit in bit_list:

        # If the bit is inside a fixed field or meta pattern field we continue until we're not.
        while ([row,column] in qr_layout["fixed_positions"]["ones"]
        or [row,column] in qr_layout["fixed_positions"]["zeros"]
        or [row,column] in qr_layout["meta_positions"]["first"]
        or [row,column] in qr_layout["meta_positions"]["second"]):
            row, column = get_next_pos(row,column,qr_layout["side_length"])

        # Set the matrix cell state to the bit.
        matrix[row][column]=bit

        # Next bit new position.
        row, column = get_next_pos(row,column,qr_layout["side_length"])

    return matrix
