#!/usr/bin/env python3


#### terminal table library ####
import curses

class tt:
    def __init__(s,master,winname, winHnum = 2) :
        s.master = master
        s.winname = winname
        s.reinit(winHnum)
    def reinit(s, winHnum = 2) :
        winVnum = int((len(s.winname)+1)/winHnum)
        s.wins = []
        #
        size = s.master.getmaxyx()
        s.size=size
        i=-1
        wHeight = int((size[0]-1)/winVnum)
        for h in range(winVnum):
            wWidth = int(size[1]/winHnum)
            for v in range(winHnum):
                i=i+1
                if i >= len(s.winname) :
                    break
                wb = s.master.derwin(wHeight+1,wWidth,wHeight*h,wWidth*v)
                wb.box()
                w = wb.derwin(wHeight-1,wWidth-2,1,1)
                s.wins.append(w)
                wb.move(0,1)
                wb.addstr(s.winname[i])
                w.scrollok(1)
                w.noutrefresh()
                wb.noutrefresh()
        #s.master.noutrefresh()
    def input(s, i, t) :
        w = s.wins[i]
        w.addstr(t)
        w.noutrefresh()
    def display(s, c) :
        s.master.move(s.size[0]-1,0)
        s.master.clrtoeol()
        s.master.addstr(c)
    def update(s) :
        curses.doupdate()
    def __del__(s) :
        s.clear()
    def clear(s):
        s.master.clear()
        s.master.refresh()


#### tail f library ####
import os

class tailf:
    def __init__(s,path):
        s.path = path
        s.f = open(path)
    def tailf(s) :
        return s.f.read()

class logstailf :
    def __init__(s,dirpathes) :
        s.tf = []
        s.names = []
        for dirpath in dirpathes :
            for f in os.listdir(dirpath) :
                name = f
                p = dirpath + '/' + f
                s.names.append(name)
                s.tf.append(tailf(p))
    def tailf(s, cb) :
        for n,tf in enumerate(s.tf) :
            t = tf.tailf()
            if t :
                cb(n,t)

####      ####
def main(master, log):
    try:
        t = tt(master, log.names)
        c = ''
        while 1 :
            log.tailf(t.input)
            t.display(c)
            t.update()
            #
            master.timeout(500)
            c = master.getch()
            if c in [curses.KEY_RESIZE]:
                t.clear()
                t.reinit()
            elif c in [113]: # 'q'
                return 0
            elif c in [114]: # 'r'
                return 1
            if c < 0 :
                c=""
            else:
                c=curses.keyname(c)
    except KeyboardInterrupt :
        print("KeyboardInterrupt")
        return 0
    #except curses.error as e:
    #    #pass
    #    c = 'curses.error=' + str(e)
    except Exception as e :
        return e


#### Main ####
import sys

dirpathes = []
i = iter(sys.argv)
next(i)
while 1 :
    try :
        a = next(i)
    except StopIteration:
        break
    if a[0] == '-' :
        pass
    else :
        dirpathes.append(a)

r=1
while r:
    log = logstailf(dirpathes)
    if len(log.names) == 0 :
        print("No files.")
        break
    r = curses.wrapper(main, log)
    if r is Exception :
        raise(r)
    print(r)

