package com.example.policlass_poc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

public class DisplayResult extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_result);

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
