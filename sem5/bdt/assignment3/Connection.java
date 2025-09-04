package xyz.retrixe;

import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;

public class Connection {
  public static MongoCollection<BasicDBObject> getCollection() {
    var client = new MongoClient("localhost", 27017);
    var db = client.getDatabase("restaurants");
    return db.getCollection("hotels", BasicDBObject.class);
  }
}
