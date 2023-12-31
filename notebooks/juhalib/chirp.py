#!/usr/bin/python
#
# single channel chirp receiver.
#
from gnuradio import gr, gru, uhd
import time, math, os
import juha
from time import strftime, gmtime
import datetime
import calendar
import signal, errno
import sys
import subprocess
from optparse import OptionParser

import chirp_config

#use_gpsdo = False
use_gpsdo = True
running = True

class sounders:
    def __init__(self):
        # What sounders are we interested in. The list contains one list of dictionaries for each
        # parallel receiver. Currently only three receivers. Scheduling is done in a round-robin fashion.
        # Each chirp in the thread list gets received sequentially.
        # If only one chirp sounder in list, it is received constantly.
        #
        #
        # todo: estimate spectrum on the fly, and whiten the noise.
        #
        self.sounders = chirp_config.sounders

        self.idx = []
        for i in range(0,len(self.sounders)):
            self.idx.append(0)

    def nsounders(self):
        return(len(self.sounders))

    def nextsounder(self,n):
        self.idx[n] = self.idx[n]+1
        return(self.sounders[n][self.idx[n]%len(self.sounders[n])])

    def findNext(self,n):
        ss = self.sounders[n]
        tnow = time.time()
        mint = tnow+1e6
        bests = ss[0]
        for s in ss:
            tt = determineNext(s['rep'],s['chirpt'])
            if tt-tnow < mint:
                mint = tt-tnow
                bests = s
        return(bests)


def determineNext(rep,chirptime):
    # calculate midnight in unix time
    tnow = time.gmtime()
    tmidnight = calendar.timegm((tnow[0],tnow[1],tnow[2],0,0,0,tnow[6],tnow[7],tnow[8]))

    # calculate the next repetition time.
    nrep = math.floor(60*60*24/rep)
    t0 = tmidnight+chirptime
    n = 0
    tnow = time.time()
    while t0 - tnow < 3:
        t0 = t0 + rep
    return(t0)

class chirprec(gr.top_block):
    def __init__(self,sr,n,op):
        gr.top_block.__init__(self, "chirprec")


        #self.u = uhd.usrp_source(device_addr="addr=%s,recv_buff_size=1000e6"%(op.usrp_ip),
        self.u = uhd.usrp_source(device_addr="serial=%s,recv_buff_size=1000e6"%(op.usrp_ip),
                                 io_type=uhd.io_type.COMPLEX_FLOAT32,
                                 num_channels=1)

        self.u.set_subdev_spec("A:A", 0)

        r = gr.enable_realtime_scheduling()
        self.u.set_center_freq(sr/2.0)
        self.u.set_samp_rate(sr)
        self.u.set_gain(20)


        if use_gpsdo:
            print "Using internal GPSDO"
            #self.u.set_clock_source("gpsdo")
            u = self.u
#            print u.get_mboard_sensor("gps_gpgga")
#            print u.get_mboard_sensor("gps_gprmc")
#            print u.get_mboard_sensor("gps_time")
#            print u.get_mboard_sensor("gps_locked")
#            print u.get_mboard_sensor("gps_servo")
#            print u.get_mboard_sensor("ref_locked")
#            print u.get_mboard_sensor("mimo_locked")
#            print u.get_time_last_pps().get_real_secs()
        else:
            # try external PPS and 10 MHz time sync
#            self.u.set_clock_source("external")
            self.u.set_clock_source("external")
            self.u.set_time_source("external")

            os.system("ntpdate -b ntp.hut.fi")
            # wait until time 0.2 to 0.5 past full second, then latch.
            # we have to trust NTP to be 0.2 s accurate.
            tt = time.time()
            while tt-math.floor(tt) < 0.3 or tt-math.floor(tt) > 0.5:
                tt = time.time()
                time.sleep(0.01)
            print "Latching at ",tt
            self.u.set_time_unknown_pps(uhd.time_spec(math.ceil(tt)+1.0))
            self.u.set_start_time(uhd.time_spec(math.ceil(tt)+2.0))

        self.n = n
        self.sr=sr
        self.cr = []

        if chirp_config.whiten == True:
            print "Whitening noise"
            self.whiten=juha.whiten(chirp_config.whiten_len,chirp_config.whiten_n)
            self.whiten.set_processor_affinity([4])
            self.connect(self.u, self.whiten)

        for i in range(0,n):
            cdc = juha.chirp_downconvert()
            cdc.set_samp_rate(sr)
            cdc.set_chirp_par(-sr/2.0, 0.5e6+8.5)
            cdc.set_dec(chirp_config.dec)
            self.cr.append(cdc)
            if chirp_config.whiten == True:
                self.connect(self.whiten, cdc)
            else:
                self.connect(self.u, cdc)

    def set_center_freq(self,cf):
        self.u.set_center_freq(cf)
        for i in range(0,self.n):
            self.cr[i].set_f0(-cf)

    # reset timing
    def set_chirp_par(self,n,t0,dur,rate,name):
        self.cr[n].set_chirp_par(-self.sr/2, rate)
        fname = "%s-%10d.out"%(name,int(t0))
        self.cr[n].set_fname(fname)
        self.cr[n].set_timing(t0, dur)
        return(fname)

    # reset timing
    def is_done(self,n):
        return(self.cr[n].is_done())

    # reset timing
    def noverruns(self):
        return(0)

    def get_lag(self):
        return(self.cr[0].get_lag())


def time_stamp():
   a=time.time()
   b=time.strftime("%Y.%m.%d_%H.%M.%S",time.strptime(time.ctime(a)))
   stmp="%s.%09d" % (b,int((a-math.floor(a))*1000000000))
   return(stmp)

def dir_time_stamp():
   a=time.time()
   b=time.strftime("%Y.%m.%d",time.strptime(time.ctime(a)))
   return(b)

class logger:
    def __init__(self,directory):
        self.fd = open(os.path.join(directory,"chirp.log"),"a")
        self.fd2 = open(os.path.join(directory,"analyzed.log"),"a")

    def stop(self):
        self.fd.flush()
        self.fd.close()
        self.fd2.flush()
        self.fd2.close()

    def log(self,msg):
        self.fd.write("%s %s\n" % (time_stamp(),msg))
        self.fd.flush()

    def log_done(self,fname):
        self.fd2.write("%s %s\n" % (time_stamp(),fname))
        self.fd2.flush()

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def change_to_day_dir(data_dir):
    os.chdir(data_dir)
    dname = dir_time_stamp()
    mkdir_p(dname)
    os.chdir(dname)
#    print "Created directory %s\n" % dname

if __name__ == "__main__":

    print 'Press Ctrl-C to stop'

    parser = OptionParser()
    parser.add_option("-o", "--outputdir", dest="outputdir", type="string", default="./datatmp",
                      help="Directory. (default %default)")
    parser.add_option("-m", "--usrp_ip", dest="usrp_ip", type="string", default="192.168.50.2",
                      help="USRP IP. (default %default)")

    (op, args) = parser.parse_args()

    data_dir=op.outputdir
    try:
        os.makedirs(data_dir)
    except:
        pass

    change_to_day_dir(data_dir)

    s = sounders()

    sr = chirp_config.sample_rate
    cr = chirprec(sr,s.nsounders(),op)
    cr.start()
    time.sleep(5)

    log = logger(op.outputdir)
    log.log("Starting")

    while running:
        for si in range(0,s.nsounders()):
            if cr.is_done(si):
                chirp = s.nextsounder(si)
                tnext = determineNext(chirp['rep'],chirp['chirpt'])
                fname = cr.set_chirp_par(si,tnext,chirp['dur'],chirp['rate'],chirp['name'])
                cr.set_center_freq(chirp['cf'])
                overruns = cr.noverruns()
                print "%s Thread %d, Next chirp %s, At %s %d:%1.3f %d %1.1f"%(fname, si, chirp['name'],strftime("%a, %d, %b, %Y, %H:%M:%S",time.gmtime(tnext)),chirp['rep'],chirp['chirpt'],overruns,cr.get_lag())
                log.log("%s Thread %d, Next chirp %s %s %d:%1.3f %d %1.1f"%(fname, si,chirp['name'],strftime("%a, %d, %b, %Y, %H:%M:%S",time.gmtime(tnext)),chirp['rep'],chirp['chirpt'],overruns,cr.get_lag()))

        time.sleep(1.0)
        change_to_day_dir(data_dir)

    print "Stopping..."
    cr.stop()
    cr.wait()


