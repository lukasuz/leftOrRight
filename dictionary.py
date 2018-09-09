

class Dictionary:
    def __init__(self, comments=[], wordToIndexDict={'<UNKOWN>': 0},
                 indexToWordDict={0: '<UNKOWN>'}):
        self.comments = comments
        self.wordToIndexDict = wordToIndexDict
        self.indexToWordDict = indexToWordDict
        self.addCommentsToDict(comments)

    def addCommentsToDict(self, comments):
        for comment in comments:
            for word in comment:
                if word not in self.wordToIndexDict:
                    self.wordToIndexDict[word] = len(self.wordToIndexDict)
                    self.indexToWordDict[len(self.wordToIndexDict)-1] = word
        print('Updated dict size: '+str(self.getSize()))
        return (self.wordToIndexDict, self.indexToWordDict)

    def translateComment(self, comment):
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
        translated_comments = []
        for comment in comments:
            translated_comments.append(self.translateComment(comment))
        return translated_comments

    def getSize(self):
        return len(self.wordToIndexDict)
