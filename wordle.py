import random

with open("data/wordle.txt") as file:
    words = [x.rstrip() for x in file.readlines()]


class puzzle(object):
    colors = ["⬜","🟨","🟩"]
    
    def reveal(self) -> None:
        print(f'The word was "{self.word}"')
        self.history.append("Word revealed.")
        self.revealed = True
    
    def is_solved(self) -> bool:
        return self.solved
    
    def n_guesses(self) -> int:
        return self.guesses
       
    def __repr__(self) -> None:
        steps = [ str(i+1)+". " + x for i, x in zip(range(len(self.history)), self.history)]
        header = "Wordle puzzle: "
        if self.solved:
            header += "(Solved)"
        elif self.revealed:
            header += "(Revealed)"
        else:
            header += f"({6-len(steps)} guesses left)"
                
        lines = [header] + steps
        return "\n".join(lines)
    
    def __init__(self, seed = None, quiet = True) -> None:
        random.seed(seed)
        self.word = random.sample(words, 1)[0]
        self.history = []
        self.solved = False
        self.revealed = False
        self.quiet = quiet
        self.guesses = 0

    def guess(self, guess: str) -> str:
        
        if self.solved or self.revealed:
            raise RuntimeError("This puzzle has already been completed.")

        if len(self.history) >= 6:
            raise RuntimeError("All 6 guesses have been exhausted.")
        
        if not isinstance(guess, str):
            raise TypeError("Guesses must be a string.")
        if len(guess) != 5:
            raise ValueError("Guesses must be length 5.")
        if guess != guess.lower():
            raise ValueError("Guesses must by all lowercase.")
        if not guess in words:
            raise ValueError("Guess not in word list.")
        
        self.guesses += 1
                   
        let_occur = [int(c in self.word) for c in guess]           # 1 if guess letter occurs in word, 0 otherwise
        let_match = [int(x==y)*2 for x,y in zip(guess, self.word)] # 2 if guess letter matches word letter, 0 otherwise
        
        for l in set(guess): # for each guess letter
            # Find the indexes of that latter in the guess and word, where they dont match
            guess_i = [i for i in range(len(guess)) if guess[i] == l and let_match[i] == 0]
            word_i  = [i for i in range(len(self.word)) if self.word[i] == l and let_match[i] == 0]
            
            if len(guess_i) > len(word_i): # Letter occurs more in guess than in word
                for i in guess_i[len(word_i):]:
                    let_occur[i] = 0
        
        res = [self.colors[max(x)] for x in zip([0,0,0,0,0], let_occur, let_match)]
        self.history.append(" ".join(res) + " ("+guess+")")
            
        if guess == self.word:
            self.solved = True
            if not self.quiet:
                print("Congradulations, you found the word!")

        return res

class puzzle_test(puzzle):
    def __init__(self, word: str) -> None:
        self.word = word
        self.history = []
        self.solved = False
        self.revealed = False
        self.quiet = True
        self.guesses = 0
    
    def guess(self, guess: str) -> str:
        words.append(guess)
        res = super().guess(guess)
        words.pop()
        
        return res
    
    
    
# Test cases taken from James Lawry's tweet:
# https://twitter.com/jmhl/status/1483965720845512705

assert puzzle_test('abcde').guess('abcde') == ['🟩','🟩','🟩','🟩','🟩']
assert puzzle_test('fghij').guess('abcde') == ['⬜','⬜','⬜','⬜','⬜']
assert puzzle_test('axxxx').guess('abcde') == ['🟩','⬜','⬜','⬜','⬜']
assert puzzle_test('bxxxx').guess('abcde') == ['⬜','🟨','⬜','⬜','⬜']
assert puzzle_test('bbxxx').guess('abcde') == ['⬜','🟩','⬜','⬜','⬜']
assert puzzle_test('edcba').guess('abcde') == ['🟨','🟨','🟩','🟨','🟨']
assert puzzle_test('rebus').guess('reels') == ['🟩','🟩','⬜','⬜','🟩'] # repeated letters in guess, not in secret.
assert puzzle_test('reels').guess('rebus') == ['🟩','🟩','⬜','⬜','🟩'] # repeated letters in secret, not in guess.
assert puzzle_test('redes').guess('reeds') == ['🟩','🟩','🟨','🟨','🟩'] # Is this correct? I think so.
assert puzzle_test('rebus').guess('asset') == ['⬜','🟨','⬜','🟨','⬜'] # Left-most of repeated letters in quess gets the yellow.
assert puzzle_test('boost').guess('igloo') == ['⬜','⬜','⬜','🟨','🟨'] # repeated letter in secret, no overlap.
assert puzzle_test('boost').guess('shoot') == ['🟨','⬜','🟩','🟨','🟩'] # repeated letter in secret, overlap.
assert puzzle_test('boost').guess('ovolo') == ['🟨','⬜','🟩','⬜','⬜'] # repeated letter in secret, three in guess.
                



















