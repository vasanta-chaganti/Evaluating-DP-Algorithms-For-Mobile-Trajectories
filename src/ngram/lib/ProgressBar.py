'''
@author: Gergely Acs <acs@crysys.hu>
@editors: Mehtap Y., Victoriia Z., Ziming Y., Koyo A. 
'''
from progressbar import Bar, ETA, Percentage, ProgressBar

class MyProgressBar:

    def __init__(self, label, maxv):
        """
        Creates a progress bar to display the progress of ngram sanitization
        Inputs:
            label: the label of the progress bar
            maxv: the maximum value that the progress bar will go up to
        """
        widgets = [label + ' ', Percentage(), ' ', Bar(), ' ', ETA()]
        self.pbar = ProgressBar(widgets=widgets, maxval=maxv).start()

    def update(self, num):
        """
        Updates the progress displayed on the progress bar
        Inputs
            num: the number to update the bar to
        """
        self.pbar.update(num)

    def finish(self):
        """
        Finishes the progress bar, indicating that computation has completed
        """
        self.pbar.finish()

