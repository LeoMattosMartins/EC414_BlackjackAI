# EC414_PokerAI

AI Poker player model using Q learning algorithm, Fall 2024

The object of the game is to collect a hand of cards whose point total is as close to 21 as possible WITHOUT going over. If your point total is over 21, then the dealer automatically wins. A hand of cards is scored as follows:

Each card is worth a certain number of points. For a card specified by a (value, suit) tuple, the number of points it is worth is completely determined by the value term in the tuple (suit is irrelevant).

If value is a number "2" through "10", then the card is worth that number of points.
If value is "Jack", "Queen" or "King", then the card is worth 10 points.
If value is "Ace", then the card is worth EITHER 1 point or 11 points - the player may choose.
The total score of a hand is the total number of points for all cards in the hand, counting each Ace in whichever manner (either 11 or 1) the player chooses.

At the start of the game, you are dealt two cards, and the dealer is dealt 1 card that is visible to you. You may take one of two actions: a "HIT" or a "STAY". If you take the "HIT" action, you will be given another card. Getting another card will increase your score, but might also make your score go over 21. If you take the "STAY" action, this indicates that you are satisfied with your current point total (i.e. you suspect that taking another card might make your score go over 21, or that the dealer will not able to beat your score without going over 21 themselves). Not that you may adjust your decision to count an Ace as 1 point or 11 points at any time. So, for example, if you hand consists of a 9 of clubs and an Ace of spades, you might count the Ace as 11 points for a total of 20 points. However, if you then take the "HIT" action (which is very inadvisable in this case!), you might be dealt an 8 of hearts, in which case your total would be either 28 (counting the Ace as 11) or 18 (counting the Ace as 1). So, you could now count the Ace as 1 point and choose the "STAY" action, to indicate that you are no longer interested in taking another car.

If you take the "HIT" action, then you are dealt a card and again have the option to either take a "HIT" or "STAY" action. You may continue taking the "HIT" action and getting cards until your total is over 21 no matter how you choose to count the Aces. If this happens, then your hand is called "bust" and you automatically lose. So, you should try to choose the "STAY" action before this occurs.

If you take the "STAY" action, then the dealer will start playing their hand. The dealer is not allowed to strategize: the dealer will continually take the "HIT" action until their hand is worth 17 points or more. Once that happens, the dealer takes the "STAY" action. The dealer must count Aces as 11 points unless counting the Ace this way would cause the dealer's score to go over 21.

## Outcome of the game:

If you go bust, you automatically lose. If you do not go bust, but the dealer does, then you win. If neither of you go bust, then the person with the highest score wins. Otherwise, it is a tie.

Note that the player gets to see the first card that the dealer is dealt, but NOT any of the other cards that the dealer will take when making their decisions.

## Reward Structure

To fit this game into the reinforcement learning framework, we need to decide on what rewards to give the player. We give rewards in the following way:

If the player takes an action that results in a loss (either "STAY" and then losing after the dealer finishes playing, or "HIT" and going bust), then the reward is -1.

If the player takes an action that results in a win (i.e. a "STAY" followed by the dealer either going bust or having a smaller score than the player), then the reward is 1.

If the player takes an action that results in a tie (i.e. a "STAY" followed by the dealer achieving the same score as the player), then the reward is 0.

If the player takes an action that does not result in the game ending (that is, a "HIT" with the possibility of taking another "HIT"), then the reward is 0.

## Action Structure

The set of actions available to the player is always either both "HIT" and "STAY", or nothing at all (which happens after taking the "STAY" action, or going bust), both of which result in entering a terminal state, as the dealer will play out their hand and the player will take no more actions.
