package com.example.policlass_poc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;

public class DisplayResult extends AppCompatActivity {

    private TextView classificationText;
    private ListView alternativesListView;
    private ArrayList<String> alternativesList;
    private ArrayAdapter<String> arrayAdapter;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_result);

        classificationText = findViewById(R.id.classification_text);
        alternativesListView = findViewById(R.id.alternative_list);
        alternativesList = new ArrayList<String>();
        arrayAdapter = new ArrayAdapter<String>(getApplicationContext(),android.R.layout.simple_spinner_item,alternativesList);

        alternativesList.add("https://www.bbc.co.uk/news/world-middle-east-51073621");
        alternativesList.add("https://www.bbc.co.uk/news/uk-england-northamptonshire-51075235");
        alternativesList.add("https://www.bbc.co.uk/news/uk-northern-ireland-51077397");

        alternativesListView.setAdapter(arrayAdapter);

        Intent intent = getIntent();
        String action = intent.getAction();
        String type = intent.getType();

        if (Intent.ACTION_SEND.equals(action) && type != null)
        {
            if ("text/plain".equals(type))
            {
                handleSendText(intent); // Handle text being sent
            }
        }
    }

    void handleSendText(Intent intent) {
        String sharedText = intent.getStringExtra(Intent.EXTRA_TEXT);
        Log.i("Shared Text ",sharedText);
        if (sharedText != null) {
            // Update UI to reflect text being shared
            GetClassification getClassification = new GetClassification(this);
            getClassification.execute(sharedText);
        }
    }

    void asyncResult(String result) {
        //This method is called when AsyncTask 'Get Classification' posts its result. Do you stuff here
    }
}
