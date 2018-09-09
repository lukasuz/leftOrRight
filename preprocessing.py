import re
from nltk import word_tokenize
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
# TODO: not optimal, some words get seperated which should like isn't to isn t


class Preprocessor:
    def __init__(self):
        self.validSymbols = re.compile('[^a-zA-Z 0-9]')
        self.email = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|' +
                                '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.emailReplacement = 'emailReplacementString'
        self.noneType = type(None)

    def preprocessComments(self, comments, min_comment_length=10):
        print('Preprocessing comments.')
        preprocessed_comments = []
        for comment in comments:
            preprocessed_comment = self.preprocessComment(comment)
            if len(preprocessed_comment) >= min_comment_length:
                preprocessed_comments.append(preprocessed_comment)
        print('  {0} comments deleted.'.format(
            str(len(comments)-len(preprocessed_comments))))
        return preprocessed_comments

    # def dumpNonAscii(self, comment):
    #     return comment.encode('ascii', errors='ignore')

    def preprocessComment(self, comment):
        return self.applyStoplist(self.arrayfy(self.dumpNonLetters(
                self.replaceLinks(comment)).strip().lower()))

    def dumpNonLetters(self, comment):
        return self.validSymbols.sub(' ', comment)

    def replaceLinks(self, comment):
        """
        TODO: replace links with domain
        """
        match = re.search(self.email, comment)
        if not isinstance(match, self.noneType):
            start, end = match.span()
            comment = comment[0:start] + self.emailReplacement + comment[end:]
        return comment

    # def autocorrectWords(self):
    #     pass

    def applyStoplist(self, comment):
        return [elm for elm in comment if elm not in stop]

    def arrayfy(self, comment):
        return re.split(' +', comment)
