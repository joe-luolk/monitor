#!/usr/bin/python
#-*- coding:utf8 -*-
#author: joe
#date: 2019.09.02
#version: 1.0.1
import sys,getopt
import httplib
import urllib
from json import *
reload(sys)
sys.setdefaultencoding('utf8')


def usage():
  print '''usage: %s -t <receivers> -s <title> -m <messages>
      -t,--to=receiver     receive weixin account delimiter use ","
      -s,--title=titles    receive title
      -m,--message         receive message,next row use "\\n"''' %sys.argv[0]

def get_token(host,uri,parms):
   try:
       httpsClient = httplib.HTTPSConnection(host,443,timeout=5)
       httpsClient.request('GET',uri+parms)
       response = httpsClient.getresponse()
       token=eval(response.read())['access_token']
       return token
   except Exception, e:
       print e
   finally:
       httpsClient.close()

def send_wx_message(host,uri,parms,body):
   try:       
       httpsClient = httplib.HTTPSConnection(host,443,timeout=5)
       httpsClient.request('POST',uri+parms,JSONEncoder(ensure_ascii=False).encode(body).replace('\\\\n','\n'))
       response = httpsClient.getresponse()
   except Exception, e:
       print e
   finally:
       httpsClient.close()
       
if __name__=="__main__":
   try:
      opts,args=getopt.getopt(sys.argv[1:],"hHt:s:m:",["help","to=","title=","message="])
      if len(sys.argv) != 7 and len(sys.argv) != 4:
         usage()
         sys.exit()
      else:
       for opt,arg in opts:
         if opt in ('-h','-H','--help'):
            usage()
            sys.exit()
         elif opt in ('-t','--to'):
           if len(arg.split(',')) > 1:
             to='|'.join(arg.split(','))
           else:
             to=arg  
         elif opt in ('-s','--title'):
           title=arg
         elif opt in ('-m','--message'):
           message=arg
       messages='['+title+']'+message
       get_hosts='qyapi.weixin.qq.com'
       get_uris='/cgi-bin/gettoken?'
       get_params=urllib.urlencode({'corpid':'wwe56eb1562fe2a5b4','corpsecret':'A_sA2liqO85fXEeumn1Z8oiPK7OxNoKpTU4HXv11uQA'})
       token=get_token(get_hosts,get_uris,get_params)
       post_hosts='qyapi.weixin.qq.com'
       post_uris='/cgi-bin/message/send?'
       post_params=urllib.urlencode({'access_token':token})
       bodys={}
       bodys['touser']=to
       bodys['msgtype']='text'
       bodys['agentid']=1000002
       bodys['text']={'content': messages}
       bodys['safe']='0'
       send_wx_message(post_hosts,post_uris,post_params,bodys)
   except Exception,e:
       print e

