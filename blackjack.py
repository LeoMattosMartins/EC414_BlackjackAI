# Two helpful functions for running a blackjack game.

def draw_card():
  '''
  returns a randomly selected (value, suit) tuple representing a random card.
  Assumes cards are drawn from infinitely many decks shuffled together (so
  your agent cannot gain an advantage by counting cards in this game).
  '''
  value = random.choice(['Ace'] + [str(i) for i in range(2,11)] + ['Jack', 'Queen', 'King'])
  suit = random.choice(['Clubs', 'Hearts', 'Spades', 'Diamonds'])

  return (value, suit)

def hand_to_str(hand):
  '''
  Returns a string containing a human-readable description of a blackjack hand.
  Note this function returns a string, it does not call `print`.
  '''
  def card_to_str(c):
    value, suit = c
    return value + ' of ' + suit
  return ', '.join([card_to_str(c) for c in hand])

def score_hand(hand):
  '''
  returns the best possible score for a given hand.

  You can read the full scoring rules below, and also at this link https://bicyclecards.com/how-to-play/blackjack/ under "Card Values/scoring".

  The rules for scoring are:
  Each card is worth a certain number of points. For a card specified by a (value, suit) tuple,
  the number of points it is worth is completely determined by the  "value" term in the tuple (suit is irrelevant).
  If the value term is a number 2 through 10, then the card is worth that number of  points.
  If the value is "Jack", "Queen" or "King", then the card is worth 10 points.
  If the value is "Ace", then the card is worth EITHER 1 point or 11 points - the player may choose.

  The total score of a hand is the total number of points for all cards in the hand, counting each Ace in whatever manner
  the player chooses.
  The objective of the game is to  have as high as score as possible WITHOUT going over 21. So a score of 21 is a "perfect" score,
  a score of 20 is a very good score, and a score of 22 is very bad score (if you go over 21 you automatically lose).

  arguments:
    hand: a list of (value, suit) pairs specifying the hand of the player.
        both "value" and "suit" are represented by strings.
  return two values:
    (score, eleven_valued_aces)

    score: a non-negative integer representing either:
      1. The highest score possible with this hand that is less than or equal to 21. Multiple scores  might be  possible  if the  hand
        contains one or more  Aces. You  must find the  largest score that is less than or equal to 21 if such a thing exists.
      2. If it is impossible for this hand to score less than or equal to 21 (the hand is called "bust" in this case),
        then return the lowest possible score for the hand (which must necessarily be >21).

    eleven_valued_aces: the number of aces in the hand that were scored at 11 points rather than 1 point
      in order to achieve the score provided in the first return value (these are also called "soft" aces).
    '''

  score = 0
  aces = 0
  for card in hand:
    value, suit = card
    if value == 'Ace':
      aces += 1
      score += 11

    elif value in ['Jack', 'Queen', 'King']:
      score += 10

    else:
      score += int(value)

  while score > 21 and aces > 0:
    score -= 10
    aces -= 1

  return (score, aces)

test_cases = {
  (('Ace', 'Clubs'),): (11, 1),
  (('Ace', 'Hearts'), ('Ace', 'Spades'),): (12, 1),
  (('8', 'Clubs'), ('King', 'Diamonds'), ('9', 'Spades'),): (27, 0),
  (('Ace', 'Hearts'), ('7', 'Diamonds'), ('Ace', 'Clubs'), ('King', 'Diamonds'),): (19, 0),
  (('10', 'Spades'),): (10, 0),
  (('King', 'Spades'), ('Ace', 'Clubs'),): (21, 1),
  (('Ace', 'Hearts'), ('7', 'Diamonds'), ('10', 'Diamonds'),): (18, 0),
  (('10', 'Clubs'), ('4', 'Hearts'), ('Ace', 'Spades'), ('8', 'Spades'),): (23, 0),
  (('4', 'Clubs'), ('7', 'Hearts'), ('Ace', 'Spades'), ('2', 'Clubs'), ('King', 'Diamonds'),): (24, 0),
  (('2', 'Hearts'), ('5', 'Hearts'), ('2', 'Hearts'), ('3', 'Hearts'), ('3', 'Diamonds'), ('King', 'Spades'),): (25, 0),
  (('10', 'Clubs'),): (10, 0),
  (('King', 'Hearts'), ('Ace', 'Spades'),): (21, 1),
  (('4', 'Spades'), ('5', 'Diamonds'), ('3', 'Hearts'),): (12, 0),
  (('4', 'Diamonds'), ('8', 'Hearts'), ('4', 'Spades'), ('6', 'Diamonds'),): (22, 0),
  (('Jack', 'Spades'),): (10, 0),
  (('10', 'Diamonds'), ('7', 'Clubs'),): (17, 0),
  (('Jack', 'Hearts'), ('6', 'Clubs'), ('6', 'Spades'),): (22, 0),
  (('2', 'Diamonds'), ('Ace', 'Spades'), ('8', 'Spades'), ('7', 'Spades'),): (18, 0),
  (('King', 'Clubs'),): (10, 0),
  (('Ace', 'Hearts'), ('Jack', 'Diamonds'),): (21, 1),
  (('4', 'Clubs'), ('2', 'Diamonds'), ('4', 'Spades'),): (10, 0),
  (('King', 'Spades'), ('10', 'Hearts'), ('2', 'Clubs'), ('5', 'Spades'),): (27, 0),
  (('Queen', 'Hearts'),): (10, 0),
}

def test_score_hand():
  for hand, true_output in test_cases.items():
    output = score_hand(list(hand))
    assert output == true_output, f"incorrect output on test case: {hand}. Expected output: {true_output}, computed output: {output}"
  print("all tests pass :)")

class BlackjackSimulator:
  '''
  This class simulates a (slightly simplified) version of the card game Blackjack.

  The player's current hand is accessible via the `player_hand` attribute.
  The dealers' current hand is accessible via the `dealer_hand` attribute.

  Both hands are stored as lists of cards, where each card is a tuple (value, suit) as
  returned by `draw_card()`

  The actions currently available to the player are accessible via `available_actions` attribute.
  The last reward earned by the player is accessible via the `reward` attribute.

  Check the docstrings of the individual methods to see what they do.
  In our reference solution, we access the `player_hand` and `dealer_hand` attribute
  in the function `get_state`. We do not use any other internals of BlackjackSimulator objects.
  However, if you find it useful to use some internal methods or attributes, you may do so.

  See the rules of blackjack here: https://bicyclecards.com/how-to-play/blackjack/

  We do not play with "naturals" here as they do not require any decision making.
  This actually makes the odds a little worse than they should be, so your agent
  would actually do slightly better in a casino than it will in this simulator.

  It still wouldn't beat the house though. Gambling is dangerous, and we do not endorse it!

  If you find any other discrepencies in the official rules and the game as implemented
  in this simulator, please write your code to do well on this simulator, not the official rules :)
  '''


  def __init__(self):
    # the player starts with two cards
    self.player_hand = [draw_card(), draw_card()]

    # the dealer starts with one visible card
    self.dealer_hand = [draw_card()]

    self.available_actions = ['HIT', 'STAY']

    # this will hold the reward of the current state of the game. It will always be
    # either -1, (loss), 0 (game in progress, or tie), or 1 (win)
    self.reward = 0


  def is_game_over(self):
    '''
    returns True if the game is over.
    At this point, self.reward will hold the result of the game
    (0 for tie, 1 for player win, -1 for player loss).
    '''
    return len(self.available_actions) == 0

  def player_hand_str(self):
    '''
    returns a string representation of the player hand (it does not actually
    call the `print` method).
    '''
    return hand_to_str(self.player_hand)

  def dealer_hand_str(self):
    '''
    returns a string representation of the dealer hand (it does not actually
    call the `print` method).
    '''
    return hand_to_str(self.dealer_hand)

  def get_reward(self):
    '''
    get reward from last action taken.
    '''
    self.reward = self._get_reward()
    return self.reward

  def _get_reward(self):
    '''
    helper function for self.get_reward: this one has all the actual logic.
    '''
    if len(self.available_actions) != 0:
      # we are still playing - you might yet win!
      return 0

    dealer_score = self.dealer_score()
    player_score = self.player_score()
    if player_score==dealer_score:
      # this is the only way to tie.
      return 0

    # we must have a winner.
    if player_score > 21:
      # dealer wins when player busts (even if the dealer also busts)
      return -1
    if dealer_score > 21:
      # dealer bust, player did not bust.
      return 1
    if player_score > dealer_score:
      return 1
    return -1

  def player_score(self):
    return score_hand(self.player_hand)[0]

  def dealer_score(self):
    return score_hand(self.dealer_hand)[0]

  def take_action(self, action: str):
    '''
    plays one turn of blackjack.

    arguments:
      action: a string value, must be an element of self.available_actions

    returns:
      a reward for this action (integer).
    '''

    assert action in self.available_actions, f"Attempted action: {action}, but the available actions are: {self.available_actions}. The current hand is: {self.player_hand()}"


    if action == 'STAY':
      self.available_actions = []
      # once the player STAYs, the dealer will play out its hand.
      while self.dealer_score() < 17:
        # dealer hits until score is 17 or bigger
        self.dealer_hand.append(draw_card())
    else:
      self.player_hand.append(draw_card())
      if self.player_score() > 21:
        # BUST!
        self.available_actions = []


    return self.get_reward()


def print_status(bs):
  print(f"Current Total: {bs.player_score()}\nCurrent hand: {bs.player_hand_str()}")
  print(f"Dealer Total: {bs.dealer_score()}\nDealer hand: {bs.dealer_hand_str()}")
  if len(bs.available_actions) == 0:
    if bs.get_reward() == 0:
      print(f"It's a tie!")
    elif bs.get_reward() == 1:
      print(f"Player Wins!")
    elif bs.get_reward() == -1:
      print(f"Player loses!")
    return False
  else:
    return True

def play_blackjack():
  bs = BlackjackSimulator()

  def get_action():
    action = None
    options = bs.available_actions
    while action not in options:
      if  action is not None:
        print(f"{action} is not an allowed action. Please select again.")
      print("Available Actions:")
      for option in options:
        print(f"* {option}")
      action = input("Your selection: ").upper()
    return action

  print_status(bs)
  while not bs.is_game_over():
    action = get_action()
    bs.take_action(action)
    print_status(bs)

def get_state(sim: BlackjackSimulator):
  '''
  find the score and number of aces values at 11 points rather than 1 point in both the player and dealer's hands (aka "soft aces").

  arguments:
    sim: a BlackjackSimulator object.

  returns:
     a tuple (player_score, player_eleven_valued_aces, dealer_score, dealer_eleven_valued_aces)
  '''

  player_score, player_eleven_valued_aces = score_hand(sim.player_hand)
  dealer_score, dealer_eleven_valued_aces = score_hand(sim.dealer_hand)

  return (player_score, player_eleven_valued_aces, dealer_score, dealer_eleven_valued_aces)

# Argument checking functions that are useful for making sure your implementation
# of Q-learning is passing the correct values around.

def assert_valid_action(action):
  assert action in ['HIT', 'STAY'], f"invalid action: {action}"

def assert_valid_state(state):
  assert type(state) == tuple, f"state must be a tuple, but was: {state}"

  p_score, p_aces, d_score, d_aces = state
  assert type(p_score) == int and type(p_aces) == int and type(d_score) == int and type(d_aces) == int, f"state has invalid types: {state}"
  assert p_score>=4 and p_aces>=0 and p_score<=31 and d_score>=2 and d_aces>=0 and d_score<=27, f"state has impossible values: {state}"

class Q_Function:
  '''
  class for holding a Q function.
  This class is essentially a manual implementation of a DefaultDict with
  default value zero and a little type checking on top to help catch some bugs
  that might occur when you use it.
  '''
  def __init__(self):
    self.Q = dict()

  def set_value(self, state, action, value):
    '''
    sets the estimated Q(s, a) to be a given value.

    arguments:
      state: the state (a tuple as returned  by get_state)
      action:  a string.
      value: a float.

    returns
      None

    This function updates the Q function so that Q(state, action) = value.
    '''

    assert_valid_state(state)
    assert_valid_action(action)
    assert value <=1.00001 and value >= -1.00001, f"Q learning should never set a Q value of: {value}!"
    if state not in self.Q:
      self.Q[state] = {}
    self.Q[state][action] = value

  def get_value(self, state, action):
    '''
    Return Q(s,a): gets the estimated Q value for a given state, action pair.
    '''
    assert_valid_state(state)
    assert_valid_action(action)
    if not self.seen(state, action):
      return 0.0
    return self.Q[state][action]

  def get_seen_actions_for_state(self, state):
    '''
    for a given state, return a list of all actions that have been "seen"
    in the  sense that the agent has taken this action from this state.
    '''
    assert_valid_state(state)
    if state not in self.Q:
      return []
    return self.Q[state].keys()

  def seen(self, state, action):
    '''
    Return True if the given  state, action pair has been visited by the agent before.
    False otherwise.
    '''
    assert_valid_state(state)
    assert_valid_action(action)
    if state not in self.Q:
      return False
    if action not in self.Q[state]:
      return False
    return True

from pickle import SETITEM

def max_q_for_state(Q, state, actions):
  '''
  finds the best action to take in a given state according to the current estimated Q function.

  arguments:
  Q:  a Q_function object (see  definition above)
  state: a tuple (player_score, player_aces, dealer_score, dealer_aces) as returned by get_state.
  actions: available actions in this state.

  returns:
  (max_value, best_action)

  max_value: the maximum Q function value associated with any action in this state.
  best_action: the  action that gives the maximum Q function value from this state.
  '''

  max_value = -1
  best_action = None
  for action in actions:
    if Q.get_value(state, action) > max_value:
      max_value = Q.get_value(state, action)
      best_action = action
  return (max_value, best_action)

class Q_Learner:
  '''
  A Q-learning class.
  '''

  def __init__(self, eta):
    '''
    eta: the learning rate for Q learning.
    '''
    self.Q = Q_Function()
    self.eta = eta

  def update(self, prev_state, prev_action, sim, reward):
    '''
    Updates the estimated Q function (self.Q) after after taking
    action `prev_action` in state `prev_state` and seeing reward  `reward`.
    `sim` holds the BlackjackSimulator object that can  be used  to determine the
    current state after taking action `prev_action`.

    arguments:
      prev_state: the previous state of the game (a tuple as returned  by get_state)
      prev_action: the action previously taken by the player.
      sim: a BlackjackSimulator object.
      reward: the reward obtained by taking prev_action in prev_state.

    returns:
      None.

    This function has no return value, but should update self.Q using the Q-learning
    update rule.
    '''
    current_state = get_state(sim)
    max_value, best_action = max_q_for_state(self.Q, current_state, sim.available_actions)
    self.Q.set_value(prev_state, prev_action, self.Q.get_value(prev_state, prev_action) + self.eta * (reward + max_value - self.Q.get_value(prev_state, prev_action)))


  def get_action(self, sim):
    '''
    find the action this agent will take given the current game state as
    specified by the BlackjackSimulator object `sim` and the current estimated
    Q function stored in `self.Q`.

    arguments:
      sim: a BlackjackSimulator object containing the current game state.

    returns:
      action: a string representing the action to take next (i.e. either "HIT" or "STAY")
    '''

    state = get_state(sim)
    max_value, action = max_q_for_state(self.Q, state, sim.available_actions)
    return action

def run_Q_learning(iter_count, eta):
  policy = Q_Learner(eta)
  pbar = tqdm(range(iter_count))
  for i in pbar:
    sim = BlackjackSimulator()
    while not sim.is_game_over():
      state = get_state(sim)
      action = policy.get_action(sim)
      reward = sim.take_action(action)
      policy.update(state, action, sim, reward)
  return policy

def run_policy_verbose(learner, verbose_level=1):
  '''
  Run a learned policy on a single game of blackjack.
  Prints out the states and actions taken during the game.
  You may control the amount of information printed by increasing `verbose_level`.

  You will not be graded on any output from this function: feel free to modify
  it when debugging your code.
  '''
  sim = BlackjackSimulator()
  print_status(sim)
  while not sim.is_game_over():
    action = learner.get_action(sim)
    state = get_state(sim)

    print(f"Learner takes action: {action}")

    if verbose_level > 0:
      seen_actions = learner.Q.get_seen_actions_for_state(state)
      print(f"Actions tested in training: {seen_actions}")
      for seen_action in seen_actions:
        print(f"Q value for action {seen_action}: {learner.Q.get_value(state, seen_action)}")

    sim.take_action(action)

    print_status(sim)

  return sim.reward

small_policy = run_Q_learning(100, 0.1)

reward = run_policy_verbose(small_policy, verbose_level=1)

policy = run_Q_learning(200000, 0.00005)

def run_policy(learner):
  sim = BlackjackSimulator()
  while not sim.is_game_over():
    action = learner.get_action(sim)
    state = get_state(sim)
    sim.take_action(action)

  return sim.reward

def test_policy(policy, iterations=10000):
  '''
  tests a policy for `iterations` number of games.
  Returns the average reward obtained by the policy.
  '''
  pbar = tqdm(range(iterations))
  total_reward = 0.0
  for i in pbar:
    total_reward += run_policy(policy)

  return total_reward/iterations

test_policy(policy)
