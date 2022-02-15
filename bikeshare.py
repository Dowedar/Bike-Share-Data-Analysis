import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = 'January,February,March,April,May,June'.lower().split(',')
days_of_week = 'Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday'.lower().split(',')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=''
    while city not in city_data:
        city = input('please select the city to analyze:chicago,new york city,washington\n'.title()).lower()      
    # get user input for month (all, january, february, ... , june)
    month = ''
    while month not in months:
        month = input('please Enter a specific month to filter:january,february,march,april,may,june or select all\n'.title()).lower()
        if month == 'all':
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day= ''
    while day not in days_of_week:
        day = input('Please enter a day of week:monday,tuesday,wednesday,thursday,friday,saturday,sunday or select all\n'.title()).lower()
        if day =='all':
            break 
    return city,month,day

def load_data(city,month,day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        data - Pandas DataFrame containing city data filtered by month and day
    """
    data = pd.read_csv(city_data[city],index_col=0)
    date = pd.to_datetime(data['Start Time'], format='%Y-%m-%d')
    data['Day'] = date.dt.day_name()
    data['Month'] = date.dt.month_name()
    if month == 'all' and day != 'all':
        data =  data[data['Day']==day.title()]
    elif month!='all'and day=='all':
        data = data[data['Month']==month.title()]
    elif month!='all'and day!='all':
       data = data[(data['Month']==month.title())&(data['Day']==day.title())]
    else:
        None
    return data

def time_stats(data):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    number_of_months = len(data['Month'].value_counts())
    number_of_days = len(data['Day'].value_counts())
    if number_of_months>1 and number_of_days>1:
      # display the most common month
      common_month =data['Month'].value_counts().head(1).index[0]
      print('the most coommon month is {}\n'.title().format(common_month))
      # display the most common day of week
      common_day =data['Day'].value_counts().head(1).index[0]
      print('the most common day of week is {}\n'.title().format(common_day))
    elif number_of_days>1 and number_of_months==1:
      # display the most common day of week
      common_day =data['Day'].value_counts().head(1).index[0]
      print('the most common day of week is {}\n'.title().format(common_day))
    elif number_of_months>1 and number_of_days==1 :
      # display the most common month
      common_month =data['Month'].value_counts().head(1).index[0]
      print('the most coommon month is {}\n'.title().format(common_month))
    else:
        None
    # display the most common start hour
    data['Hour'] =pd.DatetimeIndex(data['Start Time']).hour   
    common_start_hour = data['Hour'].value_counts().head(1).index[0]
    print('Most Frequent Start Hour is {}'.title().format(common_start_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(data):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    common_start_station = data['Start Station'].value_counts().head(1).index[0]
    print('the most common start station is {}\n'.title().format(common_start_station))
    # display most commonly used end station
    common_end_station = data['End Station'].value_counts().head(1).index[0]
    print('the most common end station is {}\n'.title().format(common_end_station))
    # display most frequent combination of start station and end station trip
    frequent_start_end_station = data[['Start Station','End Station']].value_counts().head(1).index[0]
    print('the most frequent combination is {} as start station and {} as end station'.title().format(frequent_start_end_station[0],frequent_start_end_station[1]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(data):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # display total travel time
    print('the total travel time in seconds is {}\n'.title().format(data['Trip Duration'].sum()))
    # display mean travel time
    print('the average travel time in seconds is {}'.title().format(np.average(data['Trip Duration'])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(data):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user 
    for index, name in enumerate(data['User Type'].value_counts().index.tolist()):
      print('User Type: {}: counts: {}\n'.title().format(name,data['User Type'].value_counts()[index]))
    # Display counts of gender
    try:
       for index, name in enumerate(data['Gender'].value_counts().index.tolist()):
         print('Gender Type: {}: counts: {}\n'.title().format(name,data['Gender'].value_counts()[index]))
    except:
        None  
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year =  int(data['Birth Year'].dropna().sort_values( ).unique()[0])
        most_recent_year = int(data['Birth Year'].dropna().sort_values( ).unique()[-1])
        common_year = int(data['Birth Year'].value_counts().index[0])
        print('the earliest Year of birth is {}\n'.title().format(earliest_year))
        print('the most recent year of birth is {}\n'.title().format(most_recent_year))
        print('the most common year of birth is {}'.title().format(common_year))
    except:
        None
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(data):
    """Displays 5 rows of data each time the user request"""
    display_5_data= input('\nwould you like to display the first 5 rows of data? Enter yes or no\n'.title()).lower()
    if display_5_data =='no':
        print('-'*40)
    start_count = 0
    while display_5_data == 'yes':
       print('\nDisplaying Data...\n')
       start_time = time.time()
       print(data.iloc[start_count:start_count + 5])
       start_count += 5
       print("This took %s seconds." % (time.time() - start_time))
       print('-'*40)
       display_5_data= input('would you like to display the next 5 rows of data? Enter yes or no\n'.title()).lower()
       if display_5_data == "no":
          print('-'*40)
          break
          



def main():
 while True:
        city, month, day = get_filters()
        data = load_data(city, month, day)

        time_stats(data)
        station_stats(data)
        trip_duration_stats(data)
        user_stats(data)
        display_data(data)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()