
####################################################################################################################### Libraries ##########################################################################################################################

import pandas  as pd
from matplotlib import pyplot as plt 
import numpy as np
import numpy.typing as npt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
################################################################################################################## DATA CLEANING FUNCTIONS #################################################################################################################

def outlier_detection(df, numerical_features):
    print("\n" + "_"*40)
    print("Outlier Detection Report")
    print("_"*40)

    outlier_cols = numerical_features
    outlier_report = []

    for col in outlier_cols:
        if col not in df.columns:
            continue
        data = df[col].dropna()
        if len(data) == 0:
            continue
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = data[(data < lower) | (data > upper)]
        outlier_report.append({
            'feature': col,
            'count': len(outliers),
            'percent': 100 * len(outliers) / len(data),
            'lower_bound': lower,
            'upper_bound': upper,
            'min_val': data.min(),
            'max_val': data.max()
        })
        print(f"\n{col}:")
        print(f"  - Outliers count: {len(outliers)} ({100 * len(outliers) / len(data):.2f}%)")
        print(f"  - Normal range (IQR): [{lower:.2f}, {upper:.2f}]")
        print(f"  - Actual range: [{data.min():.2f}, {data.max():.2f}]")
        print(f'  - 99 percentile: {df[col].quantile(0.99)}')
        print(f'  - 1 percentile: {df[col].quantile(0.01)}')
        print(f'  - mean: {df[col].mean()}')
        print(f'  - median: {df[col].median()}')

# for col in ['f16' , 'f20']:
#     lower = df[col].quantile(0.25)
#     upper = df[col].quantile(0.75)
#     IQR = upper - lower
#     lower_bound = lower - 1.5 * IQR
#     upper_bound = upper + 1.5 * IQR
    
#     print('-------------------------------------------------------------------------------------------------')


def f19_categorize(df:pd.DataFrame):
    wind_categories = {
        'Calm': ['^Calm$', '^CALM$'],
        'Variable': ['^VAR$', '^Variable$'],
        'North': ['^North$','^N$'],
        'NorthEast': ['^NNE$', '^NE$' , '^ENE$'],
        'NorthWest': ['^NNW$', '^NW$' , '^WNW$'],
        'South': ['^South$', '^S$'],
        'SouthEast': ['^SSE$', '^SE$' , '^ESE$'],
        'SouthWest': ['^SSW$', '^SW$' , '^WSW$'],
        'East': ['^East$', '^E$'],
        'West': ['^West$', '^W$']
    }
    # Build a mapping from each exact keyword to its category
    mapping = {}
    for cat, keywords in wind_categories.items():
        for kw in keywords:
            mapping[kw] = cat

    # Replace all at once (regex=True because patterns like '^N$' are regex)
    df['f19'] = df['f19'].replace(mapping, regex=True)



####################################################################################################################### Plots for EDA #######################################################################################################################

# NUMERICALS

def Scatter_plot(x:npt.ArrayLike , y:npt.ArrayLike , x_label:str =None, y_label:str =None , fig_size=(7,5) , title:str=None ,ax_grid=True , s:npt.ArrayLike =20):
    fig, ax = plt.subplots(figsize=fig_size)
    fig.set_facecolor('oldlace')
    ax.set_facecolor('oldlace')
    plt.tick_params(
        axis='both',          
        which='both',      
        bottom=False,      
        top=False,         
        left=False,
    )
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    plt.scatter(x , y , color='tab:blue' , alpha=0.3 , s=s )
    ax.grid(ax_grid)
    plt.show()

def Cluster_plot(df , x , y , target , Title ):

    fig = px.scatter(df , x , y , color=target , title= Title)
    fig.show()

def Box_plot(Df:pd.DataFrame , Columns : list , figsize=(20,10)):
    fig , ax = plt.subplots(int(np.ceil(len(Columns)/3)) , 3,figsize=figsize)
    ax = ax.flatten()
    fig.set_facecolor('oldlace')
    plt.tick_params(
    )
    for col in Columns : 
        ax[Columns.index(col)].set_facecolor('oldlace')
        ax[Columns.index(col)].set_title(col)
        ax[Columns.index(col)].tick_params(
            axis='both',          
            which='both',      
            bottom=False,      
            top=False,         
            left=False,
            # labelleft=False,
        )
        sns.boxplot(Df[col] , ax=ax[Columns.index(col)] , color='tab:blue' )
    
    for j in range(len(Columns) , len(ax)):
        ax[j].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()


def hist_plot( dataframe:pd.DataFrame,columns_list:list[str], figsize=(20,10), Title='Histograms of Selected Columns')-> None:

    N= len(columns_list)
    rows = int(np.floor(np.sqrt(N)))
    cols= int(np.ceil(N/rows))
    fig, axes = plt.subplots(rows, cols, figsize = figsize)
    fig.set_facecolor('oldlace')


    if N==1:
        axes = [axes] 
    else:
        axes=axes.flatten()

    for i, col in enumerate (columns_list):
        sns.histplot(ax= axes[i],x= col, data= dataframe, kde= True)
        axes[i].set_facecolor('oldlace')
        axes[i].set_title(f'{col}')
        axes[i].set_ylabel('')
        axes[i].set_xlabel('')
        axes[i].tick_params(axis='y')
        axes[i].grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.3)
        axes[i].tick_params(axis='both')
        sns.despine(ax=axes[i], top=True, right=True)
        

    fig.suptitle(Title, fontweight='bold')

    for j in range(N , len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()


#CATEGORY
def plot_mean_by_category (categorical_column: str, list_of_numerical_columns: list[str], df:pd.DataFrame, x:float , y: float , Title ='Mean Values by Category')-> None:

    grouped_obj = df.groupby(categorical_column)[list_of_numerical_columns].mean()

    N= len(list_of_numerical_columns)
    nrows = int(np.floor(np.sqrt(N)))
    ncols = int(np.ceil(N/nrows))

    fig, axes = plt.subplots(nrows,ncols, figsize=(x,y))
    fig.set_facecolor('oldlace')
    if N==1:
        axes = [axes]
    else:
        axes = axes.flatten()

    for i, col in enumerate (list_of_numerical_columns):
        sns.barplot(ax=axes[i], x= grouped_obj.index, y= grouped_obj[col],width=0.6)
        axes[i].set_facecolor('oldlace')
        axes[i].set_title(f'{col}')
        axes[i].set_ylabel('')
        axes[i].set_xlabel('')
        axes[i].tick_params(axis='y')
        axes[i].grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.3)
        axes[i].tick_params(axis='both')
        sns.despine(ax=axes[i], top=True, right=True)
    
    fig.suptitle(Title, fontweight='bold')

    for j in range(N , len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()



def ct_2var(col1_name: str, col2_name: str, df: pd.DataFrame , figsize =(20,10)):
    fig, ax = plt.subplots(2, 2, figsize=figsize)
    fig.set_facecolor('oldlace')
    ax = ax.flatten()

    table = pd.crosstab(df[col1_name], df[col2_name])
    sns.heatmap(table, ax=ax[0], annot=True, fmt='.2f', cbar=False, linewidths=0.5, square=True, cmap='Greys')
    sns.heatmap(table.div(table.sum(axis=1), axis=0), ax=ax[1], annot=True, fmt='.2f', cbar=False, linewidths=0.5, square=True, cmap='Greys')

    d = df.copy()
    d[col1_name] = d[col1_name].astype('string')
    d[col2_name] = d[col2_name].astype('string')

    sns.histplot(data=d, x=col1_name, hue=col2_name, multiple="dodge", discrete=True, shrink=0.5, stat="percent", ax=ax[2])
    sns.histplot(data=d, x=col2_name, hue=col1_name, multiple="fill", discrete=True, shrink=0.5, ax=ax[3])

    sns.despine(right=True, top=True, ax=ax[2])
    sns.despine(right=True, top=True, ax=ax[3])

    ax[3].set_ylabel('proportion- normalized')
    for i in range(4):
        ax[i].set_facecolor('oldlace')

    plt.tick_params(axis='both', which='both', length=0)
    plt.tight_layout()
    plt.show()


def corr_plot(df : pd.DataFrame , columns : list[str] ,figsize = (10 , 10)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.set_facecolor('oldlace')
    ax.set_facecolor('oldlace')
    sns.heatmap(df[columns].corr(), annot=True, ax=ax, fmt='.2f',cmap= 'vlag')
    plt.show()




def Count_plot(df : pd.DataFrame , Columns: list, hue:npt.ArrayLike , figsize =(20,10)):
    fig , axes = plt.subplots(int(np.ceil(len(Columns)/2)) , 2,figsize=figsize)
    fig.set_facecolor('oldlace')
    N= len(Columns)
    axes=axes.flatten()
    for i , Cat in enumerate(Columns) :
        sns.countplot(df,x=Cat, ax=axes[i] , hue=hue )
        axes[i].set_facecolor('oldlace')
        axes[i].set_title(f'{Cat}')
        axes[i].set_ylabel('')
        axes[i].set_xlabel('')
        axes[i].tick_params(axis='y')
        axes[i].grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.3)
        axes[i].tick_params(axis='both')
        sns.despine(ax=axes[i], top=True, right=True)
    fig.suptitle('CountPlot of Selected Categories', fontweight='bold')

    for j in range(N , len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()



############################################################################# FEATURE ENGINEERING ######################################################################


def f21_categorize_FE(df:pd.DataFrame):
    weather_categories = {
        'Clear': ['Fair', 'Clear'],
        'Cloudy': ['Cloudy' , 'Mostly Cloudy' , 'Partly Cloudy' , 'Overcast' , 'Scattered Clouds'],
        'Precipitation': ['Light Rain', 'Snow', 'Rain', 'Light Snow', 'Wintry Mix', 'Drizzle', 'Shower', 'Sleet', 'Ice Pellets'],
        'Thunderstorm': ['Thunderstorm', 'Thunder in the Vicinity', 'Thunderstorms' , 'T-Storm', 'Thunder'],
        'Fog': ['Fog', 'Mist', 'Haze' ,'Smoke', 'Patches of Fog', 'Widespread Dust'],
        'Windy' : ['Windy', 'Squalls']
    }

    for cat, keywords in weather_categories.items():
        pattern = '|'.join(keywords)
        df[f'{cat}'] = df['f21'].str.contains(pattern, case=False, na=False).astype(int)

    weather_cols = [f'{cat}' for cat in weather_categories.keys()]
    df['Other'] = (df[weather_cols].sum(axis=1) == 0).astype(int)

    df.drop(columns=['f21'] , inplace= True)


# def f19_categorize_FE(df:pd.DataFrame):
#     wind_categories = {
#         'Calm': ['calm', 'CALM'],
#         'Variable': ['var', 'variable'],
#         'North': ['north', 'nne', 'nnw', 'ne', 'nw', 'n '],
#         'South': ['south', 'sse', 'ssw', 'se', 'sw', 's '],
#         'East': ['east', 'ene', 'ese', 'e '],
#         'West': ['west', 'wnw', 'wsw', 'w ']
#     }
#     for cat, keywords in wind_categories.items():
#         pattern = '|'.join(keywords)
#         df[f'{cat}'] = df['f19'].str.contains(pattern, case=False, na=False).astype(int)

#     df.drop(columns=['f19'] , inplace=True)

def f19_categorize_FE(df:pd.DataFrame):
    wind_categories = {
        'Calm': ['^Calm$', '^CALM$'],
        'Variable': ['^VAR$', '^Variable$'],
        'North': ['^North$','^N$'],
        'NorthEast': ['^NNE$', '^NE$' , '^ENE$'],
        'NorthWest': ['^NNW$', '^NW$' , '^WNW$'],
        'South': ['^South$', '^S$'],
        'SouthEast': ['^SSE$', '^SE$' , '^ESE$'],
        'SouthWest': ['^SSW$', '^SW$' , '^WSW$'],
        'East': ['^East$', '^E$'],
        'West': ['^West$', '^W$']
    }
    for cat, keywords in wind_categories.items():
        pattern = '|'.join(keywords)
        df[f'{cat}'] = df['f19'].str.contains(pattern, case=False, na=False).astype(int)
    df.drop(columns=['f19'] , inplace=True)

