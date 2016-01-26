import pyspark.mllib.recommendation, time, sys

sc=pyspark.SparkContext()
onfig = config_activeusers = {"mongo.input.uri": "mongodb://localhost:27017/streaming_recommender.active_users"}
   {"mongo.input.uri": 
    "mongodb://localhost:27017/streaming_recommender.active_users"}
   ).
inputFormatClassName = "com.mongodb.hadoop.MongoInputFormat"
keyClassName = "org.apache.hadoop.io.Text"
valueClassName = "org.apache.hadoop.io.MapWritable"
outputFormatClassName='com.mongodb.hadoop.MongoOutputFormat',

ratings = (sc.newAPIHadoopRDD(
   inputFormatClassName, 
   keyClassName, 
   valueClassName, 
   None, 
   None, 
   config).
   map(lambda row: 
     (int(row[1]['user']), 
      int(row[1]['movie']), 
      float(row[1]['rating']))
   )

activeUsers = (sc.newAPIHadoopRDD(
   inputFormatClassName, 
   keyClassName, 
   valueClassName, 
   None, 
   None, 
   {"mongo.input.uri": 
    "mongodb://localhost:27017/streaming_recommender.active_users"}
   ).
   map(lambda row: int(row[1][u'user']))

movies = ratings.map(lambda rating: rating[1]).distinct()

candidates = activeUsers.cartesian(movies)

model = pyspark.mllib.recommendation.ALS.train(ratings, 10, 10)

predictions = model.predictAll(candidates)

t=str(time.time())

(predictions.
   filter(lambda r: r.rating > 4.9).
   map(
      lambda r: (t+str(r.user)+str(r.product), 
              {'user': int(r.user), 
               'product':int(r.product), 
               'rating':int(r.rating)
               })
   ).
   saveAsNewAPIHadoopFile(
    path='file:///this-is-unused',
    outputFormatClassName,
    keyClass=keyClassName,
    valueClass=valueClassName,
    conf={
         'mongo.output.uri': 
         'mongodb://localhost:27017/streaming_recommender.output'
    }
   )
)
