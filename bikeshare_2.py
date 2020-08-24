import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ["january", "february", "march", "april", "may", "june"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def get_filters():
    
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """
    city = ""
    month = ""
    day = ""
    
    city_selection = ""    
    timeframe_first_filter = ""
    timeframe_second_filter = ""

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city_selection not in {"ch", "ny", "w"}:
        city_selection = input("To view the available data, please type:\n'ch' for Chiacago\n'ny' for New York City\n'w' for Washington\n").lower()
        if city_selection == "ch":
            city = "chicago"
        elif city_selection == "ny":
            city = "new york city"
        elif city_selection == "w":
            city = "washington"
        else:
            print("invalid input. Try again!")
            time.sleep(1)

    # get the timeframe
    while timeframe_first_filter not in {"yes", "no"}:
        timeframe_first_filter = input("would you like to filter {}\'s data?\n'yes' if you would like\n'no' if you wouldn't\n".format(city.title())).lower()
        
        if timeframe_first_filter == "no":  # no filters required
            month = "all"
            day = "all"
        
        elif timeframe_first_filter == "yes":
            while timeframe_second_filter not in {'m', 'd', 'b'}:
                timeframe_second_filter = input("to filter the data by month type 'm'\nto filter the data by day type 'd'\nto filter the data by both type 'b'\n").lower()
            if timeframe_second_filter == "m":  # filter the month
                day = "all"
                while month not in MONTHS:
                    for item in MONTHS:
                        print(item)
                    month = input("choose the month using the list above\n").lower()         
            elif timeframe_second_filter == "d":    # filter the day
                month = "all"
                while day not in DAYS:
                    for item in DAYS:
                        print(item)
                    day = input("choose the day using the list above\n").lower()

            elif timeframe_second_filter == "b":    # filter both month and day
                while month not in MONTHS:
                    for item in MONTHS:
                        print(item)
                    month = input("choose the month using the list above\n").lower()
                while day not in DAYS:
                    for item in DAYS:
                        print(item)
                    day = input("choose the day using the list above\n").lower()
            else:   # invalid input
                print("invalid input. Try again!")
                time.sleep(1)
        else:   # invalid input
            print("invalid input. Try again!")
            time.sleep(1)

    print("loading the data for {} with the required filters.....".format(city))
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek


    # filter by month if applicable
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month = MONTHS.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the DAYS list to get the corresponding int
        day = DAYS.index(day)
        
        # filter by month to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month = MONTHS[df['month'].mode()[0] - 1]
    print("most common month is: {}".format(month))
    # display the most common day of week
    day = DAYS[df['day_of_week'].mode()[0]]
    print("most common day is: {}".format(day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour = df['hour'].mode()[0]
    print("most common start hour is: {}".format(hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("most commonly used start startion is: {}".format(start_station))
    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("most commonly used end startion is: {}".format(end_station))

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("most frequent combination of start station and end station is from '{}' to '{}'".format(combination[0], combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""    

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    hours, minutes, seconds = time_calculator(total_duration)
    print("total travel time is: {} hours, {} minutes and {} seconds".format(hours, minutes, seconds))

    # display mean travel time
    mean_duration = df['Trip Duration'].mean()
    hours, minutes, seconds = time_calculator(mean_duration)
    print("average travel time is: {} hours, {} minutes and {} seconds".format(hours, minutes, seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("number of subscribers is: {}".format(user_types['Subscriber']))
    print("number of Customers is: {}".format(user_types['Customer']))

    """ BE AWARE THAT ONLY CHICAGO AND NY CITY HAVE THESE 2 COLUMNS """
    if city != "washington":
    # Display counts of gender
        gender_counts = df['Gender'].value_counts()
        print("number of males is: {}".format(gender_counts['Male']))
        print("number of females is: {}".format(gender_counts['Female']))

    # Display earliest, most recent, and most common year of birth
        # earliest
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()

        print("earliest year of birth is: {}".format(earliest))
        print("most recent year of birth is: {}".format(most_recent))
        print("most common year of birth is: {}".format(most_common))

    else:
        print("There is no data for 'gender' or 'year of birth' in Washington city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def time_calculator(seconds):
    """ convert the time given in seconds to hours, minutes and seconds """
    hours = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60

    return hours, minutes, seconds

def display_raw_data(df, city):
    """ prompts the user if they would like to view 5 rows of the filtered data they chose"""
    user_answer = ""
    start = 0
    end = 5
    while user_answer  != "no":
        user_answer = input("would you like to display 5 rows from {}\'s data? 'yes' or 'no'\n".format(city)).lower()
        if user_answer == "no":
            print("Thank You!")
            break
        elif user_answer == "yes":
            start += 5
            end += 5
            print(df.iloc[start:end])
        else:
            print("invalid input. Try again!")
            time.sleep(1)

def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
