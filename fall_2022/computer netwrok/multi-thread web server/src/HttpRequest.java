import java.io.*;
import java.net.Socket;
import java.security.cert.CRL;
import java.util.StringTokenizer;

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
            System.out.println("process request");
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

        //open the requested file
        FileInputStream fileInputStream = null;
        boolean fileExists = true;
        try {
            fileInputStream = new FileInputStream(fileName);
        }catch (FileNotFoundException e){
            fileExists = false;
        }

        // Construct the response message.
        String statusLine = null;
        String contentTypeLine = null;
        String entityBody = null;
        if (fileExists) {
            statusLine = "200 OK:"; //????
            contentTypeLine = "content-type: " +
                    contentType( fileName ) + CRLF;
            //content-type: text/html; charset=utf-8
        } else {
            statusLine = "404 Not Found"; //?????
            contentTypeLine = "content-type: text/html" + CRLF; //????

            entityBody = "<HTML>" +
                    "<HEAD><TITLE>Not Found</TITLE></HEAD>" +
                    "<BODY>Not Found</BODY></HTML>";
        }
        // Send the status line.
        dataOutputStream.writeBytes(statusLine);

        // Send the content type line.
        dataOutputStream.writeBytes(contentTypeLine);

        // Send a blank line to indicate the end of the header lines.
        dataOutputStream.writeBytes(CRLF);

        // Send the entity body.
        if (fileExists)	{
            sendBytes(fileInputStream, dataOutputStream);
            fileInputStream.close();
        } else {
            dataOutputStream.writeBytes(entityBody);
        }

        //close the streams and socket
        dataOutputStream.close();
        bufferedReader.close();
        socket.close();
    }

    private static String contentType(String fileName)
    {
        if(fileName.endsWith(".htm") || fileName.endsWith(".html")) {
            return "text/html;";
        }
//        if() {
//		?;
//    }
//        if(?) {
//		?;
//    }
        return "application/octet-stream";
    }


    private static void sendBytes(FileInputStream fis, OutputStream os)
            throws Exception
    {
        // Construct a 1K buffer to hold bytes on their way to the socket.
        byte[] buffer = new byte[1024];
        int bytes = 0;

        // Copy requested file into the socket's output stream.
        while((bytes = fis.read(buffer)) != -1 ) {
            os.write(buffer, 0, bytes);
        }
    }
}
