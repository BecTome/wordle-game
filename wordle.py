# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By   : Alberto Becerra Tomé
# GitHub user  : BecTome
# Creation Date: 20/05/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" 
Interactive Wordle Game implementation using Python 3. 
The aim of this file is introducing basic python programming.

python pah_to_file/wordle.py
"""
# ---------------------------------------------------------------------------


from colorama import Fore
import numpy as np


def compare_wordle(w1, w2):
    '''
    Compares a given word (w1) with the solution of Wordle (w2). 

    Color code:
    G -- Gris (Gray)      -- Error in position and letter not in the word
    V -- Verde (Green)    -- Existing letter in correct position
    N -- Naranja (Orange) -- Existing letter in wrong position

    Input:
    w1 (str) -- Guess
    w2 (str) -- Solution

    Output:
    ls_out (list) -- List with tuples (letter, color code). Used for debugging purposes
    ls_print (list) -- List with colored letters using `colorama` module
    '''

    n = len(w2) # Must be equal to len(w1). In standard Wordle it would be 5.

    # Loop to checkout the green and gray and count the number of occurrences.
    # In d_count we store the letters and their occurrence in the solution.
    # Each time there's an exact coincidence, we update the number of the resting.
    ls_out = []
    i=0
    d_count = {y:w2.count(y) for y in set(w2)} # grass -> {'g':1, 'r':1, 'a':1, 's':2}
    while i < n:
        x = w1[i]
        y = w2[i]

        if x == y:
            ls_out.append((x, "V"))
            d_count[x] -= 1
        else:
            ls_out.append((x, "G"))

        i+=1
    
    # Once we have the G and the V, we are going to define the N.
    # We take the correct letters which are in the wrong position (letter in the word but not V).
    # If they have positive remaining occurrences, we mark them as orange (N).
    j=0
    while j < n:
        z = ls_out[j]

        if (z[0] in w2) & (z[1] != "V") & (d_count.get(z[0], -10) > 0):
            ls_out[j] = (z[0], "N")
            d_count[z[0]] -= 1
        j+=1
    
    # Fore color + letter = colored letter
    ls_print = [Fore.GREEN + x if y == "V" 
                    else (Fore.LIGHTYELLOW_EX + x if y == "N" 
                            else Fore.RED + x
                          )
                    for x, y in ls_out
                ]
    
    return ls_print, ls_out

if __name__=='__main__':

    from config import DICTPATH, N_TRIES, MAX_WORD_LEN

    # If we want to set a random seed so that we always choose the same solution
    # np.random.seed(0)

    # Get the vocabulary from a file and clean it
    with open(DICTPATH, "r", encoding="utf-8") as f:
        vocab = f.readlines()

    vocab = [word.replace("\n", "").upper() for word in vocab]

    # Select a random word from the dictionary
    word = np.random.choice(vocab)

    # We have N_TRIES chances to guess the word, which cannot be longer than MAX_WORD_LEN
    # With Q we quit the game
    for i in range(N_TRIES):
        guess = input(Fore.LIGHTBLUE_EX\
                        + f"Introduce una palabra (intento {i+1}/{N_TRIES})\n\n"
                    ).upper()
        while True:

            # Check if the word length is the expected one
            if (len(guess) != MAX_WORD_LEN) & (guess != "Q"):
                print(Fore.RED + f"INCORRECTO. INTRODUCE UNA PALABRA DE {MAX_WORD_LEN} LETRAS\n")
                guess = input(Fore.LIGHTBLUE_EX\
                                + f"Introduce una palabra de 5 letras (intento {i+1}/{N_TRIES})\n"
                            ).upper()

            # Check if the word is in the dictionary
            elif (guess not in vocab) & (guess!="Q"):
                print(Fore.RED + "LA PALABRA NO EXISTE\n")
                guess = input(Fore.LIGHTBLUE_EX \
                                + f"Introduce una palabra de 5 letras (intento {i+1}/{N_TRIES})\n"
                            ).upper()

            else:
                break

        # If we want to quit, we say ADIOS
        if guess == "Q":
            print(Fore.LIGHTBLUE_EX + "ADIOS!")
            break
        
        # Compare the word with the solution and print the colors
        ls_print, _ = compare_wordle(guess, word)
        print(" ".join(ls_print), "\n")

        # If we guessed, we celebrate and finish the program
        if guess == word:
            print(Fore.GREEN + "Has ganado!!")
            break
    
    # If we've reached the max number of chances then we've lost
    if i == N_TRIES - 1:
        print('\n')
        print(Fore.RED + "FIN DEL JUEGO: SE TE ACABARON LOS INTENTOS")
        print("La palabra correcta era " + Fore.GREEN + word)

    print(Fore.WHITE)