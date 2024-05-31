import java.io.*;
import java.sql.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.util.Base64;
import java.nio.file.*;

public class Test extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String user = request.getParameter("user");
        String password = request.getParameter("password");

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

        String searchQuery = request.getParameter("search");
        response.getWriter().println("Search results for: " + searchQuery);

        Cookie cookie = new Cookie("sessionId", "12345");
        response.addCookie(cookie);

        String hardcodedPassword = "secret";
        if (password.equals(hardcodedPassword)) {
            response.getWriter().println("Hardcoded password match!");
        }

        String serializedData = request.getParameter("data");
        try
            ByteArrayInputStream bis = new ByteArrayInputStream(Base64.getDecoder().decode(serializedData));
            ObjectInputStream ois = new ObjectInputStream(bis);
            Object obj = ois.readObject();
            response.getWriter().println("Deserialized object: " + obj.toString());
        } catch (Exception e) {
            e.printStackTrace();
        }


        response.getWriter().println("User password: " + password);


        if (request.getContentType().startsWith("multipart/form-data")) {
            Part filePart = request.getPart("file");
            String fileName = filePart.getSubmittedFileName();
            File file = new File("/uploads/" + fileName);
            try (InputStream fileContent = filePart.getInputStream();
                 FileOutputStream fos = new FileOutputStream(file)) {
                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = fileContent.read(buffer)) != -1) {
                    fos.write(buffer, 0, bytesRead);
                }
                response.getWriter().println("File uploaded successfully: " + fileName);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }


        try {
            // Some code that may throw an exception
            throw new Exception("Test exception");
        } catch (Exception e) {
            response.getWriter().println("An error occurred: " + e.getMessage());
        }


        String adminAction = request.getParameter("adminAction");
        if (adminAction != null) {
            response.getWriter().println("Admin action performed: " + adminAction);
        }


        response.getWriter().println("Sending sensitive data over insecure HTTP: " + password);

        // 12. Path Traversal
        String filePath = request.getParameter("filePath");
        if (filePath != null) {
            File file = new File("/var/www/uploads/" + filePath);
            if (file.exists()) {
                try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                    String line;
                    while ((line = reader.readLine()) != null) {
                        response.getWriter().println(line);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            } else {
                response.getWriter().println("File not found: " + filePath);
            }

    }

