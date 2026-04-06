import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class ChatApp {
    private static final int PORT = 12345;

    public static void main(String[] args) {
        if (args.length > 0 && args[0].equalsIgnoreCase("server")) {
            startServer();
        } else {
            startClient();
        }
    }

    // --- SERVER LOGIC ---
    private static void startServer() {
        Set<ClientHandler> clientHandlers = ConcurrentHashMap.newKeySet();
        System.out.println("--- Chat Server Started on Port " + PORT + " ---");

        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            while (true) {
                try {
                    Socket socket = serverSocket.accept();
                    ClientHandler handler = new ClientHandler(socket, clientHandlers);
                    clientHandlers.add(handler);
                    new Thread(handler).start();
                } catch (IOException e) {
                    System.err.println("Connection failure: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.err.println("Server critical error: " + e.getMessage());
        }
    }

    // --- CLIENT LOGIC ---
    private static void startClient() {
        System.out.println("--- Connecting to Chat Server ---");
        try (Socket socket = new Socket("localhost", PORT)) {
            System.out.println("Connected! Type your message and press Enter.");

            // Listening Thread
            Thread listener = new Thread(() -> {
                try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
                    String msg;
                    while ((msg = in.readLine()) != null) {
                        System.out.println("\n[Incoming]: " + msg);
                        System.out.print("> "); // Prompt for user
                    }
                } catch (IOException e) {
                    System.err.println("\nDisconnected from server.");
                }
            });
            listener.setDaemon(true);
            listener.start();

            // Sending Logic
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            Scanner scanner = new Scanner(System.in);
            while (scanner.hasNextLine()) {
                String input = scanner.nextLine();
                out.println(input);
                System.out.print("> ");
            }
        } catch (IOException e) {
            System.err.println("Could not connect to server. Is it running?");
        }
    }
}

class ClientHandler implements Runnable {
    private final Socket socket;
    private final Set<ClientHandler> allHandlers;
    private PrintWriter out;

    public ClientHandler(Socket socket, Set<ClientHandler> allHandlers) {
        this.socket = socket;
        this.allHandlers = allHandlers;
    }

    @Override
    public void run() {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
            out = new PrintWriter(socket.getOutputStream(), true);
            String clientMsg;
            while ((clientMsg = in.readLine()) != null) {
                broadcast(clientMsg);
            }
        } catch (IOException e) {
            // Handle connection drops or interruptions gracefully
        } finally {
            cleanup();
        }
    }

    private void broadcast(String message) {
        String wrappedMsg = "User-" + socket.getPort() + ": " + message;
        for (ClientHandler handler : allHandlers) {
            if (handler != this && handler.out != null) {
                handler.out.println(wrappedMsg);
            }
        }
    }

    private void cleanup() {
        allHandlers.remove(this);
        try {
            socket.close();
            System.out.println("User-" + socket.getPort() + " disconnected.");
        } catch (IOException e) {
            // Error closing socket
        }
    }
}
