package xyz.retrixe;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        try {
            // Load the FXML file
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/main_view.fxml"));
            Parent root = loader.load();

            // Create the scene and link the CSS
            Scene scene = new Scene(root, 900, 600);
            scene.getStylesheets().add(getClass().getResource("/style.css").toExternalForm());

            primaryStage.setTitle("ASCON-128 Cryptographic Tool");
            primaryStage.setScene(scene);
            primaryStage.show();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
