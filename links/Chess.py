from math import gcd

def build_board(board,letter_coordinates,number_coordinates,reverse_board):
    if reverse_board: 
        board.reverse()
        letter_coordinates.reverse()
        number_coordinates.reverse()

    count=0
    for i in range(8): # For every row
        print('\n',number_coordinates[i],'  ',end='') # Prints number next to the board
        for j in range(8): # For every column
            print(board[count],end='  ') # Prints board piece, there are 64 items in the array, thats why I use a makeshift count
            count+=1
    print('\n\n    ','  '.join(letter_coordinates)) # Prints letters below the board

    if reverse_board: # Reverses board back to the default
        board.reverse()
        letter_coordinates.reverse()
        number_coordinates.reverse()
    
    return board,letter_coordinates,number_coordinates

def read_coordinates(player,my_pieces):
    piece_dict={'P':my_pieces[0],'N':my_pieces[1],'B':my_pieces[2],'R':my_pieces[3],'Q':my_pieces[4],'K':my_pieces[5]} # To find the appropriate piece symbol
    legal_moves_dict={'P':[8,16,9,7],'N':[17,10,15,6,-17,-10,-15,-6],'B':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49],'R':[8,16,24,32,40,48,56,1,2,3,4,5,6,7,-8,-16,-24,-32,-40,-48,-56,-1,-2,-3,-4,-5,-6,-7],'Q':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49,8,16,24,32,40,56,1,2,3,4,5,6,-8,-16,-24,-32,-40,-56,-1,-2,-3,-4,-5,-6],'K':[9,8,7,-1,1,-9,-8,-7]}
    if player=='Black': # Because the pawn only moves forward, not in all directions like all the other pieces, the computer playing black will basically move the pawn backwards
        legal_moves_dict.update({'P':[-8,-16,-9,-7]})

    while True:
        coordinates=input('\nGive coordinates: ') # Accepts coordinates like Nb1c3
        if coordinates in ('O-O','O-O-O'): # Special coordinates, thats why they are put in the front
            return coordinates,None,None,piece_dict,legal_moves_dict
        elif len(coordinates)==5:
            if coordinates[0] in ('P','N','B','R','Q','K'): 
                if all(elem in ('a','b','c','d','e','f','g','h') for elem in [coordinates[1],coordinates[3]]): # If both of the second elems are in the first elems
                    if all(elem in ('1','2','3','4','5','6','7','8') for elem in [coordinates[2],coordinates[4]]):
                        return coordinates,piece_dict[coordinates[0]],legal_moves_dict[coordinates[0]],piece_dict,legal_moves_dict
        print('\nInvalid coordinates!') # If the coordinates were valid the function would have returned at some point

def castle_checking(board,player,white_castle,black_castle,castling_flag): # Checks if any of the pieces that are needed to castle (rooks,king) have moved already
    if player=='White' and castling_flag[0]==False: # If the player is white and hasn't castled already
        if board[white_castle[1][0]]==' ': # Left rook
            white_castle[0][0]=False # False = It has moved
        elif board[white_castle[1][1]]==' ': # King
            white_castle[0][1]=False
        elif board[white_castle[1][2]]==' ': # Rights rook
            white_castle[0][2]=False
        return white_castle
    elif player=='Black' and castling_flag[1]==False:
        if board[black_castle[1][0]]==' ':
            black_castle[0][0]=False
        elif board[black_castle[1][1]]==' ':
            black_castle[0][1]=False
        elif board[black_castle[1][2]]==' ':
            black_castle[0][2]=False
        return black_castle

    return [[False,False,False],[0,0,0]] # Returns this default array so no errors happen, if the player whose turn is now, has already castled

def castling(board,player,my_pieces,enemy_pieces,coordinates,temp_castle,castling_flag,king_pos):
    block_move=True
    if coordinates=='O-O' and board[temp_castle[1][1]+1]==' ' and board[temp_castle[1][1]+2]==' ' and temp_castle[0][1]==temp_castle[0][0]==True: # If short castle coordinates and the two spaces between the right rook and king have no pieces there and the right rook and king haven't moved
        for i in range(0,3): # For the 3 squares starting from the king to to the right rook
            blocking_castling_flag=castling_checking_check(board,player,my_pieces,enemy_pieces,temp_castle[1][1]+i,1,0) # Checks if an enemy piece is attacking that square (the second parameter), thus preventing the king from castling, 0 signalises why we are calling the function (to check castling blocking)
            if blocking_castling_flag:
                return block_move,castling_flag,king_pos

        # Moves king in the correct positon
        board[temp_castle[1][1]+2]=my_pieces[5]
        board[temp_castle[1][1]]=' '
        # Moves right rook in the correct position
        board[temp_castle[1][2]-2]=my_pieces[3]
        board[temp_castle[1][2]]=' '
        # To show right rook and king have moved
        temp_castle[0][1]=False
        temp_castle[0][2]=False
        block_move=False
        if player=='White':
            castling_flag[0]=True # To not check, white, for castling again
            king_pos[0]=62
        else:
            castling_flag[1]=True # To not check, black, for castling again
            king_pos[1]=6
    elif coordinates=='O-O-O' and board[temp_castle[1][1]-1]==' ' and board[temp_castle[1][1]-2]==' ' and board[temp_castle[1][1]-3]==' ' and temp_castle[0][1]==temp_castle[0][2]==True: # If long castle coordinates and the three spaces between the king and the left rook have no pieces there and the king and left rook haven't moved
        for i in range(0,3): # For the 3 squares starting from the king to the left rook, (without the last square because the king doesn't travel through there
            blocking_castling_flag=castling_checking_check(board,player,my_pieces,enemy_pieces,temp_castle[1][1]-i,1,0)
            if blocking_castling_flag:
                return block_move,castling_flag,king_pos

        board[temp_castle[1][1]-2]=my_pieces[5]
        board[temp_castle[1][1]]=' '
        board[temp_castle[1][0]+3]=my_pieces[3]
        board[temp_castle[1][0]]=' '  
        temp_castle[0][1]=False
        temp_castle[0][0]=False
        block_move=False
        if player=='White':
            castling_flag[0]=True
            king_pos[0]=58
        else:
            castling_flag[1]=True
            king_pos[1]=2

    if block_move:
        print('\nIllegal Castling!')

    return block_move,castling_flag,king_pos

def blocking_move_check(board,coordinates,start,end,print_call_type):
    # Finds a tuple of the direction, from the current position of a piece to where the coordinates want it to go (eg [-1,-1] if the piece needs to go diagonal left) (From ChatGPT, so I dont understand the details of it)
    row_diff=(end // 8)-(start // 8)
    col_diff=(end % 8)-(start % 8)
    gcd_val=gcd(row_diff,col_diff)
    direction=[row_diff // gcd_val,col_diff // gcd_val]

    block_move=False
    if coordinates[0]!='P': # This method doesn't check the last square of the coordinates, because for every other piece even if there is a enemy piece in that last square (we already check for friendly pieces in the make_move function), it's should capture it, not block it
        start+=direction[0]*8+direction[1] # Moves one square to the direction we found
        while start!=end:
            if board[start]!=' ':
                block_move=True
                if print_call_type==0: # To show message only when playing actual moves, not when playing test moves to see if a check still happens
                    print('\nThere is a piece blocking the move')
                break
            start+=direction[0]*8+direction[1]
    else: # This is for the case of a pawn moving forward, because a pawn doesn't capture in it's forward move, if there is a piece in the designated square (we already check for the diagonal captures in the make_move function)
        while start!=end:
            start+=direction[0]*8+direction[1]
            if board[start]!=' ':
                block_move=True
                if print_call_type==0:
                    print('\nThere is a piece blocking the move')
                break
    return block_move

def castling_checking_check(board,player,my_pieces,enemy_pieces,start,call_type,print_call_type): # Checks if there is an enemy piece attacking a square needed for castling and checks for checks
    reverse_enemy_piece_dict={enemy_pieces[0]:'P',enemy_pieces[1]:'N',enemy_pieces[2]:'B',enemy_pieces[3]:'R',enemy_pieces[4]:'Q',enemy_pieces[5]:'K'} # Like the normal piece dict, but the items are reversed and it's for the enemy pieces
    temp_legal_moves_dict={'P':[8,16,9,7],'N':[17,10,15,6,-17,-10,-15,-6],'B':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49],'R':[8,16,24,32,40,48,56,1,2,3,4,5,6,7,-8,-16,-24,-32,-40,-48,-56,-1,-2,-3,-4,-5,-6,-7],'Q':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49,8,16,24,32,40,56,1,2,3,4,5,6,-8,-16,-24,-32,-40,-56,-1,-2,-3,-4,-5,-6],'K':[9,8,7,-1,1,-9,-8,-7]} # Temp so not to change the values of the actual ones
    # Corners of the board, where the checking should stop
    left_pos=[56,48,40,32,24,16,8,0]
    top_pos=[0,1,2,3,4,5,6,7]
    right_pos=[63,55,47,39,31,23,15,7]
    bottom_pos=[56,57,58,59,60,61,62,63]
    if player=='White':
        directions=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] # All the possible directions that king/square can be attacked from
        end_pos=[left_pos+top_pos,[start % 8],right_pos+top_pos,[start-(start % 8)],[start+(start % 8)+1],left_pos+bottom_pos,[56+(start % 8)],right_pos+bottom_pos] # The squares where checking should stop
        temp_legal_moves_dict.update({'P':[-8,-16,-9,-7]}) # Like the previous pawn legal moves update, but we use a different method here so white is the changed one
    else:
        directions=[[1, 1],[1, 0],[1, -1],[0, 1],[0, -1],[-1, 1],[-1, 0],[-1, -1]] # Directions are reversed for black
        end_pos=[left_pos+top_pos,[start % 8],right_pos+top_pos,[start-(start % 8)],[start+(start % 8)+1],left_pos+bottom_pos,[56+(start % 8)],right_pos+bottom_pos]
        end_pos.reverse() # Since directions are reversed so should the end positions

    check_flag=False
    for i in range(len(directions)): # We check to every direction
        temp_start=start+directions[i][0]*8+directions[i][1] # We move the start one square to the first direction so we dont check for the square that we are starting from
        while True: # (Looks messy but it's the only way I get it to work)
            if temp_start>=0 and temp_start<=63: # If it goes out of the board index we stop this direction
                if board[temp_start] in my_pieces: # If it first meets a friendly piece, it means the king is safe
                    break
                elif board[temp_start] in enemy_pieces and temp_start-start in temp_legal_moves_dict[reverse_enemy_piece_dict[board[temp_start]]]: # If its an enemy piece and the distance between the king and the enemy piece is in the enemy piece's legal moves
                    check_flag=True
                    break
            else:
                break
            if temp_start in end_pos[i]: # If it has reached the end position we stop this direction, the if is put here so it first checks this end square then stops
                break

            temp_start+=directions[i][0]*8+directions[i][1] # We move one square to the direction set
        if check_flag: # Stops if there is a check on the king
            break
    
    if not check_flag: # If a check has not already happened, we check the knight's moves
        for i in range(8): # For every possible knight move
            if (start+temp_legal_moves_dict['N'][i]>=0 and start+temp_legal_moves_dict['N'][i]<=63) and abs((start % 8)-((start+temp_legal_moves_dict['N'][i]) % 8))<=2: # Starting from the king, if a knight move is in the board's index and it doesn't go from one side of the board to the other
                if board[start+temp_legal_moves_dict['N'][i]]==enemy_pieces[1]: # Starting from the king, if in a knight move there is actually a knight there, it is a check
                    check_flag=True
                    break

    if print_call_type==0: # To show message only when playing actual moves, not when playing test moves to see if a check still happens
        if check_flag and call_type==0:
            print('\nYou are in check!')
        elif check_flag and call_type==1:
            print('\nThere is an enemy piece blocking the king from castling!')

    return check_flag

def checkmate_stalemate_check(legal_moves_dict,piece_dict,board,player,my_pieces,piece,enemy_pieces,letter_value_dict,number_value_dict,temp_pawn_has_moved,en_passant_pos,en_passant_count,temp_castle,castling_flag,king_pos,check_flag):
    reverse_letter_value_dict={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
    reverse_number_value_dict={56:'1',48:'2',40:'3',32:'4',24:'5',16:'6',8:'7',0:'8'}
    reverse_piece_dict={my_pieces[0]:'P',my_pieces[1]:'N',my_pieces[2]:'B',my_pieces[3]:'R',my_pieces[4]:'Q',my_pieces[5]:'K'} # Like the normal piece dict, but the items are reversed
    
    temp_legal_moves_dict={'P':[8,16,9,7],'N':[17,10,15,6,-17,-10,-15,-6],'B':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49],'R':[8,16,24,32,40,48,56,1,2,3,4,5,6,7,-8,-16,-24,-32,-40,-48,-56,-1,-2,-3,-4,-5,-6,-7],'Q':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49,8,16,24,32,40,56,1,2,3,4,5,6,-8,-16,-24,-32,-40,-56,-1,-2,-3,-4,-5,-6],'K':[9,8,7,-1,1,-9,-8,-7]} # Temp so not to change the values of the actual ones
    left_pos=[56,48,40,32,24,16,8,0]
    top_pos=[0,1,2,3,4,5,6,7]
    right_pos=[63,55,47,39,31,23,15,7]
    bottom_pos=[56,57,58,59,60,61,62,63]
    if player=='White':
        directions=[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] # All the possible directions that king/square can be attacked from
        end_pos=[left_pos+top_pos,top_pos,right_pos+top_pos,left_pos,right_pos,left_pos+bottom_pos,bottom_pos,right_pos+bottom_pos] # The squares where checking should stop
        temp_legal_moves_dict.update({'P':[-8,-16,-9,-7]}) # Like the previous pawn legal moves update, but we use a different method here so white is the changed one
    else:
        directions=[[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]] # Directions are reversed for black
        end_pos=[left_pos+top_pos,top_pos,right_pos+top_pos,left_pos,right_pos,left_pos+bottom_pos,bottom_pos,right_pos+bottom_pos]
        end_pos.reverse() # Since directions are reversed so should the end positions

    temp_king_pos=king_pos[:]
    for i in range(len(board)):
        if board[i] in my_pieces:
            if board[i]!=my_pieces[1]:
                legal_moves=legal_moves_dict[reverse_piece_dict[board[i]]]
                temp_directions=directions
                if board[i]==my_pieces[0]:
                    temp_directions=[directions[0]]+[directions[1]]+[directions[2]]
                elif board[i]==my_pieces[2]:
                    temp_directions=[directions[0]]+[directions[2]]+[directions[5]]+[directions[7]]
                elif board[i]==my_pieces[3]:
                    temp_directions=[directions[1]]+[directions[3]]+[directions[4]]+[directions[6]]

                for j in range(len(temp_directions)): # We check to every direction
                    temp_start=i+temp_directions[j][0]*8+temp_directions[j][1] # We move the start one square to the first direction so we dont check for the square that we are starting from
                    count=1
                    while True:
                        if temp_start<=0 or temp_start>=63 or abs((i % 8)-(temp_start % 8))>j+count or board[temp_start] in my_pieces: # If it goes out of the board index we stop this direction
                            break
                        if board[i]==my_pieces[5]:
                            if player=='White':
                                temp_king_pos[0]=temp_start
                            else:
                                temp_king_pos[1]=temp_start

                        coordinates=reverse_piece_dict[board[i]]+reverse_letter_value_dict[i % 8]+reverse_number_value_dict[i-(i % 8)]+reverse_letter_value_dict[temp_start % 8]+reverse_number_value_dict[temp_start-(temp_start % 8)]
                        board,temp_pawn_has_moved,en_passant_pos,en_passant_count,castling_flag,temp_king_pos,block_move,check_flag=make_move(board,player,my_pieces,board[i],enemy_pieces,coordinates,letter_value_dict,number_value_dict,legal_moves,temp_pawn_has_moved,en_passant_pos,en_passant_count,temp_castle,castling_flag,temp_king_pos,check_flag,1)

                        if not block_move:
                            return False

                        if (count==1 and ((board[i]==my_pieces[0] and temp_directions[j]!=temp_directions[1]) or board[i]==my_pieces[5])) or (count==2 and temp_directions[j]==temp_directions[1]):
                            break

                        temp_start+=directions[j][0]*8+directions[j][1] # We move one square to the direction set
                        count+=1
            else:
                legal_moves=legal_moves_dict[reverse_piece_dict[board[i]]]
                for j in range(8): # For every possible knight move
                    if (i+legal_moves[j]>=0 and i+legal_moves[j]<=63) and abs((i % 8)-((i+legal_moves[j]) % 8))<=2:
                        if board[i+legal_moves[j]] in my_pieces:
                            continue

                        coordinates=reverse_piece_dict[board[i]]+reverse_letter_value_dict[i % 8]+reverse_number_value_dict[i-(i % 8)]+reverse_letter_value_dict[(i+legal_moves[j]) % 8]+reverse_number_value_dict[(i+legal_moves[j])-((i+legal_moves[j]) % 8)]
                        board,temp_pawn_has_moved,en_passant_pos,en_passant_count,castling_flag,king_pos,block_move,check_flag=make_move(board,player,my_pieces,board[i],enemy_pieces,coordinates,letter_value_dict,number_value_dict,legal_moves,temp_pawn_has_moved,en_passant_pos,en_passant_count,temp_castle,castling_flag,king_pos,check_flag,1)
                        
                        if not block_move:
                            return False
    return True

def make_move(board,player,my_pieces,piece,enemy_pieces,coordinates,letter_value_dict,number_value_dict,legal_moves,temp_pawn_has_moved,en_passant_pos,en_passant_count,temp_castle,castling_flag,king_pos,check_flag,call_type):
    # We backup these for later
    backup_board_2=board[:]
    backup_temp_pawn_has_moved_2=temp_pawn_has_moved[:]

    block_move=False
    if coordinates!='O-O' and coordinates!='O-O-O': # It handles castling differently
        # In coordinates like Nb1c3 b1 is the start position and c3 the end position
        start=letter_value_dict[coordinates[1]]+number_value_dict[coordinates[2]]
        end=letter_value_dict[coordinates[3]]+number_value_dict[coordinates[4]]
        start_end_diff=letter_value_dict[coordinates[1]]+number_value_dict[coordinates[2]]-(letter_value_dict[coordinates[3]]+number_value_dict[coordinates[4]])
        if start_end_diff in legal_moves and board[start]==piece and board[end] not in my_pieces: # If it's a legal move and there is the appropriate piece in the start position and there is not a friendly piece in the end position
            if coordinates[0]=='P' and start_end_diff in (legal_moves[2],legal_moves[3]): # If it's a pawn capture move
                if end+legal_moves[0]==en_passant_pos: # En passant case, end+legal_moves[0] is the position besides the friendly pawn (the position where a pawn can be en passanted), en_passant_pos gets the position of an enemy pawn when it moves 2 squares, it gets reseted next turn
                    board[end+legal_moves[0]]=' ' # Enemy pawn gets captured
                elif board[end] not in enemy_pieces:
                    if call_type==0:
                        print('\nThere is not a piece to capture there!')
                    block_move=True
            else:
                block_move=blocking_move_check(board,coordinates,start,end,call_type) # Checks if there is a piece interving the piece going from the start position to the end one
                if coordinates[0]=='P':
                    if start_end_diff==legal_moves[1]: # If pawn tries to move 2 squares
                        if temp_pawn_has_moved[letter_value_dict[coordinates[1]]]==True: # It's not allowed if that pawn has already moved
                            if call_type==0:
                                print('\nThis pawn has already moved!')
                            block_move=True
                        elif call_type==0: # Has to do an additional check, to fix a bug where it would change the en_passant_pos when checking for checkmates etc (because testing moves are being played there)
                            en_passant_pos=end
                            en_passant_count=0
                    temp_pawn_has_moved[letter_value_dict[coordinates[1]]]=True
        else:
            block_move=True
            if call_type==0:
                print('\nIllegal move!')

        if coordinates[0]=='P' and end in (0,1,2,3,4,5,6,7,56,57,58,59,60,61,62,63) and call_type==0:
            piece=pawn_promotion()
            
        if not block_move:
            board[letter_value_dict[coordinates[1]]+number_value_dict[coordinates[2]]]=' ' # Removes piece from start position
            board[letter_value_dict[coordinates[3]]+number_value_dict[coordinates[4]]]=piece # Replaces whatever there is on the end position with the piece
            if coordinates[0]=='K' and call_type==0: # # To change the king_pos only when playing actual moves, not when playing test moves to see if a check still happens
                if player=='White':
                    king_pos[0]=end
                else:
                    king_pos[1]=end
    else:
        block_move,castling_flag,king_pos=castling(board,player,my_pieces,enemy_pieces,coordinates,temp_castle,castling_flag,king_pos)

    if not block_move: # No need to go here if the move is already blocked
        if player=='White': # Checks if there are checks on the king, king_pos[0] is the position of the white king, king_pos[1] is the position of the black king
            check_flag=castling_checking_check(board,player,my_pieces,enemy_pieces,king_pos[0],0,call_type)
        else:
            check_flag=castling_checking_check(board,player,my_pieces,enemy_pieces,king_pos[1],0,call_type) 

        if check_flag: # If there is a check
            block_move=True
            # Reverts the board and the array of if the pawns have moved, because if there is still a check on the king after the move, that move cannot be played and we need to revert the board
            # board=backup_board
            # temp_pawn_has_moved=backup_temp_pawn_has_moved

    if call_type==1 or check_flag:
        board=backup_board_2
        temp_pawn_has_moved=backup_temp_pawn_has_moved_2

    if en_passant_count==2: # It resets the en passant position every 2 turns (when white or black plays again)
            en_passant_pos='Null'

    return board,temp_pawn_has_moved,en_passant_pos,en_passant_count,castling_flag,king_pos,block_move,check_flag

def pawn_promotion():
    while True:
        answer=input('\nDo you want a (K)night a (B)ishop a (Rook) or a (Q)ueen): ')
        if answer=='K':
            piece=my_pieces[1]
            return piece
        elif answer=='B':
            piece=my_pieces[2]
            return piece
        elif answer=='R':
            piece=my_pieces[3]
            return piece
        elif answer=='Q':
            piece=my_pieces[4]
            return piece
        
def change_player(turn,white_pawn_has_moved,black_pawn_has_moved,temp_pawn_has_moved,legal_moves_dict):
    turn+=1
    if turn % 2==0: # If white
        player='White'
        my_pieces=['♟','♞','♝','♜','♛','♚']
        enemy_pieces=['♙','♘','♗','♖','♕','♔']
        black_pawn_has_moved=temp_pawn_has_moved # Saves change of the previous player from the temp array
        temp_pawn_has_moved=white_pawn_has_moved # Changes the temp array to the current player
        legal_moves_dict.update({'P':[8,16,9,7]})
    else: # If black
        player='Black' 
        my_pieces=['♙','♘','♗','♖','♕','♔']
        enemy_pieces=['♟','♞','♝','♜','♛','♚']
        white_pawn_has_moved=temp_pawn_has_moved 
        temp_pawn_has_moved=black_pawn_has_moved 
        legal_moves_dict.update({'P':[-8,-16,-9,-7]})

    return turn,player,my_pieces,enemy_pieces,white_pawn_has_moved,black_pawn_has_moved,temp_pawn_has_moved,legal_moves_dict

# Initializing variables 
board=['♖','♘','♗','♕','♔','♗','♘','♖','♙','♙','♙','♙','♙','♙','♙','♙',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','♟','♟','♟','♟','♟','♟','♟','♟','♜','♞','♝','♛','♚','♝','♞','♜'] 
# For printing
number_coordinates=['(8)','(7)','(6)','(5)','(4)','(3)','(2)','(1)'] 
letter_coordinates=['  ⒜','⒝','⒞','⒟','⒠','⒡','⒢','⒣']
# Where in the board array would a coordinate like Pd2d4 land
letter_value_dict={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
number_value_dict={'1':56,'2':48,'3':40,'4':32,'5':24,'6':16,'7':8,'8':0}
# The player starting is always white
player='White'
my_pieces=['♟','♞','♝','♜','♛','♚']
enemy_pieces=['♙','♘','♗','♖','♕','♔']
# White/Black king position
king_pos=[60,4] 
# Each boolean is for the left rook, king and right rook, if its true it means that that piece hasn't moved and the second array is their position on the board
white_castle=[[True]*3,[56,60,63]]
black_castle=[[True]*3,[0,4,7]]
# If each side has castled
castling_flag=[False,False]
# Which pawns have already moved squares
white_pawn_has_moved=[False]*8
black_pawn_has_moved=[False]*8
temp_pawn_has_moved=[False]*8 # In this variable we put either the white or black variable, whether on whose turn is it
# Variables needed for en passant,check set at a default value
en_passant_pos='Null'
en_passant_count=0
check_flag=False

human='White'
reverse_board=False
while True: # Asks the player if he is white or black
    answer=input('\nAre you (W)hite or (B)lack: ')
    if answer=='W' or answer=='B':
        if answer=='B': # If the player is black we will be reversing the board to be always facing him (only for visuals)
            human='Black'
            reverse_board=True
        break
board,letter_coordinates,number_coordinates=build_board(board,letter_coordinates,number_coordinates,reverse_board)

turn=0   
end_flag=False
piece=None
piece_dict={'P':my_pieces[0],'N':my_pieces[1],'B':my_pieces[2],'R':my_pieces[3],'Q':my_pieces[4],'K':my_pieces[5]} # To find the appropriate piece symbol
legal_moves_dict={'P':[8,16,9,7],'N':[17,10,15,6,-17,-10,-15,-6],'B':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49],'R':[8,16,24,32,40,48,56,1,2,3,4,5,6,7,-8,-16,-24,-32,-40,-48,-56,-1,-2,-3,-4,-5,-6,-7],'Q':[9,18,27,36,45,54,63,7,14,21,28,35,42,49,-9,-18,-27,-36,-45,-54,-63,-7,-14,-21,-28,-35,-42,-49,8,16,24,32,40,56,1,2,3,4,5,6,-8,-16,-24,-32,-40,-56,-1,-2,-3,-4,-5,-6],'K':[9,8,7,-1,1,-9,-8,-7]}

for j in range(50):
    if not castling_flag[0]==castling_flag[1]==True: # If both sides have castled, there is no point to check if castling is legal again
        temp_castle=castle_checking(board,player,white_castle,black_castle,castling_flag)
    while True:
        backup_board_1=board[:]
        backup_temp_pawn_has_moved_1=temp_pawn_has_moved[:]
        end_flag=checkmate_stalemate_check(legal_moves_dict,piece_dict,board,player,my_pieces,piece,enemy_pieces,letter_value_dict,number_value_dict,temp_pawn_has_moved,en_passant_pos,en_passant_count,temp_castle,castling_flag,king_pos,check_flag)
        board=backup_board_1
        temp_pawn_has_moved=backup_temp_pawn_has_moved_1
        if end_flag:
            print('\nEnd of game!')
            break

        coordinates,piece,legal_moves,piece_dict,legal_moves_dict=read_coordinates(player,my_pieces)
        board,temp_pawn_has_moved,en_passant_pos,en_passant_count,castling_flag,king_pos,block_move,check_flag=make_move(board,player,my_pieces,piece,enemy_pieces,coordinates,letter_value_dict,number_value_dict,legal_moves,temp_pawn_has_moved,en_passant_pos,en_passant_count,temp_castle,castling_flag,king_pos,check_flag,0)
        if not block_move:
            en_passant_count+=1 # It's put here because it only needs to increase after every turn ends, not if the move is blocked
            break
    if end_flag:
        break

    board,letter_coordinates,number_coordinates=build_board(board,letter_coordinates,number_coordinates,reverse_board)
    turn,player,my_pieces,enemy_pieces,white_pawn_has_moved,black_pawn_has_moved,temp_pawn_has_moved,legal_moves_dict=change_player(turn,white_pawn_has_moved,black_pawn_has_moved,temp_pawn_has_moved,legal_moves_dict)
