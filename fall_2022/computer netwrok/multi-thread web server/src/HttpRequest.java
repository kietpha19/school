import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;
import java.security.cert.CRL;

final class HttpRequest implements Runnable{

    final static String CRLF = "\r\n";
    Socket socket;

    //constructor
    public HttpRequest(Socket socket) throws Exception{
        this.socket = socket;
    }
    @Override
    public void run() {
        try{
            processRequest();
        }catch (Exception e){
            System.out.println(e);
        }
    }

    private void processRequest() throws Exception{
        //get a reference to the socket's input and output streams
        InputStream inputStream =  socket.getInputStream();
        DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());

        //set up input stream filters
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

        //get the request line of the HTTP request message
        String requestLine = bufferedReader.readLine();

        //display the request line
        System.out.println();
        System.out.println(requestLine);

        //get and display the header lines
        //since we don't know how many header lines the client will send, we must get these lines within a while loop
        String headerLine = null;
        while((headerLine = bufferedReader.readLine()).length() != 0){
            System.out.println(headerLine);
        }

        //close the streams and socket
        dataOutputStream.close();
        bufferedReader.close();
        socket.close();



    }
}
