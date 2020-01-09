package com.example.policlass_poc;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    private EditText urlEditText;
    private TextView classifcationDisplay;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void On_Classify_Click(View view) {

        urlEditText = findViewById(R.id.url_input);
        classifcationDisplay = findViewById(R.id.classification_text);

        String url = urlEditText.getText().toString();
        Log.i("URL Entry: ",url);

        GetClassification getClassification = new GetClassification(this);
        getClassification.execute(url);
    }

    void asyncResult(String result) {
        //This method is called when AsyncTask posts its result. Do you stuff here
        classifcationDisplay = findViewById(R.id.classification_text);
        classifcationDisplay.setText(result.toUpperCase());
    }
}
