package org.example;

import java.io.*;
import java.sql.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class VulnerableServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String user = request.getParameter("user");
        String password = request.getParameter("password");

        // 1. SQL Injection Vulnerability
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/mydb", "root", "password");
            stmt = conn.createStatement();
            String query = "SELECT * FROM users WHERE username='" + user + "' AND password='" + password + "'";
            rs = stmt.executeQuery(query);

            if (rs.next()) {
                response.getWriter().println("Welcome " + user);
            } else {
                response.getWriter().println("Invalid credentials");
            }
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
                if (conn != null) conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

        // 2. Cross-Site Scripting (XSS) Vulnerability
        String searchQuery = request.getParameter("search");
        response.getWriter().println("Search results for: " + searchQuery);

        // 3. Insecure Cookie Handling
        Cookie cookie = new Cookie("sessionId", "12345");
        response.addCookie(cookie);

        // 4. Hardcoded Credentials
        String hardcodedPassword = "secret";
        if (password.equals(hardcodedPassword)) {
            response.getWriter().println("Hardcoded password match!");
        }
    }
}
