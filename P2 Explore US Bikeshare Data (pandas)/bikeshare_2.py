import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
       (str) a string representing one of the months included in the data
        
    '''
    while True:
        month = input('\nWhich month? January, February, March, April, May, or June?\n')
        if month.lower() not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print("Not an appropriate choice.")
        else:
            break

    return month


def get_day():
    '''Asks the user for a day and returns the specified day.

    Args:
        none.
    Returns:
        (int) day of the week, 1=Sunday, 2=Monday, etc...
    '''
    while True:
        day = input('\nWhich day? Please type your response as an integer (e.g., 1=Sunday).\n')
        if day.lower() not in ('0', '1', '2', '3', '4', '5', '6'):
                print("Not an appropriate choice.")
        else:
            break
        
    return day

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.

    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    while True:
        city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
        if city.lower() not in ('chicago', 'new york', 'washington'):
                print("Not an appropriate choice.")
        else:
            break    
 
       
    return city.lower()

def get_filters():
    '''
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    '''
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=get_city()
    
    time_period={'filter':'','filter_value':''}

    while True:
            filter = input('\nWould you like to filter the data by month, day, or not at'
                            ' all? Type "none" for no time filter.\n')
            if filter.lower() not in ('month', 'day', 'none'):
                    print("Not an appropriate choice.")
            else:
                break        
  
    if filter.lower() =='month':
        filter_value=get_month().lower()
    elif filter.lower() == 'day':
        filter_value=get_day()   
    else:
        filter_value="none"

    time_period['filter']=filter
    time_period['filter_value']=filter_value
            
    print('-'*40)

    return city, time_period

def load_data(city, time_period):
    '''
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    '''

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.strftime('%H')
    
    

    # filter by month if applicable
    if time_period['filter'] == 'month':
        # filter by month to create the new dataframe
        month = time_period['filter_value'].title()
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if time_period == 'day':
        # filter by day of week to create the new dataframe
        days = {'0':'Sunday', '1':'Monday', '2':'Tuesday', '3':'Wednesday', '4':'Thursday','5': 'Friday', '6':'Saturday'}
        day = days[time_period['filter_value']]
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df,time_period):
    '''Displays statistics on the most frequent times of travel.'''

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if time_period['filter'] == 'none':
        # display the most common month
        month_list = df['month'].value_counts().index.tolist()
        popular_month = str(month_list[0])
        print('The most popular month is {0}.'.format(popular_month))
    
    if time_period['filter'] == 'none' or time_period['filter'] =='month':
        # display the most common day of week
        day_list = df['day_of_week'].value_counts().index.tolist()
        popular_day = str(day_list[0])
        print('The most popular day is {0}.'.format(popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour is {0}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,time_period):
    '''Displays statistics on the most popular stations and trip.'''

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    grp_start_end_size = df.groupby(['Start Station']).size().reset_index(name='trip_count')
    # sorts size() number in order from biggest to smallest
    sort = grp_start_end_size.sort_values('trip_count', ascending = False).drop_duplicates(['Start Station'])
    # now that we sorted we can just read values off the first row
    pop_start = sort['Start Station'].iloc[0]
    pop_start_cnt = sort['trip_count'].iloc[0]
    print('The most popular start station is {0}, with {1} trips.'.format(pop_start, pop_start_cnt))


    # display most commonly used end station
    grp_start_end_size = df.groupby(['End Station']).size().reset_index(name='trip_count')
    # sorts size() number in order from biggest to smallest
    sort = grp_start_end_size.sort_values('trip_count', ascending = False).drop_duplicates(['End Station'])
    # now that we sorted we can just read values off the first row
    pop_end = sort['End Station'].iloc[0]
    pop_end_cnt = sort['trip_count'].iloc[0]
    print('The most popular end station is {0}, with {1} trips.'.format(pop_end, pop_end_cnt))


    # display most frequent combination of start station and end station trip
    grp_start_end_size = df.groupby(['Start Station', 'End Station']).size().reset_index(name='trip_count')
    # sorts size() number in order from biggest to smallest
    sort = grp_start_end_size.sort_values('trip_count', ascending = False).drop_duplicates(['Start Station', 'End Station'])
    # now that we sorted we can just read values off the first row
    pop_trip_start = sort['Start Station'].iloc[0]
    pop_trip_end = sort['End Station'].iloc[0]
    pop_trip_cnt = sort['trip_count'].iloc[0]
    rtn_tuple=(pop_trip_start, pop_trip_end, pop_trip_cnt)
    print('The most popular trip from {0} to {1} station, with {2} trips.'.format(rtn_tuple[0], rtn_tuple[1], rtn_tuple[2]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def seconds_converter(seconds):
    m,s = divmod(seconds, 60)
    h,m = divmod(m,60)
    return "%d Days %02d Minutes %02d Seconds" % (h,m,s)

def trip_duration_stats(df,time_period):
    '''Displays statistics on the total and average trip duration.'''

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel = df['Trip Duration'].sum()
    str_tot_travel =seconds_converter(tot_travel)

    avg_travel = df['Trip Duration'].mean()
    str_avg_travel =seconds_converter(avg_travel)

    print('The total travel duraton is {0}.'.format(str_tot_travel))
    # display mean travel time
    avg_travel = df['Trip Duration'].mean()
    print('The average travel duraton is {0}.'.format(str_avg_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,time_period):
    '''Displays statistics on bikeshare users.'''

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    gender = df['Gender'].value_counts()
    print(gender)

    # Display earliest, most recent, and most common year of birth
    earliest=df['Birth Year'].min()
    print('The earliest birth year is {0}.'.format(earliest))
    recent=df['Birth Year'].max()
    print('The most recent birth year is {0}.'.format(recent))
    most_common=df['Birth Year'].mode()[0]
    print('The most common birth year is {0}.'.format(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, time_period = get_filters()
        df = load_data(city, time_period)

        time_stats(df, time_period)
        station_stats(df, time_period)
        trip_duration_stats(df, time_period)
        if city != 'washington':
            user_stats(df, time_period)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
