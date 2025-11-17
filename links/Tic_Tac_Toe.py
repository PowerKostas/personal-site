import Dice_Competition

print('Welcome to the Tic Tac Toe Game!')

games=0
score_1=0
score_2=0
flag=False
flag_2=False
while flag_2==False:
    if games!=0:
        print('\nThe score is: ''\n'+player_1+'='+str(score_1)+' - '+player_2+'='+str(score_2))
        while flag==False:
            answer=input('\nDo you want to play again? (yes or no)\n\n')
            if answer=='yes':
                print('\nLets Go!')
                flag=True
            elif answer=='no':
                print('\nThanks for playing!')
                flag=True
                flag_2=True
            else:
                print('\nI told you to type yes or no...')
    games+=1

    if flag_2==False:
        if games==1:
            player_1=input('\nPlease enter your name Player 1: ')
            player_2=input('\nPlease enter your name Player 2: ')

        flag=True
        while flag==True:
            number=input('\nWho wants to play first? (You will also be able to choose your symbol,just type the appropriate letter)\n\n(a) '+player_1+' (b) '+player_2+' (c) Roll The Dice\n\n')
            if number=='a':
                winner=player_1
                loser=player_2
            elif number=='b':
                winner=player_2
                loser=player_1
            if number=='a' or number=='b' or number=='c':
                break
            else:
                print('\nI told you to put the appropriate letter...')

        if number=='c':
            roll_1,roll_2=Dice_Competition.dice(player_1,player_2)
            if roll_1>roll_2:
                winner=player_1
                loser=player_2
            elif roll_1<roll_2:
                winner=player_2
                loser=player_1

        mhkos=3
        platos=3

        flag=False
        while flag==False:
            symbol=input('\n'+winner+' do you want your symbol to be (X) or (O)?\n\n')
            if symbol=='X':
                symbol_winner='X'
                symbol_loser='O'
                flag=True
            elif symbol=='O':
                symbol_winner='O'
                symbol_loser='X'
                flag=True
            else:
                print('\nPut either (X) or (O)')
        
        turn=1
        list_1=[]
        flag_3=True
        while turn<=mhkos*platos and flag_3:
            flag=False
            while flag==False:
                try:
                    if turn==1:
                        rest=(
                        '_____ ',
                        '     |',
                        '_____|',
                        )
                        shape='\n' 
                        for i in range(platos):  
                            if i==0:
                                shape=shape+'      '+str(i+1)      
                            elif i>=10:
                                shape=shape+'    '+str(i+1)
                            else:    
                                shape=shape+'     '+str(i+1)
                        shape=shape+'\n''    '+rest[0]*platos
                        for i in range(1,mhkos+1):
                            for j in range(2):
                                if j==1:
                                    if i>=10:
                                        shape=shape+'\n'+str(i)+' |'+rest[1]*platos
                                    else:
                                        shape=shape+'\n'+str(i)+'  |'+rest[1]*platos
                                else: 
                                    shape=shape+'\n''   |'+rest[1]*platos
                            shape=shape+'\n''   |'+rest[2]*platos
                        print(shape)
                            
                        x,y=input('\n'+winner+' plays first! (Put the coordinates of your choice seperated by a space) ').split()
                        new_shape=list(shape)
                        symbol_used=symbol_winner
                        flag=True

                    elif turn % 2!=0:
                        x,y=input('\n'+winner+' make your decision... ').split()
                        symbol_used=symbol_winner
                        flag=True
                    else:
                        x,y=input('\n'+loser+' make your decision... ').split()
                        symbol_used=symbol_loser
                        flag=True

                    x=int(x)
                    y=int(y)
                    if x>mhkos or y>platos:
                        print('\nCoordinates out of limits...')
                        flag=False
                    elif x<0 or y<0:
                        print("\nCoordinates can't be below zero...")
                        flag=False
                    elif x==0 or y==0:
                        print("\nCoordinates can't be equal to zero...")
                        flag=False
                    for i in range(len(list_1)-1)[::2]:
                        if list_1[i]==x and list_1[i+1]==y:
                            print('\nThere is already a symbol in that square...')
                            flag=False
                    list_1.append(x)
                    list_1.append(y)
                except ValueError:
                    print('\nPut two integers seperated by a comma...')
                
            turn+=1
            addment=(platos-3)*18
            x_1=69+addment  
            new_shape[(x_1*x)+(y*6)-2]=symbol_used 
            optional=0  

            i=1
            m=0
            z=0
            addment_1=0
            flag=True
            k=73+addment
            k_like=k
            k_like_3=k
            while i<=mhkos and flag:
                #vertical checking
                if i<=mhkos:                       
                    if new_shape[k]==new_shape[k+6]==new_shape[k+12]==symbol_used:
                        for i in range(1,12):
                            if k+optional+i!=k+6+optional:
                                new_shape[k+i]='-'
                        print(''.join(new_shape))
                        flag=False
                        flag_3=False
                        break
                addment_1=0
                #horizontal checking
                if i<=platos:
                    if new_shape[73+addment+m]==new_shape[73+addment+69+addment+m]==new_shape[73+addment+(69+addment)*2+m]==symbol_used:
                        for i in range(5):
                            z+=23+(platos-3)*6
                            if 73+addment+m+z!=73+addment+69+addment+m:
                                new_shape[73+addment+m+z]='┃'
                        print(''.join(new_shape))
                        flag=False
                        flag_3=False
                addment_1=0
                m+=6
                z=0
                #diagonal right checking
                if new_shape[k_like]==new_shape[k_like+75+addment]==new_shape[k_like+(75+addment)*2]==symbol_used:
                    for i in range(5):
                        z+=25+(platos-3)*6
                        if k_like+z!=k_like+75+addment:
                            new_shape[k_like+z]='\\'
                    print(''.join(new_shape))
                    flag=False
                    flag_3=False
                addment_1=0
                z=0
                #diagonal left checking
                if new_shape[k_like_3+(platos-1)*6]==new_shape[k_like_3+(platos-2)*6+69+addment]==new_shape[k_like_3+(platos-3)*6+(69+addment)*2]==symbol_used:
                    for i in range(5):
                        z+=21+(platos-3)*6
                        if k_like_3+(platos-1)*6+z!=k_like_3+(platos-2)*6+69+addment:
                            new_shape[k_like_3+(platos-1)*6+z]='/'
                    print(''.join(new_shape))
                    flag=False
                    flag_3=False

                addment_1=0
                k_like+=6
                k_like_3-=6
                k+=69+addment
                i+=1     
            if flag_3==False:
                if winner==player_1:
                    if symbol_used==symbol_winner:
                        score_1+=1
                    else:
                        score_2+=1
                else:
                    if symbol_used==symbol_winner:
                        score_2+=1
                    else:
                        score_1+=1 
            if flag_3:
                print(''.join(new_shape))
            flag=False