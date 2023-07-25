# Simulation-of-the-spread-of-Covid-19-using-Python

Introduction
The purpose of the assignment is to simulate the spread of COVID-19 in some specified countries, using a set of data that are provided to you. For this matter, you need to create a sample population of people according to the data provided (sample ration is provided in the test.py, for example one sample per one million population). This should be done according to the age structure in each country (percentage of population in each age group).

Then for each individual in the sample you run a simulation (a Markov Chain similar to assignment 2) for a specific period of steps (days). Starting and ending dates are provided to you in (the test.py).The Markov chain simulation should consider 5 states (H,I,S,M,D) which are described later. This result needs to be exported to a CSV file (a3-covid-simulated-timeseries.csv).

At the end you need to accumulate data for each specified country and each date (see the Output section). The result should be saved as (a3-covid-summary-timeseries.csv). Then you need to call create_plot() function, provided to you ,to create a chart (a3-covid-simulation.png)

About Creating Samples
You need to create samples for each specified country, according to the sample ratio, the population of the specified countries, and the age structure (age group) distribution in those countries. For example if the specified countries are 'Australia' and 'Sweden'. Then by reading a3-countries.csv you notice that Australia has a population of 25921089 which means for a sample ratio of 1e6 you need to create 25 samples. However, you also notice from the same file that the age group distribution in Australia is like this: less_5 ⇒ 6.5% ,5_to_14 ⇒ 12.7% ,15_to_24 ⇒ 12.2%, 25_to_64 ⇒ 52.3% and over_65 ⇒ 16.2%. Which means that the number of samples for each age group should be 25*percentage/100 (rounded to integer). With this approach, some age groups might have zero sample. Also, note that you should do the same for other specified countries (Sweden in this example) and keep them along other countries.

You can imagine that a smaller sample ration can create finer simulation results. However, we tried to keep the value in a range that does not take a long time for simulation. You may want to test your code, for your own sake, with smaller values.

About Time-Series
There is a starting date ('2021-04-01' in the test.py) and ending date ('2022-04-30' in the test.py) for the simulation (395 days totally). You need to create a data structure to store the state of each sample in each date in this range (you may use standard features such as list and dictionary, or instead use DataFrame in pandas). This data structure is going to be filled in by your simulation result. Please note that starting and ending dates might change in the evaluation (so the total number of days in the simulation). This time-series data structure is going to be save to a CSV file later.

Note about the size of the time-series. For an example, for countries Afghanistan, Sweden, and Japan with 166 million population totally, with a sample ratio of 1e6 you will have 166 sample population. Then for 395 days that will be 166*395 = 65965 records to store. There is a technical suggestion for implementing this time-series, later in this instruction.

About Simulation for Individual Samples
The simulation of infection with COVID-19 for each individual is shown in the Markov Chain in the image below:
![assignment3_markov_chain](https://github.com/jotheesh1729/Simulation-of-the-spread-of-Covid-19-using-Python-S/assets/66893484/2cf15ade-183b-4c58-b7b7-a32d28c4f8cb)

