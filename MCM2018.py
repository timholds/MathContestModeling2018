import pandas as pd
from pandas.plotting import table
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def run_all():
    df = data_in()

def data_in():
    
    ''' Takes in data from the CSV, and gets the relevant data
     :returns a dataframe '''
    
    df = pd.read_csv('ProblemCData.csv')
    material_codes = ['FFTCB', 'PATCB', 'EMTCB', 'MGTCB', 'JFTCB', 'NGTCB','CLTCB','WWTCB', 'DFTCB', 'RFTCB','NUEGB','RETCB','HYTCB','GETCB','SOTCB','WYTCB', 'BMTCB'] # list of material codes from excel[]

    data = df.loc[df['MSN'].isin(material_codes)]
    return data

def get_materials_numbers(data):
    
    ''' Aggregate the data from different specific energy sources into general sources
        :returns a list of numbers '''
    
    dfPA = data[data.loc[:, 'MSN']== 'PATCB']
    dfEM = data[data.loc[:, 'MSN']== 'EMTCB']
    dfJF = data[data.loc[:, 'MSN']== 'JFTCB']
    dfMG = data[data.loc[:, 'MSN']== 'MGTCB']
    dfRF = data[data.loc[:, 'MSN']== 'RFTCB']
    dfDF = data[data.loc[:, 'MSN']== 'DFTCB']
    petro = dfPA.loc[:, 'Data'].values + dfEM.loc[:, 'Data'].values + dfJF.loc[:, 'Data'].values + dfMG.loc[:, 'Data'].values + dfRF.loc[:, 'Data'].values + dfDF.loc[:, 'Data'].values

    dfNG = data[data.loc[:, 'MSN']== 'NGTCB']
    natural_gas = dfNG.loc[:, 'Data'].values
    
    dfCoal = data[data.loc[:, 'MSN']== 'CLTCB']
    dfWood = data[data.loc[:, 'MSN']== 'WWTCB'] 
    coal_wood = dfCoal.loc[:, 'Data'].values + dfWood.loc[:, 'Data'].values 
    
    dfNuc = data[data.loc[:, 'MSN']== 'NUEGB'] 
    nuclear = dfNuc.loc[:, 'Data'].values
    
    dfWind = data[data.loc[:, 'MSN']== 'WYTCB'] 
    wind = dfWind.loc[:, 'Data'].values
    
    dfSol = data[data.loc[:, 'MSN']== 'SOTCB'] 
    solar = dfSol.loc[:, 'Data'].values
    
    dfHydro = data[data.loc[:, 'MSN']== 'HYTCB'] 
    hydro = dfHydro.loc[:, 'Data'].values
    
    dfGeo = data[data.loc[:, 'MSN']== 'GETCB'] 
    geo = dfGeo.loc[:, 'Data'].values
    
    dfBio = data[data.loc[:, 'MSN']== 'BMTCB'] 
    bio = dfBio.loc[:, 'Data'].values
    
    total = petro + natural_gas + coal_wood + nuclear + wind + solar + hydro + geo + bio
    
    data_values = [petro, natural_gas, coal_wood, nuclear, wind, solar, hydro, geo, bio, total]
    return data_values

def make_state_df(df, state):
    
    ''' Get data for a single state and return the dataframe '''
    
    state_df = df[df['StateCode']== state]
    return state_df

def make_year_df(df, year):
    
    ''' Get data for a single year and return the dataframe '''
    
    year_df = df[df['Year']== year]
    return year_df


def make_profile_df_unrefined(df):

    ''' Prepare the data to make energy profile for a given state in a given year
        :param dataframe in the form dfStateYear
        :returns df, which each cell is populated by a float'''
    
    data_abs = get_materials_numbers(df)
    total = sum(data_abs)
    
    data_rel = []
    for i in range(len(data_abs)):
        data_rel.append((data_abs[i] / total) *2)
    materials = ['Petroleum and Oil', 'Natural Gas', 'Coal and Wood', 'Nuclear', 'Wind', 'Solar', 'Hydroelectric', 'Geothermal', 'Biomass', 'total']
    inputs = {'Usage in BTUs': data_abs, 'Percenage of Total Energy Consumed': data_rel}
    data = pd.DataFrame(inputs, index=materials)

    s = data.loc[:, 'Percenage of Total Energy Consumed']
    percentage_list = []
    for x in s:
        percentage_list.extend(x * 100)

    t = fd.loc[:, 'Usage in BTUs']
    usage_list = []
    for y in t:
        usage_list.extend(y)


    return usage_list, percentage_list

def make_profile_df(usage_list, percentage_list):
    
    ''' Returns a profile for a states energy use in a year as a dataframe'''
    
    pd.options.display.float_format = '{:,.2f}'.format
     
    materials = ['Petroleum and Oil', 'Natural Gas', 'Coal and Wood', 'Nuclear', 'Wind', 'Solar', 'Hydroelectric', 'Geothermal', 'Biomass', 'Total']
    inputs = {'Usage in BTUs': usage_list, 'Percentage of Total Energy Consumed': percentage_list}
    data = pd.DataFrame(inputs, index=materials).sort_values(by=['Percentage of Total Energy Consumed'], ascending=False)
    data.columns.name = 'California Energy Profile for 2009'

    return data

#usage_list, percentage_list= make_profile_df_unrefined(dfStateYear)
#make_profile_df(usage_list, percentage_list)

def get_state_data_for_plotting(state1):
    state = state1
    df = data_in()
    data1 = df[df.loc[:, 'StateCode'] == state]
    # Get their data for the relevant columns as a series over all the years

    data = data1.filter(items=['Year', 'MSN', 'Data']).set_index(['Year'])
    # print(data)

    dfPA = data[data.loc[:, 'MSN'] == 'PATCB']
    dfEM = data[data.loc[:, 'MSN'] == 'EMTCB']
    dfJF = data[data.loc[:, 'MSN'] == 'JFTCB']
    dfMG = data[data.loc[:, 'MSN'] == 'MGTCB']
    dfRF = data[data.loc[:, 'MSN'] == 'RFTCB']
    dfDF = data[data.loc[:, 'MSN'] == 'DFTCB']
    petro = dfPA.loc[:, 'Data'] + dfEM.loc[:, 'Data'] + dfJF.loc[:, 'Data'] + dfMG.loc[:, 'Data'] + dfRF.loc[:,
                                                                                                    'Data'] + dfDF.loc[
                                                                                                              :, 'Data']

    dfNG = data[data.loc[:, 'MSN'] == 'NGTCB']
    natural_gas = dfNG.loc[:, 'Data']

    dfCoal = data[data.loc[:, 'MSN'] == 'CLTCB']
    dataCoal = dfCoal.loc[:, 'Data']

    dfWood = data[data.loc[:, 'MSN'] == 'WWTCB']
    dataWood = dfWood.loc[:, 'Data']
    coal_wood = dataCoal + dataWood

    dfNuc = data[data.loc[:, 'MSN'] == 'NUEGB']
    nuclear = dfNuc.loc[:, 'Data']

    dfWind = data[data.loc[:, 'MSN'] == 'WYTCB']
    wind = dfWind.loc[:, 'Data']

    dfSol = data[data.loc[:, 'MSN'] == 'SOTCB']
    solar = dfSol.loc[:, 'Data']

    dfHydro = data[data.loc[:, 'MSN'] == 'HYTCB']
    hydro = dfHydro.loc[:, 'Data']

    dfGeo = data[data.loc[:, 'MSN'] == 'GETCB']
    geo = dfGeo.loc[:, 'Data']

    dfBio = data[data.loc[:, 'MSN'] == 'BMTCB']
    bio = dfBio.loc[:, 'Data']

    renewable = wind + solar + hydro + geo + bio
    nonrenewable = petro + natural_gas + coal_wood + nuclear

    data_labels = ['petro', 'natural_gas', 'coal_wood', 'nuclear', 'wind', 'solar', 'hydro', 'geo', 'bio', 'renewables',
                   'nonrenewables']
    data_values = [petro, natural_gas, coal_wood, nuclear, wind, solar, hydro, geo, bio, renewable, nonrenewable]

    dataf = pd.DataFrame(index=data_labels, data=data_values)

    return dataf

def get_state_data_for_plotting0(state1):
    state = state1
    df = data_in()
    data1 = df[df.loc[:, 'StateCode'] == state]
    # Get their data for the relevant columns as a series over all the years

    data = data1.filter(items=['Year', 'MSN', 'Data']).set_index(['Year'])
    # print(data)

    dfPA = data[data.loc[:, 'MSN'] == 'PATCB']
    dfEM = data[data.loc[:, 'MSN'] == 'EMTCB']
    dfJF = data[data.loc[:, 'MSN'] == 'JFTCB']
    dfMG = data[data.loc[:, 'MSN'] == 'MGTCB']
    dfRF = data[data.loc[:, 'MSN'] == 'RFTCB']
    dfDF = data[data.loc[:, 'MSN'] == 'DFTCB']
    petro = dfPA.loc[:, 'Data'] + dfEM.loc[:, 'Data'] + dfJF.loc[:, 'Data'] + dfMG.loc[:, 'Data'] + dfRF.loc[:,
                                                                                                    'Data'] + dfDF.loc[
                                                                                                              :, 'Data']

    dfNG = data[data.loc[:, 'MSN'] == 'NGTCB']
    natural_gas = dfNG.loc[:, 'Data']

    dfCoal = data[data.loc[:, 'MSN'] == 'CLTCB']
    dataCoal = dfCoal.loc[:, 'Data']

    dfWood = data[data.loc[:, 'MSN'] == 'WWTCB']
    dataWood = dfWood.loc[:, 'Data']
    coal_wood = dataCoal + dataWood

    dfNuc = data[data.loc[:, 'MSN'] == 'NUEGB']
    nuclear = dfNuc.loc[:, 'Data']

    dfWind = data[data.loc[:, 'MSN'] == 'WYTCB']
    wind = dfWind.loc[:, 'Data']

    dfSol = data[data.loc[:, 'MSN'] == 'SOTCB']
    solar = dfSol.loc[:, 'Data']

    dfHydro = data[data.loc[:, 'MSN'] == 'HYTCB']
    hydro = dfHydro.loc[:, 'Data']

    dfGeo = data[data.loc[:, 'MSN'] == 'GETCB']
    geo = dfGeo.loc[:, 'Data']

    dfBio = data[data.loc[:, 'MSN'] == 'BMTCB']
    bio = dfBio.loc[:, 'Data']

    renewable = wind + solar + hydro + geo + bio
    nonrenewable = petro + natural_gas + coal_wood + nuclear
    total = wind + solar + hydro + geo + bio + petro + natural_gas + coal_wood + nuclear

    data_labels = ['petro', 'natural_gas', 'coal_wood', 'nuclear', 'wind', 'solar', 'hydro', 'geo', 'bio', 'renewable',
                   'nonrenewable', 'total']
    data_values = [petro, natural_gas, coal_wood, nuclear, wind, solar, hydro, geo, bio, renewable, nonrenewable, total]

    dataf = pd.DataFrame(index=data_labels, data=data_values)

    return dataf

#df = get_state_data_for_plotting('CA')
#plot_sources_over_time1(df)

dfCA = get_state_data_for_plotting0('CA')
dfAZ = get_state_data_for_plotting0('AZ')
dfNM = get_state_data_for_plotting0('NM')
dfTX = get_state_data_for_plotting0('TX')

def plot_energy_usage_over_time_all_states(dfCA, dfAZ, dfNM, dfTX):
    ax = plt.figure(figsize=(12, 5)).add_subplot(111)

    # total = df.loc['renewables', :] + df.loc['nonrenewables', :]

    axCA = dfCA.loc['total', :].plot(color='blue', grid=True, label='CA')
    axAZ = dfAZ.loc['total', :].plot(color='green', grid=True, label='AZ')
    axNM = dfNM.loc['total', :].plot(color='gray', grid=True, label='NM')
    axTX = dfTX.loc['total', :].plot(color='red', grid=True, label='TX')
    # axNM = (df.loc['nonrenewables', :] / total * 100 ).plot(color='red', grid=True, label='Non-renewables')

    h1, l1 = axCA.get_legend_handles_labels()

    ax.set_title('Energy Usage over Time')
    ax.set_ylabel('Total Energy Used (BTUs)', rotation=0, labelpad=70)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))

    ax.legend(h1, l1, loc=2)
    plt.show()

def plot_energy_from_renewables_over_time_all_states(dfCA, dfAZ, dfNM, dfTX):
    ax = plt.figure(figsize=(12, 5)).add_subplot(111)

    # total = df.loc['renewables', :] + df.loc['nonrenewables', :]

    axCA = dfCA.loc['renewable', :].plot(color='blue', grid=True, label='CA')
    axAZ = dfAZ.loc['renewable', :].plot(color='green', grid=True, label='AZ')
    axNM = dfNM.loc['renewable', :].plot(color='gray', grid=True, label='NM')
    axTX = dfTX.loc['renewable', :].plot(color='red', grid=True, label='TX')
    # axNM = (df.loc['nonrenewables', :] / total * 100 ).plot(color='red', grid=True, label='Non-renewables')

    h1, l1 = axCA.get_legend_handles_labels()

    ax.set_title('Renewable Energy Use over Time')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%2.0f'))
    #ax.set_yticks([20, 40, 60, 80])
    ax.set_ylabel('Total Renewable Energy Usage (BTUs)', rotation=0, labelpad=70)

    ax.legend(h1, l1, loc=2)
    plt.show()

def plot_energy_from_renewables_over_time_all_states_relative(dfCA, dfAZ, dfNM, dfTX):
    ax = plt.figure(figsize=(12, 5)).add_subplot(111)

    totalCA = dfCA.loc['renewable', :] + dfCA.loc['nonrenewable', :]
    totalAZ = dfCA.loc['renewable', :] + dfAZ.loc['nonrenewable', :]
    totalNM = dfCA.loc['renewable', :] + dfNM.loc['nonrenewable', :]
    totalTX = dfCA.loc['renewable', :] + dfTX.loc['nonrenewable', :]

    axCA = (dfCA.loc['renewable', :]/ totalCA * 100).plot(color='blue', grid=True, label='CA')
    axAZ = (dfAZ.loc['renewable', :]/ totalAZ * 100).plot(color='green', grid=True, label='AZ')
    axNM = (dfNM.loc['renewable', :]/ totalNM * 100).plot(color='gray', grid=True, label='NM')
    axTX = (dfTX.loc['renewable', :]/ totalTX * 100).plot(color='red', grid=True, label='TX')
    # axNM = (df.loc['nonrenewables', :] / total * 100 ).plot(color='red', grid=True, label='Non-renewables')

    h1, l1 = axCA.get_legend_handles_labels()

    ax.set_title('Renewable Energy Usage over Time for States as a Percentage of Total Enery Usage')
    ax.set_ylabel('% of Total Energy Usage', rotation=0, labelpad=70)

    ax.legend(h1, l1, loc=2)
    plt.show()

def produce_graphs(dfCA, dfAZ, dfNM, dfTX):
    plot_energy_usage_over_time_all_states(dfCA, dfAZ, dfNM, dfTX)
    plot_energy_from_renewables_over_time_all_states(dfCA, dfAZ, dfNM, dfTX)
    plot_energy_from_renewables_over_time_all_states_relative(dfCA, dfAZ, dfNM, dfTX)


def get_state_profiles_2009(state):
    ''' For a given state, show their energy profile in 2009'''

    df = data_in()
    make_profile_df_unrefined(df)
    make
    state_df(state)
    year_df(2009)
    get_materials_numbers(df)
    plot_df()
    plot_sources_pi()

def plot_sources_pie(df):
    
    ''' Create a pie chart for energy sources for a given state in a given year
    :returns a matplotlib plot '''

    profile_df = make_profile_df(df)
    percentages = profile_df.loc[:, 'Percentage of Total Energy Consumed']
    #print(percentages)
    
    materials = ['Petroleum and Oil', 'Natural Gas', 'Coal and Wood', 'Nuclear', 'Wind', 'Solar', 'Other']
    # TODO fix this print statement
    print('Where Other is Hydroelectric, Geothermal, & Biomass')
    colors = ['red', 'red', 'red', 'red', 'green', 'green', 'green']
    scaling = 5
    
    sizes = [item*scaling for item in percentages[:-1]]
    print(len(sizes))
    # TODO switch out the sizes and use the one representing the actual data
    
    #sizes = proportion * scaling
    #sizes = [215, 130, 245, 210, 215, 130, 245, 210]
    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)  # explode 1st slice

    plt.pie(sizes, explode=explode, labels=materials, colors=colors,
            autopct='%5.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

def plot_df(df):
    
    ''' Not sure if I still need this method '''
    
    ax = plt.subplot(111) #, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis

    table(ax, df)  # where df is your data frame

    plt.show(table)

def get_state_sources_data(data):

    dfNG = data[data.loc[:, 'MSN'] == 'NGTCB']
    natural_gas = dfNG.loc[:, 'Data'].values

    dfCoal = data[data.loc[:, 'MSN'] == 'CLTCB']
    dfWood = data[data.loc[:, 'MSN'] == 'WWTCB']
    coal_wood = dfCoal.loc[:, 'Data'].values + dfWood.loc[:, 'Data'].values

    dfNuc = data[data.loc[:, 'MSN'] == 'NUEGB']
    nuclear = dfNuc.loc[:, 'Data'].values

    dfWind = data[data.loc[:, 'MSN'] == 'WYTCB']
    wind = dfWind.loc[:, 'Data'].values

    dfSol = data[data.loc[:, 'MSN'] == 'SOTCB']
    solar = dfSol.loc[:, 'Data'].values

    dfHydro = data[data.loc[:, 'MSN'] == 'HYTCB']
    hydro = dfHydro.loc[:, 'Data'].values

    dfGeo = data[data.loc[:, 'MSN'] == 'GETCB']
    geo = dfGeo.loc[:, 'Data'].values

    dfBio = data[data.loc[:, 'MSN'] == 'BMTCB']
    bio = dfBio.loc[:, 'Data'].values

    renewables = petro + natural_gas + coal_wood + nuclear
    nonrenewables = wind + solar + hydro + geo + bio
    total = petro + natural_gas + coal_wood + nuclear + wind + solar + hydro + geo + bio

    # Get the values for each year for each state as a numpy series

    # Add up the df.loc[]

    # Slice the dataframe to get the numbers for each city each year
    #data_values = [petro, natural_gas, coal_wood, nuclear, wind, solar, hydro, geo, bio, total]

    # Data
    df = pd.DataFrame({'x': range(1969, 2009), 'y1': renewables, 'y2': nonrenewables,
                       'y3': np.random.randn(10) + range(11, 21)})

    # multiple line plot
    plt.plot('x', 'y1', data=df, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    plt.plot('x', 'y2', data=df, marker='', color='olive', linewidth=2)
    plt.plot('x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    plt.legend()

def plot_state_sources_over_time(df):
    ''' Make a line chart showing a states relative use of renewable and non renewable energy'''

    plt.plot(year, ff_rel_use, color='red')
    plt.plot(year, rn_rel_use, color='green')
    plt.xlabel('Time')
    plt.ylabel('Percentage of Total Energy')
    plt.title('{State} use of energy over time')
    plt.show()



#fd = make_profile_df_unrefined(dfCA2009)
#usage_list, percentage_list = turn_profile_df_lists_to_numbers(fd)
#dfCA2009_profile = make_profile_df(usage_list, percentage_list)
#dfCA2009_profile.name = 'California 2009 Profile'
#dfCA2009_profile.plot.line()
#get_state_sources_data(df)
#plot_sources_pie(dfCA2009)
#plot_state_sources_over_time(df)
#get_materials_numbers(data)

'''
# Get the values for 2009 for all the codes for all the states
df2009 = make_year_df(df, 2009)
df2009.name = '2009 Data'

dfCA = state_df(df, 'CA')
dfCA2009 = year_df(dfCA, 2009)
dfCA2009.name = 'California 2009 Data'

dfAZ = state_df(df, 'AZ')
dfAZ2009 = year_df(dfAZ, 2009)
dfAZ2009.name = 'Arizona 2009 Data'

dfNM = state_df(df, 'NM')
dfNM2009 = year_df(dfNM, 2009)
dfNM2009.name = 'New Mexico 2009 Data'

dfTX = state_df(df, 'TX')
dfTX2009 = year_df(dfTX, 2009)
dfTX2009.name = 'Texas 2009 Data'
'''




# Write some code to add up the different types of fuels
# ff_total_use = df.loc['Fossiel Fuel']
# rn_total_use = df.loc['Renewable']
# total_usage = ff_total_use + rn_total_use

# ff_rel_use = [i / total_usage for i in df.loc['Fossil Fuel']]
# rn_rel_use = [i / total_usage for i in df.loc['Renewable']]





