import java.util.*;

class RecommendationSystem {
    protected String userID;
    protected String contentType;
    protected List<String> viewingHistory;
    protected double preferenceScore;

    public RecommendationSystem(String userID, String contentType,
                                List<String> viewingHistory, double preferenceScore) {
        this.userID = userID;
        this.contentType = contentType;
        this.viewingHistory = viewingHistory;
        this.preferenceScore = preferenceScore;
    }

    // Method Overloading
    public void generateRecommendation(double preferenceScore) {
        System.out.println("\nRecommendation based on Preference Score:");
        if (preferenceScore >= 8)
            System.out.println("Recommended: Premium Trending Content");
        else if (preferenceScore >= 5)
            System.out.println("Recommended: Popular Content");
        else
            System.out.println("Recommended: Basic Content");
    }

    public void generateRecommendation(List<String> history) {
        System.out.println("\nRecommendation based on Viewing History:");
        if (history.isEmpty())
            System.out.println("Recommended: Explore New Content");
        else
            System.out.println("Recommended similar to: " + history.get(history.size() - 1));
    }

    public void generateRecommendation(double preferenceScore, List<String> history) {
        System.out.println("\nRecommendation based on Preference + History:");
        if (preferenceScore > 7 && !history.isEmpty())
            System.out.println("Recommended: Advanced content related to " + history.get(0));
        else
            System.out.println("Recommended: General Trending Content");
    }

    public void platformRecommendation() {
        System.out.println("General Platform Recommendation");
    }
}

class VideoPlatform extends RecommendationSystem {

    public VideoPlatform(String userID, String contentType,
                         List<String> viewingHistory, double preferenceScore) {
        super(userID, contentType, viewingHistory, preferenceScore);
    }

    public void platformRecommendation() {
        System.out.println("\n[Video Streaming Platform]");
        if (preferenceScore >= 7)
            System.out.println("Suggesting HD Action Movies & Web Series");
        else
            System.out.println("Suggesting Short Trending Videos");
    }
}

class MusicPlatform extends RecommendationSystem {

    public MusicPlatform(String userID, String contentType,
                         List<String> viewingHistory, double preferenceScore) {
        super(userID, contentType, viewingHistory, preferenceScore);
    }

    public void platformRecommendation() {
        System.out.println("\n[Music Platform]");
        if (preferenceScore >= 7)
            System.out.println("Suggesting Premium Playlists & Albums");
        else
            System.out.println("Suggesting Trending Singles");
    }
}

class ELearningPlatform extends RecommendationSystem {

    public ELearningPlatform(String userID, String contentType,
                             List<String> viewingHistory, double preferenceScore) {
        super(userID, contentType, viewingHistory, preferenceScore);
    }

    public void platformRecommendation() {
        System.out.println("\n[E-Learning Platform]");
        if (preferenceScore >= 7)
            System.out.println("Suggesting Advanced Certification Courses");
        else
            System.out.println("Suggesting Beginner Friendly Courses");
    }
}

public class DigitalContentRecommendation {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter User ID: ");
        String userID = sc.nextLine();

        System.out.println("\nSelect Platform:");
        System.out.println("1. Video Streaming");
        System.out.println("2. Music");
        System.out.println("3. E-Learning");
        System.out.print("Enter choice: ");
        int choice = sc.nextInt();
        sc.nextLine();

        System.out.print("Enter Content Type (e.g., Movies, Songs, Courses): ");
        String contentType = sc.nextLine();

        System.out.print("Enter Preference Score (0-10): ");
        double preferenceScore = sc.nextDouble();
        sc.nextLine();

        System.out.print("Enter number of items in viewing history: ");
        int n = sc.nextInt();
        sc.nextLine();

        List<String> history = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            System.out.print("Enter history item " + (i + 1) + ": ");
            history.add(sc.nextLine());
        }

        RecommendationSystem user;

        if (choice == 1)
            user = new VideoPlatform(userID, contentType, history, preferenceScore);
        else if (choice == 2)
            user = new MusicPlatform(userID, contentType, history, preferenceScore);
        else
            user = new ELearningPlatform(userID, contentType, history, preferenceScore);

        user.generateRecommendation(preferenceScore);
        user.generateRecommendation(history);
        user.generateRecommendation(preferenceScore, history);

        user.platformRecommendation();

        sc.close();
    }
}
