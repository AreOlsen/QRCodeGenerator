from logic.matrix_fields import set_fixed_fields, set_meta_fields

def should_flip(row:int, col:int, mask_no:int)->bool:
    '''
    Function that decides if the current cell should be flipped according to the mask.
    '''
    match mask_no:
        case 0:
            return ((row + col) % 2 == 0)
        case 1:
            return (row % 2 == 0)
        case 2:
            return (col % 3 == 0)
        case 3:
            return ((row + col) % 3 == 0)
        case 4:
            return ((row//2 + col//3) % 2 == 0)
        case 5:
            return  ((row*col) % 2 + (row*col) % 3 == 0)
        case 6:
            return (((row*col) % 2 + (row*col) % 3) % 2 == 0)
        case 7:
            return (((row+col) % 2 + (row*col) % 3) % 2 == 0)
        case _:
            return False



def score_matrix(matrix:list[int])->int:
    '''
    To have an effective QR code,
    there should be as much black cells as white cells,
    this function scores the QR according to this.
    '''
    num_ones = 0
    num_zeros = 0

    # Get count of both cell types.
    for row in matrix:
        for cell in row:
            if cell:
                num_ones+=1
            else:
                num_zeros+=1

    #Return matrix score.
    return abs(num_ones-num_zeros)



def get_masked_matrix(matrix:list[int], mask_no:int)->list[int]:
    '''
    This takes the QR code raw bit matrix, and applies the mask to it.
    '''

    #Initialize new matrix with 0 for each position.
    masked_matrix = [[0]*len(matrix[0]) for row in range(len(matrix))]

    #Go through all values and apply rules and mask.
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            #Apply the XOR rule specified.
            masked_matrix[row_index][col_index] = cell ^ should_flip(row_index,col_index,mask_no)

    return masked_matrix



def get_refined_matrix(raw_matrix:list[int], error_correction_level:str, qr_layout:dict)->list[int]:
    '''
    There are many data variations of the same QR code.
    This applies the fields ( which are used for better tracking, etc. ).
    And then chooses the best QR code.
    '''

    #Masked matrix.
    qr_variations = [
        get_masked_matrix(raw_matrix, mask_no)
        for mask_no in range(8)
    ]

    # Apply fields (destructive) functions to matrices.
    for mask_no, masked_matrix in enumerate(qr_variations):
        set_meta_fields(masked_matrix, error_correction_level, mask_no, qr_layout)
        set_fixed_fields(masked_matrix, qr_layout)

    # Get lowest (best) scoring QR code variation.
    scores = [score_matrix(matrix) for matrix in qr_variations]
    best_mask_no = scores.index(min(scores))

    return qr_variations[best_mask_no]
