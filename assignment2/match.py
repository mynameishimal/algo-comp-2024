import numpy as np
from typing import List, Tuple
import random


def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    # modified_scores = modified scores

    # First, we will modify the scores such that if the preferences do not match, score = 0
    modified_scores = [row[:] for row in scores]

    for i in range(len(gender_id)):
        for j in range(len(gender_id)):
            if gender_pref[i] != gender_id[j]:  # Check if gender preference doesn't match
                modified_scores[i][j] = 0  # If gender preference doesn't match, score = 0

    # Next, we divide the list of people randomly into proposers and receivers.
    n = len(gender_id)
    all_indices = list(range(n))
    random.shuffle(all_indices)
    num_matches = n // 2

    proposer_indices = all_indices[:num_matches]  # half of indices are proposers
    receiver_indices = all_indices[num_matches:] # half of indices are receivers

    # Get preferences for proposers and receivers in order of the scores from modified_scores
    proposer_prefs = {
        proposer: sorted(receiver_indices, key=lambda receiver: modified_scores[proposer][receiver], reverse=True) for
        proposer in proposer_indices}

    receiver_prefs = {
        receiver: sorted(proposer_indices, key=lambda proposer: modified_scores[proposer][receiver], reverse=True) for
        receiver in receiver_indices}

    # Gale-Shapley Matching Algorithm from PDF
    matches = {}
    proposer_proposals = {proposer: 0 for proposer in proposer_indices}

    # while some man is free and hasn't proposed to every woman
    while True:
        free_proposer = None
        # Iterate through proposer_indices to find the next free proposer
        for proposer in proposer_indices:
            if proposer_proposals[proposer] < len(receiver_indices):
                free_proposer = proposer
                break

        # finds first woman on m's list to whom m has not uyet proposed
        receiver = proposer_prefs[free_proposer][proposer_proposals[free_proposer]]
        proposer_proposals[free_proposer] += 1

        if receiver not in matches:
            matches[receiver] = free_proposer # match m and w if w is free (not in matches yet)
        else:
            current_partner = matches[receiver]
            # replace w's current partner w proposer if proposer is higher up on receiver's list
            if receiver_prefs[receiver].index(free_proposer) < receiver_prefs[receiver].index(current_partner):
                matches[receiver] = free_proposer
                matches[current_partner] = None  # Frees up m;

    # we have been asked to return a list of tuples of matches
    return [(proposer, receiver) for receiver, proposer in matches.items() if proposer is not None]


if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
