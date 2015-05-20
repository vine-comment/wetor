# coding:utf-8
'''
Created on 2015-5-19
@author: bn
'''

import time
import re
import os
import sys
import threading
from multiprocessing import Process
from string import capitalize

try: 
    input = raw_input
except NameError:
    pass

try:
    import urllib.request
    #import urllib.parse
except ImportError:
    import urllib
    urllib.request = __import__('urllib2')
    urllib.parse = __import__('urlparse')
 
urlopen = urllib.request.urlopen
request = urllib.request.Request

def get_content_from_url(url):
    attempts = 0
    content = ''

    while attempts < 5:
        #url_lock.acquire()
        try:
            content = urlopen(url).read().decode('utf-8', 'ignore')
            time.sleep(2)
            #url_lock.release()
            break
        except Exception as e:
            attempts += 1
            time.sleep(2)
            #url_lock.release()
            print(e)

    return content

def notify(url, pattern, target):
    html = get_content_from_url(url)
    retlist = re.findall(pattern, html)
    global notified
    if len(retlist) == 1 and not notified:
        print "%s, you have got a message." % target
        notified = True
    elif len(retlist) == 0 and notified:
        notified = False
    else:
        print "notifed"
    global timer
    timer = threading.Timer(300, notify, [url, pattern, target])
    timer.start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "ONE argument, the url needed"
        sys.exit(-1)
    #for ret in retlist:
    #    print ret
    notified = False
    timer = threading.Timer(1, notify, [sys.argv[1], "switch switch_on", "Luoben's phone"])
    timer.start()
