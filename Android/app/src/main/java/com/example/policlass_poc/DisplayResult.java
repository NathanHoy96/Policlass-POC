package com.example.policlass_poc;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.Intent;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.TextView;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;


public class DisplayResult extends AppCompatActivity {

    private TextView classificationText;
    private ArrayList<String> alternativesList;
    private ArrayAdapter<String> arrayAdapter;
    private RecyclerView recyclerView;
    private ParseAdapter adapter;
    private ArrayList<ParseItem> parseItems = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_result);

        classificationText = findViewById(R.id.classification_text);
        alternativesList = new ArrayList<String>();
        arrayAdapter = new ArrayAdapter<String>(getApplicationContext(), android.R.layout.simple_spinner_item, alternativesList);

        recyclerView = findViewById(R.id.recyclerView);

        recyclerView.setHasFixedSize(true);
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        adapter = new ParseAdapter(parseItems, this);
        recyclerView.setAdapter(adapter);

        Intent intent = getIntent();
        String action = intent.getAction();
        String type = intent.getType();

        if (Intent.ACTION_SEND.equals(action) && type != null) {
            if ("text/plain".equals(type)) {
                handleSendText(intent); // Handle text being sent
            }
        }
    }

    void handleSendText(Intent intent) {
        String sharedText = intent.getStringExtra(Intent.EXTRA_TEXT);
        Log.i("Shared Text ", sharedText);
        if (sharedText != null) {
            // Update UI to reflect text being shared
            GetClassification getClassification = new GetClassification(this);
            getClassification.execute(sharedText);
        }
    }

    void asyncResult(String result) {
        //This method is called when AsyncTask 'Get Classification' posts its result. Do you stuff here
        String[] items = result.split(",");
        for (int i = 0; i < items.length; i++) {
            alternativesList.add(items[i]);
        }

        for (int j = 0; j < alternativesList.size(); j++) {
            Log.i("List items", alternativesList.get(j) + "\n");
        }

        findViewById(R.id.progress_bar).setVisibility(View.GONE);
        findViewById(R.id.progress_text).setVisibility(View.GONE);

        classificationText.setText("Your article was classed as "+ alternativesList.get(0) + " wing");

        alternativesList.remove(0);
        updateView();
    }

    private void updateView() {
        //arrayAdapter.notifyDataSetChanged();
        Log.i("Getting images", ":True");
        Content content = new Content();
        content.execute();
    }


    private class Content extends AsyncTask<Void, Void, Void> {



        @Override
        protected void onPostExecute(Void aVoid) {
            super.onPostExecute(aVoid);
            adapter.notifyDataSetChanged();
        }

        @Override
        protected Void doInBackground(Void... voids) {

            for (int i = 0 ; i < alternativesList.size(); i++)
            {
                try {
                    String url = alternativesList.get(i);
                    Document doc = Jsoup.connect(url).get();

                    Elements data = doc.select("head");
                    int size = data.size();
                    Log.d("doc", "doc: " + doc);
                    Log.d("data", "data: " + data);
                    Log.d("size", "" + size);
                    for (int j = 0; j< size; j++) {
                        String imgUrl = String.valueOf(data.select("meta[property=og:image]").attr("content"));

                        String title = String.valueOf(data.select("meta[property=og:title]").attr("content"));

                        String detailUrl = String.valueOf(data.select("meta[property=og:url]").attr("content"));

                        parseItems.add(new ParseItem(imgUrl, title, detailUrl));
                        Log.d("items", "img: " + imgUrl + " . title: " + title);
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return null;
        }
    }

}