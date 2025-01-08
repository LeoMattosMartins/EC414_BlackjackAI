# EC414_BlackjackAI

AI Blackjack player model using Q learning algorithm, Fall 2024

## Overview

This project implements an AI Poker player using the Q-learning algorithm. The goal of the AI is to learn to play Poker by maximizing its cumulative reward through the process of trial and error.

## How It Works

### Game Rules

The object of the game is to collect a hand of cards whose point total is as close to 21 as possible without going over. If your point total is over 21, then the dealer automatically wins.

 - Each card is worth a certain number of points:
    - "2" through "10": Worth that number of points.
    - "Jack", "Queen", "King": Worth 10 points.
    - "Ace": Worth either 1 point or 11 points, chosen by the player.
 - At the start of the game, the player is dealt two cards, and the dealer is dealt one visible card.
 - The player can either "HIT" (take another card) or "STAY" (end their turn).
 - The dealer continues to "HIT" until their hand is worth 17 or more points.
 - 
### Outcome of the Game

 - If the player goes bust (total over 21), they lose.
 - If the dealer goes bust, the player wins.
 - If neither goes bust, the highest score wins.
 - If scores are tied, the game is a draw.

### Reward Structure

To fit the game into the reinforcement learning framework, rewards are assigned as follows:

 - Losing the game: -1
 - Winning the game: +1
 - Tying the game: 0
 - Continuing the game without ending: 0

### Action Structure

The set of actions available to the player is either "HIT" or "STAY," or nothing if the game has ended.

## Q-Learning Implementation

The AI uses the Q-learning algorithm, a model-free reinforcement learning technique, to learn the optimal strategy for playing Poker.

### Steps of Q-Learning

 - Initialize Q-Table: The Q-table is initialized with all zeros. It maps state-action pairs to rewards.
 - Choose Action: The AI chooses an action based on the current state using an ε-greedy policy (a balance between exploration and exploitation).
 - Perform Action: The chosen action is performed, and the next state and reward are observed.
 - Update Q-Table: The Q-value for the state-action pair is updated using the Q-learning update rule.
 - Repeat: Steps 2-4 are repeated for multiple episodes to allow the AI to learn the optimal strategy.

### Q-Learning Update Rule

1. Take action $a_t=\text{argmax}_{a} Q(s_t,a)$.
2. See reward $r_t=r(s,a)$, transition to state $s_{t+1}$.
3. Update the value of $Q(s_t,a_t)$ via the formula:
   
$$
Q(s_t, a_t)\leftarrow Q(s_t, a_t) + \eta \cdot (\max_a Q(s_{t+1}, a) + r_t - Q(s_t, a_t))
$$

where $\eta$ is some provided learning rate.

## Conclusion

This AI Poker player uses the Q-learning algorithm to learn and improve its strategy over time. By continuously updating its Q-values based on the rewards it receives, the AI aims to maximize its cumulative reward and become an effective Poker player.
