#Import data
# set the file path
file_path = Path("Data/LA_CPI_apparel.csv")
file_path_2= Path("Data/LA_CPI_foodaway.csv")
file_path_3= Path("Data/LA_CPI_housing.csv")

# create a Pandas dataframe from a csv file
apparel_df = pd.read_csv(file_path, index_col='Year')
foodaway_df = pd.read_csv(file_path_2, index_col='Year')
housing_df = pd.read_csv(file_path_3, index_col='Year')
housing_df

#Select Annual Data for each dataframe
apparel_df = apparel_df['Annual']
foodaway_df = foodaway_df['Annual']
housing_df = housing_df['Annual']

#Concatenate the dataframes from 2012-2021

combined_df = pd.concat([apparel_df, foodaway_df, housing_df], axis='columns', join='inner')
combined_df

#Assign the column names
combined_df.columns=["LA Apparel CPI", "LA Food Away from home CPI", "LA Housing CPI"]
combined_df

#Store combined dataframe to csv
combined_df.to_csv("Data/LA_combined_cpi.csv")

#Calculate the year over year percent change in CPI for each
annual_change = combined_df.pct_change()
annual_change= annual_change.drop([2012, 2013, 2014])
annual_change

annual_change.plot(title="CPI Year over Year percent change in LA", ylabel= "YoY percent change")

#Format current date as ISO format
start = pd.Timestamp("2012-01-01", tz="America/New_York").isoformat()
end = pd.Timestamp("2021-12-31", tz="America/New_York").isoformat()
timeframe="1Day"

#Fetch stock data for each industry of interest
real_estate = ["TSCO","DHI","LOW","LGIH"]
apparel = ["NKE", "UA","GPS", "LULU", "JWN"]
food_away = ["MCD","YUM", "DRI", "QSR"]

def alpacas_api(symbols,timeframe, start,end):
    dataframe = alpaca.get_bars(symbols, timeframe=timeframe, start=start, end=end).df
    new_df = dataframe[['open','close','trade_count', 'symbol']]

    return new_df

Real_Estate_stocks = alpacas_api(real_estate, timeframe,start,end)
Apparel_stocks = alpacas_api(apparel, timeframe,start,end)
Food_stocks = alpacas_api(food_away, timeframe,start,end)

# Create pivot tables for closing prices for each stock df
Real_Estate_close = Real_Estate_stocks.pivot_table(values="close", index="timestamp",columns="symbol")
Apparel_close = Apparel_stocks.pivot_table(values="close", index="timestamp",columns="symbol")
Food_close = Food_stocks.pivot_table(values="close", index="timestamp",columns="symbol")
Food_close

#Calculate annual percentage change for each stock dataframe
# use resample to get annual data instead of daily
Real_Estate_stocks = Real_Estate_stocks.resample("Y").mean()
Real_estate_stock_annual = Real_Estate_stocks["close"].pct_change()
Real_estate_stock_annual.index = Real_estate_stock_annual.index.year
Real_estate_stock_annual

Apparel_stocks= Apparel_stocks.resample("Y").mean()
Apparel_stocks_annual= Apparel_stocks["close"].pct_change()
Apparel_stocks_annual.index = Apparel_stocks_annual.index.year

Food_stocks = Food_stocks.resample("Y").mean()
Food_stocks_annual = Food_stocks["close"].pct_change()
Food_stocks_annual.index = Food_stocks_annual.index.year
Apparel_stocks_annual

#Fetch percent change for each CPI measure
apparel_pct_change = annual_change["LA Apparel CPI"]
Food_pct_change = annual_change["LA Food Away from home CPI"]
Housing_pct_change = annual_change[ "LA Housing CPI"]
Housing_pct_change.dropna()

#Create a function to concat CPI data and stock data
def concat_stocks_cpi(stock, cpi):
    df = pd.concat([stock,cpi], axis=1, join="inner")
    return df

#Combine housing CPI and housing stocks
Housing_combined = concat_stocks_cpi(Real_estate_stock_annual, Housing_pct_change)
Housing_combined.columns = ['Real Estate stocks', "LA housing CPI"]
Housing_plot= Housing_combined.hvplot.line(xlabel="Year", ylabel="Annual Percent Change", title="LA Housing CPI and Real Estate Stocks annual percent change")



#Combine and plot Apparel CPI and stock data
Apparel_combined = concat_stocks_cpi(Apparel_stocks_annual, apparel_pct_change)
Apparel_combined.columns = ['Apparel stocks', "LA Apparel CPI"]
Apparel_plot= Apparel_combined.hvplot.line(xlabel="Year", ylabel="Annual Percent Change", title="LA Apparel CPI and Apparel stocks percent changes over time", rot=90)

#Combine and plot Food away from home CPI and stock data
Food_combined = concat_stocks_cpi(Food_stocks_annual, Food_pct_change)
Food_combined.columns = ['Food stocks', "LA Food Away from home CPI"]
Food_plot=Food_combined.hvplot.line(xlabel="Year", ylabel= "Annual Percent change", title="LA Food away home CPI percent change vs Food Stocks percent change", rot=90, ylim=(-0.2, 0.3), yticks=0.1, height=500)

#What is the relationship between the CPI percent change and real estate stocks?
covariance= Housing_pct_change.cov(Real_estate_stock_annual)
covariance

# Question 1. For each industry, during the biggest increase and decrease in CPI, what was the stock market trend?
def extract_max(df):
    return df[df.iloc[:, 1] == df.iloc[:, 1].max()]

def extract_min(df):
     return df[df.iloc[:, 1] == df.iloc[:, 1].min()]

def graph_max(df):
    bar = extract_max(df)
    graph = bar.plot.bar(ylabel="Percentage change", xlabel="Year", title="CPI Highest year and corresponding stock data")
    return graph

def graph_min(df):
    bar = extract_min(df)
    graph = bar.plot.bar(ylabel="Percentage change", xlabel="Year", title="CPI Lowest year and corresponding stock data")
    return graph

graph_max(Housing_combined)
graph_max(Food_combined)
graph_max(Apparel_combined)

#Qn 2. Which city has the largest rate of inflation for each industry?
#Import Philly and Seattle data
# set the file paths
file_path_4 = Path("Philly_combined_CPI.csv")
file_path_5= Path("seattle_data/seattle_cpi_data.csv")


# create a Pandas dataframe from a csv file
combined_philly_df = pd.read_csv(file_path_4, index_col='Year').dropna()
combined_seattle_df = pd.read_csv(file_path_5, index_col='Year').dropna()

#concatenate all 3 city CPI dataframes
combined_cities_cpi= pd.concat([combined_philly_df, combined_seattle_df, combined_df], axis="columns", join="inner")
combined_cities_cpi

combined_cpi_change=combined_cities_cpi.pct_change().dropna()
combined_cpi_change

#Fetch CPI data by industry 
combined_apparel_cpi= combined_cpi_change[["PHL Apparel Annual", "Seattle Apparel CPI", "LA Apparel CPI"]]
combined_food_cpi = combined_cpi_change[["PHL Commercial Food Annual", "Seattle Food Away from Home CPI", "LA Food Away from home CPI"]]
combined_housing_cpi = combined_cpi_change[["PHL Housing Annual", "Seattle Rental Equivalent CPI", "LA Housing CPI" ]]
combined_housing_cpi

housing_combined_plot= combined_housing_cpi.hvplot.line(x="Year", ylabel="Annual percent change", title="Housing YoY changes in LA, PHL, and Seattle")
housing_combined_plot

apparel_combined_plot= combined_apparel_cpi.hvplot.line(xlabel="Year", ylabel="Annual percent change", title="Apparel YoY changes in LA, PHL, and Seattle")
apparel_combined_plot

food_combined_plot= combined_food_cpi.hvplot.line(xlabel="Year", ylabel="Annual percent change", title="Food away from Home YoY changes in LA, PHL, and Seattle")
food_combined_plot