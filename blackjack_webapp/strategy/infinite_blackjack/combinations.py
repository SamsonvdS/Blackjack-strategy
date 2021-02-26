

import math

# minimum and maximum number of cards
MIN_CARDS = 2
MAX_CARDS = 13


class DealerCombinations:
    """
    stores all combinations of dealer and player hands and the probabilities of 
    achieving each hand
    """

    def __init__(self):
        """ initializes variables """
        # values of each card
        self.card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        # all dealer combinations with their respective outcomes
        self.all_combinations = self.find_all_combination_outcomes()

        # probabilities for bust it side bet
        self.bust_it_prob = {}

        # probabilities for playing blackjack
        self.open_card_prob = {}
        self.blackjack_ev_prob = {}

        

    def find_all_combination_outcomes(self):
        """find hand combinations for each bust type and non-busts"""
        # all (non-)busting hand combinations of dealer
        all_outcomes = {}
        all_outcomes['not_busted_17'] = []
        all_outcomes['not_busted_18'] = []
        all_outcomes['not_busted_19'] = []
        all_outcomes['not_busted_20'] = []
        all_outcomes['not_busted_21'] = []
        all_outcomes['busted_3'] = []
        all_outcomes['busted_4'] = []
        all_outcomes['busted_5'] = []
        all_outcomes['busted_6'] = []
        all_outcomes['busted_7'] = []
        all_outcomes['busted_8'] = []

        # get all dealer's possible hand combinations
        self.find_all_combinations(all_outcomes, [])

        return all_outcomes


    def find_all_combinations(self, all_outcomes, hand1):
        """
        this finds all possible hand combinations of the dealer
        and adds them to the correct list, if the dealer busts or not
        """
        for card in self.card_values:
            hand = hand1.copy()
            hand.append(card)
            
            # correct for soft values
            if 11 in hand and sum(hand) > 21:
                while sum(hand) > 21 and 11 in hand:
                    hand[hand.index(11)] = 1
            
            hand_sum = sum(hand)
            
            # append hand to correct list, else take extra card
            if hand_sum > 21:
                # convert all to string
                hand = [str(i) for i in hand]
                
                # change all A values to 'A'
                while '1' in hand:
                    hand[hand.index('1')] = 'A'
                while '11' in hand:
                    hand[hand.index('11')] = 'A'
                
                hand_length = len(hand)
                
                if hand_length < 8:
                    all_outcomes[f'busted_{hand_length}'].append(hand)
                else:
                    all_outcomes['busted_8'].append(hand)
                    
            elif 17 <= hand_sum <= 21:
                # convert all to string
                hand = [str(i) for i in hand]
                
                # change all A values to 'A'
                while '1' in hand:
                    hand[hand.index('1')] = 'A'
                while '11' in hand:
                    hand[hand.index('11')] = 'A'
                
                # append combination to correct outcome
                all_outcomes[f'not_busted_{hand_sum}'].append(hand)

            elif hand_sum < 17:
                self.find_all_combinations(all_outcomes, hand)




    def calculate_comb_prob(self, Deckdf):
        """ calculates probabilities of all possible combinations of dealer hand outcome """
        # copy simple probdf so that it doesn't interfere with other calculations
        probdf_simple = Deckdf.probdf_simple.copy()


        # save probabilities of dealer (not) busting with a specific open card
        open_card_prob = {}
        for card in probdf_simple.index:
            open_card_prob[card] = {}
            
            # for each open card add outcomes (prob busted and prob not busted 17 - 21)
            open_card_prob[card]['prob_busted'] = 0
            open_card_prob[card]['prob_not_busted_17'] = 0
            open_card_prob[card]['prob_not_busted_18'] = 0
            open_card_prob[card]['prob_not_busted_19'] = 0
            open_card_prob[card]['prob_not_busted_20'] = 0
            open_card_prob[card]['prob_not_busted_21'] = 0
            open_card_prob[card]['prob_not_busted_BJ'] = 0  # keep this because dealer doesn't check for BJ if open card is 10
            

        # save probabilities of all possible outcomes
        prob_combos = {}
        prob_combos['prob_not_busted_17'] = 0
        prob_combos['prob_not_busted_18'] = 0
        prob_combos['prob_not_busted_19'] = 0
        prob_combos['prob_not_busted_20'] = 0
        prob_combos['prob_not_busted_21'] = 0
        prob_combos['prob_not_busted_BJ'] = 0
        prob_combos['prob_busted_3'] = 0
        prob_combos['prob_busted_4'] = 0
        prob_combos['prob_busted_5'] = 0
        prob_combos['prob_busted_6'] = 0
        prob_combos['prob_busted_7'] = 0
        prob_combos['prob_busted_8'] = 0


        # get all combinations
        all_outcomes = self.all_combinations

        # total number of cards in deck
        n_cards_in_deck = sum(probdf_simple.loc[:, 'Total_cards'])

        # precalculate deck permutations
        deck_perm = {len_hand: math.perm(n_cards_in_deck, len_hand) for len_hand in range(MIN_CARDS, MAX_CARDS + 1)}

        # total number of cards of each card
        n_each_card = probdf_simple.loc[:, 'Total_cards'].to_dict()

        # all possible permutations for each card
        all_card_perm = {}

        for card in n_each_card:
            all_card_perm[card] = {n_card: math.perm(n_each_card[card], n_card) for n_card in range(MAX_CARDS)}

        # total probability of dealer getting specific outcome
        for outcome in prob_combos:
            # prob_combos does not have BJ combinations seperate
            if 'BJ' in outcome:
                continue
                
            for combi in all_outcomes[f'{outcome[5:]}']:
                # probability of this specific combinations
                prob = self.probability(combi, deck_perm, all_card_perm)
                
                # keep blackjack probabilities seperate, because dealer checks for BJ if open card is A and not if it is 10
                if combi == ['A', '10']:
                    prob_combos['prob_not_busted_BJ'] += prob
                    continue
                elif combi == ['10', 'A']:
                    prob_combos['prob_not_busted_BJ'] += prob
                    open_card_prob[combi[0]]['prob_not_busted_BJ'] += prob
                    continue
                
                # add probabilities to the outcomes
                prob_combos[outcome] += prob
                
                # add probabilities to each possible dealer open card
                if 'not' in outcome:
                    open_card_prob[combi[0]][outcome] += prob
                else:
                    open_card_prob[combi[0]]['prob_busted'] += prob

        # save open card probabilities
        self.open_card_prob = open_card_prob

        # rescale probabilities to 100%
        self.rescale_probabilities()

        # calculate probabilities for blackjack ev and bust it side bet
        self.create_probability_dicts(prob_combos)



    """ helper functions """

    def create_probability_dicts(self, prob_combos):
        """
        creates dictionaries with probabilities needed for bust it side bet and 
        to calculate the expected value of playing blackjack
        """
        # probabilities needed to calculate blackjack ev
        self.blackjack_ev_prob = {}
        self.blackjack_ev_prob['prob_busted'] = 0

        # for either blackjack the game or the bust it side bet
        self.bust_it_prob = {}
        self.bust_it_prob['prob_not_busted'] = 0

        # split prob_combos
        for outcome in prob_combos:
            if "not_busted" in outcome:
                self.blackjack_ev_prob[outcome] = prob_combos[outcome]
                self.bust_it_prob['prob_not_busted'] += prob_combos[outcome]
            else:
                self.blackjack_ev_prob['prob_busted'] += prob_combos[outcome]
                self.bust_it_prob[outcome] = prob_combos[outcome]

        # correct bust it probabilities, because blackjack pushes the bust it side bet
        for prob in self.bust_it_prob:
            self.bust_it_prob[prob] -= self.bust_it_prob[prob] * prob_combos['prob_not_busted_BJ']


    def rescale_probabilities(self):
        """ rescales probabilities for every possible open card for the dealer """
        # rescale probabilities to scale of 1 (100%)
        for card in self.open_card_prob:
            card = self.open_card_prob[card]
            
            # total prob in card needed for rescaling
            total_prob = 0
            
            # calculate total_prob
            for prob in card:
                total_prob += card[prob]
            
            # rescale as long as total_prob > 0
            if total_prob:
                for prob in card:
                    card[prob] /= total_prob
        

    def probability(self, combi, deck_perm, all_card_perm):
        """
        takes a combination of cards and calculates number of permutations
        returns probability of this specific combination of cards
        """
        # find unique cards in hand combination
        unique = set(combi)
        
        total_permutations = 0
        
        for card in unique:       
            # number of permutations to get this card as many times as it occurs in combi
            n_permutations = all_card_perm[card][combi.count(card)] # math.perm(n_each_card[card], combi.count(card))
            
            if total_permutations:
                total_permutations *= n_permutations
            else:
                total_permutations += n_permutations
            
        return total_permutations /  deck_perm[len(combi)]










if __name__ == "__main__":
    import time
    from deck_df import Deckdf

    deckdf = Deckdf(8)

    start = time.time()
    dc = DealerCombinations()
    print(time.time() - start)

    start = time.time()
    dc.calculate_comb_prob(deckdf)
    print(time.time() - start)

    print(dc.bust_it_prob)
    print(dc.open_card_prob)
    print(dc.blackjack_ev_prob)
    
    print("-------------")

    # profile the code
    import cProfile, pstats
    cProfile.run("dc.calculate_comb_prob(deckdf)", "{}.profile".format(__file__))
    s = pstats.Stats("{}.profile".format(__file__))
    s.strip_dirs()
    # only show the most time consuming things
    s.sort_stats("time").print_stats(15)