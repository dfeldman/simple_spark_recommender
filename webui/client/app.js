//client only code

MY_USER_ID = Math.trunc((Math.random()+1) * 1000000)
Meteor.subscribe("movies_to_rate");
Meteor.subscribe("ratings");
Meteor.subscribe("stats");
Meteor.subscribe("output", MY_USER_ID);
Meteor.subscribe("movies");
stats = new Mongo.Collection("stats");
//assert(MY_USER_ID < Math.pow(2,31));

Template.input_ratings.helpers({
  ratings: function () {
    console.log( MoviesToRate.find({}).count()); return MoviesToRate.find({});
  }
});

Template.recommendations.helpers({
   recs: function() { console.log("XX123"); console.log(Recommendations.findOne()); 

query = Recommendations.find({}, {limit:50, sort: {'value.rating':-1}}); 
return query;


}
});

Template.one_rec.helpers({ 
   movietoname: function() { 
     val = Movies.findOne({movie: this.value.product.toString()}); 
     if (val != null) { return val['movieTitle']; } 
     else {console.log('unknown movie' + this.value.product);}
   }
});

Template.input_ratings.events({
});

Template.rating.helpers({
  input_rating_val: function() { console.log(this.rating); return this.rating; }
});


Template.rating.events({
  'click .rating': function (evt, tpl) {
    movieId = this.movieId;
    rating=tpl.$('.ratingwidget').data('userrating');
//    console.log("userId " + MY_USER_ID + " MovieID " + movieId + " rating " + rating);
    Meteor.call("setIncomingRating", MY_USER_ID, movieId, rating);
    updateStats();
  }
});

function updateStats() {
    Meteor.call("getTotalRatings", function(e,v) {Session.set("total_ratings", v); } )
    Meteor.call("getTotalRecommendations", function(e,v) {Session.set("total_recommendations", v); } )
    Meteor.call("getActiveUsers", function(e,v) {console.log(v);Session.set("active_users", v); } )
    Meteor.call("getDistinctUsers", function(e,v) {console.log(v);Session.set("distinct_users", v); } )
    Session.set("user_id", MY_USER_ID);
}


Template.stats.helpers({ 
    total_ratings: function() { return Session.get("total_ratings"); } ,
    total_recommendations: function() { return Session.get("total_recommendations"); } ,
    active_users: function() { return Session.get("active_users"); } ,
    user_id: function() { return Session.get("user_id"); } ,
    distinct_users: function() { return Session.get("distinct_users"); } 
});

Meteor.startup(function(){
    updateStats();
});
