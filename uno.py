import random
"""
uno card break down
19 number cards (1 zero and 2 of each number up to 9)
2 reverse cards.
2 skip cards.
2 draw 2 cards.
4 wild draw 4 cards.
4 wild cards.
"""
colours=['Red','Green','Blue','Yellow']

name= input("Please enter your name: ")
print()
class card:
    colour=""
    num=""
    def __init__(self,colour,num):
        self.num=num
        self.colour=colour
    def __eq__(self, other):
        if(self.num==other.num and self.colour==other.colour):
            return True
        return False
    def __str__(self):
        return "Colour: "+self.colour+" num: "+self.num
shuffled_deck=[]
for i in colours:
    shuffled_deck.append(card(i,str(0)))
    for l in range(10):
        shuffled_deck.append(card(i,str(l)))
        shuffled_deck.append(card(i,str(l)))
    for l in range(2):
        shuffled_deck.append(card(i,"skip"))
        shuffled_deck.append(card(i,"reverse"))
        shuffled_deck.append(card(i,"+2"))
for i in range(4):
    shuffled_deck.append(card("power","+4"))
    shuffled_deck.append(card("power","change colour"))
random.shuffle(shuffled_deck)
waste=[]
def play(user, pick, isPlayer,multiplayer,direction):#Method for playing a card and accounting for power cards for computer and player at the card being played is pick
    waste.append(pick)
    effects=[None]*4 
    effects[1]="" 
    effects[2]=False
    effects[3]=direction
    if(isPlayer):                
        print("You played "+pick.__str__())
        if(pick.colour=="power"):
            for i in range(4):
                print(str(i+1)+": "+colours[i])
            while(True):    
                try:  
                    choice=int(input("Please enter the number correlating to the card you would like to play: "))-1
                    if(choice<0):
                        raise IndexError()
                    effects[0]=colours[choice]
                except (ValueError ,IndexError) as e:
                    print("Your previous input was either not a number correlating to the options given or not an integer value.")
                else:
                    break
            if(pick.num=="+4"):
                effects[1]="+4"
        else:
            effects[0]=pick.colour
            if(pick.num=="skip" or pick.num=="reverse" and not multiplayer or pick.num=="reverse" and len(cards)==2):
                effects[2]=True
            elif(pick.num=="reverse" and multiplayer):
                effects[3]= not direction       
            elif(pick.num=="+2"):
                effects[1]="+2"
    else:
        if(pick.colour=="power"):
            most=[0,0,0,0]
            for i in user:
                match i.colour:#computer changes colour to colour it has the most cards in
                    case "Red":
                        most[0]=most[0]+1
                    case "Green":
                        most[1]=most[1]+1
                    case "Blue":
                        most[2]=most[2]+1
                    case "Yellow":
                        most[3]=most[3]+1
                    case _:
                        continue
            effects[0]=colours[most.index(max(most))]
            input("The computer has changed the colour to "+effects[0]+" using "+pick.__str__())
            if(pick.num=="+4"):
                effects[1]="+4"
        else:
            effects[0]=pick.colour
            input("Computer has played a "+pick.__str__())
            if(pick.num=="reverse"or pick.num=="skip"):
                effects[2]=True
            elif(pick.num=="+2"):
                effects[1]="+2"
    return effects

def draw():
    return shuffled_deck.pop()

player=[]
comp=[]
for i in range(14):
    if(i<7):
        player.append(draw())
    else:
        comp.append(draw())
topCard=draw()
while(topCard.colour=="power"or topCard.num=="+2"or topCard.num=="reverse" or topCard.num=="skip" ):
    shuffled_deck.insert(0,topCard)
    topCard=draw()
print("Welcome to the game "+name+". If the game stops moving without asking for a choice press enter to continue and good luck.\n")
current=topCard.colour
skipPlayer=False
skipComp=False
add=""
def spotFinder(spot, cards):
    if(direction):
        spot+=1
        if(spot==len(cards)):
            spot=0
    else:
        spot-=1
        if(spot<0):
            spot=len(cards)-1
    return spot
while(True):
    try:
        players=int(input("Please enter the number of players you would like to have in this game: "))
        if(players<1 or players>4):
            raise ValueError()
    except ValueError :
        print("You did not enter a valid number between 2 and 4")
    else:
        break
multiplayer= players>1
if(multiplayer):
    names=[]
    cards=[]
    cards.append(player)
    cards.append(comp) 
    names.append(name)

    for i in range(2,players+1):
        temp=[]
        names.append(input("Please enter the name of player "+str(i)+": "))
        if(i>2):
            for i in range(7):
                temp.append(draw())
            cards.append(temp)
print()
spot=0   
direction=True
while(len(player)>0 and len(comp)>0 and len(shuffled_deck)>0):
    if(multiplayer):
        for i in range(100):
            print()
        player=cards[spot]
        name=names[spot] 
    if(topCard.colour=="power"):
        print("The colour of playable cards is "+ current)
    input("The top card is "+topCard.__str__()+"\n")
    playable=[]
    if(len(add)==0):
        if not skipPlayer:
            print(name+"'s full deck:")
            for i in player:
                print(i)
            input()
            for i in player:
                if(i.colour==current or i.colour=="power"or i.num==topCard.num):
                    playable.append(i)
            if(len(playable)!=0):
                print("Your playable cards are: ")
                for i in range(len(playable)):
                    print(str(i+1)+": "+playable[i].__str__())
                while(True):    
                    try:    
                        choice=int(input("Please enter the number correlating to the card you would like to play: "))-1
                        if(choice<0):
                            raise IndexError()
                        topCard=playable[choice]
                    except (ValueError, IndexError) as e:
                        print("Your previous input was either not a number correlating to the options given or not an integer value.")
                    else:
                        break
                effects=play(player,topCard,True,multiplayer,direction)
                current=effects[0]
                add=effects[1]
                if(multiplayer):
                    skipPlayer=effects[2]
                    direction=effects[3]
                    spot=spotFinder(spot,cards)
                else:
                    skipComp=effects[2]
                player.remove(topCard)
            else:
                print(name+" has picked up a card because you had no cards you could play that card is: ")
                pick=draw()
                input(pick)
                if(pick.colour==current or pick.num==topCard.num or pick.colour=="power"):
                    choice=input(name+"'s card is playable if you would like to play it please type yes any other entry will be marked as a decision to not play it: ")
                    if(choice.lower()=="yes"):
                        topCard=pick
                        effects=play(player,topCard,True,multiplayer,direction)
                        current=effects[0]
                        add=effects[1]
                        if(multiplayer):
                            skipPlayer=effects[2]
                            direction=effects[3]
                            spot=spotFinder(spot,cards)
                        else:
                            skipComp=effects[2]
                    else:
                        player.append(pick)    
                        if(multiplayer):
                            cards[spot]=player
                            spot=spotFinder(spot,cards)
                else:
                    player.append(pick)    
                    if(multiplayer):
                        cards[spot]=player
                        spot=spotFinder(spot,cards)                     
        else:
            skipPlayer=False
            input(name+"'s turn has been skipped")
            if(multiplayer):
                spot=spotFinder(spot,cards)
    else:
        for i in player:
            if(add[:2]==i.num):
                playable.append(i)     
        if(len(playable)!=0):
            print("\n\nThis is your deck: ")
            for i in player:
                print(i)
            print("Below is a list of all your cards that counter the + card just played: ") 
            for i in range(len(playable)):
                print(str(i+1)+" "+playable[i].__str__())
            while(True):    
                try:    
                    choice=int(input("Please enter the number correlating to the card you would like to play: "))-1
                    if(choice<0):
                        raise IndexError()
                    topCard=playable[choice]
                except (ValueError,IndexError) as e:
                    print("Your previous input was either not a number correlating to the options given or not an integer value.")
                else:
                    break
            effects=play(player,topCard,True,multiplayer,direction)
            current=effects[0]
            add=add+effects[1]
            player.remove(topCard)
            if(multiplayer):
                cards[spot]=player
                spot=spotFinder(spot,cards)
        else:
            sum=0
            for i in range(int(len(add)/2)):
                sum+=int(add[1])
            input(name+" doesn't have a counter card so they are going to pick up "+str(sum)+" cards")
            for i in range(sum):
                player.append(draw())
            print()
            add=""
            for i in player:
                print(i)
            input("Above is your full deck after picking up cards")
            if(multiplayer):
                spot=spotFinder(spot,cards)          
    if(len(player)>1):#Announce player card and end game if the player can't pick up more
        input(name+" has "+str(len(player))+" cards.")
    elif(len(player)==1):
        input(name+" has an uno")
    else:
        break
    print()
    playable=[]
    if(multiplayer):
        continue
    if(len(add)==0):
        if(not skipComp):
            for i in comp:
                if(i.colour==current or i.colour=="power"or i.num==topCard.num):
                    playable.append(i)
            if(len(playable)!=0):
                topCard=random.choice(playable)
                effects=play(comp,topCard,False,multiplayer,direction)
                current=effects[0]
                add=effects[1]
                skipPlayer=effects[2]
                comp.remove(topCard)
            else:
                pick=draw()
                if(pick.colour==current or pick.num==topCard.num or pick.colour=="power"):
                    input("The computer has picked up a card and decide to play it")
                    topCard=pick
                    effects=play(comp,topCard,False,multiplayer,direction)
                    current=effects[0]
                    add=effects[1]
                    skipPlayer=effects[2]
                else:
                    input("The computer has picked up a card and did not play it")
                    comp.append(pick)
        else:
            print("The computer's turn has been skipped")
            skipComp=False    
    else:
        for i in comp:
            if(add[:2]==i.num):
                playable.append(i)
        if(len(playable)>0):
            print("The computer countered your "+playable[0].num+" with their own")
            topCard=random.choice(playable)
            effects=play(comp,topCard,False,multiplayer,direction)
            current=effects[0]
            add=add+effects[1]
            comp.remove(topCard)
        else:
            sum=0
            for i in range(int(len(add)/2)):
                sum+=int(add[1])
            print("The computer has picked up "+str(sum)+" cards.")
            for i in range(sum):
                comp.append(draw())
            add=""
    if(len(comp)>1):
        input("The computer has "+str(len(comp))+" cards.\n")
    elif(len(comp)==1):
        input("The computer has an uno\n")
print("\n\n\n")
if(len(player)==0):
    print("Congrats "+name+" you won the game of uno!")
elif(len(comp)==0):
    print("Sorry it appears the computer has won better luck next time")
else:
    print("We ran out of cards so we're going to just call it a draw")
