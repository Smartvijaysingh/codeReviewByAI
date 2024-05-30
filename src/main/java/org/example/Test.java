package org.example;

public class Test {

    private String password;

    public PasswordManager(String password) {
        this.password = password;
    }

    public void savePasswordToFile(String fileName) {
        try {
            FileWriter fw = new FileWriter(fileName);
            fw.write("Password: " + password);
            fw.close();
        } catch (IOException e) {
            System.out.println("Error saving password to file: " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        String password = args[0];
        PasswordManager pm = new PasswordManager(password);
        pm.savePasswordToFile("password.txt");
        System.out.println("Password saved to file.");
    }
}
