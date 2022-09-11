import java.net.*;
import java.io.*;
import java.util.*;

public class WebServer {
    private static int port = 8080;
    public static void main(String args[]) throws Exception{
        ServerSocket serverSocket = new ServerSocket(port);

        while(true) {
            Socket connectionSocket = serverSocket.accept();
            HttpRequest request = new HttpRequest(connectionSocket);
            Thread thread = new Thread(request);
            thread.start();
        }
    }
}
