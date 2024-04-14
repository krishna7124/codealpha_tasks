# Hangman Word Guessing Game

import random


def get_word(category):
    # Define word lists for different categories
    category_word_lists = {
        '1': ["Basketball", "Soccer", "Tennis", "Baseball", "Swimming", "Golf", "Volleyball", "Wrestling", "Cycling", "Running", "Boxing", "Hockey", "Badminton", "Table-Tennis", "Gymnastics", "Skiing", "Archery", "Diving", "Sailing", "Rowing", "Fencing", "Cricket", "Rugby", "Track", "Softball", "Karate", "Taekwondo", "Weightlifting", "Skateboarding", "Equestrian"],

        '2': ["Toyota", "Honda", "Ford", "Chevrolet", "BMW", "Mercedes", "Audi", "Volkswagen", "Nissan", "Hyundai", "Subaru", "Porsche", "Jeep", "Tesla", "Lexus", "Ferrari", "Jaguar", "Maserati", "Lamborghini", "McLaren", "Bugatti", "Rolls-Royce", "Bentley", "Mini", "GMC", "Dodge", "Chrysler", "Buick"],

        '3': ["Mountain", "Road", "BMX", "Hybrid", "Cruiser", "Touring", "Folding", "Electric", "Tandem", "Tricycle", "Recumbent", "Cyclocross", "Gravel", "City", "Dirt", "Racing", "Kids", "Vintage", "Suspension", "10-Speed", "Chainless", "Commuter", "Track", "Titanium"],

        '4': ["Pizza", "Burger", "Sushi", "Pasta", "Tacos", "IceCream", "Chocolate", "Pancakes", "Sandwich", "Curry", "Salad", "Soup", "Steak", "Shrimp", "Donut", "Waffle", "Cucumber", "Pineapple", "Blueberry", "Kiwi"],

        '5': ["USA", "Canada", "France", "Germany", "UK", "Japan", "Australia", "Brazil", "India", "China", "Russia", "Italy", "Spain", "Mexico", "Korea", "Africa", "Argentina", "Egypt", "Greece", "Sweden", "Turkey", "Thailand", "Switzerland", "Singapore", "Nigeria", "Pakistan", "Indonesia", "Malaysia", "Vietnam"],

        '6': ["Smartphone", "Laptop", "Internet", "AI", "Blockchain", "Robotics", "Cybersecurity", "Cloud-Computing", "Biotechnology", "Nanotechnology", "IoT", "DarkWeb", "Space", "Biometrics", "Drones", "Wearables", "Robots", "Automation", "Chatbots", "Data", "Website", "Internet"]
    }

    # Get a random word from the specified category
    category_word_list = category_word_lists.get(category, [])
    return random.choice(category_word_list).upper()


def display_hangman(tries):
    # Define stages of the hangman
    stages = [
        """
        +---+
            |
            |
            |
            |
            |
        =========
        """,
        """
        +---+
        O   |
            |
            |
            |
            |
        =========
        """,
        """
        +---+
        O   |
        |   |
            |
            |
            |
        =========
        """,
        """
        +---+
        O   |
       /|   |
            |
            |
            |
        =========
        """,
        """
        +---+
        O   |
       /|\\  |
            |
            |
            |
        =========
        """,
        """
        +---+
        O   |
       /|\\  |
       /    |
            |
            |
        =========
        """,
        """
        +---+
        O   |
       /|\\  |
       / \\  |
            |
            |
        =========
        """
    ]
    return stages[tries]


def play(word, player_name, category):
    word = word.upper()
    print(word)
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    # Display welcome message and initial hangman
    print(f"Welcome to Hangman, {player_name}!")
    print(f"Category: {category}")
    print(f"Hint: The word has {len(word)} letters.")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")

    # Main game loop
    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").upper()
        guess = guess.replace(" ", "")

        # Handle single letter guess
        if len(guess) == 1:
            if guess in guessed_letters:
                print(f"You already guessed the letter {guess}")
            elif guess not in word:
                print(f"{guess} is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print(f"Good job, {guess} is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = []
                for i, letter in enumerate(word):
                    if letter == guess:
                        indices.append(i)

                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
        # Handle whole word guess
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print(f"You already guessed the word {guess}")
            elif guess != word:
                print(f"{guess} is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Not a valid guess.")

        # Display current hangman and word completion
        print(display_hangman(tries))
        print(word_completion)
        print("\n")

    # Display game outcome
    if guessed:
        print("Congrats, you guessed the word! You win!")
    else:
        print(
            f"Sorry, you ran out of tries. The word was {word}. Maybe next time!")


def main():
    print("Welcome to Hangman!")

    # Get player's name
    player_name = input("Enter your name: ").capitalize()

    while True:
        # Display categories
        print("\nChoose a category:")
        category_map = {
            '1': 'Sports',
            '2': 'Cars',
            '3': 'Bikes',
            '4': 'Food',
            '5': 'Countries',
            '6': 'Technologies'
        }

        for key, value in category_map.items():
            print(f"{key}. {value}")

        # Get category choice from the player
        category_choice = input("Enter the number of the category: ")

        # Start the game with the chosen category
        if category_choice in category_map:
            category = category_map[category_choice]
            word = get_word(category_choice)
            play(word, player_name, category)
        else:
            print("Invalid category choice")

        # Ask if the player wants to play again
        play_again = input("Play again? (yes/no): ").lower()
        if play_again != "yes":
            break

    print(f"Thank you for playing, {player_name}!")


# Start the game
main()
