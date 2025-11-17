#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <windows.h>
#include <string.h>

struct cards // Krataei tin aksia tis kartas kai thn morfh pou tha exei otan ektypwnetai
{
	int value;
	char design[10][15];
};
	
struct cards fill_card_details(struct cards card,int random_num,int *hand_value) // Gemizei tyxaia mia karta kai thn epistrefei
{	
	// Prepei na ginoun ksexorista autes oi kartes giati periexoun chars (K,Q...) kai oxi ints (2,3...), opws oi ypoloipes
	// Epishs pairnoun diaforetikes times apo autes pou etyxan (px h karta K tha exei aksia 10 kai oxi 13 opws tha tyxaine)
	if (random_num==13)
	{
		card.value=10;
		strcpy(card.design[1],"| K       K |"); // Auto einai to meros ths kartas pou allazei kathe fora
	}
	else if (random_num==12)
	{
		card.value=10;
		strcpy(card.design[1],"| Q       Q |");
	}
	else if (random_num==11)
	{
		card.value=10;
		strcpy(card.design[1],"| J       J |");
	}
	else if (random_num==10)
	{
		card.value=10;
		strcpy(card.design[1],"| 10     10 |");
	}
	else if (random_num==1)
	{
		if (*hand_value+11<=21) // H aksia tou assou tha einai 11, efoson o paikths den kaigetai, alliws tha einai 1
			card.value=11;
		else
			card.value=1;
		strcpy(card.design[1],"| A       A |");
	}
	else 
	{
		card.value=random_num;
		// Metatrepei ton tyxaio int se char gia na mpei stï ypoloipo string pou tha ektypwthei
		char char_from_int[2];
		sprintf(char_from_int,"| %d       %d |",random_num,random_num);
		strcpy(card.design[1],char_from_int);
	}
	// H ypoloiph karta tha einai idia se kathe periptwsh
    strcpy(card.design[0]," ___________ ");
	strcpy(card.design[2],"|           |");
	strcpy(card.design[3],"|           |");
    strcpy(card.design[4],"|           |");
    strcpy(card.design[5],"|           |");
    strcpy(card.design[6],"|           |");
    strcpy(card.design[7],"|           |");
    strcpy(card.design[8],"|           |");
    strcpy(card.design[9],"|___________|");
    return card;
}

void lower_aces(struct cards hand[],int *card_count,int *hand_value)
{
	int i;
	for (i=0;i<*card_count;i+=1) // Gia kathe karta
	{
		if (hand[i].value==11) // An h karta einai assos katevenei 
		{
			*hand_value-=10;
			hand[i].value=1;
		}
	}
}
	
void draw_card(struct cards hand[],int *card_count,int *hand_value) // Travaei tyxaia karta
{
	srand(time(0)); // Tyxaio seed
	int random_num=(rand() % 13)+1; // O arithmos ths kartas pou tha travhxtei, pou to 13 einai o arithmos twn diaforetikwn kartwn sthn trapoula (1...10,K,Q,J)
	hand[*card_count]=fill_card_details(hand[*card_count],random_num,hand_value); // Gemizei thn karta kai thn vazei ston pinaka me tis ypoloipes
	*hand_value+=hand[*card_count].value;
	if (*hand_value>21) // Elegxei kathe fora an prepei na katevei kapoios assos apo aksia 11 se 1, epeidh o paikths kahke
		lower_aces(hand,card_count,hand_value); 
	*card_count+=1;
}
		
void print_hand(struct cards hand[],int card_count)
{
	int i;
	int j;
	for (i=0;i<10;i+=1) // Gia kathe epipedo tou design ths kartas
	{
		for (j=0;j<card_count;j+=1) // Gia kathe karta sto xeri tou paikth
			printf(" %s ",hand[j].design[i]);
		printf("\n");
	}
}

int main()
{
	int player_wins=0;
	int player_draws=0;
	int player_losses=0;
	int player_balance=100;
	int dealer_balance=100;
	int end_game=0;
	while (end_game==0) // Oso einai mhden paizetai kainourgia partida
	{
		// Krataei tis kartes ton paiktwn gia authn thn partida (10 tyxaios megalos arithmos)
		struct cards dealer_hand[10];
		struct cards player_hand[10];
		
		// Synolo kartwn pou exei traviksei kathe paikths
		int dealer_card_count=0;
		int player_card_count=0;
		
		// Aksia ton kartwn kathe paikth
		int dealer_hand_value=0;
		int player_hand_value=0;
		
		char answer[5];
		int bet=0;
		int dealer_turn=0; // Ama ginei 1 ksekinaei h seira tou dealer
		int end_hand=0;
		while (player_hand_value<21 & end_hand==0) // O paikths travaei ki allh karta an h aksia tous einai mikroterh tou 21 kai den exei epileksei na stamatisei
		{	
			// O dealer travaei karta mono thn prwth fora
			if (dealer_card_count==0)
				draw_card(dealer_hand,&dealer_card_count,&dealer_hand_value);
				Sleep(1000); // Prepei na perimenei ligo gia na mh vgoun oi idies kartes kai gia tous dyo paiktes
			
			draw_card(player_hand,&player_card_count,&player_hand_value);
			
			printf("\n\n");
			print_hand(dealer_hand,dealer_card_count);
			printf("\n Dealer's hand: %d",dealer_hand_value);
			
			printf("\n\n");	
			print_hand(player_hand,player_card_count);
			printf("\n Player's hand: %d",player_hand_value);
			
			// Zhtaei apo ton paikth to pontarisma, mono thn prwth fora
			if (bet==0)
			{
				do
				{
					printf("\n\n Posa tha pontareis [Player's Balance:%d] [Dealer's Balance:%d] : ",player_balance,dealer_balance);
					scanf("%d",&bet);
					if (bet<=0)
						printf("\n Pontarisma mikrotero h iso tou mhden...");
					else if (bet>player_balance)
						printf("\n Pontarisma megalytero apo to balance sou...");
					else if (bet>dealer_balance)
						printf("\n Pontarisma megalytero apo to balance tou dealer...");
				}
				while (bet<=0 | bet>player_balance | bet>dealer_balance);
			}
			
			// Rotaei ton paikth an thelei na synexisei, ean oi kartes tou einai mikroteres tou 21
			if (player_hand_value<21)
			{
				do
				{
					printf("\n\n (Hit) gia na travhkseis (Stand) gia na stamathseis: ");
					scanf("%s",answer);
				}
				while (strcmp(answer,"Hit")!=0 & strcmp(answer,"Stand")!=0);
				
				if (strcmp(answer,"Stand")==0)
					end_hand=1;
			}
			// Ean oi kartes tou einai megalyteres apo to 21, h partida teleionei
			else if (player_hand_value>21)
			{
				printf("\n\n Player Busted");
				end_hand=1;
				player_losses+=1;
				dealer_turn=1;
				player_balance-=bet;
				dealer_balance+=bet;
			}
			else
			{
				printf("\n\n Player Blackjack!");
				end_hand=1;
			}
			Sleep(1000);
		}
		
		// Seira na traviksei kartes o dealer, efoson den exei kaei o paikths
		if (dealer_turn==0)
		{
			while (dealer_hand_value<17) // Stamataei na travaei kartes otan exei kartes megalyteres tou 17
			{	
				Sleep(1000);
				draw_card(dealer_hand,&dealer_card_count,&dealer_hand_value);
			}
			if (dealer_hand_value==21)
				printf("\n\n Dealer Blackjack!");
			printf("\n\n");
			
			// Emfanizei ta telika apotelesmata, afou o dealer traviksei oles tis kartes tou
			print_hand(dealer_hand,dealer_card_count);
			printf("\n Dealer's hand: %d",dealer_hand_value);
				
			printf("\n\n");	
			print_hand(player_hand,player_card_count);
			printf("\n Player's hand: %d",player_hand_value);
				
			// Emfanizei poios kerdise, symfona me tis aksies twn kartwn kathe paikth
			if (dealer_hand_value<=21)
			{
				if (dealer_hand_value>player_hand_value)
				{
					printf("\n\n Dealer wins!");
					player_losses+=1;
					player_balance-=bet;
					dealer_balance+=bet;
				}
				else if (player_hand_value>dealer_hand_value)
				{
					printf("\n\n Player wins!");
					player_wins+=1;
					player_balance+=bet;
					dealer_balance-=bet;
				}
				else // Ama h aksia twn kartwn einai idia einai isopalia, ektos an exoun kanei kai oi dyo blackjack, tote kerdizei autos pou exei tis ligoteres kartes
				{
					if (dealer_hand_value!=21 & player_hand_value!=21)
					{
						printf("\n\n Push...");
						player_draws+=1;
					}
					else
					{
						if (player_card_count>dealer_card_count)
						{
							printf("\n\n Dealer wins!");
							player_losses+=1;
							player_balance-=bet;
							dealer_balance+=bet;
						}
						else if (dealer_card_count>player_card_count)
						{
							printf("\n\n Player wins!");
							player_wins+=1;
							player_balance+=bet;
							dealer_balance-=bet;
						}
						else
						{
							printf("\n\n Push...");
							player_draws+=1;
						}
					}
				}
			}
			else
			{
				printf("\n\n Dealer Busted");
				player_wins+=1;
				player_balance+=bet;
				dealer_balance-=bet;
			}
		}
		
		// Emfanish statistikwn
		printf("\n\n Player's wins: %d Player's draws: %d Player's losses: %d",player_wins,player_draws,player_losses);
		printf("\n Player's balance: %d Dealer's balance: %d",player_balance,dealer_balance);
		
		// Emfanizei katallhlo mynhma kai teleionei to paixnidi, an teleiosei to balance kapoiou paikth
		if (player_balance==0)
		{
			printf("\n\n Teleiose to balance tou paikth...");
			end_game=1;
		}
		else if (dealer_balance==0)
		{
			printf("\n\n Teleiose to balance tou dealer...");
			end_game=1;
		}
		
		// An den exei teleiosei to balance kapoiou paikth, rotaei an thelei na paixtei kainourgia partida
		if (end_game!=1)
		{
			do
			{
				printf("\n\n (0) gia na paikseis ksana (1) gia na teleiosei to paixnidi: ");
				scanf("%d",&end_game);
			}
			while (end_game!=0 & end_game!=1);
		}
	}	
	int pause;
	printf("\n\n Type anything to exit the program... ");
	scanf("%d",pause);
	return 0;
}
