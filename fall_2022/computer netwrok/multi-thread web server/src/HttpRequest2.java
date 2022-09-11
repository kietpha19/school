import java.io.*;
import java.net.Socket;
import java.util.StringTokenizer;

final class HttpRequest2 implements Runnable{

    final static String CRLF = "\r\n";
    Socket socket;

    //constructor
    public HttpRequest2(Socket socket) throws Exception{
        this.socket = socket;
    }
    @Override
    public void run() {
        try{
            //System.out.println("process request");
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

        //extract the file name from the request line
        StringTokenizer tokens = new StringTokenizer(requestLine);
        tokens.nextToken(); //skip over the method, which should be "GET"
        String fileName = tokens.nextToken();
        //Because the browser precedes the filename with a slash, we prefix a dot so that the resulting pathname starts within the current directory.
        fileName = "./src" + fileName;

        ////////////////////////////////////////////////////////////////////////////////////////
        dataOutputStream.writeBytes("HTTP/1.0 200 OK\r\n");
        dataOutputStream.writeBytes("Content-Type: text/html\r\n");
        dataOutputStream.writeBytes("\r\n");
        dataOutputStream.writeBytes("<TITLE>Exemple</TITLE>");
        dataOutputStream.writeBytes("<P>Hello world</P>");

        /////////////////////////////////////////////////////////////////////////////////////////

        dataOutputStream.flush();
        //close the streams and socket
        dataOutputStream.close();
        bufferedReader.close();
        socket.close();
    }

}
