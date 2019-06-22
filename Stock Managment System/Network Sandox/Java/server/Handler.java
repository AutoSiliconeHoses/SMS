import java.io.*;
import java.net.*;
import java.util.*;

public class Handler extends Thread {
	private Socket handleSocket = null;

	public Handler(Socket handleSocket ){
		super("Handler");
		this.handleSocket = handleSocket;
	}

	private String ListFiles(){
		File[] dirList = new File("./serverFiles").listFiles();
		String files = "Files in Directory:";
		for (File serverDir: dirList) {
			files += "\n" + serverDir;
		}
		return files;
	}
	// functionality for put
	private void GetFromClient(String name) throws IOException{
		OutputStream outFile = new FileOutputStream("./serverFiles/" + name); // makes file object
		InputStream inFile = handleSocket.getInputStream();
		byte[] fBytes = new byte[65536];
		for (int x; (x = inFile.read(fBytes)) > 0;) { // reads data from stream
			outFile.write(fBytes, 0, x); // puts data into file
		}
		outFile.close();
		inFile.close();
	}

	private void GiveToClient(String name) throws IOException{
		File sending = new File("./serverFiles/" + name); // makes file object
		InputStream inFile = new FileInputStream(sending);
		OutputStream outFile = handleSocket.getOutputStream();
		byte[] fBytes = new byte[65536];
		for (int x; (x = inFile.read(fBytes)) > 0;) { // reads data from file
			outFile.write(fBytes, 0, x); //puts data into stream
		}
		inFile.close();
		outFile.close();
	}

	public void run(){
		String command, fName;
		try{
			BufferedReader iStream = new BufferedReader(new InputStreamReader(handleSocket.getInputStream())); // get from client
			PrintWriter oStream = new PrintWriter(handleSocket.getOutputStream(), true); // sends to client
			InetAddress inet = handleSocket.getInetAddress();
			System.out.println("Connection made from " + inet.getHostName());
			String inputLine, outputLine;
			inputLine = iStream.readLine();
			String[] input = inputLine.trim().split("\\s+"); // splits the sent arguments string from client

			if(input.length == 1){
				command = input[0];
				fName = "";
			}
			else {
				command = input[0];
				fName = input[1];
			}

			if (command.equalsIgnoreCase("list")) {
				oStream.println(ListFiles());
			}
			else if (command.equalsIgnoreCase("get")){
				if (fName.equalsIgnoreCase("")) {
					System.err.println("Error: client provided no file for get request");
				}
				else {
					GiveToClient(fName);
				}
			}
			else if(command.equalsIgnoreCase("put")){
				if (fName.equalsIgnoreCase("")) {
					System.err.println("Error: client provided no file for put request");
				}
				else {
					GetFromClient(fName);
				}
			}
			else {
				outputLine = "Command not regognised";
			}

			oStream.close();
			iStream.close();
			handleSocket.close();
		}
		catch(IOException e){
			e.printStackTrace();
		}
	}
}
