#
# py_plot.py
#
#

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import matplotlib 

os.chdir(r'D:\Documents\Python\DATA_SCIENCE_TOOLKIT')
#print(os.getcwd())

#df = pd.read_csv('AB_NYC_2019.csv', low_memory= False)
#cols = df.columns

#dtype_df = pd.DataFrame(df.dtypes)
#dtype_df.reset_index()
#dtype_df.columns = ['var']
#print(dtype_df)



def cuberoot(x):
    if x < 0:
        x = abs(x)
        cube_root = x**(1/3)*(-1)
    else:
        cube_root = x**(1/3)
    return cube_root



def box_hist(df, x_var_name):
    n_row, n_col = df.shape
    var = list(df[x_var_name])
    new_var = [x for x in var if str(x) != 'nan']

    l = len(new_var)

    percent_blank = round(((n_row - l) / n_row)*100, ndigits=2)
    
    colors =  ['#0E4D92']

    sns.set(font_scale = 1.2)
    sns.set_style("whitegrid")
    f, (a0, a1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 3]}, sharex=True, figsize=(6.5, 4.5))

    # calculate stuff
    avg = round(np.mean(new_var), ndigits=2)
    median = round(np.median(new_var), ndigits=2)
    upper_quartile = round(np.percentile(new_var, 75), ndigits=2)
    lower_quartile = round(np.percentile(new_var, 25), ndigits=2)

    iqr = upper_quartile - lower_quartile
    upper_whisker = upper_quartile+(1.5*iqr)
    lower_whisker = lower_quartile-(1.5*iqr)
    
    bin_width = (2 * iqr) / cuberoot(l)
    max(upper_whisker, max(new_var))

    #min_plot_window = (min(abs(lower_whisker), abs(min(new_var))))
    #max_plot_window = (min(abs(upper_whisker), abs(max(new_var))))
   # if abs(iqr) < 1:
   #     min_plot_window = lower_quartile *.99
   #     max_plot_window = upper_quartile * 1.01
   #     #n_bins = int(((max_plot_window - min_plot_window)/ bin_width))
   #     bin_width = (20 * iqr) / cuberoot(l)
   #     if bin_width ==0:
   #         bin_width = .10
   #     n_bins = int(((max_plot_window - min_plot_window)/ bin_width))
   #     print(n_bins)
   #     if n_bins <0:
   #         n_bins = abs(n_bins)
   #     if n_bins == 0:
   #         n_bins = 20
   #     #n_bins = 15
   # if iqr >= 1: 
   #     min_plot_window = lower_quartile *.50
   #     max_plot_window = upper_quartile *1.50
   #     n_bins = int(((max(new_var) - min(new_var))/ bin_width))
   #     #print(n_bins)
    
    
    bp = a0.boxplot(new_var, vert = False, patch_artist=True, showmeans=True)
    a0.axes.get_yaxis().set_visible(False)

    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    a1.hist(new_var, color = colors[0])
    a1.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,p: format(int(x), ',')))

    #if max(new_var) > 10000:        
    #print("MIN X " + str(min_plot_window) + "  MAX PLOT " + str(max_plot_window))
    #plt.xlim(min_plot_window ,max_plot_window )
    plt.ylabel("Count")

    plt.xlabel(x_var_name)
    f.tight_layout()
    if not os.path.exists("temp_plots"):
        os.makedirs('temp_plots')

    plt.savefig('temp_plots/' +x_var_name + '.png')

    sum_stats = pd.DataFrame({'25th_p':[lower_quartile],
                              'median':[median], 
                              '75th_p':[upper_quartile],
                              'mean':[avg],
                              'N':[l], 
                              'p_blank':[percent_blank] })
    #plt.show()
    return(sum_stats)



def bar_chart(df, x_var_name):

    n_row, n_col = df.shape
    new_col = [1]* n_row
    try:
        df.insert(1, 'temp_count_id',new_col)
    except ValueError:
        print("WARNING: cannot insert temp_count_id already exists.")
    
    sns.set(font_scale = 1.2)
    sns.set_style("whitegrid")

    pivot_table = pd.pivot_table(df, values = ['temp_count_id'], index = [x_var_name],
                                aggfunc = {'temp_count_id':'count'}) 
    
    try:
        df = df.drop(['temp_count_id'], axis=1)
    except ValueError:
        print("cannot drop temp_count_id")


    pivot_table = pivot_table.reset_index()
    pivot_table.columns = [x_var_name, 'count']
    pivot_table = pivot_table.sort_values(by = ['count'], ascending= False)
    pivot_table.head()

    # Take the top 8 rows!
    sub_pivot = pivot_table[:6]

    n_row, n_col = sub_pivot.shape
    total_count = sum(pivot_table['count'])

    prob = []
    cum_prob = []
    for i in range(0, n_row):
        value = pivot_table['count'].iloc[i]
        prob.append(round(value / total_count, ndigits = 2))
        if i ==0:
            cum_prob.append(prob[i])
        else:
            cum_prob.append(round(sum(prob),ndigits=2))
        
    #sub_pivot.insert(2, 'prob', prob)
    sub_pivot.insert(2, 'cumulative %', cum_prob)

    # BEGIN PLOTTING. 
    fig, ax = plt.subplots(figsize=(5.5, 6))
    #f = plt.figure(figsize=(6.5, 4.5))
    sns.barplot(x=x_var_name, y="count", data=sub_pivot, palette="Blues_d")
    
    # ROTATE THE FONT & MAKE IT SMALLER
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=13)

    plt.ylabel("count")
    plt.xlabel(x_var_name)
    fig.tight_layout()
    
    if not os.path.exists("temp_plots"):
        os.makedirs('temp_plots')

    plt.savefig('temp_plots/' + x_var_name + '.png')
    

    return(sub_pivot)

#df = pd.read_csv('AB_NYC_2019.csv', low_memory= False)
#box_hist(df, 'latitude')


