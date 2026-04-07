<%@ page import="java.util.*, xyz.retrixe.model.ServiceRequest" %>
<table border="1">
    <tr>
        <th>ID</th><th>Type</th><th>Description</th><th>Status</th>
    </tr>
    <%
        List<ServiceRequest> list = (List<ServiceRequest>) request.getAttribute("requestList");
        if(list != null) {
            for(ServiceRequest req : list) {
    %>
    <tr>
        <td><%= req.getId() %></td>
        <td><%= req.getServiceType() %></td>
        <td><%= req.getDescription() %></td>
        <td><%= req.getStatus() %></td>
    </tr>
    <%      } 
        } 
    %>
</table>
