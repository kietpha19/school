import java.io.*;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.StringTokenizer;

final class HttpRequest implements Runnable{

    final static String CRLF = "\r\n";
    final static String http_version = "HTTP/1.0 ";
    Socket socket;

    //constructor
    public HttpRequest(Socket socket) throws Exception{
        this.socket = socket;
    }
    @Override
    public void run() {
        try{
            //System.out.println("process request"); // for debugging
            processRequest();
        }catch (Exception e){
            System.out.println(e);
        }
    }

    private void processRequest() throws Exception{
        //create an outputSTream from the socket
        DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());

        //get a reference to the socket's input and output streams
        InputStream inputStream =  socket.getInputStream();
        //set up input stream filters
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
        //get the request line of the HTTP request message
        String requestLine = bufferedReader.readLine();

        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //these lines of code for display to the console at server side for debugging purpose
        //display the request line
        System.out.println();
        System.out.println(requestLine);

        //get and display the header lines
        //since we don't know how many header lines the client will send, we must get these lines within a while loop
        String headerLine = null;
        while((headerLine = bufferedReader.readLine()).length() != 0){
            System.out.println(headerLine);
        }
        ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


        //extract the file name from the request line
        StringTokenizer tokens = new StringTokenizer(requestLine);
        tokens.nextToken(); //skip over the method, which should be "GET"
        String fileName = tokens.nextToken();


        HashSet<String> pages = getAvailablePages();
        String statusLine = getStatusLine(pages, fileName);
        if(statusLine == "404 Not Found"){
            fetchNotFound(dataOutputStream);
        }
        else{
            fetch_page(statusLine, fileName, dataOutputStream);
        }


        dataOutputStream.flush();
        //close the streams and socket
        dataOutputStream.close();
        bufferedReader.close();
        socket.close();
    }

    private static void fetch_page(String statusLine, String fileName, DataOutputStream dataOutputStream) throws IOException {
        FileInputStream fileInputStream = null;
        if(statusLine == "200 OK"){
            //Because the browser precedes the filename with a slash, we prefix a dot so that the resulting pathname starts within the src directory.
            fileName = "./src/pages" + fileName;
        }
        else if(statusLine == "301 Moved Permanently"){
            fileName = "./src/pages/home.html";
        }
        //open the requested file
        try {
            fileInputStream = new FileInputStream(fileName);
        }catch (FileNotFoundException e){
            fetchNotFound(dataOutputStream);
        }
        statusLine = http_version + statusLine + CRLF;
        String contentTypeLine = "Content-Type: " + contentType( fileName ) + CRLF;
        try {
            dataOutputStream.writeBytes(statusLine);
            dataOutputStream.writeBytes(contentTypeLine);
            // Send a blank line to indicate the end of the header lines.
            dataOutputStream.writeBytes(CRLF);
            sendBytes(fileInputStream,dataOutputStream);
        }
        catch (Exception e){
            fetchNotFound(dataOutputStream);
        }
        fileInputStream.close();
    }

    private static void fetchNotFound(DataOutputStream dataOutputStream) {
        String statusLine = http_version + "404 Not Found" + CRLF;
        String contentTypeLine = "Content-Type: text/html" + CRLF;

        String entityBody = "<HTML>" +
                    "<HEAD><TITLE>Not Found</TITLE></HEAD>" +
                    "<BODY>Not Found</BODY></HTML>";
        try {
            dataOutputStream.writeBytes(statusLine);
            dataOutputStream.writeBytes(contentTypeLine);
            // Send a blank line to indicate the end of the header lines.
            dataOutputStream.writeBytes(CRLF);
            dataOutputStream.writeBytes(entityBody);
        }catch (Exception e) {
            System.out.println(e);
        }
    }

    private static String getStatusLine(HashSet<String> pages, String fileName){
        if(fileName.equals("/index.html")){
            return "301 Moved Permanently";
        }
        else if(pages.contains(fileName)){
            return "200 OK";
        }
        return "404 Not Found";
    }

    //this function return a hashset that contain all available file name that can be fetched from GET funtion in http
    private static HashSet<String> getAvailablePages(){
        HashSet<String> pages = new HashSet<>();
        String path_name = System.getProperty("user.dir") + "/src/pages";
        File dir_pages = new File(path_name);
        File[] files = dir_pages.listFiles();
        for(File file : files){
            pages.add("/" + file.getName());
        }
        return pages;
    }

    //this function for now only handle html file,
    //if need to handle more different file type, can add more if condition
    private static String contentType(String fileName)
    {
        if(fileName.endsWith(".htm") || fileName.endsWith(".html")) {
            return "text/html";
        }
        return "application/octet-stream";
    }

    //this function take all content from file and write it into a DataOutputStream
    private static void sendBytes(FileInputStream fis, DataOutputStream os)
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
