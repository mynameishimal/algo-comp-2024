#!usr/bin/env python3
import json
import sys
import os
import numpy as np
from scipy.stats import entropy

INPUT_FILE = 'testdata.json'  # Constant variables are usually in ALL CAPS


class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility

def compute_score(user1, user2, question_weights):
    weighted_diff = sum(w * abs(a - b) for w, a, b in zip(question_weights, user1.responses, user2.responses))
    max_diff = sum(question_weights)

    # Apply a sigmoid function as we discussed in meeting 2 to map the weighted difference to the [0, 1] range
    normalized_score = 1 / (1 + np.exp(-weighted_diff / max_diff))

    return normalized_score


def get_max_ans(users):
    max_answer_choice = max(max(user.responses) for user in users)
    return max_answer_choice

# Utilizes entropy weight method to calculate an "inter-question" based weighting system
def calculate_question_weights(users):
    num_users = len(users)
    num_questions = len(users[0].responses)
    max_answer_choice = get_max_ans(users)

    # Create a 2D array to store answer counts for each question and choice
    answer_counts = np.zeros((num_questions, max_answer_choice + 1), dtype=int)

    for user in users:
        for i, response in enumerate(user.responses):
            answer_counts[i][response] += 1

    # Calculate the entropy for each question
    question_entropies = [entropy(counts / np.sum(counts)) for counts in answer_counts]

    # Normalize entropies to get question weights
    max_entropy = max(question_entropies)
    question_weights = [1 - (entropy / max_entropy) for entropy in question_entropies]

    return question_weights


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    q_weights = calculate_question_weights(users)

    for i in range(len(users) - 1):
        for j in range(i + 1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2, q_weights)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
