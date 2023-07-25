import datetime

from covid_simulator import CovidSimulation
import pandas as pd
import helper
import random
import csv


def exportSimulatedToCsv(filename, columns, dataList):
    """
    Export the simulated time series result to a csv file
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(columns)  # Writing Header at first row

        # Writing the csv file row by row
        for data in dataList:
            tmpList = []

            # Retrieve data from dictionary to list
            for item in columns:
                tmpList.append(data[item])

            # Writing the constructed data list to a single row
            writer.writerow(tmpList)


def exportSummaryToCsv(filename, summary):
    """
    Export the summary time series result to a csv file
    """
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["date", "country", "D", "H", "I", "M", "S"])  # Writing Header at first row

        # Retrieve data from dictionary to list and write to the csv file row by row
        for date, country_info in summary.items():
            for country, states_info in country_info.items():
                writer.writerow([date, country, states_info["D"], states_info["H"], states_info["I"], states_info["M"], states_info["S"]])


def generateTimelinePopulationAndSimulation(population_list, start_date, end_date):
    """
    Generate the timeline for each individuals and run the COVID simulation for a given date range
    """
    timeline_population = []

    # Loop through sample population individually
    for individual in population_list:

        # Create COVID Simulator with id, age group and country specified.
        simulator = CovidSimulation(id=individual["person_id"],
                                    age_group=individual["age_group_name"],
                                    country=individual["country"],
                                    init_state='H')

        # First Day - Initial State
        tmp_dict = individual.copy()
        tmp_dict["date"] = start_date
        tmp_dict["state"], tmp_dict["staying_days"], tmp_dict["prev_state"] = simulator.getResults()
        timeline_population.append(tmp_dict)
        new_start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=1)

        # Run COVID simulation day by day
        for date in pd.date_range(start=new_start_date.strftime('%Y-%m-%d'), end=end_date):
            tmp_dict = individual.copy()
            tmp_dict["date"] = date.strftime('%Y-%m-%d')

            # Trigger simulation for a single day
            simulator.simulate()

            # Getting the simulation results
            tmp_dict["state"], tmp_dict["staying_days"], tmp_dict["prev_state"] = simulator.getResults()

            # Save the result into a list
            timeline_population.append(tmp_dict)
    print(timeline_population)

    return timeline_population


def summarizeNumOfStates(dataList, start_date, end_date, country_list):
    """
    Summarize the number of states for each date for each specified country.

    Example output
    summary_dict = {
        "2021-04-01": {"Sweden": {"D":0, "H":7, "I":3, "M":0, "S":0}},
        "2021-04-01": {"Japan": {"D":0, "H":96, "I":28, "M":0, "S":0}},
        "2021-04-02": {"Sweden": {"D":0, "H":3, "I":7, "M":0, "S":0}},
        "2021-04-02": {"Japan": {"D":0, "H":72, "I":52, "M":0, "S":0}},
        ...
    }
    """
    summary_dict = {date.strftime('%Y-%m-%d'): {country: {"D": 0, "H": 0, "I": 0, "M": 0, "S": 0} for country in country_list} for date in pd.date_range(start=start_date, end=end_date)}
    for data in dataList:
        summary_dict[data["date"]][data["country"]][data["state"]] += 1
    return summary_dict


def generateSamplePopulation(population_df, country_list, sample_ratio):
    """
    Create a sample population according to the population of each specified country and its age group distributions.
    """
    sample_population = []
    count_all = 0

    # Loop for each specified countries
    for country in country_list:
        # Get the row index of the dataframe for the specified country
        index = population_df.country[population_df.country == country].index[0]

        # Get the number of samples based on the sample ratio
        population = float(population_df.iloc[index].population) / sample_ratio

        # Get the percentage of the age group distribution (0 to 100%)
        perc_less_5 = float(population_df.loc[index, 'less_5'])
        perc_5_to_14 = float(population_df.loc[index, '5_to_14'])
        perc_15_to_24 = float(population_df.loc[index, '15_to_24'])
        perc_25_to_64 = float(population_df.loc[index, '25_to_64'])
        perc_over_65 = float(population_df.loc[index, 'over_65'])
        count = 0

        # Creating individuals in less_5 age group
        for i in range(int(population * perc_less_5 / 100)):
            sample_population.append({"person_id": count_all + count, "age_group_name": "less_5", "country": country})
            count += 1

        # Creating individuals in 5_to_14 age group
        for i in range(int(population * perc_5_to_14 / 100)):
            sample_population.append({"person_id": count_all + count, "age_group_name": "5_to_14", "country": country})
            count += 1

        # Creating individuals in 15_to_24 age group
        for i in range(int(population * perc_15_to_24 / 100)):
            sample_population.append({"person_id": count_all + count, "age_group_name": "15_to_24", "country": country})
            count += 1

        # Creating individuals in 25_to_64 age group
        for i in range(int(population * perc_25_to_64 / 100)):
            sample_population.append({"person_id": count_all + count, "age_group_name": "25_to_64", "country": country})
            count += 1

        # Creating individuals in over_65 age group
        for i in range(int(population * perc_over_65 / 100)):
            sample_population.append({"person_id": count_all + count, "age_group_name": "over_65", "country": country})
            count += 1

        # Randomly create individuals (Based on the age group distribution percentage) for the remaining slots
        # to fulfil the number of the samples required
        if count < int(population):
            for i in range(0, int(population) - count):
                randomValue = random.randint(1, 100)
                if randomValue <= perc_less_5:
                    sample_population.append({"person_id": count_all + count, "age_group_name": "less_5", "country": country})
                elif randomValue <= (perc_less_5 + perc_5_to_14):
                    sample_population.append({"person_id": count_all + count, "age_group_name": "5_to_14", "country": country})
                elif randomValue <= (perc_less_5 + perc_5_to_14 + perc_15_to_24):
                    sample_population.append({"person_id": count_all + count, "age_group_name": "15_to_24", "country": country})
                elif randomValue <= (perc_less_5 + perc_5_to_14 + perc_15_to_24 + perc_25_to_64):
                    sample_population.append({"person_id": count_all + count, "age_group_name": "25_to_64", "country": country})
                else:
                    sample_population.append({"person_id": count_all + count, "age_group_name": "over_65", "country": country})

                count += 1
        count_all += count

    return sample_population


def run(countries_csv_name, countries, sample_ratio, start_date, end_date):

    # Read the CSV file and store it in a data structure.
    actual_population_df = pd.read_csv(countries_csv_name)

    # Create a sample population according to the population of each specified country and its age group distributions.
    sample_population = generateSamplePopulation(population_df=actual_population_df,
                                                 country_list=countries,
                                                 sample_ratio=sample_ratio)

    # Create a timeline for all individuals in the population and for the specified days of simulation
    # Then simulate for each day and store in wide-table format
    timeline_population = generateTimelinePopulationAndSimulation(population_list=sample_population,
                                                                  start_date=start_date,
                                                                  end_date=end_date)

    # Export the simulated time series results to a csv file
    exportSimulatedToCsv(filename="a3-covid-simulated-timeseries.csv",
                         columns=timeline_population[0].keys(),
                         dataList=timeline_population)

    # Summarize (accumulate) the number of states for each date for each specified country.
    summary = summarizeNumOfStates(dataList=timeline_population,
                                   start_date=start_date,
                                   end_date=end_date,
                                   country_list=countries)

    # Export the summary to a csv file
    exportSummaryToCsv(filename="a3-covid-summary-timeseries.csv", summary=summary)

    # Plot the final result
    helper.create_plot(summary_csv="a3-covid-summary-timeseries.csv", countries=countries)
