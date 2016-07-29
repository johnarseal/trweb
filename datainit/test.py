# some script used to catch exit signal

import time  
import signal
import sys

def term_sig_handler(signum, frame):  
    print 'catched singal: %d' % signum  
    sys.exit()  
    

print "asd"

# catch term signal  
signal.signal(signal.SIGTERM, term_sig_handler)  
signal.signal(signal.SIGINT, term_sig_handler)  
while True:  
    print 'hello'  
    time.sleep(3)  