package xyz.retrixe;

import jakarta.mail.*;
import jakarta.mail.internet.*;
import java.util.Properties;

public class EmailService {
    // Replace these with your actual Ethereal credentials
    private static final String USERNAME = "georgette.hintz@ethereal.email";
    private static final String PASSWORD = "rMtsqzcUS4GYCuWZWN";

    public static void sendOTP(String recipientEmail, String otp) throws MessagingException {
        Properties prop = new Properties();
        prop.put("mail.smtp.auth", "true");
        prop.put("mail.smtp.starttls.enable", "true");
        prop.put("mail.smtp.host", "smtp.ethereal.email");
        prop.put("mail.smtp.port", "587");

        Session session = Session.getInstance(prop, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(USERNAME, PASSWORD);
            }
        });

        Message message = new MimeMessage(session);
        message.setFrom(new InternetAddress("security-suite@ascon.com"));
        message.setRecipients(Message.RecipientType.TO, InternetAddress.parse(recipientEmail));
        message.setSubject("Identity Verification Code");

        String htmlContent = "<h1>Verification Required</h1>" +
                "<p>Your security OTP is: <b>" + otp + "</b></p>" +
                "<p>If you did not request this, please ignore this email.</p>";

        message.setContent(htmlContent, "text/html");

        Transport.send(message);
    }
}
