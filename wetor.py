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
import xinge
import logging

ISOTIMEFORMAT='%m-%d %H:%M'
UrlDict = {"http://www.douyutv.com/16789":"安德罗妮丶",
           "http://www.douyutv.com/25515":"秋日丶",
           "http://www.douyutv.com/211086":"赵小臭",
           "http://www.douyutv.com/fxy":"风行云",
           "http://www.douyutv.com/241449":"Alex"}

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
            logging.ERROR(e)

    return content


# 定义通知
def BuildNotification(url):
    msg = xinge.Message()
    msg.type = xinge.Message.TYPE_NOTIFICATION
    msg.title = title_global
    # 消息为离线设备保存的时间，单位为秒。默认为0，表示只推在线设备
    msg.expireTime = 86400
    # 定时推送，非必须
    #msg.sendTime = '2012-12-12 18:48:00'
    # 自定义键值对，key和value都必须是字符串，非必须
    #msg.custom = {'aaa':'111', 'bbb':'222'}
    # 使用多包名推送模式，详细说明参见文档和wiki，如果您不清楚该字段含义，则无需设置
    #msg.multiPkg = 1

    # 允许推送时段设置，非必须
    #ti1 = xinge.TimeInterval(9, 30, 11, 30)
    #ti2 = xinge.TimeInterval(14, 0, 17, 0)
    #msg.acceptTime = (ti1, ti2)

    # 通知展示样式，仅对通知有效
    # 样式编号为2，响铃，震动，不可从通知栏清除，不影响先前通知
    style = xinge.Style(2, 1, 1, 0, 0)
    style.lights = 1
    msg.style = style

    # 点击动作设置，仅对通知有效
    # 以下例子为点击打开url
    action = xinge.ClickAction()
    action.actionType = xinge.ClickAction.TYPE_URL
    action.url = url
    # 打开url不需要用户确认
    action.confirmOnUrl = 0
    msg.action = action

    # 以下例子为点击打开intent。例子中的intent将打开拨号界面并键入10086
    # 使用intent.toUri(Intent.URI_INTENT_SCHEME)方法来得到序列化后的intent字符串，自定义intent参数也包含在其中
    #action = xinge.ClickAction()
    #action.actionType = xinge.ClickAction.TYPE_INTENT
    #action.intent = 'intent:10086#Intent;scheme=tel;action=android.intent.action.DIAL;S.key=value;end'
    #msg.action = action

    return msg

def notify(url, pattern):
    html = get_content_from_url(url)
    retlist = re.findall(pattern, html)
    global notified
    if len(retlist) == 1 and not notified:
        msg.content = time.strftime(ISOTIMEFORMAT, time.localtime())+" " \
                      + UrlDict[url] + content_global
        logging.info(x.PushAllDevices(0, msg))
        notified = True
    elif len(retlist) == 0 and notified:
        notified = False
        logging.info(UrlDict[url] + " off line")
    global timer
    timer = threading.Timer(interval_global, notify, [url, pattern])
    timer.start()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "ONE argument, the url needed"
        sys.exit(-1)
    #for ret in retlist:
    #    print ret
    notified = True
    access_id = 2100117119
    secret_key = "e19a1e2dcd5ec42cca9e8e1b9922dfba"

#test id begin
#    access_id = 2100034106
#    secret_key = "a2578e26d5d44ff44cce85481ff9a179"
#test id end
    x = xinge.XingeApp(access_id, secret_key)

    url = sys.argv[1]
    title_global = "斗鱼老司机"
    content_global = " 上线啦 点击追剧 >>"
    msg = BuildNotification(url)

    interval_global = 300
    logfile = "/opt/wetor/log/"+UrlDict[url]+".log"
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=logfile,
                filemode='w')


    logging.info("====== Start monitoring %s ======" % url)
    timer = threading.Timer(1, notify, [url, "switch switch_on"])
    timer.start()
