__author__ = 'animeshjain'

import urllib2
import time
import os
import robotparser
from bs4 import BeautifulSoup
import urlparse
import sys

#root_url = "http://www.ccs.neu.edu"
root_url = sys.argv[1]
line = 0
if os.path.isfile('/jainani/hw1/python/ListofLinks.txt'):
    os.remove("/jainani/hw1/python/ListofLinks.txt")


d = {}
crawlurl =[]

def robot_parser(get_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    get_hostname1 = urlparse.urlparse(get_url).hostname
    change_string_hostname1 = "http://" + get_hostname1
    get_new_url = urlparse.urljoin(change_string_hostname1, '/robots.txt')
    request = urllib2.Request(get_new_url,headers=headers)
    response = urllib2.urlopen(request)
    rp = robotparser.RobotFileParser()
    rp.parse(response.readlines())
    parser_response = rp.can_fetch("*", get_url)
    return  parser_response


def Crawler(root, steps):

    urls = [root]
    visited = [root]
    counter = 0


    while counter <steps:

        step_url = scrapeStep(urls)
        if line is 100:
            break
        urls = []
        for u in step_url:
            if u not in visited:
                urls.append(u)
                visited.append(u)




        counter+=1

    return visited

def scrapeStep(root):

    matrix1 = []
    global line
    result_urls = []
    getnewurl = []
    getnewurl12 = []
    headers1 = { 'User-Agent' : 'Firefox'}
    headers = { 'User-agent' : 'Firefox' }
    counterforheader = 0






    for url in root:

        #print url
        if line is 100:
            break
        fo = open("/jainani/hw1/python/ListofLinks.txt", "a")
        hostname2 =  urlparse.urlparse(url).hostname
        boolean_response = robot_parser(url)
        if hostname2 == 'www.ccs.neu.edu' or hostname2 == 'www.northeastern.edu':
            if url not in crawlurl:
                fo.write(url+' ')

        try:
            hostname3 = urlparse.urlparse(url).hostname
            if hostname3 == 'www.ccs.neu.edu' or hostname3 == 'www.northeastern.edu':
                if url not in crawlurl and boolean_response is True:


                    visited11 = urllib2.Request(url, None, headers1)
                    htmltext = urllib2.urlopen(visited11)
                    time.sleep(5)
                    content_type = htmltext.info().getheader('Content-Type')
                else:
                    if url in d.keys():

                        if line is 100:
                            break
                        fo.write(url+' ')
                        getnewarray = d[url]


                        for s in getnewarray:
                            if line is 100:
                                break
                            fo.write(s+' ')
                        fo.write('\n')

                        getnewarray = []
                        line +=1
                    fo.close()

            if content_type.startswith('text/html'):
                gethtml = htmltext.read()
                soup = BeautifulSoup(gethtml)
                for link in soup.findAll('a', href=True):
                        try:
                            newurl = urlparse.urljoin(link.base_url, link['href'])
                            hostname1 = urlparse.urlparse(newurl).hostname
                            outlinks_boolean_request = robot_parser(newurl)
                            req = urllib2.Request(newurl, None, headers)
                            if outlinks_boolean_request is True:
                                response = urllib2.urlopen(req)
                                content_type_outgoing = response.info().getheader('Content-Type')

                                if newurl not in crawlurl and content_type_outgoing.startswith('text/html'):
                                    gethtml1 = response.read()
                                    soup1 = BeautifulSoup(gethtml1)
                                    counterforheader +=1

                                    for link_int in soup1.findAll('a', href=True):

                                        matrix  = urlparse.urljoin(link_int.base_url, link_int['href'])
                                        specialchar = matrix[-4:]
                                        hostname5 = urlparse.urlparse(matrix).hostname
                                        if matrix not in getnewurl12 and specialchar not in ['.jpg','.jpeg']:
                                            if hostname5 == 'www.ccs.neu.edu' or hostname5 == 'www.northeastern.edu':
                                                specialcharacters = matrix[-1:]
                                                if specialcharacters in ['#']:
                                                    matrix =  matrix[:-1]
                                                specialcharacters = ''
                                                result_urls.append(matrix)
                                                getnewurl12.append(matrix)
                                                matrix1.append(matrix)
                                    getnewurl12 = []
                                    d[newurl] = matrix1

                                    matrix1 = []



                        except:
                            pass
                        if newurl not in getnewurl:
                            if hostname1 == 'www.ccs.neu.edu' or hostname1 == 'www.northeastern.edu':
                                if content_type_outgoing.startswith('text/html') or content_type_outgoing.startswith('application/pdf'):
                                    newstr = newurl[-1:]
                                    if newstr in ['#']:
                                        newurl = newurl[:-1]
                                    fo.write(newurl+' ')
                                    getnewurl.append(newurl)
                                    crawlurl.append(newurl)
                                    result_urls.append(newurl)

                getnewurl = []

                fo.write('\n')
                line +=1

        except:
            pass
        fo.close()

        crawlurl.append(url)

    return result_urls

Crawler(root_url,11)





