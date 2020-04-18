# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Daniel Sprehe
# Date: 4/16/2020

import feedparser
import string
import time
import threading
from ps5_project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

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
            # pubdate = pubdate.astimezone(pytz.timezone('EST'))
            # pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

# ======================
# Data structure design
# ======================


# Problem 1
class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
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


# ======================
# Triggers
# ======================
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
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        new_text = ''

        # Clean the text
        for symbol in string.punctuation:
            text = text.replace(symbol, ' ')
        split_text = text.split()
        for word in split_text:
            new_text += word.strip() + ' '

        # Check the text for the phrase
        if self.phrase.lower() in new_text.lower():
            for word in self.phrase.lower().split():
                if word in new_text.lower().split():
                    continue
                else:
                    return False
            return True
        else:
            return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        if self.is_phrase_in(story.get_title()):
            return True
        else:
            return False


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        super().__init__(phrase)

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        if self.is_phrase_in(story.get_description()):
            return True
        else:
            return False


# TIME TRIGGERS
# Problem 5
class TimeTrigger(Trigger):
    # Constructor:
    # Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
    # Convert time from string to a datetime before saving it as an attribute.
    def __init__(self, time):
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(
            tzinfo=pytz.timezone("EST"))


# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        super().__init__(time)

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.time > story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))


class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        super().__init__(time)

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.time < story.get_pubdate().replace(tzinfo=pytz.timezone("EST"))


# COMPOSITE TRIGGERS
# Problem 7
class NotTrigger(Trigger):
    def __init__(self, OtherTrigger):
        self.OtherTrigger = OtherTrigger

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return not self.OtherTrigger.evaluate(story)


# Problem 8
class AndTrigger(Trigger):
    def __init__(self, Trigger1, Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.Trigger1.evaluate(story) and self.Trigger2.evaluate(story)


# Problem 9
class OrTrigger(Trigger):
    def __init__(self, Trigger1, Trigger2):
        self.Trigger1 = Trigger1
        self.Trigger2 = Trigger2

    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        return self.Trigger1.evaluate(story) or self.Trigger2.evaluate(story)


# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    new_stories = []
    for trig in triggerlist:
        for story in stories:
            if trig.evaluate(story):
                new_stories.append(story)
    return new_stories


# ======================
# User-Specified Triggers
# ======================
def trigger_list_dictionary(triggerlines):
    triggers = {}
    for line in triggerlines:
        line = line.split(',')
        if line[0][0] == 't':
            if line[1] == 'TITLE':
                triggers[line[0]] = TitleTrigger(line[2])
            if line[1] == 'DESCRIPTION':
                triggers[line[0]] = DescriptionTrigger(line[2])
            if line[1] == 'AFTER':
                triggers[line[0]] = AfterTrigger(line[2])
            if line[1] == 'BEFORE':
                triggers[line[0]] = BeforeTrigger(line[2])
            if line[1] == 'NOT':
                triggers[line[0]] = NotTrigger(triggers[line[2]])
            if line[1] == 'AND':
                triggers[line[0]] = AndTrigger(
                    triggers[line[2]], triggers[line[3]])
            if line[1] == 'OR':
                triggers[line[0]] = OrTrigger(
                    triggers[line[2]], triggers[line[3]])
    return triggers


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
    triggerlist = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_dict = trigger_list_dictionary(lines)

    for line in lines:
        line = line.split(',')
        if line[0] == 'ADD':
            for triggers in line:
                if triggers[0] == 't':
                    triggerlist.append(trigger_dict[triggers])

    return triggerlist


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        '''t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]'''

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('ps5_triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(
                    END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(
                    END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            stories = []
            # Get stories from Google's Top Stories RSS news feed
            stories += process("http://news.google.com/news?output=rss")

            # Get stories from more RSS feeds
            # Reddit has error - No published Attribute
            # stories += process("https://www.reddit.com/r/worldnews/.rss")
            # Reddit has error - No description Attribute
            # stories += process("https://news.yahoo.com/rss/topstories")

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
