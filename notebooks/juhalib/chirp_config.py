#
# a list of chirp "carousels". each element in list is executed in a separate thread.
# if each thread has more than one chirp sounder, the soundings are done in a round-robin fashion
# cylcing through each one.
#
# rmin and rmax effect plotting only (and can be changed after the fact).
# edit them so that the distance between you and the transmitter fits within
# rmin and rmax.
#
#sounders = [[{'rep':600,'chirpt':594,'name':'sod','rate':0.5e6+8.5,'dur':35, 'cf':12.5e6,'rmin':0,'rmax':3000.0,'fmin':0.0,'fmax':16.0}]]
#sounders = [[{'rep':60,'chirpt':594,'name':'cyprus1','rate':0.5e6+8.5,'dur':35, 'cf':12.5e6,'rmin':0,'rmax':1500.0,'fmin':0.0,'fmax':16.0}]]

sounders = [[{
'rep':300,'chirpt':0.00855263136327267,'name':'dmixed','rate':100166.14948319287,'dur':0.5, 'cf':12.5e6, 'rmin':7500, 'rmax':17500, 'fmin':0, 'fmax':16.0#,
#'rep':300,'chirpt':235,'name':'cyprus1','rate':0.1e6,'dur':250, 'cf':12.5e6, 'rmin':7500, 'rmax':17500, 'fmin':0, 'fmax':16.0#,
# 'rep':300,'chirpt':235,'name':'sounder','rate':50.e6,'dur':10.0629, 'cf':25.0e6, 'rmin':7500, 'rmax':17500, 'fmin':0, 'fmax':50.0
}]]

#data_dir = "/data/chirp0/"

#sample_rate = 25e6
sample_rate = 50e6
#sample_rate = 20e6
#dec = 625
dec = 500
if_rate = sample_rate/dec
whiten = False
whiten_len = 8192
whiten_n = 30000

def get_all_sounders():
    sounder_list = []
    for sounder_thread in sounders:
        for sounder in sounder_thread:
            sounder_list.append(sounder)
    return(sounder_list)
