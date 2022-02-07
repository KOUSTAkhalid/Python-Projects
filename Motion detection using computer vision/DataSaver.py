import threading
import csv
import os

lock = threading.Lock()

def save_to_file(id, center, dimension, time):
    lock.acquire()
    print("ID : " + str(id) + ", (x,y) : " + str(center) + ", (largeur,hauteur): " + str(dimension) + ", temps : " + str(time))
    
    path_n_file = "localisation.txt"
   
    if not os.path.isfile(path_n_file):
            with open(path_n_file, 'a', newline='') as tabFile:
                 fw = csv.writer(tabFile, dialect='excel-tab')
                 fw.writerow(["ID", "(x,y)", "        (larg,haut)", " temps(ms)"])

    with open(path_n_file, 'a', newline='') as tabFile:
        fw = csv.writer(tabFile, delimiter="\t", dialect='excel-tab')
        fw.writerow([id, center, dimension, time])
        
    lock.release()

