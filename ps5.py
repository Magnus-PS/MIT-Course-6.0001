# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import string
import threading
import time
from datetime import datetime

import feedparser
import pytz as pytz
from mtTkinter import *
from project_util import translate_html


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
            # pubdate = pubdate.astimezone(pytz.timezone('EST')) #take time in as EST
            # pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate): #initialize constructor
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    def __init__(self, phrase): # subclass constructor: implement phrase trigger abstract class
        self.phrase = phrase # take in string phrase as argument to constructor

    def is_string_in(self, text): #implement new method

        # create list of words at white space, remove leading / trailing punctuation, and make letters lowercase
        text = text.lower() #make it lowercase to handle case variability

        #Reference for below implementation: https://www.jeddd.com/article/mit-python-ps5-news-story.html

        text = text.translate(str.maketrans(string.punctuation, ' ' * len(string.punctuation))) #remove punctuation and spaces

        text_list = text.split()
        phrase_list = self.phrase.lower().split()
        for i in range(len(text_list) - len(phrase_list) + 1):
            if text_list[i:i + len(phrase_list)] == phrase_list:
                return True
                break
        return False

# Problem 3
class TitleTrigger(PhraseTrigger): #implement TitleTrigger class as a subclass of PhraseTrigger
    def evaluate(self, story):
        return self.is_string_in(story.get_title())


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_string_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):

    # Constructor:
    #        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
    #        Convert time from string to a datetime before saving it as an attribute.

    def __init__(self, string_time): # subclass constructor: implement time trigger abstract class
        self.time = datetime.strptime(string_time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone('EST'))

# Problem 6
class BeforeTrigger(TimeTrigger): #implement BeforeTrigger class as a subclass of TimeTrigger
    def evaluate(self, story):
        return story.get_pubdate().astimezone(pytz.timezone('EST')) < self.time #fire when a story is published BEFORE the trigger's time

        #print('BEFORE: ' + str(story.get_pubdate().astimezone(pytz.timezone('EST'))) + ' VS ' + str(
            #self.time) + ' : ' + str(BeforeBool))

class AfterTrigger(TimeTrigger): #implement AfterTrigger class as a subclass of TimeTrigger
    def evaluate(self, story):

        return story.get_pubdate().astimezone(pytz.timezone('EST')) > self.time #fire when a story is published AFTER the trigger's time

        #print('AFTER: ' + str(story.get_pubdate().astimezone(pytz.timezone('EST'))) + ' VS ' + str(
            #self.time) + ' : ' + str(AfterBool))

# COMPOSITE TRIGGERS

# Problem 7

class NotTrigger(Trigger):

    def __init__(self, Trigger):
        self.trigger = Trigger #take trigger as argument

    def evaluate(self, news_item):
        return not self.trigger.evaluate(news_item) #invert output of another trigger

# Problem 8

class AndTrigger(Trigger):

    def __init__(self, Trigger1, Trigger2):
        self.t1 = Trigger1
        self.t2 = Trigger2

    def evaluate(self, news_item):
        return self.t1.evaluate(news_item) and self.t2.evaluate(news_item)

# Problem 9

class OrTrigger(Trigger):

    def __init__(self, Trigger1, Trigger2):
        self.t1 = Trigger1
        self.t2 = Trigger2

    def evaluate(self, news_item):
        return self.t1.evaluate(news_item) or self.t2.evaluate(news_item)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    filtered_stories = [] #initialize list

    for story in stories: #cycle through every story in stories list
        for trigger in triggerlist: #cycle through every trigger in trigger list
            if trigger.evaluate(story): #if the trigger fires for that story
                filtered_stories.append(story) #add that story to the filtered_stories list

    return filtered_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    t_dict = {} #initialize trigger dictionary.
    t_list = [] #initialize trigger list. to be returned.

    # for every line in lines, split the string into a list (arg) using commas for delineation
    for line in lines:
        arg = line.split(',')
        print(str(arg))

        # when the first element of arg is 'ADD', add the corresponding triggers to t_list
        if arg[0] == 'ADD':
            t_list.append(t_dict[arg[1]])
            t_list.append(t_dict[arg[2]])

        # otherwise assign the proper trigger to the dictionary for that particular t# (ie.t1)
        # based on the second (and sometimes third) element of line
        elif arg[1] == 'TITLE':
            t_dict[arg[0]] = TitleTrigger(arg[2])
        elif arg[1] == 'DESCRIPTION':
            t_dict[arg[0]] = DescriptionTrigger(arg[2])
        elif arg[1] == 'NOT':
            t_dict[arg[0]] = NotTrigger(arg[2])
        elif arg[1] == 'AND':
            t_dict[arg[0]] = AndTrigger(arg[2], arg[3])
        elif arg[1] == 'OR':
            t_dict[arg[0]] = OrTrigger(arg[2], arg[3])
        elif arg[1] == 'BEFORE':
            t_dict[arg[0]] = BeforeTrigger(arg[2])
        elif arg[1] == 'AFTER':
            t_dict[arg[0]] = AfterTrigger(arg[2])

    return t_list #return this trigger list

#Problem 11 Conclusion: items were properly processed and added to the list. There was an object display error
# That I believe traces to the

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("COVID-19")
        t2 = DescriptionTrigger("USA")
        t3 = DescriptionTrigger("Trump")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

