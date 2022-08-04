#
# textmodel.py
#
# TextModel project!
#
# Name(s): Andre Nesbit, Anya Raghuvanshi, Haven Qin
#
from porter import create_stem
import math
class TextModel:
    """A class supporting complex models of text."""

    def __init__(self):
        """Create an empty TextModel."""
        # 
        # The text in the model, all in a single string--the original
        # and "cleaned" versions.
        #
        self.text = ''            # No text present yet
        self.cleanedtext = ''     # Nor any cleaned text yet
                                  # ..(cleaned == only letters, all lowercase)

        #
        # Create dictionaries for each characteristic
        #
        self.words = {}           # For counting words
        self.wordlengths = {}     # For counting word lengths
        self.stems = {}           # For counting stems
        self.sentencelengths = {} # For counting sentence lengths
        # Create another dictionary of your own
        #
        self.myparameter = {}     # For counting punctuation

    def __repr__(self):
        """Display the contents of a TextModel."""
        s = f'Words:\n{str(self.words)}\n\n'
        s += f'Word lengths:\n{str(self.wordlengths)}\n\n'
        s += f'Stems:\n{str(self.stems)}\n\n'
        s += f'Sentence lengths:\n{str(self.sentencelengths)}\n\n'
        s += f'MY PARAMETER:\n{str(self.myparameter)}\n\n'
        s += '+'*55 + '\n'
        s += f'Text[:42]    {self.text[:42]}\n'
        s += f'Cleaned[:42] {self.cleanedtext[:42]}\n'
        s += '+'*55 + '\n\n'
        return s

    # We provide two text-adding methods (functions) here:
    def addRawText(self, text):
        """addRawText accepts self (the object itself)
                      and text, a string of raw text to add.
           Nothing is returned from this method, but
           the text _is_ added.
        """
        self.text += text 
        self.cleanedtext += self.cleanString(self.text) 

    # The second one adds text from a file:
    def addFileText(self, filename):
        """addFileText accepts a filename.
            
           Nothing is returned from this method, but
           the file is opened and its text _is_ added.

           If the file is not present, it will crash!
        """
        f = open(filename, 'r', encoding='latin1')
                               # The above may need utf-8 or utf-16, depending
        text = f.read()        # Read all of the contents into text 
        f.close()              # Close the file
        self.addRawText(text)  # Uses the previous method!

    # Include other functions here.
    # In particular, you'll need functions that add to the model.

    def makeSentenceLengths(self):
        """Creates the dictionary of sentence lengths
               should use self.text, because it needs the punctuation!
        """
        x = 1
        a = self.text
        a = a.split()
        for i in a:
            if i[-1] not in '.?!':
                x += 1
            else:
                if x not in self.sentencelengths:
                    self.sentencelengths[x] = 1
                else:
                    self.sentencelengths[x] += 1
                x = 1

    def cleanString(self, s):
        """Returns the string s, but
           with only ASCII characters, only lowercase, and no punctuation.
           See the description and hints in the problem!
        """
        result = s.lower()    # Not implemented fully: this just lower-cases
        result = result.replace("\n", "")
        new = ''
        for i in range(len(result)):  # ..things for now
            if result[i] not in '".,\'?!':
                new += result[i]
            else:
                new += result[i][:-2:]
        result = new
        return result

    def makeWordLengths(self):
        """ creates dictionary of the length of each word
            within self.text
        """
        a = self.cleanString(self.text)
        for word in a.split():
            if len(word) not in self.wordlengths:
                self.wordlengths[len(word)] = 1
            else:
                self.wordlengths[len(word)] += 1

    def makeWords(self):
        """ Counts the frequency of how often a word appears
            within self.text(
        """
        a = self.cleanString(self.text)
        for word in a.split():
            if word not in self.words:
                self.words[word] = 1
            else: self.words[word] += 1

    def makeStems(self):
        """ creates a dictionary from self.txt for words that
            share the same stem. e.g. "spam" and "spamming"
            share the same stem.
        """
        a = self.cleanString(self.text)
        for word in a.split():
            if create_stem(word) not in self.stems:
                self.stems[create_stem(word)] = 1
            else:
                self.stems[create_stem(word)] += 1
    
    def makePunctuation(self):
        '''Counts the frequency of how often punctuation appears in self.txt
        '''
        a = self.text
        a = a.split()
        for i in a:
            if i[-1] in "!?.',":
                if i[-1] not in self.myparameter:
                    self.myparameter[i[-1]] = 1
                else: self.myparameter[i[-1]] += 1

    def getSharedVocab(self, d, d1, d2):
        """ Accepts three dictionaries and returns a list of
            unique word that appear in at least one of the
            three dictionaries
        """
        unique = []
        unique += list(d.keys())
        unique += list(d1.keys())
        unique += list(d2.keys())
        words = set(unique)
        return list(words)
    
    def smoothDictionary(self, d, vocab):
        """ takes a dictionary and a vocab list and adds 1 to the
            value for each vocab item in the list
        """
        vocabScore = {}
        for word in d:
            if word in vocab and word not in vocabScore:
                vocabScore[word] = 1
            elif word in vocab and word in vocabScore:
                vocabScore[word] += 1
        return vocabScore
    def normalizeDictionary(self, d):
        """ returns a normalized version of the dictionary
        """
        normal = {}
        for k in d:
            normal[k] = d[k] / sum(d.values())
        return normal
    
    def smallestValue(self, nd1, nd2):
        """ accepts two model dictionaries and returns
            the smalles positive value across them both.
            when used, the two input dictionaries are
            likely to be normalized, but should work
            regardless of being normalized
        """
        return min([min(self.normalizeDictionary(nd1).values()), min(self.normalizeDictionary(nd2).values())])

    def compareDictionaries(self, d, nd1, nd2):
        """ Computes the log probability that the dictionary d
            arose from the distribution of data in the normalized
            nd1 and nd2
        """
        total_log_prob = 0.0
        epsilon = self.smallestValue(nd1, nd2) / 2
        L = []
        for word in d:
            if word not in nd1:
                total_log_prob += d[word] * math.log(epsilon)
            else:
                total_log_prob += d[word] * math.log(nd1[word])
        L.append(total_log_prob)
        total_log_prob = 0.0
        for word in d:
            if word not in nd2:
                total_log_prob += d[word] * math.log(epsilon)
            else:
                total_log_prob += d[word] * math.log(nd2[word])
        L.append(total_log_prob)
        return L
    def createAllDictionaries(self):
        """Create out all five of self's
           dictionaries in full.
        """
        self.makeSentenceLengths()
        self.makeWords()
        self.makeStems()
        self.makeWordLengths()
        self.makePunctuation()
    
    def compareTextWithTwoModels(self, model1, model2):
        """ runs compare Dictionaries method for each of
            the feature dictionare in self against the corresponding
            dictionaries in model1 and model2
        """
        mod1 = 0
        mod2 = 0
        self.createAllDictionaries()
        model1.createAllDictionaries()
        model2.createAllDictionaries()

        nd1 = self.normalizeDictionary(model1.words)
        nd2 = self.normalizeDictionary(model2.words)
        LogProbsWords = self.compareDictionaries(self.words, nd1, nd2)

        nd1 = self.normalizeDictionary(model1.wordlengths)
        nd2 = self.normalizeDictionary(model2.wordlengths)
        LogProbsWordLengths = self.compareDictionaries(self.wordlengths, nd1, nd2)

        nd1 = self.normalizeDictionary(model1.sentencelengths)
        nd2 = self.normalizeDictionary(model2.sentencelengths)
        LogProbsSentenceLengths = self.compareDictionaries(self.sentencelengths, nd1, nd2)
        
        nd1 = self.normalizeDictionary(model1.stems)
        nd2 = self.normalizeDictionary(model2.stems)
        LogProbsStems = self.compareDictionaries(self.stems, nd1, nd2)

        nd1 = self.normalizeDictionary(model1.myparameter)
        nd2 = self.normalizeDictionary(model2.myparameter)
        LogProbsPunctuation = self.compareDictionaries(self.myparameter, nd1, nd2)

        if max(LogProbsWords) == LogProbsWords[0]:
            mod1 += 1
        else:
            mod2 += 1
        if max(LogProbsWordLengths) == LogProbsWordLengths[0]:
            mod1 += 1
        else:
            mod2 += 1
        if max(LogProbsSentenceLengths) == LogProbsSentenceLengths[0]:
            mod1 += 1
        else:
            mod2 += 1
        if max(LogProbsStems) == LogProbsStems[0]:
            mod1 += 1
        else:
            mod2 += 1
        if max(LogProbsPunctuation) == LogProbsPunctuation[0]:
            mod1 += 1
        else:
            mod2 += 1

        print("Overall Comparison:\n")
        print(f"     {'name':>20s}   {'vsTM1':>10s}   {'vsTM2':>10s} ")
        print(f"     {'----':>20s}   {'-----':>10s}   {'-----':>10s} ")
        d_name = 'words'
        print(f"     {d_name:>20s}   {LogProbsWords[0]:>10.2f}   {LogProbsWords[1]:>10.2f} ")
        d_name = 'wordlengths'
        print(f"     {d_name:>20s}   {LogProbsWordLengths[0]:>10.2f}   {LogProbsWordLengths[1]:>10.2f} ")
        d_name = 'sentencelengths'
        print(f"     {d_name:>20s}   {LogProbsSentenceLengths[0]:>10.2f}   {LogProbsSentenceLengths[1]:>10.2f} ")
        d_name = 'stems'
        print(f"     {d_name:>20s}   {LogProbsStems[0]:>10.2f}   {LogProbsStems[1]:>10.2f} ")
        d_name = 'punctuation'
        print(f"     {d_name:>20s}   {LogProbsPunctuation[0]:>10.2f}   {LogProbsPunctuation[1]:>10.2f} ")
        print("\n\n")
        print("-->\tModel1 wins on", mod1,"features")
        print("-->\tModel2 wins on", mod2, "features")
        if mod1 > mod2:
            print("Model1 is the better match")
        else:
            print("Model2 is the better match")
Manifesto = TextModel()
Federalist = TextModel()
HB = TextModel()
Manifesto.addFileText("CommunistManifesto.txt")
Federalist.addFileText("Federalist.txt")
HB.addFileText("train2.txt")
HB.createAllDictionaries()
Manifesto.createAllDictionaries()
Federalist.createAllDictionaries()
HB.compareTextWithTwoModels(Manifesto, Federalist)
