package xyz.retrixe;

import javafx.beans.property.BooleanProperty;
import javafx.beans.property.SimpleBooleanProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class User {
    private final StringProperty username, password, role, status;
    private final StringProperty fullName, email, phone, address;
    private final BooleanProperty verified;

    public User(String u, String p, String r, String s, String fn, String em, String ph, String ad, boolean v) {
        this.username = new SimpleStringProperty(u);
        this.password = new SimpleStringProperty(p);
        this.role = new SimpleStringProperty(r);
        this.status = new SimpleStringProperty(s);
        this.fullName = new SimpleStringProperty(fn);
        this.email = new SimpleStringProperty(em);
        this.phone = new SimpleStringProperty(ph);
        this.address = new SimpleStringProperty(ad);
        this.verified = new SimpleBooleanProperty(v);
    }

    // Getters for the Properties (JavaFX needs these)
    public StringProperty usernameProperty() { return username; }
    public StringProperty passwordProperty() { return password; }
    public StringProperty roleProperty() { return role; }
    public StringProperty statusProperty() { return status; }
    public StringProperty fullNameProperty() { return fullName; }
    public StringProperty emailProperty() { return email; }
    public StringProperty phoneProperty() { return phone; }
    public StringProperty addressProperty() { return address; }
    public BooleanProperty verifiedProperty() { return verified; }

    // Standard string getters
    public String getUsername() { return username.get(); }
    public String getPassword() { return password.get(); }
    public String getRole() { return role.get(); }
    public String getStatus() { return status.get(); }
    public String getFullName() { return fullName.get(); }
    public String getEmail() { return email.get(); }
    public String getPhone() { return phone.get(); }
    public String getAddress() { return address.get(); }
    public boolean getVerified() { return verified.get(); }
}
