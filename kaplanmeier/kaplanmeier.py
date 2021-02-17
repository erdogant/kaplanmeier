""" This packages computes the log-rank P-value and computes survival curves based on kaplan meier
    
    import kaplanmeier as km

	df  = km.example_data()
	out = km.fit(time_event, censoring, labx, <optional>)
	      km.plot(out)

 SEE ALSO
   from lifelines import KaplanMeierFitter, datetimes_to_durations

"""

#--------------------------------------------------------------------------
# Name        : kaplanmeier.py
# Author      : E.Taskesen
# Date        : July. 2018
#--------------------------------------------------------------------------

#%% Libraries
import os
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt
from lifelines.statistics import logrank_test
from lifelines import KaplanMeierFitter
from lifelines.plotting import add_at_risk_counts
from kaplanmeier.helpers.savefig import savefig

#%% Main function
def fit(time_event, censoring, labx, verbose=3):
    '''

    Parameters
    ----------
    time_event:     [FLOAT]: Numpy array with survival-time in years/months/days (not a datetime!)

    censoring:      [INT]: numpy array with censoring (1=event, 0=ongoing)
                    At the time you want to make inferences about durations, it is possible, likely true, that not all the death events have occured yet. 
                    In case of patients, you would like to put 1=death as an event.
                   
    labx:           [INT] or [STRING]: numpy array with class labels. Each class label is seperately plotted

    verbose:        [INT] Print messages to screen.
                    0: NONE
                    1: ERROR
                    2: WARNING
                    3: INFO (default)
                    4: DEBUG
                    5: TRACE

    Returns
    -------
    Dictionary containing logrank pvalue and keys required to make plots.


    Example
    ----------
    import kaplanmeier as km
    df= km.example_data()
    out=km.fit(df['time'], df['Died'], df['group'])
    km.plot(out)

    km.plot(out, cmap='Set1', savepath='test.png')
    km.plot(out, cmap='Set1', cii_lines=True, cii_alpha=0.05)
    km.plot(out, cmap=[(1, 0, 0),(0, 0, 1)])
    km.plot(out, cmap='Set1', methodtype='custom')

    out['logrank_P']
    out['logrank_Z']

    '''

    if 'pandas' in str(type(time_event)):
        if verbose<=2: print('[KM] Input data <time_event> must be of type numpy array or list. Converting now..')
        time_event = time_event.astype(float).values
    if 'pandas' in str(type(censoring)):
        if verbose<=2: print('[KM] Input data <censoring> must be of type numpy array or list.  Converting now..')
        censoring = censoring.astype(int).values

    out_lr={}
    p_value=np.nan
    test_statistic=np.nan

    # Combine data and gather class labels
    uilabx = np.unique(labx)

    # Compute log-rank test between two lines
    if len(uilabx)==2:
        alpha=0.05
        class1=labx==uilabx[0]
        class2=labx==uilabx[1]
        # Compute logrank
        out_lr = logrank_test(time_event[class1], time_event[class2], censoring[class1], censoring[class2], alpha=1-alpha)
        p_value = out_lr.p_value
        test_statistic = out_lr.test_statistic

    # Store
    out = dict()
    out['logrank_P']=p_value
    out['logrank_Z']=test_statistic
    out['logrank']=out_lr
    out['labx']=labx
    out['uilabx']=uilabx
    out['time_event']=time_event
    out['censoring']=censoring
    
    return(out)

#%% Make plot
def plot(out, fontsize=12, savepath='', width=10, height=6, cmap='Set1', cii_alpha=0.05, cii_lines='dense', methodtype='lifeline'):
    '''
    

    Parameters
    ----------
    out :       [dict] Dictionary derived from the fit function.

    fontsize :  [INT],  Font size for the graph
                default is 12.
    
    savepath:   [STRING], Path to store the figure

    width:      [INT], Width of the figure
                10 (default)
                
    height:     [INT], Width of the figure
                6 (default)

    cmap:       [STRING], Specify your own colors for each class-label or use a colormap:  https://matplotlib.org/examples/color/colormaps_reference.html
                [(1, 0, 0),(0, 0, 1),(..)]
                'Set1'       (default)     
                'Set2'       Discrete colors
                'Pastel1'    Discrete colors
                'Paired'     Discrete colors
                'rainbow'
                'bwr'        Blue-white-red
                'binary' or 'binary_r'
                'seismic'    Blue-white-red 
                'Blues'      white-to-blue
                'Reds'       white-to-red

    cii_alpha:  [FLOAT], Confidence interval (works only when methodtype='lifelines')
                0.05 (default)
                
    cii_lines:  [STRING], Confidence lines (works only when methodtype='lifelines')
                'lifelines' (default)
                'custom'

    methodtype:  [STRING], Implementation type
                 'dense'   (dense/filled lines)
                 'line' 
                  None  (no lines)

    Returns
    -------
    None.

    '''
    KMcoord  = dict()
    Param = dict()
    Param['width'] = width
    Param['height'] = height
    Param['fontsize'] = fontsize
    Param['savepath'] = savepath
    labx=out['labx']
    
    # Combine data and gather class labels
    data = np.vstack((out['time_event'],out['censoring'])).T

    # Make colors and legend-names for class-labels
    [class_colors, classlabel] = make_class_color_names(data, out['labx'], out['uilabx'], cmap=cmap)
    
    if methodtype=='lifeline':
        # Init
        kmf_all=[]
        
        # Startup figure
        fig = plt.figure(figsize=(Param['width'],Param['height']))
        ax = fig.add_subplot(111)
#        ax.grid(True)
#        ax.ylabel('Percentage survival')
        if out['logrank']!=[]:
            plt.title('Survival function, P=%.5f' %out['logrank_P'])

        # Compute KM survival coordinates per class
        if cii_lines=='dense':
            cii_lines=False
        if cii_lines=='line':
            cii_lines=True
        if cii_lines=='' or cii_lines==None or cii_alpha==None:
            cii_lines=False
            cii_alpha=0

        for i in range(0, len(out['uilabx'])):
            kmf = KaplanMeierFitter()
            idx=np.where(labx==out['uilabx'][i])[0]
            # Fit
            kmf.fit(out['time_event'][idx], event_observed=out['censoring'][idx], label=classlabel[i], ci_labels=None, alpha=1-cii_alpha)
            # Plot
            kmf.plot(ax=ax,ci_force_lines=cii_lines, color=class_colors[i], show_censors=True)
            # Store
            kmf_all.append(kmf.fit(out['time_event'][idx], event_observed=out['censoring'][idx], label=classlabel[i], ci_labels=None, alpha=1-cii_alpha))
        
        if len(kmf_all)==1:
            add_at_risk_counts(kmf_all[0], ax=ax)
        elif len(kmf_all)==2:
            add_at_risk_counts(kmf_all[0], kmf_all[1], ax=ax)
        elif len(kmf_all)==3:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2], ax=ax)
        elif len(kmf_all)==4:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2],kmf_all[3], ax=ax)
        elif len(kmf_all)==5:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2],kmf_all[3],kmf_all[4], ax=ax)
        elif len(kmf_all)==6:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2],kmf_all[3],kmf_all[4],kmf_all[5], ax=ax)
        elif len(kmf_all)==7:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2],kmf_all[3],kmf_all[4],kmf_all[5],kmf_all[6], ax=ax)
        elif len(kmf_all)==8:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2],kmf_all[3],kmf_all[4],kmf_all[5],kmf_all[6],kmf_all[7], ax=ax)
        elif len(kmf_all)==9:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2],kmf_all[3],kmf_all[4],kmf_all[5],kmf_all[6],kmf_all[7],kmf_all[8], ax=ax)
        elif len(kmf_all)==10:
            add_at_risk_counts(kmf_all[0], kmf_all[1], kmf_all[2],kmf_all[3],kmf_all[4],kmf_all[5],kmf_all[6],kmf_all[7],kmf_all[8],kmf_all[9], ax=ax)
        else:
            print('[KM] Maximum of 10 classes is reached.')
            
        ax.tick_params(axis='x',length=15,width=1,direction='out',labelsize=Param['fontsize'])
        ax.tick_params(axis='y',length=15,width=1,direction='out',labelsize=Param['fontsize'])
        ax.spines['bottom'].set_position(['outward',Param['fontsize']])
        ax.spines['left'].set_position(['outward',Param['fontsize']])
        #    ax.rc('font', size= Param['fontsize'])   # controls default text sizes
        #    ax.rc('axes',  labelsize = Param['fontsize'])  # fontsize of the x and y labels

        if Param['savepath']!='':
            savefig(fig, Param['savepath'])


    if methodtype=='custom':
        # Compute KM survival coordinates per class
        for i in range(0, len(out['uilabx'])):
            idx        = np.where(labx==out['uilabx'][i])[0]
            tmpdata    = data[idx,:].tolist()
            KMcoord[i] = compute_coord(tmpdata)

        # Plot KM survival lines
        plotkm(KMcoord, classlabel, cmap=class_colors, width=Param['width'], height=Param['height'], fontsize=Param['fontsize'])
        
#%% Compute coordinates (custom implementation)
def compute_coord(survtimes):
    h_coords=[]
    v_coords=[]
    lost=[]
    y=1

    # Sort survival time
    survtimes.sort(key=lambda x:(x[0],x[1]))

    for i in survtimes:
        if i[1]!=1:
            lost.append([i[0],y])
        else:
            h_coords.append([i[0],y])
            y=1*len(survtimes[survtimes.index(i)+1:])/float(len(survtimes[survtimes.index(i):]))
            v_coords.append([i[0],h_coords[-1][-1],y])
            break
    
    newsurv=survtimes[survtimes.index(i)+1:]
    while len(newsurv)>0:
        newsurv,y,h_coords,v_coords,lost=loop(newsurv,y,h_coords,v_coords,lost)
    return (h_coords,v_coords,lost)

#%% Part of computing coordinates (custom implementation)
def loop(newsurv,y,h_coords,v_coords,lost):
    for j in newsurv:
        if j[1]!=1:
            lost.append([j[0],y])
        else:
            h_coords.append([j[0],y])
            y=y*len(newsurv[newsurv.index(j)+1:])/float(len(newsurv[newsurv.index(j):]))
            v_coords.append([j[0],h_coords[-1][-1],y])
            break

    newsurv=newsurv[newsurv.index(j)+1:]
    return (newsurv,y,h_coords,v_coords,lost)

#%% Show surival plot (custom implementation)s
def plotkm(KMcoord, uilabx, cmap='Set1', fontsize=10, width=10, height=6):
    
    # Get unique colors for class-labels
    if 'str' in str(type(cmap)):
        class_colors=sns.color_palette(cmap,len(KMcoord))
    else:
        class_colors=cmap
    
    fig = plt.figure(figsize=(width,height))
    
    for k in range(0,len(KMcoord)):
        KM=KMcoord[k]
        ax = fig.add_subplot(111)
        fig.subplots_adjust(bottom=.1)
        fig.subplots_adjust(top=.95)
        fig.subplots_adjust(left=.05)
        fig.subplots_adjust(right=.7)
    
        width=3
        start=0
        
        for i in KM[0]:
            ax.hlines(i[1]*100,start,i[0],linewidths=width,color=class_colors[k])
            start=i[0]
        
        if KM[-1][-1][0]>KM[0][-1][0]:
            ax.hlines(KM[-1][-1][1]*100,KM[0][-1][0],KM[-1][-1][0],linewidths=width,color=class_colors[k])
        
        for i in KM[1]:
            ax.vlines(i[0],i[2]*100-(width*71/1000.0),i[1]*100+(width*71/1000.0),linewidths=width,color=class_colors[k])
        
        for i in KM[2]:
            ax.vlines(i[0],(i[1]-.01)*100,(i[1]+.01)*100, color=class_colors[k])
        
        # To plot beneath is only to add the label
        ax.plot(KM[2][0], KM[2][0], label=uilabx[k],color=class_colors[k])
        
        # labels
        ax.tick_params(axis='x',length=15,width=1,direction='out',labelsize=fontsize)
        ax.tick_params(axis='y',length=15,width=1,direction='out',labelsize=fontsize)
        ax.spines['bottom'].set_position(['outward',fontsize])
        ax.spines['left'].set_position(['outward',fontsize])
        # ax.set_xticks([0,800,1600,2400,3200,4000])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1)
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['left'].set_bounds(0,100)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
    
    plt.legend()
    plt.ylim(0,105)
    plt.xlim(0,)
    plt.show()

#%% Make class colors
def make_class_color_names(data, labx, uilabx, cmap):
    if 'str' in str(type(cmap)):
        class_colors=sns.color_palette(cmap,len(uilabx))
    else:
        class_colors=cmap

    classlabel=uilabx.astype('O')
    for i in range(0, len(uilabx)):
        idx = np.where(labx==uilabx[i])[0]
        classlabel[i]='%s (%.0f/%.0f)' %(classlabel[i], sum(data[idx,1]==0), len(idx))

    return(class_colors, classlabel)

#%% Example data
def example_data():
    curpath = os.path.dirname(os.path.abspath( __file__ ))
    PATH_TO_DATA=os.path.join(curpath,'data','survival_example_data.txt')
    if os.path.isfile(PATH_TO_DATA):
        df=pd.read_csv(PATH_TO_DATA, sep='\t')
        return df
    else:
        print('[KM] Oops! Example data not found! Try to get it at: www.github.com/erdogant/kaplanmeier')
        return None