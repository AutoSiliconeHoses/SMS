import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;

public class Server{
	public static void main(String[] args) throws IOException {
		ServerSocket server = null;
		ExecutorService exService = null;
		boolean listen = true;
		int port = 8888;

		System.out.println("Connecting to port " + port + ".");
		try{
			server = new ServerSocket(port);
		}
		catch(IOException e){
			System.err.println("Error: Could not listen to port: " + port + ".");
			System.exit(-1);
		}
		System.out.println("Succefully connected to port " + port + ".");
		exService = Executors.newFixedThreadPool(10);
		System.out.println("Service Created.");
		while (listen){
			Socket client = server.accept();
			exService.submit(new Handler(client));
		}
		server.close();
	}
}
