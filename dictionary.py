

class Dictionary:
    """Creates a dictionary for embedding purposes"""
    def __init__(self, comments=[], wordToIndexDict={'<UNKOWN>': 0},
                 indexToWordDict={0: '<UNKOWN>'}):
        self.comments = comments
        self.wordToIndexDict = wordToIndexDict
        self.indexToWordDict = indexToWordDict
        self.addCommentsToDict(comments)

    def addCommentsToDict(self, comments):
        """Adds words fromt comments to the dictionary

        Arguments:
            comments: list<String>, comments that should be added to the dict

        Returns:
            {wordToIndexDict: <dict>, indexToWordDict<dict>}, dictionaries with
            index -> word and vice versa"""
        for comment in comments:
            for word in comment:
                if word not in self.wordToIndexDict:
                    self.wordToIndexDict[word] = len(self.wordToIndexDict)
                    self.indexToWordDict[len(self.wordToIndexDict)-1] = word
        print('Updated dict size: '+str(self.getSize()))
        return (self.wordToIndexDict, self.indexToWordDict)

    def translateComment(self, comment):
        """Maps a word to its index number according to the dictionary

        Arguments:
            comment: String, the comment to be translated

        Returns:
            String, the translated comment"""
        if isinstance(comment[0], str):
            dict = self.wordToIndexDict
        else:
            dict = self.indexToWordDict
        for index, word in enumerate(comment):
            if word in dict:
                comment[index] = dict[word]
            else:
                first_elm = next(iter(dict))
                comment[index] = dict[first_elm]
        return comment

    def translateComments(self, comments):
        """Translates multiple comments, see translateComment()

        Arguments:
            comments: list<String>, the comments to be translated

        Returns:
            list<String>, the translated comments"""
        translated_comments = []
        for comment in comments:
            translated_comments.append(self.translateComment(comment))
        return translated_comments

    def getSize(self):
        """Returns the size of the dictionary

        Returns:
            int, size of the dictionary"""
        return len(self.wordToIndexDict)
