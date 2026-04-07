package xyz.retrixe.servlet;

import java.io.*;
import java.sql.*;
import java.util.*;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import xyz.retrixe.model.*;

@WebServlet("/requests")
public class RequestServlet extends HttpServlet {
    private final String DB_URL = "jdbc:mysql://localhost:3306/ServicePortal";
    private final String DB_USER = "root";
    private final String DB_PASS = "password";

    // Handle New Request Submission
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String type = request.getParameter("serviceType");
        String desc = request.getParameter("description");

        try { Class.forName("com.mysql.cj.jdbc.Driver"); } catch (ClassNotFoundException e) { e.printStackTrace(); }
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS)) {
            String sql = "INSERT INTO requests (service_type, description) VALUES (?, ?)";
            PreparedStatement pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, type);
            pstmt.setString(2, desc);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        response.sendRedirect("requests"); // Refresh list
    }

    // Retrieve All Requests
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        List<ServiceRequest> list = new ArrayList<>();
        try { Class.forName("com.mysql.cj.jdbc.Driver"); } catch (ClassNotFoundException e) { e.printStackTrace(); }
        try (Connection conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASS)) {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM requests");
            while (rs.next()) {
                list.add(new ServiceRequest(
                    rs.getInt("id"),
                    rs.getString("service_type"),
                    rs.getString("description"),
                    rs.getString("status")
                ));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        request.setAttribute("requestList", list);
        request.getRequestDispatcher("viewRequests.jsp").forward(request, response);
    }
}
