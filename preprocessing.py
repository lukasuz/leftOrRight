import re
from nltk import word_tokenize
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
# TODO: not optimal, some words get seperated which should like isn't to isn t


class Preprocessor:
    """ Creates a new Preprocessor for processing multiple reddit comments"""
    def __init__(self):
        self.validSymbols = re.compile('[^a-zA-Z 0-9]')
        self.email = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|' +
                                '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.emailReplacement = 'emailReplacementString'
        self.noneType = type(None)

    def preprocessComments(self, comments, min_comment_length=10):
        """Preprocesses a bunch of reddit comments

        Arguments:
            comments: list<String>
            min_comment_length: mininum length a comment has to be, otherwise
                it will be deleted

        Returns:
            list<String>, the preprocessed comments"""
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
        """Preprocesses a reddit comments

        Arguments:
            comment: String, the comment to be processed

        Returns:
            String, the preprocessed comment"""
        return self.applyStoplist(self.arrayfy(self.dumpNonLetters(
                self.replaceLinks(comment)).strip().lower()))

    def dumpNonLetters(self, comment):
        """Dumps all non letter characters in a comment

        Arguments:
            comment: String, the comment to be processed

        Returns:
            String, the preprocessed comment"""
        return self.validSymbols.sub(' ', comment)

    def replaceLinks(self, comment):
        """Replaces all links with a placeholder.
           TODO: replace links with domain

        Arguments:
            comment: String, the comment to be processed

        Returns:
            String, the preprocessed comment
        """
        match = re.search(self.email, comment)
        if not isinstance(match, self.noneType):
            start, end = match.span()
            comment = comment[0:start] + self.emailReplacement + comment[end:]
        return comment

    # def autocorrectWords(self):
    #     pass

    def applyStoplist(self, comment):
        """Applies the ntlk.corpus stop list.
           Dumps all stop words from a comment

        Arguments:
            comment: String, the comment to be processed

        Returns:
            String, the preprocessed comment"""
        return [elm for elm in comment if elm not in stop]

    def arrayfy(self, comment):
        """listifies a String

        Arguments:
            comment: String, the comment to listified

        Returns:
            list, the string as a list"""
        return re.split(' +', comment)
