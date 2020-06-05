import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    month = ""
    day = ""
    while city not in CITY_DATA:
        city = input("What city do you want to look at?").lower()

    #get user input for month (all, january, february, ... june)
    monthoptions = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while month not in monthoptions:
        month = input("What month (or \"all\") do you want to filter by?").lower()
        if month not in monthoptions:
            print("Not a valid entry. Please try again.")

    #get user input for day of week (all, monday, tuesday, ... sunday)
    dayoptions = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    while day not in dayoptions:
        day = input("What day of the week (or \"all\") do you want to filter by?").lower()
        if day not in dayoptions:
            print("Not a valid entry. Please try again.")


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
    #get file
    df = pd.read_csv(CITY_DATA[city])

    #convert to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #filter by month
    df['month'] = df['Start Time'].dt.month
    df['month'] = df['month'].replace([1,2,3,4,5,6], ['January', 'February', 'March', 'April', 'May', 'June'])
    if month != 'all':
        df = df[df['month'] == month.title()]

    #filter by dayofweek
    df['dayofweek'] = df['Start Time'].dt.weekday_name
    if day != 'all':
        df = df[df['dayofweek'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    popmonth = df['month'].mode()[0]
    print("The most popular month to travel is ", popmonth)

    #display the most common day of week
    popdow = df['dayofweek'].mode()[0]
    print("The most popular day of the week to travel is ", popdow)

    #display the most common start hour
    pophour = df['Start Time'].dt.hour.mode()[0]%12
    AMorPM = " "
    if pophour/12 == 0:
        AMorPM = "AM"
    else:
        AMorPM = "PM"
    print("The most popular hour of the day to travel is {} {}".format(pophour,AMorPM))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays stats on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    popstart = df['Start Station'].mode()[0]
    print("The most popular starting station is ", popstart)

    #display most commonly used end station
    popend = df['End Station'].mode()[0]
    print("The most popular ending station is ", popend)

    #display most frequent combination of start station and end station trip
    popcombo = ("starting at "+df['Start Station']+" ending at "+df['End Station']).mode()[0]
    print("The most popular start and end station combo is ", popcombo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays stats on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    total_travel_seconds = sum(df['Trip Duration'])
    total_days = total_travel_seconds//86400
    add_hours = (total_travel_seconds%86400)//3600
    add_mins = (total_travel_seconds%3600)//60
    add_secs = total_travel_seconds%60
    print("The total travel time for this subset of data was {} seconds".format(total_travel_seconds))
    print("This total travel time is equivalent to {} days, {} hours, {} minutes, and {} seconds\n".format(total_days,add_hours,add_mins,add_secs))

    #Display mean travel time
    mean_travel_seconds = df['Trip Duration'].mean()
    mean_mins = mean_travel_seconds//60
    mean_secs = mean_travel_seconds%60
    print("The mean travel time for this subset of data was {} seconds".format(mean_travel_seconds))
    print("This mean travel time is equivalent to {} minutes and {} seconds".format(mean_mins,mean_secs))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,"\n")

    #Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print(gender_counts,"\n")
    except KeyError:
        print("No gender information is available for this subset of data\n")

    #Display earliest, most recent, and most common year of birth
    try:
        early_year = int(df['Birth Year'].min())
        print("The earliest birth year is", early_year)

        recent_year = int(df['Birth Year'].max())
        print("The most recent birth year is", recent_year)

        most_common_birth = int(df['Birth Year'].mode()[0])
        print("The most common birth year is", most_common_birth)

    except KeyError:
        print("Birth year information is not available for this subset of data\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    line = 0
    while True:
        five_boole=input('Would you like to see 5 lines of raw data? Indicate "yes" or "no".').lower()
        if five_boole == "yes":
            print(df.iloc[line:line+5])
            line+=5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Show five lines of raw data if requested
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
