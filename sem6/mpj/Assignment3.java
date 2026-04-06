import java.io.*;
import java.util.*;

abstract class LearningData {
    protected int studentID;
    protected double completionPercentage;

    public LearningData(int studentID, double completionPercentage) {
        this.studentID = studentID;
        this.completionPercentage = completionPercentage;
    }

    abstract void displayData();
}

interface AnalyticsReport {
    void generateReport();
}

class LearningAnalytics extends LearningData implements AnalyticsReport {

    public LearningAnalytics(int studentID, double completionPercentage) {
        super(studentID, completionPercentage);
    }

    void displayData() {
        System.out.println("Student ID: " + studentID +
                " | Completion: " + completionPercentage + "%");
    }

    public void generateReport() {
        if (completionPercentage >= 75) {
            System.out.println("Status: Completed");
        } else if (completionPercentage >= 50) {
            System.out.println("Status: In Progress");
        } else {
            System.out.println("Status: Needs Improvement");
        }
        System.out.println("----------------------");
    }
}

public class LearningAnalyticsProcessor {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter file name (with path): ");
        String fileName = sc.nextLine();

        try {
            BufferedReader br = new BufferedReader(new FileReader(fileName));
            String line;

            br.readLine();

            System.out.println("\n--- Learning Analytics Report ---");

            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");

                int studentID = Integer.parseInt(data[0].trim());
                double completion = Double.parseDouble(data[1].trim());

                LearningAnalytics student =
                        new LearningAnalytics(studentID, completion);

                student.displayData();
                student.generateReport();
            }

            br.close();
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }

        sc.close();
    }
}
