import random
from django.shortcuts import render, redirect

# Parameters
NUM_ITERATIONS = 5
PARAMETER_A = 2  # You can modify this value as needed

# Sample questions and options
QUESTIONS = [
    ("Choose either Option A or B", ["Option A", "Option B"]),
    ("Choose either Option A or B", ["Option A", "Option B"]),
]

# Initialize global variables
choices_list = []
player1_scores = 0
player2_scores = 0
question_index = random.randint(0, len(QUESTIONS) - 1)


def index(request):
    global choices_list, player1_scores, player2_scores, question_index

    # Reset scores and choices if it's a new game
    if not choices_list:
        player1_scores = 0
        player2_scores = 0
        question_index = random.randint(0, len(QUESTIONS) - 1)

    if request.method == "POST":
        # Retrieve player inputs
        player1_choice = request.POST.get("player1")
        player2_choice = request.POST.get("player2")

        # Append choices to the list
        choices_list.append((player1_choice, player2_choice))

        # Calculate score for this round
        if player1_choice == "A" and player2_choice == "A":
            player1_scores += PARAMETER_A
            player2_scores += 1
        elif player1_choice == "B" and player2_choice == "B":
            player1_scores += 1
            player2_scores += PARAMETER_A
        # If choices are different, no score is added

        # Check if game is over
        if len(choices_list) >= NUM_ITERATIONS:
            # Calculate final scores
            player1_scores, player2_scores = calculate_scores(choices_list, PARAMETER_A)
            file1 = open(f"btp_first/scores_a_{PARAMETER_A}_and_n_{NUM_ITERATIONS}.txt", "a")
            # write the choice list of players 1 and 2 in the file like Player 1: followed by Player 2: in the next line in the file
            file1.write('Player 1: ')
            for choice in choices_list:
                file1.write(f"{choice[0]} ")
            file1.write('\n')
            file1.write('Player 2: ')
            for choice in choices_list:
                file1.write(f"{choice[1]} ")
            file1.write('\n')
            file1.write(f"Player 1: {player1_scores}, Player 2: {player2_scores}\n")
            file1.close()
            return render(request, "btp_first/index.html", {
                "question": QUESTIONS[question_index][0],
                "options": QUESTIONS[question_index][1],
                "choices_list": choices_list,
                "player1_scores": player1_scores,
                "player2_scores": player2_scores,
                "message": "Game Over! Final Scores are shown above.",
                "restart": True,
                "a_value": PARAMETER_A,
            })

    # Render template for ongoing rounds
    return render(request, "btp_first/index.html", {
        "question": QUESTIONS[question_index][0],
        "options": QUESTIONS[question_index][1],
        "choices_list": choices_list,
        "player1_scores": None,
        "player2_scores": None,
        "message": f"Round {len(choices_list)} completed. Keep playing!",
        "restart": False,
        "a_value": PARAMETER_A,
    })


def restart_game(request):
    global choices_list
    choices_list = []  # Reset the choices list for a new game
    return redirect("index")


def calculate_scores(choices_list, parameter_a):
    """
    Calculate the scores for both players based on their choices.

    :param choices_list: List of tuples representing choices of Player 1 and Player 2.
                         Example: [('A', 'A'), ('B', 'B'), ('A', 'B')]
    :param parameter_a: The value of 'a' in the payoff matrix.
    :return: A tuple (player1_score, player2_score)
    """
    player1_score = 0
    player2_score = 0

    for player1_choice, player2_choice in choices_list:
        if player1_choice == "A" and player2_choice == "A":
            player1_score += parameter_a
            player2_score += 1
        elif player1_choice == "B" and player2_choice == "B":
            player1_score += 1
            player2_score += parameter_a
        # No score is added if choices are different

    return player1_score, player2_score