"""Compute the log-rank P-value and survival curves based on kaplan meier.

# Name        : kaplanmeier.py
# Author      : E.Taskesen
# Date        : July. 2018
"""

# %% Libraries
import os
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt
from lifelines.statistics import logrank_test
from lifelines import KaplanMeierFitter
from lifelines.plotting import add_at_risk_counts
from kaplanmeier.helpers.savefig import savefig
from matplotlib.ticker import PercentFormatter


# %% Main function
def fit(time_event, censoring, labx, verbose=3):
    """Compute the log-rank P-value and survival curves based on kaplan meier.

    Parameters
    ----------
    time_event : Float.
        Numpy array with survival-time in years/months/days (not a datetime!)
    censoring : array-like
        numpy array with censoring (1=event, 0=ongoing).
        At the time you want to make inferences about durations, it is possible, likely true, that not all the death events have occured yet.
        In case of patients, you would like to put 1=death as an event.
    labx : array-like of type string or int
        Class labels. Each class label is seperately plotted.
    verbose : int, (default: 3)
        Verbosity messages.

    Returns
    -------
    dict()
        * logrank_P (float) : P-value
        * logrank_Z (float) : Z-score
        * logrank (float) : fitted logrank_test model
        * labx (list) : Class labels
        * uilabx (list) : Unique Class labels
        * time_event (float) : Time to event
        * censoring (bool) : Censored or not

    Examples
    --------
    >>> # Import library
    >>> import kaplanmeier as km
    >>>
    >>> # Example data
    >>> df = km.example_data()
    >>>
    >>> # Fit
    >>> results = km.fit(df['time'], df['Died'], df['group'])
    >>>
    >>> # Plot
    >>> km.plot(results)
    >>>
    >>> km.plot(results, cmap='Set1', cii_lines=True, cii_alpha=0.05)
    >>> km.plot(results, cmap=[(1, 0, 0),(0, 0, 1)])
    >>> km.plot(results, cmap='Set1', methodtype='custom')
    >>>
    >>> results['logrank_P']
    >>> results['logrank_Z']

    """
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
        out_lr = logrank_test(time_event[class1], time_event[class2], censoring[class1], censoring[class2], alpha=(1 - alpha))
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


# %% Make plot
def plot(out, fontsize=12, savepath='', width=10, height=6, cmap='Set1', cii_alpha=0.05, cii_lines='dense', methodtype='lifeline', title=None, full_ylim=False, y_percentage=False):
    """Make plot.

    Parameters
    ----------
    out : dict
        Results from the fit function.
    fontsize : int (default: 12)
        Font size for the graph.
    savepath : String (default: '')
        Path to store the figure.
    width : int (default: 10)
        Width of the figure.
    height : int (default: 10)
        height of the figure.
    cmap : str (default: 'Set1')
        Specify your own colors for each class-label or use a colormap:  https://matplotlib.org/examples/color/colormaps_reference.html.
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
    cii_alpha : float (default: 0.05)
        Confidence interval (works only when methodtype='lifelines').
    cii_lines : String (default: 'dense')
        Confidence lines (works only when methodtype='lifelines').
        'dense' (default)
        'lifelines'
        'custom' or None
    methodtype : str (default: 'lifeline')
        Implementation type.
        'dense'   (dense/filled lines)
        'line'
         None  (no lines)
    title : str (default: None)
        In case of None, the logrank P-values is shown.
        Title of the plot.

    Returns
    -------
    None.

    Examples
    --------
    >>> # Import library
    >>> import kaplanmeier as km
    >>>
    >>> # Example data
    >>> df = km.example_data()
    >>>
    >>> # Fit
    >>> results = km.fit(df['time'], df['Died'], df['group'])
    >>>
    >>> # Plot
    >>> km.plot(results)
    >>>
    >>> km.plot(results, cmap='Set1', cii_lines=True, cii_alpha=0.05)
    >>> km.plot(results, cmap=[(1, 0, 0),(0, 0, 1)])
    >>> km.plot(results, cmap='Set1', methodtype='custom')

    """
    if title is None: title = ('Survival function\nLogrank P-Value = %.5f' % (out['logrank_P']))
    KMcoord = {}
    Param = {}
    Param['width'] = width
    Param['height'] = height
    Param['fontsize'] = fontsize
    Param['savepath'] = savepath
    labx=out['labx']

    # Combine data and gather class labels
    data = np.vstack((out['time_event'], out['censoring'])).T

    # Make colors and legend-names for class-labels
    [class_colors, classlabel] = make_class_color_names(data, out['labx'], out['uilabx'], cmap=cmap)

    if methodtype=='lifeline':
        # Init
        kmf_all=[]

        # Startup figure
        fig = plt.figure(figsize=(Param['width'], Param['height']))
        ax = fig.add_subplot(111)
        if full_ylim:
            ax.set_ylim([0.0, 1.05])
        if y_percentage:
            ax.yaxis.set_major_formatter(PercentFormatter(1.0))
        plt.title(title)

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
            kmf.fit(out['time_event'][idx], event_observed=out['censoring'][idx], label=classlabel[i], ci_labels=None, alpha=(1 - cii_alpha))
            # Plot
            kmf.plot(ax=ax, ci_force_lines=cii_lines, color=class_colors[i], show_censors=True)
            # Store
            kmf_all.append(kmf.fit(out['time_event'][idx], event_observed=out['censoring'][idx], label=classlabel[i], ci_labels=None, alpha=(1 - cii_alpha)))

        add_at_risk_counts(*kmf_all, ax=ax)

        ax.tick_params(axis='x', length=15, width=1, direction='out', labelsize=Param['fontsize'])
        ax.tick_params(axis='y', length=15, width=1, direction='out', labelsize=Param['fontsize'])
        ax.spines['bottom'].set_position(['outward', Param['fontsize']])
        ax.spines['left'].set_position(['outward', Param['fontsize']])
        #    ax.rc('font', size= Param['fontsize'])   # controls default text sizes
        #    ax.rc('axes',  labelsize = Param['fontsize'])  # fontsize of the x and y labels

        if Param['savepath']!='':
            savefig(fig, Param['savepath'])

    if (methodtype=='custom') or (methodtype is None):
        # Compute KM survival coordinates per class
        for i in range(0, len(out['uilabx'])):
            idx = np.where(labx==out['uilabx'][i])[0]
            tmpdata = data[idx, :].tolist()
            KMcoord[i] = compute_coord(tmpdata)

        # Plot KM survival lines
        _plotkm(KMcoord, classlabel, cmap=class_colors, width=Param['width'], height=Param['height'], fontsize=Param['fontsize'], title=title)


# %% Compute coordinates (custom implementation)
def compute_coord(survtimes):
    """Compute coordinates."""
    h_coords=[]
    v_coords=[]
    lost=[]
    y=1

    # Sort survival time
    survtimes.sort(key=lambda x: (x[0], x[1]))

    for i in survtimes:
        if i[1]!=1:
            lost.append([i[0], y])
        else:
            h_coords.append([i[0], y])
            y=1 * len(survtimes[survtimes.index(i) + 1:]) / float(len(survtimes[survtimes.index(i):]))
            v_coords.append([i[0], h_coords[-1][-1], y])
            break

    newsurv=survtimes[survtimes.index(i) + 1:]
    while len(newsurv)>0:
        newsurv, y, h_coords, v_coords, lost=loop(newsurv, y, h_coords, v_coords, lost)
    return (h_coords, v_coords, lost)


# %% Part of computing coordinates (custom implementation)
def loop(newsurv, y, h_coords, v_coords, lost):
    """Part of computing coordinates (custom implementation)."""
    for j in newsurv:
        if j[1]!=1:
            lost.append([j[0], y])
        else:
            h_coords.append([j[0], y])
            y=y * len(newsurv[newsurv.index(j) + 1:]) / float(len(newsurv[newsurv.index(j):]))
            v_coords.append([j[0], h_coords[-1][-1], y])
            break

    newsurv=newsurv[newsurv.index(j) + 1:]
    return (newsurv, y, h_coords, v_coords, lost)


# %% Show surival plot (custom implementation)
def _plotkm(KMcoord, uilabx, cmap='Set1', fontsize=10, width=10, height=6, title=None):
    """Surival plot."""
    # Get unique colors for class-labels
    if 'str' in str(type(cmap)):
        class_colors=sns.color_palette(cmap, len(KMcoord))
    else:
        class_colors=cmap

    fig = plt.figure(figsize=(width, height))

    ax = fig.add_subplot(111)
    fig.subplots_adjust(bottom=.1)
    fig.subplots_adjust(top=.95)
    fig.subplots_adjust(left=.05)
    fig.subplots_adjust(right=.7)

    for k in range(0, len(KMcoord)):
        KM=KMcoord[k]
        width=3
        start=0

        for i in KM[0]:
            ax.hlines(i[1] * 100, start, i[0], linewidths=width, color=class_colors[k])
            start=i[0]

        if KM[-1][-1][0] > KM[0][-1][0]:
            ax.hlines(KM[-1][-1][1] * 100, KM[0][-1][0], KM[-1][-1][0], linewidths=width, color=class_colors[k])

        for i in KM[1]:
            ax.vlines(i[0], i[2] * 100 - (width * 71 / 1000.0), i[1] * 100 + (width * 71 / 1000.0), linewidths=width, color=class_colors[k])

        for i in KM[2]:
            ax.vlines(i[0], (i[1] - .01) * 100, (i[1] + .01) * 100, color=class_colors[k])

        # To plot beneath is only to add the label
        ax.plot(KM[2][0], KM[2][0], label=uilabx[k], color=class_colors[k])

        # labels
        ax.tick_params(axis='x', length=15, width=1, direction='out', labelsize=fontsize)
        ax.tick_params(axis='y', length=15, width=1, direction='out', labelsize=fontsize)
        ax.spines['bottom'].set_position(['outward', fontsize])
        ax.spines['left'].set_position(['outward', fontsize])
        # ax.set_xticks([0,800,1600,2400,3200,4000])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1)
        ax.spines['bottom'].set_linewidth(1)
        ax.spines['left'].set_bounds(0, 100)
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

    plt.legend()
    plt.title(title)
    plt.ylim(0, 105)
    plt.xlim(0,)
    plt.show()


# %% Make class colors
def make_class_color_names(data, labx, uilabx, cmap):
    """Create class colors."""
    if 'str' in str(type(cmap)):
        class_colors=sns.color_palette(cmap, len(uilabx))
    else:
        class_colors=cmap

    classlabel=uilabx.astype('O')
    for i in range(0, len(uilabx)):
        idx = np.where(labx==uilabx[i])[0]
        classlabel[i]='%s (%.0f/%.0f)' %(classlabel[i], sum(data[idx, 1]==0), len(idx))

    return(class_colors, classlabel)


# %% Example data
def example_data():
    """Create example data.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    curpath = os.path.dirname(os.path.abspath(__file__))
    PATH_TO_DATA=os.path.join(curpath, 'data', 'survival_example_data.txt')
    if os.path.isfile(PATH_TO_DATA):
        df=pd.read_csv(PATH_TO_DATA, sep='\t')
        return df
    else:
        print('[KM] Oops! Example data not found! Try to get it at: www.github.com/erdogant/kaplanmeier')
        return None
