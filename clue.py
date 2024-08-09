import random
class Clue:
    def __init__(self,players,characters,weapons,rooms):
        self.players = players
        self.characters = characters
        self.rooms = rooms
        self.weapons = weapons
        self.scoring_sheets = {player: {} for player in self.players}
        self.player_locations = {player: {} for player in self.players}
        self.solution = {}
    def make_solution(self):
        #write your implementation below
        solution_character = random.choice(self.characters)
        solution_weapon = random.choice(self.weapons)
        solution_room = random.choice(self.rooms)
        self.solution = {"Character" : solution_character, "Weapon": solution_weapon, "Room": solution_room}
        
    def distribute_cards(self):
        #write your implementation below
        #uses list comprehension to make a list of characters, weapons, and rooms that are not in the solution to be distributed
        remaining_characters = [c for c in self.characters if c!=self.solution["Character"]]
        remaining_weapons = [w for w in self.weapons if w!=self.solution["Weapon"]]
        remaining_rooms = [r for r in self.rooms if r!=self.solution["Room"]]
        all_cards = remaining_rooms + remaining_characters + remaining_weapons
        random.shuffle(all_cards)
        player_cards = {player: [] for player in self.players} 
        player_index = 0
        while all_cards:
            card = all_cards.pop()  # Removes and returns the last card
            player_cards[self.players[player_index]].append(card)
            player_index = (player_index + 1) % len(self.players)  # Moves to the next player and loops back if needed
        self.player_cards = player_cards
        return player_cards
    def move_player(self,player):
        #write your implementation below
        #randomly generates the number of spaces to move  
        move_count = random.randint(1, len(self.rooms))
        room_index = move_count - 1
        new_room = self.rooms[room_index]
        self.player_locations[player] = new_room
        return new_room
    def make_suggestion(self,player,character,weapon,room):
        #write your implementation below
        if self.player_locations[player] != room:
            print(f"Can't make suggestion: {player} is not in the {room}.") #Prohibits player from making a suggestion if not in correct room
            return None
        responses = {}
        for other_player in self.players:
            if other_player == player:
                continue  # Skip the player making the suggestion
            player_cards = self.player_cards[other_player]
            
            if character in player_cards:
                responses[other_player] = character
            elif weapon in player_cards:
                responses[other_player] = weapon
            elif room in player_cards:
                responses[other_player] = room
            else:
                responses[other_player] = None

        # Return the suggestion and responses
        return {"suggestion": {"character": character, "weapon": weapon, "room": room}, "responses": responses}

    
    def make_accusation(self,player,character,weapon,room):
    # Check if the player is in the accused room
        if self.player_locations[player] != room:
            print(f"Can't make accusation: {player} is not in the {room}.")
            return False

        # Check if the accusation matches the solution
        if self.solution["Character"] == character and self.solution["Weapon"] == weapon and self.solution["Room"] == room:
            return True
        else:
            # The accusation is incorrect, eliminate the player from the game
            print(f"{player} made a wrong accusation and is eliminated from the game.")
            self.players.remove(player)  # Remove the player from the game
            return False

    def update_scoring_sheet(self,player,suggestion,response):
            # Iterate through the responses
        for responder, card_shown in response.items(): #used ChatGPT
            if card_shown:
                # Update the scoring sheet - the card is not part of the solution
                self.scoring_sheets[player][card_shown] = False

            # make all other suggested cards as unknown (or True) since they weren't shown
            for key in suggestion:
                if suggestion[key] != card_shown:
                    self.scoring_sheets[player][suggestion[key]] = True


