import pandas, pymongo, json, csv, time, fileinput
client = pymongo.MongoClient()

db = client['streaming_recommender']

ratings_collection = db['ratings']
ratings_collection.drop()
movies_collection = db['movies']
movies_collection.drop()
movies_to_rate = db['movies_to_rate']
movies_to_rate.drop()

# Load the movie ids and names into mongo
csv = csv.reader(open('data/ml-latest/movies.csv','rb'), delimiter=',', quotechar='"')
for line in csv:
    if line[0]=='movieId': continue
    (movieId, movieTitle, genres) = line
    print line
    movies_collection.insert_one({'movie':movieId, 'movieTitle': movieTitle})
users_collection = db['active_users']
users_collection.insert_one({'user':1})



# Load the top 1000 most-rated movies with their name in movies_to_rate
# Also, store these top 1000 in a set for later
top_movie_ids = set()

csv = pandas.read_csv('data/ml-latest/ratings.csv')
grouped=csv.groupby('movieId').count()
sorted=grouped.sort_values('userId', ascending=False)
f = open('sample_movies.csv','w')

output=[]
for sample_movie in sorted.index.values[:1000]:
    print 'finding name of ', sample_movie
    results = movies_collection.find(filter={'movie': str(sample_movie)})
    print results
    print results[0]['movieTitle']
    name=results[0]['movieTitle']
    output += [[str(sample_movie), name]]
    movies_to_rate.insert_one({"movieId": str(sample_movie), "name":name})
    top_movie_ids.add(str(sample_movie))

# Now load the actual ratings from Movielens. Only ratings for the top 
# 1000 movies are included.

users=set()
bulk=ratings_collection.initialize_unordered_bulk_op()
i=0
for line in fileinput.input("data/ml-latest/ratings.csv"):
    if i > 1000000: break
    if fileinput.isfirstline():
        continue
    (user, movie, rating, _time) = line.split(',')
    if movie not in top_movie_ids: continue
    users.add(user)
    if rating == '0':
        # In the Movielens file, ratings of 0 are bad data
        continue
    struct = {'user':user, 'movie':movie, 'rating':float(rating), 'source':'movielens'}
    bulk.insert(struct)
    if i%10000==0: print i
    i += 1
bulk.execute()

print "USERS"
print len(users)
