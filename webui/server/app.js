//server only code

Meteor.startup(function () {
});

Meteor.publish("ratings", function() {
   ratings = Ratings.find ({}, {limit:10} );
   return ratings;
});

Meteor.publish("movies_to_rate", function() {
   ratings = MoviesToRate.find ({}, {limit:50} );
   return ratings;
});

Meteor.publish("movies", function() {
   ratings = Movies.find ({});
   return ratings;
});

Meteor.publish("output", function(user_id) {
   console.log("OUTPUT");
   var self=this;
   ratings = Recommendations.find (
      {'value.user': user_id},
      {sort: {"value.rating":-1}, limit: 100}
   );

   ratings.observeChanges({
    added: function (id, fields) {
      self.added("output", id, fields);
    },
    changed: function(id, fields) {
      self.changed("output", id, fields);
    },
    removed: function (id) {
      self.removed("output", id);
    }
  });

console.log("Added");
   console.log(ratings.count());
   return ratings;
});

Meteor.methods({
   setIncomingRating: function(userId, myMovieId, newRating) {
      console.log(userId+ " " + myMovieId+ " " + newRating);
      if (newRating==null){ return; }
      Ratings.upsert({user: userId, movie: Number(myMovieId)}, 
                     {user: userId, movie:Number(myMovieId), rating: newRating});
      if (! ActiveUsers.findOne({user: userId})) {
          ActiveUsers.insert({user: userId})
      }
   },
   // Stats
   getTotalRatings: function() {
      return Ratings.find({}).count();
   },
   getTotalRecommendations: function() {
      return Recommendations.find({}).count();
   },
   getActiveUsers: function() {
      return ActiveUsers.find({}).count();
   },
   getDistinctUsers: function() {
     // return Ratings.distinct('user').count();
     return 3
   }
});
