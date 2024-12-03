package com.example.hw2_explicitintent_twoway;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class DivActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        setTitle("Div_Activity");

        Intent inIntent = getIntent();
        final float hapValue = (float) inIntent.getIntExtra("Num1", 0)
                / inIntent.getIntExtra("Num2", 0);

        Toast.makeText(getApplicationContext(), "나눗셈 결과 :" + hapValue,
                Toast.LENGTH_LONG).show();

        Button btnReturn = (Button) findViewById(R.id.btnReturn);
        btnReturn.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Intent outIntent = new Intent(getApplicationContext(),
                        MainActivity.class);
                outIntent.putExtra("Hap", hapValue);
                setResult(RESULT_OK, outIntent);
                finish();
            }
        });
    }
}
