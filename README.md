# saul-bot

Generate text in the style of the text in the given files.

## Examples

### Word-based model

Train a 4-gram word-based language model on a file called `alice.txt` and generate 5 lines of text.

    python2 ngrams.py alice.txt --chars=false --order=4 --lines=5

This will produce a sequence of words that are found in the original text. Each word generated will be based on (at most) the previous three words (`--order=4`).

### Character-based model

Train a 7-gram character-based language model on a file called `alice.txt` and generate 10 lines of text.

    python2 ngrams.py alice.txt --chars=true --order=7 --lines=10

This will produce a sequence of characters, not words, which means that the output text may contain words that are not actual words.

## Full usage

    usage: ngrams.py [-h] [--lines LINES] [--order ORDER] [--chars CHARS]
                     [--stop_symbols STOP_SYMBOLS]
                     FILE [FILE ...]

    positional arguments:
      FILE                  The files to use for language model training.

    optional arguments:
      -h, --help            show this help message and exit
      --lines LINES         The number of lines of text to generate.
      --order ORDER         The order of the n-gram model (the maximum 'n').
      --chars CHARS         Use a character-based model instead of a word-based
                            model.
      --stop_symbols STOP_SYMBOLS
                            Symbols that will stop the generation of a single
                            text. This is optional, but an example might be
                            ----stop_symbols=".?!"
