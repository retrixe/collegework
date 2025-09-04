package xyz.retrixe;

import com.mongodb.BasicDBList;
import com.mongodb.BasicDBObject;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Updates;
import com.mongodb.client.result.UpdateResult;

import java.util.Scanner;

public class Main {
    private static void createHotel(Scanner scanner, MongoCollection<BasicDBObject> collection) {
        var hotel = new BasicDBObject();
        System.out.print("Enter ID: ");
        hotel.append("Id", scanner.nextInt());
        System.out.print("Enter Name: ");
        hotel.append("Name", scanner.next());
        System.out.print("Enter Type: ");
        hotel.append("Type", scanner.next());
        System.out.print("Enter Rating: ");
        hotel.append("Rating", scanner.nextDouble());
        System.out.print("Enter Likes: ");
        hotel.append("Likes", scanner.nextDouble());
        var address = new BasicDBObject();
        System.out.print("Enter Address Area: ");
        address.append("Area", scanner.next());
        System.out.print("Enter City: ");
        address.append("City", scanner.next());
        System.out.print("Enter Pincode: ");
        address.append("Pincode", scanner.next());
        System.out.print("Enter number of Rooms: ");
        int roomCount = scanner.nextInt();
        var rooms = new BasicDBList();
        for (int i = 0; i < roomCount; i++) {
            var room = new BasicDBObject();
            System.out.print("Enter Roomno: ");
            room.append("Roomno", scanner.nextInt());
            System.out.print("Enter Type: ");
            room.append("Type", scanner.next());
            System.out.print("Enter Price: ");
            room.append("Price", scanner.nextDouble());
        }
        hotel.append("Rooms", rooms);
        System.out.print("Enter number of Cuisines: ");
        int cuisineCount = scanner.nextInt();
        var cuisines = new BasicDBList();
        for (int i = 1; i <= cuisineCount; i++) {
            System.out.print("Enter Cuisine #" + i + ": ");
            cuisines.add(scanner.next());
        }
        hotel.append("Cuisines", cuisines);

        collection.insertOne(hotel);
    }

    private static void updateHotel(Scanner scanner, MongoCollection<BasicDBObject> collection) {
        var filter = new BasicDBObject();
        System.out.print("Enter ID: ");
        filter.append("Id", scanner.nextInt());

        System.out.print("Enter field name to update: ");
        var name = scanner.next();
        System.out.print("Enter field value: ");
        var value = scanner.next();
        UpdateResult result;
        try {
            result = collection.updateOne(filter, Updates.set(name, Double.parseDouble(value)));
        } catch (NumberFormatException e) {
            result = collection.updateOne(filter, Updates.set(name, value));
        }
        if (result.getModifiedCount() == 1) {
            System.out.println("Updated successfully!");
        } else {
            System.out.println("Document not found!");
        }
    }

    private static void findHotel(Scanner scanner, MongoCollection<BasicDBObject> collection) {
        System.out.print("Enter ID: ");
        var id = scanner.nextInt();
        var result = collection.find(Filters.eq("Id", id));
        if (result.first() != null) {
            for (BasicDBObject hotel : result) {
                System.out.println(hotel.toJson());
            }
        } else {
            System.out.println("No hotel found!");
        }
    }

    private static void showHotels(MongoCollection<BasicDBObject> collection) {
        var result = collection.find();
        if (result.first() != null) {
            for (BasicDBObject hotel : result) {
                System.out.println(hotel.toJson());
            }
        } else {
            System.out.println("No hotels found!");
        }
    }

    private static void deleteHotel(Scanner scanner, MongoCollection<BasicDBObject> collection) {
        System.out.print("Enter ID: ");
        var id = scanner.nextInt();
        var result = collection.deleteOne(Filters.eq("Id", id));
        if (result.getDeletedCount() == 1) {
            System.out.println("Deleted successfully!");
        } else {
            System.out.println("Document not found!");
        }
    }

    public static void main(String[] args) {
        try {
            var collection = Connection.getCollection();

            var scanner = new Scanner(System.in);
            while (true) {
                System.out.print("""
                        ==========
                        1. Create Hotel
                        2. Update Hotel
                        3. Find Hotel By ID
                        4. Show All Hotels
                        5. Delete Hotel
                        0. Exit
                        Enter choice:\s""");
                int option = scanner.nextInt();
                if (option == 0)
                    break;
                switch (option) {
                    case 1 -> createHotel(scanner, collection);
                    case 2 -> updateHotel(scanner, collection);
                    case 3 -> findHotel(scanner, collection);
                    case 4 -> showHotels(collection);
                    case 5 -> deleteHotel(scanner, collection);
                    default -> System.out.println("Wrong choice!");
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
