from redditComments import CommentGetter
from preprocessing import Preprocessor
from dictionary import Dictionary
from classifier import Classifier
import pickler
import random

subreddit_collection = [
    {'name': 'latestagecapitalism', 'tag': 'left'},
    {'name': 'anarchism', 'tag': 'left'},
    {'name': 'anarchy', 'tag': 'left'},
    {'name': 'anarchy101', 'tag': 'left'},
    {'name': 'sandersforpresident', 'tag': 'left'},
    {'name': 'socialism', 'tag': 'left'},
    {'name': 'communism', 'tag': 'left'},
    {'name': 'lgbt', 'tag': 'left'},
    {'name': 'fuckthealtright', 'tag': 'left'},
    {'name': 'feminism', 'tag': 'left'},
    {'name': 'prochoice', 'tag': 'left'},
    {'name': 'the_donald', 'tag': 'right'},
    {'name': 'conservative', 'tag': 'right'},
    {'name': 'cringeanarchy', 'tag': 'right'},
    {'name': 'nra', 'tag': 'right'},
    {'name': 'prolife', 'tag': 'right'},
    {'name': 'mensrights', 'tag': 'right'},
    {'name': 'mgtow', 'tag': 'right'},
    {'name': 'progun', 'tag': 'right'},
    {'name': 'greatawakening', 'tag': 'right'},
    {'name': 'capitalism', 'tag': 'right'},
    {'name': 'republican', 'tag': 'right'}]


class Handler:
    def __init__(self, max_comments_per_subreddit=100000):
        self.getter = CommentGetter()
        self.preprocessor = Preprocessor()
        self.max_comments_per_subreddit = max_comments_per_subreddit
        # if load_from_files:
        #     self.dictionary = Dictionary(
        #         wordToIndexDict=pickler.loadData('wordToIndexDict'),
        #         indexToWordDict=pickler.loadData('indexToWordDict'))
        # else:
        #     self.dictionary = Dictionary()
        self.dictionary = Dictionary()

    # def getProcessTranslateAndSave(self, subreddit_name, amount_comments,
    #                                with_replies=False):
    #     comments = self.getter.getComments(subreddit_name,
    #                                        amount_comments=amount_comments)
    #     comments = self.preprocessor.preprocessComments(comments['comments'])
    #     self.dictionary.addCommentsToDict(comments)
    #     comments = self.dictionary.translateComments(comments)
    #     # save comments
    #     pickler.saveDataAsPickle(subreddit_name, comments)
    #     # save Dictionaries for translation
    #     pickler.saveDataAsPickle('wordToIndexDict',
    # self.dictionary.wordToIndexDict)
    #     pickler.saveDataAsPickle('indexToWordDict',
    # self.dictionary.indexToWordDict)

    def getAndSaveBatchOfComments(self, subreddits):
        """Lädt und speichert subreddit Kommentare ab.

        Arguments:
          subreddits:
          list<{name: string, tag:string}>
        """
        left_amount = 0
        right_amount = 0
        for subreddit in subreddits:
            comments = self.getter.getComments(subreddit['name'],
                                               self.max_comments_per_subreddit,
                                               with_replies=False)
            pickler.saveDataAsPickle(comments=comments['comments'],
                                     tag=subreddit['tag'],
                                     amount=len(comments['comments']),
                                     name=subreddit['name'])
            if subreddit['tag'] is 'left':
                left_amount += len(comments['comments'])
            elif subreddit['tag'] is 'right':
                right_amount += len(comments['comments'])
        print('Left amount: ', left_amount)
        print('right_amount: ', right_amount)

    def loadCommentsAndTrainClassifier(self):
        files = pickler.loadAllFilesFromData()
        left_comments = []
        right_comments = []
        for f in files:
            print(f['name'], f['tag'], len(f['comments']))
            if f['tag'] == 'left':
                left_comments += f['comments']
            elif f['tag'] == 'right':
                right_comments += f['comments']
        random.shuffle(left_comments)
        random.shuffle(right_comments)
        print('Right comments loaded: {0}, left comments loaded: {1}'.format(
            len(right_comments), len(left_comments)))

        length = min(len(right_comments), len(left_comments))
        left_comments = left_comments[:length]
        right_comments = right_comments[:length]

        left_comments = self.preprocessor.preprocessComments(left_comments)
        right_comments = self.preprocessor.preprocessComments(right_comments)

        self.dictionary.addCommentsToDict(left_comments+right_comments)
        left_comments_translated = self.dictionary.translateComments(
            left_comments)
        right_comments_translated = self.dictionary.translateComments(
            right_comments)

        self.createAndTrainClassifier(
            right_comments_translated,
            left_comments_translated,
            self.dictionary.getSize())

    def createAndTrainClassifier(self, right, left, dictionary_size):
        data = right + left
        labels = ([0] * len(right)) + ([1] * len(left))
        self.classifier = Classifier(
            data, labels, dictionary_size)

    def startQuestionRound(self):
        while True:
            print('\033[92mWhat do you have to say? \033[0m')
            text_input = input()
            preprocessed_input = self.preprocessor.preprocessComment(
                text_input)
            translated_comment = self.dictionary.translateComment(
                preprocessed_input)
            prediction = self.classifier.predict(translated_comment)
            if prediction[0] > 0.5:
                print('\033[92mThat sounds left winged. \033[0m',
                      prediction[0], '\n')
            else:
                print('\033[92mThat sounds right winged. \033[0m',
                      prediction[0], '\n')

# TODO: save raw comments, create dictionary after loading, dont save


def main():
    handler = Handler()
    handler.getAndSaveBatchOfComments(subreddit_collection)
    handler.loadCommentsAndTrainClassifier()
    handler.startQuestionRound()


if __name__ == '__main__':
    main()
