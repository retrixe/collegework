import java.util.Scanner;

class LearningContent {
    protected String title;
    protected String type;

    public LearningContent(String title, String type) {
        this.title = title;
        this.type = type;
    }

    public void display() {
        System.out.println("Content: " + title + " | Type: " + type);
    }
}

class VideoLecture extends LearningContent {
    public VideoLecture(String title) {
        super(title, "Video Lecture");
    }
}

class Quiz extends LearningContent {
    public Quiz(String title) {
        super(title, "Quiz");
    }
}

public class ContentHierarchy {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number of contents: ");
        int n = sc.nextInt();
        sc.nextLine(); 

        LearningContent[] contents = new LearningContent[n];

        for (int i = 0; i < n; i++) {
            System.out.println("\nChoose Content Type:");
            System.out.println("1. Video Lecture");
            System.out.println("2. Quiz");
            System.out.print("Enter choice: ");
            int choice = sc.nextInt();
            sc.nextLine();

            System.out.print("Enter Title: ");
            String title = sc.nextLine();

            if (choice == 1) {
                contents[i] = new VideoLecture(title);
            } else if (choice == 2) {
                contents[i] = new Quiz(title);
            } else {
                System.out.println("Invalid choice. Skipping...");
                i--;
                continue;
            }
        }

        System.out.println("\n--- Content List ---");
        for (LearningContent content : contents) {
            content.display();
        }

        sc.close();
    }
}
