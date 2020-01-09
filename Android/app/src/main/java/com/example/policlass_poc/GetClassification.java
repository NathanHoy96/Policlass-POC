package com.example.policlass_poc;

import android.os.AsyncTask;
import android.text.LoginFilter;
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
    private String serverIP = "35.178.29.132";
    private Socket socket;
    private PrintWriter clientOutput;
    private BufferedReader clientInput;
    MainActivity main;

    private String response;

    GetClassification(MainActivity m)
    {
        this.main = m;
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
        main.asyncResult(s);
    }
}

