package xyz.retrixe;

import javafx.beans.property.SimpleStringProperty;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.layout.HBox;
import javafx.scene.layout.VBox;

public class SecurityController {
    // UI Panels
    @FXML private VBox encryptionPanel, userManagementPanel, adminLogsPanel;
    @FXML private HBox mainApp;
    @FXML private VBox loginScreen, registerScreen, otpScreen;

    // Inputs
    @FXML private TextField keyField, nonceField, adField;
    @FXML private TextArea inputArea, outputArea, logArea;
    @FXML private CheckBox hexModeToggle;
    @FXML private TableView<User> userTable;
    @FXML private TextField usernameField;
    @FXML private PasswordField passwordField;
    @FXML private Label statusLabel;
    @FXML private TextField newUserName, newUserPass;
    @FXML private ComboBox<String> roleSelector;
    @FXML private PasswordField adminResetPassField;

    @FXML private Button btnUserManager;
    @FXML private Button btnAdminLogs;

    @FXML private TableColumn<User, String> colUsername;
    @FXML private TableColumn<User, String> colPassword;
    @FXML private TableColumn<User, String> colRole;

    @FXML private Label pendingCountLabel;
    @FXML private TextArea regAddress;
    @FXML private TextField regFullName, regEmail, regPhone, regUsername, regPassword, otpInput;
    @FXML private Button regSubmitButton;

    public void showRegisterScreen() {
        loginScreen.setVisible(false);
        loginScreen.setManaged(false);
        registerScreen.setVisible(true);
        registerScreen.setManaged(true);
    }

    public void showLoginScreen() {
        registerScreen.setVisible(false);
        registerScreen.setManaged(false);
        otpScreen.setVisible(false);
        otpScreen.setManaged(false);
        loginScreen.setVisible(true);
        loginScreen.setManaged(true);
    }

    private String currentOTP;

    @FXML
    public void handleRegister() {
        regSubmitButton.setDisable(true);
        log("[SYSTEM] Initiating SMTP handshake...");
        String email = regEmail.getText();
        String otp = String.format("%06d", new java.util.Random().nextInt(999999));

        // Run this in a background thread so the UI doesn't freeze!
        new Thread(() -> {
            try {
                EmailService.sendOTP(email, otp);

                // 3. CRITICAL: Switch screens back on the UI thread
                javafx.application.Platform.runLater(() -> {
                    currentOTP = otp;

                    registerScreen.setVisible(false);
                    registerScreen.setManaged(false);

                    otpScreen.setVisible(true);
                    otpScreen.setManaged(true);

                    log("OTP successfully routed to: " + email);
                });
            } catch (Exception e) {
                javafx.application.Platform.runLater(() -> {
                    log("SMTP FAILURE: " + e.getMessage());
                    regSubmitButton.setDisable(false); // Re-enable so they can try again
                });
            }
        }).start();
    }

    @FXML
    public void handleVerifyOTP() {
        if (otpInput.getText().equals(currentOTP)) {
            try {
                String user = regUsername.getText();
                String pass = regPassword.getText();

                // 1. Save to Database
                Database.registerUser(
                        user,
                        pass,
                        "USER",
                        regFullName.getText(),
                        regEmail.getText(),
                        regPhone.getText(),
                        regAddress.getText()
                );

                log("[IDENTITY VERIFIED] Account created for: " + user);

                // 2. Direct Login Bypass
                otpScreen.setVisible(false);
                otpScreen.setManaged(false);

                // Show the Main App immediately
                mainApp.setVisible(true);

                // Configure UI for the 'USER' role (Hide Admin buttons)
                btnUserManager.setVisible(false);
                btnUserManager.setManaged(false);
                btnAdminLogs.setVisible(false);
                btnAdminLogs.setManaged(false);

                showEncryptionPanel(); // Switch to the crypto tool view

                log("Session started automatically for new user: " + user);

            } catch (Exception e) {
                log("Database Error: " + e.getMessage());
            }
        } else {
            log("Invalid OTP. Access Denied.");
            otpInput.setStyle("-fx-border-color: red;");
        }
    }

    @FXML
    public void initialize() {
        roleSelector.getItems().addAll("USER", "ADMIN");

        colUsername.setCellValueFactory(cellData -> cellData.getValue().usernameProperty());
        colPassword.setCellValueFactory(cellData -> {
            int len = cellData.getValue().getPassword().length();
            return new SimpleStringProperty("*".repeat(Math.min(len, 12)));
        });
        colRole.setCellValueFactory(cellData -> cellData.getValue().roleProperty());

        try { Database.init(); } catch (Exception e) {}
        showEncryptionPanel(); // Default view
        setupUserTable();
    }

    // --- NAVIGATION ---
    public void showEncryptionPanel() {
        hideAll();
        encryptionPanel.setVisible(true);
        encryptionPanel.setManaged(true);
    }

    public void showUserManagement() {
        // Double-check if the button is even visible before showing the panel
        if (btnUserManager.isVisible()) {
            hideAll();
            userManagementPanel.setVisible(true);
            userManagementPanel.setManaged(true);
            refreshUserTable();
        } else {
            log("[SECURITY ALERT] Unauthorized access attempt to User Management.");
        }
    }

    public void showAdminLogs() {
        hideAll();
        adminLogsPanel.setVisible(true);
        adminLogsPanel.setManaged(true);
    }

    private void hideAll() {
        encryptionPanel.setVisible(false); encryptionPanel.setManaged(false);
        userManagementPanel.setVisible(false); userManagementPanel.setManaged(false);
        adminLogsPanel.setVisible(false); adminLogsPanel.setManaged(false);
    }

    // --- FUNCTIONAL ASCON ---
    public void handleEncrypt() {
        runAscon("encrypt");
    }

    public void handleDecrypt() {
        runAscon("decrypt");
    }

    private void runAscon(String mode) {
        try {
            byte[] key = parseHex(keyField.getText());
            byte[] nonce = parseHex(nonceField.getText());
            byte[] ad = parseHex(adField.getText());

            boolean isHexMode = hexModeToggle.isSelected();

            if (mode.equals("encrypt")) {
                byte[] pt;
                if (isHexMode) {
                    pt = parseHex(inputArea.getText().replaceAll("\\s", ""));
                } else {
                    pt = inputArea.getText().getBytes(java.nio.charset.StandardCharsets.UTF_8);
                }

                // APPLY INTERNAL ZERO PADDING
                // If the user enters "seggs" (5 bytes), this makes it 32 bytes of "seggs\0\0..."
                pt = padWithZeroes(pt, 64);

                Ascon.CiphertextWithTag res = Ascon.encrypt(key, nonce, pt, ad);
                outputArea.setText(toHex(res.ciphertext) + ":" + toHex(res.tag));
                log("[SUCCESS] Encryption complete (" + (isHexMode ? "Hex" : "UTF-8") + " mode)");

            } else {
                // DECRYPT MODE
                String[] parts = inputArea.getText().trim().split(":");
                byte[] ct = parseHex(parts[0]);
                byte[] tag = parseHex(parts[1]);

                byte[] pt = Ascon.decrypt(key, nonce, ct, tag, ad);

                if (isHexMode) {
                    outputArea.setText(toHex(pt));
                } else {
                    // Convert to string and remove null characters
                    String result = new String(pt, java.nio.charset.StandardCharsets.UTF_8);
                    outputArea.setText(result.replace("\0", ""));
                }
                log("[SUCCESS] Decryption complete.");
            }
        } catch (Exception e) {
            log("[FAILURE] Check data/format: " + e.getMessage());
            outputArea.setText("ERROR");
        }
    }

    // --- USER MANAGEMENT ---
    private void setupUserTable() {
        // Simple TableView setup for User objects
    }

    private void log(String msg) {
        logArea.appendText("[" + java.time.LocalTime.now().format(java.time.format.DateTimeFormatter.ofPattern("HH:mm:ss")) + "] " + msg + "\n");
        System.out.println("[" + java.time.LocalTime.now().format(java.time.format.DateTimeFormatter.ofPattern("HH:mm:ss")) + "] " + msg + "\n");
    }

    // Helper to parse hex strings
    private byte[] parseHex(String s) {
        s = s.replaceAll("[^0-9A-Fa-f]", ""); // Strip everything but hex chars
        if (s.length() % 2 != 0) s = "0" + s; // Pad if odd length
        byte[] d = new byte[s.length() / 2];
        for (int i = 0; i < d.length; i++) {
            d[i] = (byte) Integer.parseInt(s.substring(i * 2, i * 2 + 2), 16);
        }
        return d;
    }

    private String toHex(byte[] b) {
        StringBuilder sb = new StringBuilder();
        for (byte x : b) sb.append(String.format("%02x", x));
        return sb.toString();
    }

    // 1. handleLogin - Connects the Login screen to the Database logic

    @FXML
    public void handleLogin() {
        String user = usernameField.getText();
        String pass = passwordField.getText();

        try {
            String role = Database.login(user, pass);

            if (role != null) {
                loginScreen.setVisible(false);
                mainApp.setVisible(true);

                // --- THE SECURITY LOCK ---
                boolean isAdmin = role.equalsIgnoreCase("ADMIN");

                btnUserManager.setVisible(isAdmin);
                btnUserManager.setManaged(isAdmin); // Removes the space it takes up

                btnAdminLogs.setVisible(isAdmin);
                btnAdminLogs.setManaged(isAdmin);

                if (isAdmin) {
                    int pending = Database.getPendingCount();
                    if (pending > 0) {
                        Alert alert = new Alert(Alert.AlertType.WARNING);
                        alert.setTitle("Security Notification");
                        alert.setHeaderText(pending + " Pending Password Resets");
                        alert.setContentText("Please review the User Management panel to handle recovery requests.");
                        alert.showAndWait();
                    }
                }

                log("Access Granted. Role: " + role);
                showEncryptionPanel();
            } else {
                statusLabel.setText("Access Denied.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // 2. refreshUserTable - Pulls data from SQLite and pushes it to the TableView
    public void refreshUserTable() {
        try {
            java.util.List<User> users = Database.getAllUsers();
            userTable.getItems().setAll(users);
            updatePendingAlert();
            log("User database refreshed.");
        } catch (Exception e) {
            log("Database Fetch Error: " + e.getMessage());
        }
    }

    // 3. handleAddUser - Takes input from the User Manager panel and saves it
    @FXML
    public void handleAddUser() {
        String u = newUserName.getText();
        String p = newUserPass.getText();
        String r = roleSelector.getValue(); // Get role from ComboBox

        if (u.isEmpty() || p.isEmpty() || r == null) {
            log("Error: All fields must be filled.");
            return;
        }

        try {
            Database.addUser(u, p, r);
            refreshUserTable();
            newUserName.clear();
            newUserPass.clear();
            log("Identity Created: " + u + " as " + r);
        } catch (Exception e) {
            log("Database Error: " + e.getMessage());
        }
    }

    @FXML
    public void handleLogout() {
        // 1. Clear sensitive session data
        usernameField.clear();
        passwordField.clear();
        inputArea.clear();
        outputArea.clear();
        keyField.clear();
        nonceField.clear();

        // 2. Reset the UI state
        mainApp.setVisible(false);
        loginScreen.setVisible(true);

        // 3. Optional: Reset the status label with a message
        statusLabel.setText("Successfully logged out.");
        statusLabel.setStyle("-fx-text-fill: #00ffcc;");

        log("User session terminated.");
    }

    @FXML
    public void handleDeleteUser() {
        User selected = userTable.getSelectionModel().getSelectedItem();
        if (selected == null) {
            log("Error: No user selected for deletion.");
            return;
        }

        if (selected.getUsername().equals("admin")) {
            log("Security Violation: Cannot delete the primary SuperAdmin account.");
            return;
        }

        try {
            Database.deleteUser(selected.getUsername());
            refreshUserTable();
            log("Successfully purged user identity: " + selected.getUsername());
        } catch (Exception e) {
            log("Deletion Error: " + e.getMessage());
        }
    }

    @FXML
    public void handleResetPassword() {
        User selected = userTable.getSelectionModel().getSelectedItem();
        String newPass = adminResetPassField.getText();

        if (selected == null) {
            log("Error: Select a user from the table first.");
            return;
        }
        if (newPass.isEmpty()) {
            log("Error: New password field is empty.");
            return;
        }

        try {
            Database.updatePassword(selected.getUsername(), newPass);
            adminResetPassField.clear();
            refreshUserTable(); // Refresh to show the new "starred" length
            log("[ADMIN ACTION] Password overridden for user: " + selected.getUsername());
        } catch (Exception e) {
            log("Database Update Error: " + e.getMessage());
        }
    }

    // Called in the Login screen
    @FXML
    public void handleForgotPassword() {
        String user = usernameField.getText();
        if (user.isEmpty()) {
            statusLabel.setText("Enter username.");
            return;
        }
        try {
            Database.requestReset(user);
            log("[ALERT] Reset flagged in DB for: " + user);
            statusLabel.setText("Admin has been notified.");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Call this inside refreshUserTable()
    private void updatePendingAlert() {
        try {
            int count = Database.getPendingCount();
            pendingCountLabel.setText(String.valueOf(count));
            if (count > 0) {
                pendingCountLabel.setStyle("-fx-text-fill: red; -fx-font-weight: bold;");
            } else {
                pendingCountLabel.setStyle("-fx-text-fill: white;");
            }
        } catch (Exception e) { e.printStackTrace(); }
    }

    @FXML
    public void filterPendingUsers() {
        try {
            // Fetch all users first
            java.util.List<User> allUsers = Database.getAllUsers();

            // Use Java Streams to filter for only 'PENDING' status
            // Note: You'll need to add a 'status' field to your User POJO as well
            java.util.List<User> pendingUsers = allUsers.stream()
                    .filter(u -> u.getStatus().equalsIgnoreCase("PENDING"))
                    .collect(java.util.stream.Collectors.toList());

            if (pendingUsers.isEmpty()) {
                log("No pending reset requests found.");
                refreshUserTable(); // Show everyone if nothing is pending
            } else {
                userTable.getItems().setAll(pendingUsers);
                log("Filtering view: Showing " + pendingUsers.size() + " recovery requests.");
            }
        } catch (Exception e) {
            log("Filter Error: " + e.getMessage());
        }
    }

    @FXML
    public void handlePrefill() {
        // Standard 16-byte hex strings (32 chars)
        String testKey = "0123456789abcdef0123456789abcdef";
        String testNonce = "abcdef0123456789abcdef0123456789";
        String testAD = "internal_system_data_v1";

        keyField.setText(testKey);
        nonceField.setText(testNonce);
        adField.setText(testAD);

        log("[UI] Test vectors loaded into cryptographic registers.");
    }

    private byte[] padWithZeroes(byte[] input, int targetLength) {
        if (input.length >= targetLength) {
            return input; // Already long enough
        }
        byte[] padded = new byte[targetLength];
        System.arraycopy(input, 0, padded, 0, input.length);
        // Java initializes new arrays with 0x00 automatically, so no need to loop
        return padded;
    }
}
