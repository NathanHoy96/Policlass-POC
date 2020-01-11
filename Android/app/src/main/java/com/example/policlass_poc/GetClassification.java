package com.example.policlass_poc;

import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class GetClassification extends AsyncTask<String,Void,String> {

    private int serverPort = 8000;
    private String serverIP = "52.56.96.103";
    private Socket socket;
    private PrintWriter clientOutput;
    private BufferedReader clientInput;
    DisplayResult displayResult;

    private String response;

    GetClassification(DisplayResult displayResult)
    {
        this.displayResult = displayResult;
    }

    @Override
    protected String doInBackground(String... voids) {

        try {
            Log.i("Progress", "Executing thread");
            socket = new Socket(serverIP,serverPort);
            Log.i("Connected to: ",socket.getRemoteSocketAddress().toString());
            clientOutput = new PrintWriter(new OutputStreamWriter(socket.getOutputStream(), StandardCharsets.UTF_8), true);
            clientInput = new BufferedReader(new InputStreamReader(socket.getInputStream(), StandardCharsets.UTF_8));
            clientOutput.println(voids[0]);
            Log.i("Message state:","Sent");
            response = clientInput.readLine();
            Log.i("Response: ",response);
            socket.close();
            clientOutput.close();
            clientInput.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
        return response;
    }

    @Override
    protected void onPostExecute(String s) {
        displayResult.asyncResult(s);
    }
}

