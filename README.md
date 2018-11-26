# saul-bot

Generate text in the style of the text in the given files.

## Get Started
### Option 1: using Git
1. Install Git on your computer (I have no idea how to do this. wahhh.)
2. Download the repository
    1. open the command line
    2. Use the command `cd path\to\directory` to navigate to the directory where you want to work.
    3. Use the command `git clone git@github.com:dhgarrette/saul-bot.git` to download the repository. If you open the folder you should see that it has downloaded inside a new folder called `saul-bot`.

### Option 2: just download the file
In the upper right of the github home page you can choose `download`. You'll get a zipped folder that you have to unzip. It will be called saul-bot-master, so either rename to saul-bot or plann accordingly.

### Create a training file
The repository will come with a training file (alice.txt) that will create an aliceinwonderlandbot. But if you want it based on someone else's work, you'll need to give it something else to train on. It should be a `.txt` file full of words by the person you want to roboticize. Save the file in `saul-bot`.

### Run the program
There are examples below, but in general you'll need to do the following things:
1. Choose a file containing training text (i.e. alice.txt)
2. Decide on length for your story (i.e. 5 lines)
3. Decide on the order, i.e. how much linguistic context you want the bot to use. The standard is 3, meaning it's a 3-gram or trigram model that chooses each word based on the two words that precede it.
4. Open the command line and navigate to the `saul-bot` folder using the cd command.
5. Enter a command to run the program. There are examples below, but the basic format is:
` programminglanguage programname trainingfile.txt --chars=false --order=number --lines=number`
`python2 ngrams.py alice.txt --chars=false --order=3 --lines=5`


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
