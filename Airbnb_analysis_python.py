import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium


# Load the dataset
listings_df = pd.read_csv('C:/Users/sotin/Downloads/listings.csv.gz')
reviews_df = pd.read_csv('C:/Users/sotin/Downloads/reviews.csv.gz')
#print(listings_df.head())
#print(reviews_df.head())


# Calculate total reviews per listing
#total_reviews_per_listing = reviews_df.groupby('listing_id')['comments'].value_counts()

# Calculate total reviews per listing
total_reviews_per_listing = reviews_df.groupby('listing_id').size()

# Plot the data in a bar chart
plt.figure(figsize=(12, 6))
total_reviews_per_listing.plot(kind='bar')
plt.title('Distribution of Total Reviews per Listing')
plt.xlabel('Listing ID')
plt.ylabel('Total Number of Reviews')
plt.xticks(rotation=45)
plt.show()




# Task 1: Calculate reviews per year
reviews_df['year'] = pd.to_datetime(reviews_df['date']).dt.year
#print(reviews_df['year'].head())
reviews_per_year = reviews_df['year'].value_counts().sort_index()
#print(reviews_per_year)
reviews_per_year.plot(kind='bar', title='Reviews per Year')
plt.xlabel('Year')
plt.ylabel('Number of Reviews')
plt.show()

# Task 2: Listings per room type
listings_per_room_type = listings_df['room_type'].value_counts()
#print(listings_per_room_type)
listings_per_room_type.plot(kind='bar', title='Listings per Room Type')
plt.xlabel('Room Type')
plt.xticks(rotation=45)
plt.ylabel('Number of Listings')
plt.show()

# Task 3: Bookings per property type
bookings_per_property_type = listings_df.groupby('property_type').size().sort_values(ascending = False)[:20]
#print(bookings_per_property_type)
bookings_per_property_type.plot(kind='bar', title='Bookings per Property Type')

plt.xlabel('Property Type')
plt.xticks(rotation=45)
plt.ylabel('Number of Bookings')
plt.show()

bookings_per_property_type = listings_df.groupby('property_type').size().sort_values(ascending = False)[20:]
#print(bookings_per_property_type)
bookings_per_property_type.plot(kind='bar', title='Bookings per Property Type')

plt.xlabel('Property Type')
plt.xticks(rotation=45)
plt.ylabel('Number of Bookings')
plt.show()


# Task 4: Average reviews per room type
average_reviews_per_room_type = listings_df.groupby('room_type')['number_of_reviews'].mean()
#print(average_reviews_per_room_type)
average_reviews_per_room_type.plot(kind='bar', title='Average Reviews per Room Type')
plt.xlabel('Room Type')
plt.xticks(rotation=45)
plt.ylabel('Average Number of Reviews')
plt.show()

# Task 5: Total bookings per neighborhood
total_bookings_per_neighborhood = listings_df['neighbourhood_cleansed'].value_counts().nlargest(10)
#print(total_bookings_per_neighborhood)
total_bookings_per_neighborhood.plot(kind='bar', title='Total Bookings per Neighborhood')
plt.xlabel('Neighborhood')
plt.xticks(rotation=45)
plt.ylabel('Total Bookings')
plt.show()

# Task 6: Average listings per host
average_listings_per_host = listings_df.groupby('host_id').size().mean()
print("Average Listings per Host:", average_listings_per_host)
plt.figure(figsize=(10,6))
plt.bar(['Average Listings per Host'], [average_listings_per_host])
plt.title('Average Listings per Host')
plt.xlabel('Metric')
plt.xticks(rotation=45)
plt.ylabel('Average Number of Listings')
plt.show()

# Task 7: Total reviews per listing
total_reviews_per_listing = reviews_df['listing_id'].value_counts()
total_reviews_per_listing.plot(kind='hist', bins=30, title='Distribution of Total Reviews per Listing')
plt.xlabel('Total Reviews')
plt.ylabel('Number of Listings')
plt.show()

# Task 8: Total reviews per instant bookable flag
reviews_per_instant_bookable = listings_df.groupby('instant_bookable')['number_of_reviews'].sum()
reviews_per_instant_bookable.plot(kind='bar', title='Total Reviews per Instant Bookable Flag')
plt.xlabel('Instant Bookable')
plt.ylabel('Total Reviews')
plt.show()

# Task 9: Most and least common amenities
amenities_counts = listings_df['amenities'].str.strip('[]').str.split(',').explode().str.strip().value_counts()
most_common_amenities = amenities_counts.head(10)
least_common_amenities = amenities_counts.tail(10)

most_common_amenities.plot(kind='bar', title='Top 10 Most Common Amenities')
plt.xlabel('Amenity')
plt.ylabel('Count')
plt.show()

least_common_amenities.plot(kind='bar', title='Top 10 Least Common Amenities')
plt.xlabel('Amenity')
plt.ylabel('Count')
plt.show()



#calendar data analysiss
calendar_df = pd.read_csv('C:/Users/sotin/Downloads/calendar.csv.gz')
print(calendar_df.head())
calendar_df['price'] = calendar_df['price'].replace(r'[\$,]', '', regex=True).astype(float)
calendar_df['date'] = pd.to_datetime(calendar_df['date'])
calendar_df['month'] = calendar_df['date'].dt.month
calendar_df['day_of_week'] = calendar_df['date'].dt.day_name()
print(calendar_df['available'].unique())
calendar_df['available'] = calendar_df['available'].replace({'f': 0, 't': 1})

# Average availability per month
availability_per_month = calendar_df.groupby('month')['available'].mean()
availability_per_month.plot(kind='line', marker='o', title='Average Availability per Month')
plt.xlabel('Month')
plt.ylabel('Availability')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()

# Average price per month
calendar_df['price'] = calendar_df['price'].replace('[\$,]', '', regex=True).astype(float)
average_price_per_month = calendar_df.groupby('month')['price'].mean()
average_price_per_month.plot(kind='line', marker='o', title='Average Price per Month')
plt.xlabel('Month')
plt.ylabel('Average Price')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.show()

# Average availability per day of week
availability_per_day = calendar_df.groupby('day_of_week')['available'].mean()
availability_per_day = availability_per_day.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
availability_per_day.plot(kind='bar', title='Average Availability per Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Availability')
plt.show()


'''
#textural data analysis
from textblob import TextBlob

# Sentiment analysis of reviews
reviews_df['polarity'] = reviews_df['comments'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
reviews_df['subjectivity'] = reviews_df['comments'].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)

# Distribution of polarity and subjectivity
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.histplot(reviews_df['polarity'], bins=30, kde=True)
plt.title('Distribution of Polarity in Reviews')
plt.xlabel('Polarity')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
sns.histplot(reviews_df['subjectivity'], bins=30, kde=True)
plt.title('Distribution of Subjectivity in Reviews')
plt.xlabel('Subjectivity')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
'''

# Word cloud of most frequent words in reviews
from wordcloud import WordCloud

text = ' '.join(reviews_df['comments'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Reviews')
plt.show()




# Load your data
#listings_df = pd.read_csv('C:/Users/sotin/Downloads/listings.csv.gz')
#listings_df['price'] = listings_df['price'].replace('[\$,]', '', regex=True).astype(float)
listings_df['price'] = listings_df['price'].replace('[\$,]', '', regex=True).astype(float)
listings_df = listings_df.dropna(subset=['price']) #remove nan
# Sort the DataFrame by 'price' to get the top 20 most expensive and least expensive listings
top_20_expensive = listings_df.nlargest(50, 'price')
top_20_least_expensive = listings_df.nsmallest(50, 'price')
#print(top_20_expensive)
#print(top_20_least_expensive)
# Create a map centered around the average latitude and longitude
map_ = folium.Map(location=[listings_df['latitude'].mean(), listings_df['longitude'].mean()], zoom_start=10)

# Add markers for the top 20 most expensive listings
for _, listing in top_20_expensive.iterrows():
    folium.Marker(
        location=[listing['latitude'], listing['longitude']],
        popup=f"Price: ${listing['price']}",
        icon=folium.Icon(color='red')
    ).add_to(map_)

# Add markers for the top 20 least expensive listings
for _, listing in top_20_least_expensive.iterrows():
    folium.Marker(
        location=[listing['latitude'], listing['longitude']],
        popup=f"Price: ${listing['price']}",
        icon=folium.Icon(color='green')
    ).add_to(map_)


# Display the map
map_

# Save the map to an HTML file
map_.save('C:/Users/sotin/Downloads/map.html')

# If you want to display the map within a Jupyter notebook, you can simply display the map object:
# map_