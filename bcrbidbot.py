#!/usr/bin/python

import sys, urllib2, time, datetime, subprocess, os, thread, pexpect
from PyQt4 import QtGui, QtCore
from threading import Timer
from datetime import datetime as dt



####################################################################################################
# thread class
####################################################################################################

class GenericThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
 
    def __del__(self):
        self.wait()
 
    def run(self):
        self.function(*self.args,**self.kwargs)
        return

####################################################################################################
# main window class
####################################################################################################

class CC(QtGui.QWidget):
    
    def __init__(self, parent=None):
        super(CC, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        global t1, tcbval, estval, cmvval, until, c2, c4, t2, b1, ed 
        global b3, e, c3b, status, cmvval, edv, f, s3, schedbit
        
        schedbit = '0'
	
        logo = QtGui.QLabel(self)
        logo.move(5, 5)
        logo.setFixedWidth(215)
        logo.setFixedHeight(71)
        logo.setObjectName('logo')

        t = QtGui.QLabel('Current time: ', self)
        t.move (20, 90)
        t.setFixedWidth(180)
        t.setObjectName('t')
	
        t2 = QtGui.QLabel('...', self)
        t2.move (210, 90)
        t2.setFixedWidth(200)

        cbp = QtGui.QLabel('Bidding time left: ', self)
        cbp.setFixedWidth(180)
        cbp.move(20, 110)
        cbp.setObjectName('cbp')

        t1 = QtGui.QLabel('Calculating...', self)
        t1.setFixedWidth(150)
        t1.move(210, 110)
        t1.setObjectName('t1')

        tcb = QtGui.QLabel('Total Current Bids (BTC): ', self)
        tcb.setFixedWidth(180)
        tcb.move(20, 130)
        tcb.setObjectName('tcb')

        tcbval = QtGui.QLabel('Fetching... ', self)
        tcbval.setFixedWidth(180)
        tcbval.move(210, 130)

        est = QtGui.QLabel('Estimated BCR Rate: ', self)
        est.setFixedWidth(180)
        est.move(20, 150)
        est.setObjectName('est')

        estval = QtGui.QLabel('Fetching... ', self)
        estval.setFixedWidth(180)
        estval.move(210, 150)

        cmv = QtGui.QLabel('Current Market Price: ', self)
        cmv.setFixedWidth(180)
        cmv.move(20, 170)
        cmv.setObjectName('cmv')

        cmvval = QtGui.QLabel('fetching... ', self)
        cmvval.setFixedWidth(180)
        cmvval.move(210, 170)

        c1 = QtGui.QLabel('Given existing bids, ', self)
        c1.setFixedWidth(180)
        c1.move(20, 210)
        c1.setObjectName('c1')

        c1a = QtGui.QLabel('a bid of (BTC) ', self)
        c1a.setFixedWidth(180)
        c1a.move(20, 230)
        c1a.setObjectName('c1')

        c2 = QtGui.QLineEdit(self)
        c2.setFixedWidth(80)
        c2.move(210, 228)
        c2.setText('0.0053')
        c2.setToolTip('Press ENTER to calculate')
        c2.setObjectName('c2')
        c2.returnPressed.connect(self.calc)

        c3 = QtGui.QLabel('would win appx: ', self)
        c3.setFixedWidth(180)
        c3.move(20, 250)
        c3.setObjectName('c3')

        c4 = QtGui.QLabel('...', self)
        c4.setFixedWidth(180)
        c4.move(210, 250)

        c3a = QtGui.QLabel('@ ', self)
        c3a.setFixedWidth(180)
        c3a.move(20, 270)
        c3a.setObjectName('c3')

        c3b = QtGui.QLabel('... ', self)
        c3b.setFixedWidth(180)
        c3b.move(210, 270)
        c3b.setObjectName('c3b')

        b1 = QtGui.QRadioButton('Make one-time bid as per calc above ', self)
        b1.setChecked(False)
        b1.move(20, 300)
        b1.setObjectName('b1')

        b3 = QtGui.QRadioButton('Bid fixed amount every day: ', self)
        b3.setChecked(False)
        b3.move(20, 340)
        b3.setObjectName('b3')

        ed = QtGui.QLabel('Amount (BTC): ', self)
        ed.setFixedWidth(180)
        ed.move(20, 370)
        ed.setObjectName('ed')
        
        edv = QtGui.QLineEdit(self)
        edv.setFixedWidth(80)
        edv.move(210, 368)
        edv.setText('0.0053')
        edv.setObjectName('edv')

        ed2 = QtGui.QLabel('@Time (GMT hh:mm:ss): ', self)
        ed2.setFixedWidth(180)
        ed2.move(20, 390)
        ed2.setObjectName('ed2')

        f = QtGui.QLineEdit('00:00:30', self)
        f.setFixedWidth(80)
        f.move(210, 390)	

        a = QtGui.QLabel('Electrum password:', self)
        a.setFixedWidth(180)
        a.move(20, 425)

        e = QtGui.QLineEdit(self)
        e.setFixedWidth(350)
        e.move(20, 445)
        e.setEchoMode(QtGui.QLineEdit.Password)
        e.setText('')
        e.setObjectName('edv')

        bid = QtGui.QPushButton('Bid!', self)
        bid.move(20, 475)
        bid.setFixedWidth(100)
        bid.setToolTip('Make one-time bid or schedule every-day bid')
        bid.setObjectName('bid')
        bid.clicked.connect(self.callbidthread)

        status = QtGui.QLabel('Status: Idle', self)
        status.setFixedWidth(400)
        status.move(0, 520)
        status.setObjectName('status')       

        ####################################################################################################
	# main window shiznit
	####################################################################################################

        self.setGeometry(100, 100, 400, 540)
        self.setFixedSize(400, 540)
        self.setWindowTitle('Bitcredit Bidbot')
        self.setWindowIcon(QtGui.QIcon('bcr.ico'))
        
        # stylesheet
        self.setStyleSheet("""
        QWidget {background: white;}
        QLabel#t {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#cbp {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#tcb {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#est {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#cmv {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#c1 {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#c3 {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#ed {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#ed2 {background: grey; color: white; qproperty-alignment: AlignRight;}
        QLabel#status {background: grey; color: white; qproperty-alignment: AlignCenter;}
        QLineEdit {border: 1px solid #ffa405;}
        QPushButton#bid {border: 2px solid #2597ef; font-weight: bold;}
        QLabel#logo {background-image: url('logo.png');}
        """) 


        # background image
        #palette = QPalette()
        #palette.setBrush(QPalette.Background,QBrush(QPixmap("rh333.png")))
        #self.setPalette(palette)
      
        self.show()

        # start event monitor thread
        self.genericThread = GenericThread(self.events)
        self.genericThread.start()

    #################################################################################################### 
    # in-class functions
    ####################################################################################################

    # get current bid period
    def getcbp(self):
        global t1, until
        startdate = 1450396800
        current = int(time.time())
        diff = current - startdate
        until = 86400 - (diff % 86400)
        untilh = str(datetime.timedelta(seconds=until))
        t1.setText(untilh)

    # get current bids
    def getcurrentbids(self):
        global tcbval, estval
        try:
    	    site = 'https://blockchain.info/q/addressbalance/1BCRbid2i3wbgqrKtgLGem6ZchcfYbnhNu'
    	    req = urllib2.Request(site)
    	    page = urllib2.urlopen(req)
    	    data = page.read()
    	    scaledup = float(data)/100000000
    	    tcbval.setText(str(scaledup))
    	    rate = scaledup/18000
    	    estval.setText(str('%.08f' % rate))
        except:
    	    tcbval.setText('blockchain.info slow or down!')

    # get curent market price		
    def getcmp(self):
        try:
    	    global cmvval
    	    site = 'https://bittrex.com/api/v1.1/public/getticker?market=BTC-BCR'
    	    req = urllib2.Request(site)
    	    page = urllib2.urlopen(req)
    	    data = page.read()
    	    last =  data[-12:]
    	    last2= last[:-2]
    	    cmvval.setText(str(last2))
        except:
    	    cmvval.setText('Bittrex slow or down!')

    # calc how much BCR we'll get    		
    def calc(self):
        global until, tcbval, c2, c4, c3b, cmvval
        try:
    	    podl = float(until)/86400
    	    newtotal = float(tcbval.text()) + float(c2.text())
    	    mybcr = (float(c2.text()) / newtotal) * 18000 * podl
    	    cost = float(c2.text()) / mybcr      
     	    c4.setText(str('%.08f' % mybcr) + ' BCR')
     	    c3b.setText(str('%.08f' % cost))
        except:
    	    c4.setText('awaiting data refresh...')


    # bid according to user choices
    def onetimebid(self):
        global b1, b3, c2, e, status, edv, f
        try:
            # create tx
            cmd = 'electrum payto 1BCRbid2i3wbgqrKtgLGem6ZchcfYbnhNu ' + str(edv.text())
            status.setText('Status: Creating transaction...')
            QtGui.qApp.processEvents()
            print 'running: ' + cmd
            #p = subprocess.check_output(cmd)
            p = pexpect.spawn(cmd)
            i = p.expect('Password:')
            p.sendline(str(e.text()))
            i = p.expect(pexpect.EOF)
            q = p.before
            print q
            # extract hex
            linez = (line.strip() for line in q.splitlines())
            for line in linez:
                if 'hex' in line:
                    line = line[8:-1]
                    #print 'hex: ' + line
                    # broadcast tx
                    cmd = 'electrum broadcast ' + line
                    status.setText('Status: Broadcasting tx...')
                    QtGui.qApp.processEvents()
                    print 'running: ' + cmd
                    p = subprocess.check_output(cmd, shell=True)
                    status.setText('Status: Bid made!')
                    QtGui.qApp.processEvents()
        except Exception, error:
            status.setText('Status: ' + str(error))
            return

    def gets3(self):
        global f, t1, s3
        hhmmss1 = f.text() # time after gmt
        # convert to seconds
        hours = hhmmss1.split(':')[0]
        mins = hhmmss1.split(':')[1]
        secs = hhmmss1.split(':')[2]
        s1 = int(hours)*3600 + int(mins)*60 + int(secs) # secs after gmt
        hhmmss2 = t1.text() # time to gmt
        # convert to seconds
        hours2 = hhmmss2.split(':')[0]
        mins2 = hhmmss2.split(':')[1]
        secs2 = hhmmss2.split(':')[2]
        s2 = int(hours2)*3600 + int(mins2)*60 + int(secs2) # secs until gmt
        # total secs until bid
        s3 = s1 + s2 
        return s3

    def scheduledbid(self):
        global status, c2
        try:
            # create tx
            cmd = 'electrum payto 1BCRbid2i3wbgqrKtgLGem6ZchcfYbnhNu ' + str(c2.text())
            status.setText('Status: Creating transaction...')
            QtGui.qApp.processEvents()
            print 'running: ' + cmd
            #p = subprocess.check_output(cmd)
            p = pexpect.spawn(cmd)
            i = p.expect('Password:')
            p.sendline(str(e.text()))
            i = p.expect(pexpect.EOF)
            q = p.before
            print q
            # extract hex
            linez = (line.strip() for line in q.splitlines())
            for line in linez:
                if 'hex' in line:
                    line = line[8:-1]
                    #print 'hex: ' + line
                    # broadcast tx
                    cmd = 'electrum broadcast ' + line
                    status.setText('Status: Broadcasting tx...')
                    QtGui.qApp.processEvents()
                    print 'running: ' + cmd
                    p = subprocess.check_output(cmd, shell=True)
                    status.setText('Status: Bid made!')
                    QtGui.qApp.processEvents()
                    self.callbidthread()
        except Exception, error:
            status.setText('Status: ' + str(error))
            return

    def callbidthread(self):
        global b1, b3, status, s3, schedbit
        if b1.isChecked():
            #self.genericThread2 = GenericThread(self.onetimebid)
            #self.genericThread2.start()
            self.onetimebid()
        elif b3.isChecked():
	    # get secs delay then launch scheduled bid via timer
            s3 = self.gets3()
            t = Timer(s3, self.scheduledbid)
            t.start()
            # update status, set schedbit so events func. updates status regularly
            a = datetime.timedelta(seconds=int(s3))
            status.setText('Status: Bid scheduled!')
            schedbit = '1'

        
    # do this stuff every 10 secs
    def events(self):   
        global t2, status, s3, schedbit
        while 1:
            now = time.strftime("%T")
            t2.setText(now)
            self.getcbp()
            self.getcurrentbids()
            self.getcmp()
            self.calc()
            if schedbit == '1':
	        s3 = self.gets3()
                a = datetime.timedelta(seconds=int(s3))
                status.setText('Status: Bid scheduled, executing in: ' + str(a))
            time.sleep(10)
     	

# shindig
def main():
    app = QtGui.QApplication(sys.argv)
    ex = CC()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
