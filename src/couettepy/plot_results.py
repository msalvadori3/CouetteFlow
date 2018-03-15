import os
import sys
import glob
import numpy as np
from inputfile import *
import matplotlib.pyplot as plt
from matplotlib import rcParams
from math import atan2,degrees
from utilities import read_path
import matplotlib.ticker as ticker
from matplotlib import cm
from matplotlib import pylab
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.ticker import LinearLocator, FormatStrFormatter
rcParams.update({'figure.autolayout': True})

class plot_results(object):

    def get_plot_properties_single(self,inputfile,args):
        """ In this routine we set some properties
            for the single plot
        """
        # plot properties from the input file
        self.fnames = inputfile.plot_names
        self.style  = inputfile.style
        self.label  = inputfile.label

        # setup properties from input file

        self.time_step = inputfile.dt
        self.scheme = inputfile.theta

        # plot properties from user input
        if 'title' in args:
            self.title = args['title']
        else:
            self.title = ['example']
        if 'xlabel' in args:
            self.xlabel = args['xlabel']
        else:
            self.xlabel = []
        if 'ylabel' in args:
            self.ylabel = args['ylabel']
        else:
            self.ylabel = []
        if 'legend' in args:
            self.legend = args['legend']
            if 'legend_frame' in args:
                self.legend_frame = args['legend_frame'][0]
            else:
                self.legend_frame = False
            if 'legend_loc' in args:
                self.legend_loc = args['legend_loc'][0]
            else:
                self.legend_loc = 'upper right'
        else:
            self.legend = False
        if 'grid' in args:
            self.grid = args['grid']
        else:
            self.grid = 'False'
        if 'log' in args:
            self.log = args['log']
            if 'log_x' in args:
                self.log_x = args['log_x'][0]
            else:
                self.log_x = False
            if 'log_y' in args:
                self.log_y = args['log_y'][0]
            else:
                self.log_y = False
        else:
            self.log = False
        if 'variables' in args:
            if int(len(args['variables'][0].split(' '))) > 2:
                print 'Error: the variables position has to be'
                print 'in the format "{\'variables\':[\'<num1> <num2>\']}"'
                print 'where \'<num1>\' and \'<num2>\' must be integers. Got: ',args['variables']
                sys.exit()
            elif int(len(args['variables'][0].split(' '))) == 2: 
                x_t = args['variables'][0].split(' ')
                for i in range(0,2):
                    if int(x_t[i] < 0):
                        print 'Error. The option entries in the \'variables\' item must be non-negative integers. Got: ', args['variables']
                        sys.exit()
                    else:
                        self.variables = []
                        for i in range(0,len(x_t)):
                            self.variables.append(int(x_t[i]))
        else:
            # if no inputs are provided, by default we assign x = 1 and y = 2 as positions for the variables to be plot
            self.variables = [1,2]

    def __init__(self, name, args, outdir="./output"):

        # read from input file
        inputfile = read_input_file('input_file.xml')

        # set plot options
        params1 = {
           'legend.fontsize': inputfile.legsize,
           'figure.figsize':  inputfile.figsize,
           'axes.labelsize':  inputfile.axislsize,
           'axes.titlesize':  inputfile.axistsize,
           'xtick.labelsize': inputfile.xticks,
           'ytick.labelsize': inputfile.yticks,
           }

        pylab.rcParams.update(params1)

        if name == 'multi_plot':

            # get plot properties

            self.get_plot_properties_single(inputfile,args)

            # make pre-made plot

            self.plot_main(inputfile,name,args)

        elif name == 'single_plot':

            if args['name'] == 'options':
                # read the parsed keywords and continue

                # get some plot properties
                self.get_plot_properties_single(inputfile,args)

                # make plot
                self.plot_main(inputfile,name,args)
            else:
                # tell user how to specify the inputs
                print 'Error: wrong argument \'name\' parsed:'
                print 'args[\'name\'] = ',args['name']
                print 'The correct syntax for this utility is:'
                print './setup.py -p single_plot options '
                print '"{\'title\':[\'<user title>\'],\'xlabel\':[\'<user xlabel>\'],\'ylabel\':[\'<user ylabel>\'],\'variables\':[\'<var. positions (integers)>\'],\'grid\':[\'<logical>\'],\'legend\':[\'<logical>\'],\'legend_frame\':[\'<logical>\'],\'legend_loc\':[\'<options>\'],\'log\':[\'<logical>\'],\'log_x\':[\'<logical>\'],\'log_y\':[\'<logical>\']}"'
                print 'Example:'
                print './setup.py -p single_plot options "{\'title\':[\'RMSvsIter\'],\'xlabel\':[\'Iteration Number\'],\'ylabel\':[\'RMS\'],\'variables\':[\'2\'],\'grid\':[\'True\'],\'legend\':[\'True\'],\'legend_frame\':[\'True\'],\'legend_loc\':[\'lower right\'],\'log\':[\'True\'],\'log_x\':[\'False\'],\'log_y\':[\'True\']}"'
                print '================================:'
                print 'More infos: <type>, <default>'
                print '\'title\': <string> (optional),  \'example\''
                print '\'xlabel\': <string> (optional), \'None\''
                print '\'ylabel\': <string> (optional), \'None\''
                print '\'variables\': <string> w/ integers (optional), \'1 2\''
                print '\'grid\': <string> (logical/optional), \'False\''
                print '\'legend\': <string> (logical/optional), \'False\''
                print '\'legend_frame\': <string> (logical/optional - requires legend=\'True\'), \'False\''
                print '\'legend_loc\': <string> (logical/optional - requires legend=\'True\'), \'False\''
                print 'available options:'
                print     'upper right'
                print     'upper left'
                print     'lower left'
                print     'lower right'
                print     'right'
                print     'center left'
                print     'center right'
                print     'lower center'
                print     'upper center'
                print     'center'
                print '\'log\': <string> (logical/optional), \'False\''
                print '\'log_x\': <string> (logical/optional), \'False\''
                print '\'log_y\': <string> (logical/optional), \'False\''

                sys.exit()


    def plot_main(self,inputfile,name,args):
            # main call for all kind of plots

            if name == 'single_plot':
                # this plot routine reads a simple data files and
                # variables to plot are taken from the input file
                outpath = read_path('OUT_DIR')

                # assign user inputs to local variables for convenience
                files = self.fnames
                style = self.style
                label = self.label
                title = self.title
                xlabel = self.xlabel
                ylabel = self.ylabel
                variables = self.variables
                legend    = self.legend
                log = self.log

                if legend:
                    legend_frame = self.legend_frame
                    legend_loc = self.legend_loc
                if log:
                    log_x = self.log_x
                    log_y = self.log_y
                grid = self.grid

                # import data from file
                n = 0
                for fil in files:
                    data = np.genfromtxt(outpath+fil+'.dat')
                    if log[0] == True:
                        if log_x == True:
                            plt.semilogx(data[:,variables[0]-1],data[:,variables[1]-1],style[n],label=label[n])
                        elif log_y == True:
                            plt.semilogy(data[:,variables[0]-1],data[:,variables[1]-1],style[n],label=label[n])
                    
                    plt.plot(data[:,variables[0]-1],data[:,variables[1]-1],style[n],label=label[n])

                    n = n + 1
                # add picture title and axes labels
                plt.ylabel(ylabel[0])
                plt.xlabel(xlabel[0])
                plt.title(title[0])
                plt.grid(grid[0])
                if legend[0]:
                    plt.legend(
                        loc           = legend_loc,
                        borderpad     = 0.25,
                        handletextpad = 0.25,
                        borderaxespad = 0.25,
                        labelspacing  = 0.0,
                        handlelength  = 2.0,
                        numpoints=1)
                    legendText = plt.gca().get_legend().get_texts()
                    plt.setp(legendText,fontsize=inputfile.legsize)
                    legend_fram = plt.gca().get_legend()
                    legend_fram.draw_frame(legend_frame)

                # Save Picture in the ../output/plot/ folder as png. Folder is created if not present.
                if not os.path.exists('./output/' +'/plot/'):
                    os.makedirs('./output/' +'/plot/')
                filename_plot = os.path.join('./output/' +'/plot/', '_'.join(title[0].split(' '))+'.'+'png')
                plt.savefig(filename_plot, format='png')


            elif name == 'multi_plot':

                case = raw_input("Input desired folder name:")
                dt = float(self.time_step)#float(raw_input("Input the chosen dt:"))
                theta = float(self.scheme) #float(raw_input("Input the value of theta:"))
                
                plt.style.use('ggplot')
                plt.rcParams['font.family'] = 'serif'
                plt.rcParams['font.serif'] = 'Ubuntu'
                plt.rcParams['font.monospace'] = 'Ubuntu Mono'
                plt.rcParams['font.size'] = 12
                plt.rcParams['axes.labelsize'] = 12
                plt.rcParams['axes.labelweight'] = 'bold'
                plt.rcParams['axes.titlesize'] = 12
                plt.rcParams['xtick.labelsize'] = 10
                plt.rcParams['ytick.labelsize'] = 10
                plt.rcParams['legend.fontsize'] = 8
                plt.rcParams['figure.titlesize'] = 14


                # this plot routine reads a simple data files and
                # variables to plot are taken from the input file
                outpath = read_path('OUT_DIR')

                fileList = []
                fileList = glob.glob(os.path.join(outpath,'data_*.dat'))

                nIter = []
                for File in fileList:
                    c,k = File.split('data_t_')
                    k,c=k.split('.dat')
                    nIter.append(k)

                nIter = np.array(nIter)
                fileList = np.array(fileList)
                sortIndex = np.argsort(nIter)
                nIter = nIter[sortIndex]
                fileList=fileList[sortIndex]

                num_colors = 20
                colormap = plt.cm.gist_ncar
                plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_colors)])

                labels=[]

                # import data from file
                for i in xrange(len(nIter)):

                    file = fileList[i]
                    time = nIter[i]

                    data = np.genfromtxt(file)

                    yp = data[:,3]
                    up = data[:,4]
                    up_exact = data[:,5]

                    xmin = 0.0
                    xmax = 2.0
                    ymin = 0.0
                    ymax = 1.0

                    # add picture title and axes labels

                    plt.figure(0)
                    plt.plot(up,yp,'-',label='Numerical @t = %s s'%(time))
                    plt.plot(up_exact,yp,'o',label='Analytical @t = %s s'%(time))
                    plt.xlabel('u/u$_{top}$')
                    plt.ylabel('y/L')
                    plt.title('$\Theta = %s$' %(theta))
                    plt.grid(True)
                    plt.axis([xmin,xmax,ymin,ymax])
                    #plt.legend(ncol=1, loc='upper center', 
                    #            bbox_to_anchor=[0.90, 0.9], 
                    #            columnspacing=1.0, labelspacing=0.0,
                    #            handletextpad=0.0, handlelength=1.5,
                    #            fancybox=True, shadow=True)

                    # Save Picture in the ../output/plot/ folder as png. Folder is created if not present.
                    if not os.path.exists('./output/' +'/plot/'+case):
                        os.makedirs('./output/' +'/plot/'+case)

                    filename_plot = os.path.join('./output/' +'/plot/'+case, 'VelProfile'+'.'+'png')
                    plt.savefig(filename_plot, format='png')

                    # New Plot
                    
                    plt.figure(i+1)
                    plt.plot(up,yp,'b-')
                    plt.plot(up_exact,yp,'bo')
                    plt.xlabel('u/u$_{top}$')
                    plt.ylabel('y/L')
                    plt.title('$\Theta = %s$' %(theta))
                    plt.grid(True)
                    plt.axis([xmin,xmax,ymin,ymax])
                    plt.title('$\Theta = %s$, dt = %s, t = %s, Iter = %s' %(theta,dt,time,int(float(time)/dt)))

                    #Plotting single files separated
                    pltFile = os.path.join('./output/' + '/plot/'+case,'VelProfile_%6.6i.png'%(int(float(time)/dt)))
                    plt.savefig(pltFile,format='png')


def postproc(opts,args):

    # reference list containing the available plot options
    avail_plot_opts = ['multi_plot','single_plot']

    if opts in avail_plot_opts:
        plot_results(opts,args)
    else:
        print 'this option is not recognized: ',opts
        sys.exit()
