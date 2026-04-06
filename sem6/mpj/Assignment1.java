import java.util.Scanner;

class OnlineExam {

    private String examID;
    private int totalDuration;     
    private int timeConsumed;       
    private int warningThreshold;   

    public OnlineExam(String examID, int totalDuration, int warningThreshold) {
        this.examID = examID;
        this.totalDuration = totalDuration;
        this.warningThreshold = warningThreshold;
        this.timeConsumed = 0; 
    }

    public void updateTime(int minutes) {
        if (minutes > 0 && (timeConsumed + minutes) <= totalDuration) {
            timeConsumed += minutes;
            System.out.println("Time updated successfully.");
        } else {
            System.out.println("Invalid time input or exceeds total duration.");
        }
    }

    public void generateAlert() {
        int remainingTime = totalDuration - timeConsumed;

        System.out.println("\nExam ID: " + examID);
        System.out.println("Total Duration: " + totalDuration + " minutes");
        System.out.println("Time Consumed: " + timeConsumed + " minutes");
        System.out.println("Remaining Time: " + remainingTime + " minutes");

        if (remainingTime <= 0) {
            System.out.println("⛔ Time is over! Exam auto-submitted.");
        } 
        else if (remainingTime <= warningThreshold) {
            System.out.println("⚠ Warning: Only " + remainingTime + " minutes left!");
        } 
        else {
            System.out.println("✔ You have sufficient time remaining.");
        }
    }
    public String getExamID() {
        return examID;
    }

    public int getRemainingTime() {
        return totalDuration - timeConsumed;
    }
}

public class OnlineExamManager {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter Exam ID: ");
        String examID = sc.nextLine();

        System.out.print("Enter Total Exam Duration (in minutes): ");
        int totalDuration = sc.nextInt();

        System.out.print("Enter Warning Threshold (minutes before end): ");
        int warningThreshold = sc.nextInt();

        OnlineExam exam = new OnlineExam(examID, totalDuration, warningThreshold);

        int choice;

        do {
            System.out.println("\n--- Online Exam Time Manager ---");
            System.out.println("1. Update Time Consumed");
            System.out.println("2. Generate Alert");
            System.out.println("3. Exit");
            System.out.print("Enter choice: ");
            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    System.out.print("Enter minutes consumed: ");
                    int minutes = sc.nextInt();
                    exam.updateTime(minutes);
                    break;

                case 2:
                    exam.generateAlert();
                    break;

                case 3:
                    System.out.println("Exiting system...");
                    break;

                default:
                    System.out.println("Invalid choice!");
            }

        } while (choice != 3);

        sc.close();
    }
}
