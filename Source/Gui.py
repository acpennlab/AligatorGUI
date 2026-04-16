from PyQt5 import sip
import sys
import os
import time
import aligator.rcj_IO as iou
import aligator.relaxes as re
import aligator.mechanisms
import aligator.aligator
import pprint
import re

import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QFileDialog
from PyQt5 import QtCore, uic



qtCreatorFile = ".\Aligator_Gui.ui" #Path for ui file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
            
class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.current_directory.setText(os.getcwd())        
        self.exit_button.clicked.connect(self.close)
        self.choose_directory_button.clicked.connect(self.save_dir)
        self.execute_button.clicked.connect(self.execute)
        self.pulse_delay_spinner.valueChanged.connect(self.calc_freq)
        self.pulse_freq_spinner.valueChanged.connect(self.calc_delay)
        self.about_button.clicked.connect(self.about)

    def close(self): #Exit button
        sys.exit()
           
    def save_dir(self): # Dialog to set save directory
        cd=QFileDialog.getExistingDirectory(self, 'Set Save Directory')
        if cd != '':
            self.current_directory.setText(cd)

    def calc_freq(self): # Changes Freq/Delay spinner depending on user input
        self.pulse_freq_spinner.blockSignals(True)
        self.pulse_freq_spinner.setValue(1000/self.pulse_delay_spinner.value())
        self.pulse_freq_spinner.blockSignals(False)
        
    def calc_delay(self): # Changes Freq/Delay spinner depending on user input
        self.pulse_delay_spinner.blockSignals(True)
        self.pulse_delay_spinner.setValue(1000/self.pulse_freq_spinner.value())
        self.pulse_delay_spinner.blockSignals(False)

    def about(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Agligator: Analysis of Ligand Gating: trains and other relaxations\nDeveloped by Andrew Plested of FMP Berlin to model glutamate receptor gating (Carbone and Plested, 2012),(Carbone and Plested, 2016)\nhttps://doi.org/10.1016/j.neuron.2012.04.020\nhttps://doi.org/10.1038/ncomms10178\nPackaged and simplified by Samuel Liu and Andrew Penn of Sussex University")
        self.msg.setStyleSheet("messagebox-text-interaction-flags: 5;")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        self.msg.exec_()      
   
        
        
        
    def execute(self): # run aligator if protocol set right
            olddir = os.getcwd()
            if self.pulse_freq_spinner.value() == 0 or self.pulse_delay_spinner.value() == 0 or self.pulse_width_spinner.value() >= self.pulse_delay_spinner.value() :
                self.msg = QMessageBox()
                self.msg.setIcon(QMessageBox.Warning)
                self.msg.setText("Check parameters in Protocol Box\n\nThe width of pulse must be less than the time between pulses\nThe time between pulses/frequency of pulses must be non-zero")
                self.msg.setStandardButtons(QMessageBox.Ok)
                self.msg.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
                self.msg.exec_()      
            else:
                fname = "tempmech"
                fpath = os.path.normpath(os.path.join(olddir, fname + ".py"))
                fpathc = os.path.normpath(os.path.join(olddir, fname + ".pyc"))
                f = open(fpath,'w+')
                f.write("def mech_definition():\n    rd = {\n    (5, 0) : ['beta',      [ " + str(self.beta_spinner.value()) + ", 0]] ,\n    (0, 5) : ['alpha',     [ "+ str(self.alpha_spinner.value()) +", 0]] ,\n    (3, 2) : ['d2_plus',   [  " + str(self.d2plus_spinner.value()) + ", 0]] ,\n    (2, 3) : ['d2_min',    [   " + str(self.d2minus_spinner.value()) + ", 0]] ,\n    (1, 4) : ['d0_plus',   [    " + str(self.d0plus_spinner.value()) + ", 0]] ,\n    (4, 1) : ['d0_min',    [    " + str(self.d0minus_spinner.value()) + ", 0]] ,\n    (5, 3) : ['d1_plus',   [  " + str(self.d1plus_spinner.value()) + ", 0]] ,\n    (3, 5) : ['d1_min',    [  " + str(self.d1minus_spinner.value()) + ", 0]] ,\n    (0, 2) : ['d2op_plus', [  " + str(self.d2starplus_spinner.value()) + ", 0]] ,\n    (2, 0) : ['d2op_min',  [   " + str(self.d2starminus_spinner.value()) + ", 0]] ,\n    (4, 3) : ['kd_plus',   [  " + str(self.kplus_spinner.value()) + ", 1]] ,\n    (3, 4) : ['kd_min',    [ " + str(self.kdminus_spinner.value()) + ", 0]] ,\n    (1, 5) : ['k_plus',    [  " + str(self.kplus_spinner.value()) + ", 1]] ,\n    (5, 1) : ['k_min',     [" + str(self.kminus_spinner.value()) + ", 0]] ,\n    }\n\n    N_states = 6 # state this rather than obtain automatically.\n\n    #states and their conductances\n    open_states = {0:.4}\n\n    return rd, N_states, open_states")
                f.close()
                save_directory = self.current_directory.text()

                mod = "_"
                file_list, wd = iou.getpath(True, save_directory)
                #generate time string (unique to the second) and make a new folder with that
                #timestamp, so we can work in any directory without fear of overwriting 
                #anything
                
                timestr = time.strftime("%y%m%d-%H%M%S")   
                iou.make_folder(timestr + mod, wd)

                Log = aligator.aligator.Logger(timestr+'_log.txt')        #create logfile
                aligator.aligator.announce()                              #announce program version
                
                #define experiments to be done here
                mech_list=['tempmech']
                expt_list=['train']
                rate=["d2_min"]         #Useless for one train like it is here
                power = [0] #Has to be 0 for 1 train, else chooses how much rate is varied in experiment
                range = 0 #Has to be 0 for 1 train
                npulse = self.pulsen_spinner.value()
                pulsewidth = self.pulse_width_spinner.value()
                pulsefreq = self.pulse_freq_spinner.value()
                          
                aligator.aligator.package(expt_list, mech_list, rate, power, range, 1, npulse, pulsewidth , pulsefreq)

                
                del Log

                #write out mechanisms

                f = open(timestr+'_mechs.txt', "w")
                for m in mech_list:
                    r, n, o = aligator.mechanisms.mechanism(m)
                    
                    f.write("rate mechanism " + str(m) + "\n")
                    f.write(pprint.pformat(r)) 
                    f.write("\n**********\n")
                    f.write("\nOpen states " + str(o))
                    f.write("\n**********\n\n\n")
                f.close() 
                
                ######## plots graph ##############
                prot = expt_list[0]
                
                
                #extracts data 
                fname = prot+"_mtempmech_linear.txt"
                newdir = os.getcwd()
                fpath = os.path.normpath(os.path.join(newdir, fname))
                f = open(fpath,'r')

                lines=f.readlines()

                line0 = lines[0].rstrip()

                f.close()

                nums = re.findall("\d+\.\d+", line0)

                #time axis
                timeaxis = []
                for x in lines:
                    timeaxis.append(x.split()[-2])

                del timeaxis[0]

                timeaxis = [float(i) for i in timeaxis]
                
                plt.figure()

                #current axis
                for index, num in enumerate(nums):
                    result=[]
                    for x in lines:
                        result.append(x.split()[index])
                    del result[0]
                    result = [float(i) for i in result]
                    plt.plot(timeaxis,result)
                
                #glutamate data
                glu = []
                for x in lines:
                    glu.append(x.split()[-1])

                del glu[0]
                glu = [float(i) for i in glu]
                glu = [i-1.015 for i in glu] 
                
                #labels and legend
                leg = []
                for x, num2 in enumerate(nums):
                    leg.append('Trial '+ str(x+1))

                leg.append('Glu')
                
                plt.plot(timeaxis,glu)

                plt.legend(leg)

                plt.title("Aligator Output")
                plt.xlabel("Time (s)")
                plt.ylabel("Response (au)")
                xlim2 = (100+(self.pulsen_spinner.value())*self.pulse_delay_spinner.value())/1000
                xlim1 = max(0.1-(self.pulse_width_spinner.value()*3)/1000,0.1-(self.pulse_delay_spinner.value()*0.5)/1000,0.09)
                plt.xlim(left=xlim1,right=xlim2)
                
                plt.savefig('output')
                plt.savefig('output.svg')
                plt.savefig('output.eps')
                os.chdir(olddir) 
                plt.show()

if __name__ == "__main__":
    app = QApplication.instance() # sets up QApplication if there isnt one already
    if not app:
        app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())	