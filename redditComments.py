# Makes fetching thousands of comments from reddit easy
import praw


class CommentGetter:
    def __init__(self):
        """Creates a new commentGetter Instance."""
        self.reddit = praw.Reddit(client_id='DdZR4AqiURh8wg',
                                  client_secret='-ZL8nr760knqyZdpwd8JIx7bLpg',
                                  user_agent='left_or_right')

    def getComments(self, subreddit_name, amount_comments=1000,
                    minimum_comment_score=3, with_replies=False):
        """Main function, tries to fetch a certain amount of comments from a
        subreddit and returns them in the format {'comments': <list>,
        'excessive': <list>}

        Arguments:
            subreddit_name: string, name of the subreddit
            minimum_comment_score: int, the minimum score a comment has to have
            amount_comments: int, the amount of comments that should be fetched
            with_replies: Bool, True if all replies to comments should be
            fetched too. ATTENTION: makes the fetching really slow.

        Returns:
            {'comments': <list>, 'excessive': <list>}, exessive is overflow
            container if more comments were fetched than wanted."""
        limit = None if with_replies else 1
        subreddit = self.reddit.subreddit(subreddit_name)
        top_submissions = subreddit.top()
        comments = set()
        self.printTitle(subreddit)
        try:
            while len(comments) < amount_comments:
                current_submission = next(top_submissions)
                self.printSubmission(current_submission)
                subreddit_comments_w_scores = self.getCommentsFromSubreddit(
                    current_submission, limit=limit)
                cleaned_subreddit_comments = self.clean(
                    subreddit_comments_w_scores,
                    minimum_comment_score)
                self.printComments(cleaned_subreddit_comments)
                comments |= set(cleaned_subreddit_comments)
        except StopIteration:
            self.printCouldNotFetAmount()
        payload = self.splitComments(comments, amount_comments)
        self.printPayLoadInfo(payload)

        return payload

    def getCommentsFromSubreddit(self, submission, limit=None):
        """Helper Function. Retrieves comments from a submission.
        Arguments:
            submission: praw submission object, the target submission
            limit: int | None, amount that comments show be reloaded
        Returns:
            list({'text': <string>, 'score': <int>})"""
        comments = []  # {'text': <string>, 'score': <int}
        submission.comments.replace_more(limit=limit)
        for comment in submission.comments.list():
            comments.append({
                'text': comment.body,
                'score': comment.score
            })
        return comments

    def clean(self, comments, minimum_comment_score):
        """Helper Function.Clean unwanted comments: deleted, removed and
        comments that have too low score.
        Arguments:
            comments: list({'text': <string>, 'score': <int>}), from
                getCommentsFromSubreddit()
            minimum_comment_score: int, minimum score of a comment
        Returns:
            list(<string>)"""
        clean_comments = []  # text only
        for comment in comments:
            if ('[removed]' not in comment['text'] and
                    '[deleted]' not in comment['text'] and
                    comment['score'] >= minimum_comment_score):
                clean_comments.append(comment['text'])
        return clean_comments

    def splitComments(self, comments, amount):
        """Helper Function. Splits commentset into two arrays if more comments
        were retrieved than wanted.
        Arguments:
            comments: set, set of comments
            amount: int, amount of comments that should be in the comments list
        """
        comments_as_list = list(comments)
        splitA = comments_as_list[:amount]
        splitB = comments_as_list[amount:]
        return {'comments': splitA, 'excessive': splitB}

    def printPayLoadInfo(self, payload):
        """Prints Progress"""
        comment_amount = len(payload['comments'])
        excessive_amount = len(payload['excessive'])
        total = comment_amount + excessive_amount
        print('Fetched {0} comments. Excessive: {1}. Total: {2}'
              .format(comment_amount, excessive_amount, total), '\n')

    def printTitle(self, subreddit):
        """Prints Progress"""
        print('Fetching comments from: ', (subreddit.title).encode('utf-8'),
              '\n')

    def printSubmission(self, submission):
        """Prints Progress"""
        print('  Fetching comment from submission: ',
              submission.title.encode('utf-8'))

    def printComments(self, comments):
        """Prints Progress"""
        print('  Using {0} comments'.format(len(comments)), '\n')

    def printCouldNotFetAmount(self):
        """Prints Progress"""
        print('Could not fetch wanted amount of comments.')


# getter = CommentGetter()
# comments = getter.getComments('potato', amount_comments=500)
