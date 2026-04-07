package xyz.retrixe.model;

public class ServiceRequest {
    private int id;
    private String serviceType;
    private String description;
    private String status;

    public ServiceRequest() {}

    public ServiceRequest(String serviceType, String description) {
        this.serviceType = serviceType;
        this.description = description;
        this.status = "Pending"; // Default status
    }

    public ServiceRequest(int id, String serviceType, String description, String status) {
        this.id = id;
        this.serviceType = serviceType;
        this.description = description;
        this.status = status;
    }

    public int getId() {
        return id;
    }

    public String getServiceType() {
        return serviceType;
    }

    public String getDescription() {
        return description;
    }

    public String getStatus() {
        return status;
    }

    public void setId(int id) {
        this.id = id;
    }

    public void setServiceType(String serviceType) {
        this.serviceType = serviceType;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    @Override
    public String toString() {
        return "ServiceRequest{" +
                "id=" + id +
                ", serviceType='" + serviceType + '\'' +
                ", status='" + status + '\'' +
                '}';
    }
}
