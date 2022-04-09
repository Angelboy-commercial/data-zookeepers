csvpath = Path("..\seattle_data\Seattle_Apparel_CPI.csv")
seattleCPI_apparel_df = pd.read_csv(csvpath)

csvpath1 = Path("..\seattle_data\Seattle_FoodAwayFromHome_CPI.csv")
seattleCPI_FoodAway_df = pd.read_csv(csvpath1)

csvpath3 = Path("..\seattle_data\Seattle_RentalEquivalent_CPI.csv")
seattleCPI_RentalEquivalent_df = pd.read_csv(csvpath3)

seattleCPI_apparel_df.reset_index(drop=True, inplace=True)
seattleCPI_apparel_df.set_index("Year", inplace=True)

seattleCPI_FoodAway_df.reset_index(drop=True, inplace=True)
seattleCPI_FoodAway_df.set_index("Year", inplace=True)

seattleCPI_RentalEquivalent_df.reset_index(drop=True, inplace=True)
seattleCPI_RentalEquivalent_df.set_index("Year", inplace=True)


seattleCPI_apparel_df.rename(columns= {'Annual': 'Seattle Apparel CPI'}, inplace= True)
seattleCPI_FoodAway_df.rename(columns= {'Annual': 'Seattle Food Away from Home CPI'}, inplace= True)
seattleCPI_RentalEquivalent_df.rename(columns= {'Annual': 'Seattle Housing CPI'}, inplace= True)

seattleCPI_apparel_pctchange = seattleCPI_apparel_df.pct_change()
seattleCPI_FoodAway_pctchange = seattleCPI_FoodAway_df.pct_change()
seattleCPI_RentalEquivalent_pctchange = seattleCPI_RentalEquivalent_df.pct_change()

