import java.io.*;
import java.net.*;
import java.util.*;

public class Client {
	private Socket cwClientSocket = null;
	private BufferedReader clientInput = null;
	private PrintWriter clientOutput = null;
	private static String command, fName;

 //if only one argument is given, when list is requested
	private Client(String comm){
		this.command = comm;
		this.fName = "";
	}
	//if 2 arguments are given, for put and get
	private Client(String comm, String fN){
		this.command = comm;
		this.fName = fN;
	}
	// List files function
	private void ListFiles() throws IOException {
		String file; // a string is created in handler, and is given to client line by line
		while ((file = clientInput.readLine()) != null){
			System.out.println(file);// as long as line != null each line will be printed
		}
	}
	// functionality for put
	private void PutIntoServer (String name) throws IOException {
		File sending = new File("./clientFiles/" + name); // makes file object
		InputStream inFile = new FileInputStream(sending);
		OutputStream outFile = cwClientSocket.getOutputStream();
		byte[] fBytes = new byte[65536];
		for (int x; (x = inFile.read(fBytes)) > 0;) {//reads bytes from file
			outFile.write(fBytes, 0, x);//sends bytes into stream
		}
		inFile.close();
		outFile.close();
	}
	// functionality for get
	private void GetFromServer(String name) throws IOException {
		OutputStream outFile = new FileOutputStream("./clientFiles/" + name); // makes file object
		InputStream inFile = cwClientSocket.getInputStream();
		byte[] fBytes = new byte[65536];
		for (int x; (x = inFile.read(fBytes)) > 0;) { // reads bytes from stream
			outFile.write(fBytes, 0, x); //writes bytes into file
		}
		outFile.close();
		inFile.close();
	}
	public void runClient(){
		try{
			cwClientSocket = new Socket("192.168.0.43", 8888);
			clientInput = new BufferedReader(new InputStreamReader(cwClientSocket.getInputStream())); //puts data into strea
			clientOutput = new PrintWriter(cwClientSocket.getOutputStream(), true);
		}
		catch(UnknownHostException e){
			System.err.println("Unknown Host\n");
			System.exit(1);
		}
		catch(IOException e){
			System.err.println("Couldn't retrieve IO for connection to host.\n");
			System.exit(1);
		}

		try{
			System.out.println(fName);
			clientOutput.println(command + " " + fName); // sends the arguments to server
			if (command.equalsIgnoreCase("list")) {
				ListFiles();
			}
			else if (command.equalsIgnoreCase("put")){
				if (!(fName.equals(""))) {
					PutIntoServer(fName);
				}
				else {
					System.err.println("Error: no file input");
				}
			}
			else if (command.equalsIgnoreCase("get")){
				if (!(fName.equals(""))) {
					GetFromServer(fName);
				}
				else {
					System.err.println("Error: no file input");
				}
			}

			clientOutput.close();
			clientInput.close();
			cwClientSocket.close();
		}
		catch(IOException e){
			System.err.println("IO Exception during execution\n");
			System.exit(1);
		}
	}

	public static void main( String[] args ){
		 //input is requred because otherwise nothing will be done
		if (args.length == 0){
			System.err.println("Error: No inputs");
		}
		// optional inputs are created because get and put need file arguments, but list does not
		else if (args.length == 1){
			Client client = new Client(args[0]);
			client.runClient();
		}
		else if (args.length == 2){
			Client client = new Client(args[0], args[1]);
			//System.out.println(args[1]);
			client.runClient();
		}
		//error handling for more than 2 arguments
		else{
			System.err.println("Error: Too many inputs");
		}
	}
}
