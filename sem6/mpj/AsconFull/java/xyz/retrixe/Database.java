package xyz.retrixe;

import java.sql.*;

public class Database {
    private static Connection conn;

    public static void init() throws Exception {
        conn = DriverManager.getConnection("jdbc:sqlite:security_suite.db");
        Statement stmt = conn.createStatement();

        // Updated table string
        stmt.execute("CREATE TABLE IF NOT EXISTS users (" +
                "username TEXT PRIMARY KEY, " +
                "password TEXT, " +
                "role TEXT, " +
                "reset_status TEXT DEFAULT 'NORMAL', " +
                "full_name TEXT, " +
                "email TEXT, " +
                "phone TEXT, " +
                "address TEXT, " +
                "is_verified INTEGER DEFAULT 0, " +
                "otp_code TEXT);");

        // Use INSERT OR IGNORE to avoid primary key errors on restart
        stmt.execute("INSERT OR IGNORE INTO users (username, password, role, reset_status) " +
                "VALUES ('admin', 'password123', 'ADMIN', 'NORMAL')");

        stmt.execute("INSERT OR IGNORE INTO users (username, password, role, reset_status) " +
                "VALUES ('user', '12345', 'USER', 'NORMAL')");
    }

    public static String login(String user, String pass) throws Exception {
        PreparedStatement pstmt = conn.prepareStatement("SELECT role FROM users WHERE username=? AND password=?");
        pstmt.setString(1, user);
        pstmt.setString(2, pass);
        ResultSet rs = pstmt.executeQuery();
        return rs.next() ? rs.getString("role") : null;
    }

    public static void registerUser(String u, String p, String role, String name, String email, String phone, String addr) throws Exception {
        String sql = "INSERT INTO users (username, password, role, full_name, email, phone, address, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?, 1)";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, u);
            pstmt.setString(2, p);
            pstmt.setString(3, role);
            pstmt.setString(4, name);
            pstmt.setString(5, email);
            pstmt.setString(6, phone);
            pstmt.setString(7, addr);
            pstmt.executeUpdate();
        }
    }

    // Add this to Database.java
    public static void addUser(String user, String pass, String role) throws Exception {
        String sql = "INSERT INTO users (username, password, role) VALUES (?, ?, ?)";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, user);
            pstmt.setString(2, pass);
            pstmt.setString(3, role);
            pstmt.executeUpdate();
        }
    }

    public static void deleteUser(String username) throws Exception {
        String sql = "DELETE FROM users WHERE username = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, username);
            pstmt.executeUpdate();
        }
    }

    public static void updatePassword(String username, String newPassword) throws Exception {
        String sql = "UPDATE users SET password = ?, reset_status = 'NORMAL' WHERE username = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, newPassword);
            pstmt.setString(2, username);
            pstmt.executeUpdate();
        }
    }

    public static java.util.List<User> getAllUsers() throws Exception {
        java.util.List<User> list = new java.util.ArrayList<>();
        // Expanded SQL to include PII and verification status
        String sql = "SELECT username, password, role, reset_status, full_name, email, phone, address, is_verified FROM users";

        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                list.add(new User(
                        rs.getString("username"),
                        rs.getString("password"),
                        rs.getString("role"),
                        rs.getString("reset_status"),
                        rs.getString("full_name"),
                        rs.getString("email"),
                        rs.getString("phone"),
                        rs.getString("address"),
                        rs.getInt("is_verified") == 1 // Converts SQL integer (0/1) to Java boolean
                ));
            }
        }
        return list;
    }

    public static void requestReset(String username) throws Exception {
        String sql = "UPDATE users SET reset_status = 'PENDING' WHERE username = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, username);
            pstmt.executeUpdate();
        }
    }

    public static int getPendingCount() throws Exception {
        String sql = "SELECT COUNT(*) FROM users WHERE reset_status = 'PENDING'";
        try (Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }
}
