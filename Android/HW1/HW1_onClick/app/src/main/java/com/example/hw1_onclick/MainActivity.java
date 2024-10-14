package com.example.hw1_onclick;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    TextView text2;
    LinearLayout linearLayout1;
    ImageView imageview1, imageview2, imageview3;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 위젯을 변수에 대입
        text2 = (TextView) findViewById(R.id.Text2);
        linearLayout1 = (LinearLayout) findViewById(R.id.linearLayout1);
        imageview1 = (ImageView) findViewById(R.id.imageView1);
        imageview2 = (ImageView) findViewById(R.id.imageView2);
        imageview3 = (ImageView) findViewById(R.id.imageView3);
    }

    public void onButtonCliked(View v) {
        text2.setVisibility(View.VISIBLE);
        linearLayout1.setVisibility(View.VISIBLE);
    }

    public void onCheckBoxClicked(View v) {
        boolean checked = ((CheckBox) v).isChecked();

        // switch 문 대신 if-else 문 사용
        if (v.getId() == R.id.checkBox1) {
            if (checked) {
                imageview1.setVisibility(View.VISIBLE);
            } else {
                imageview1.setVisibility(View.INVISIBLE);
            }
        } else if (v.getId() == R.id.checkBox2) {
            if (checked) {
                imageview2.setVisibility(View.VISIBLE);
            } else {
                imageview2.setVisibility(View.INVISIBLE);
            }
        } else if (v.getId() == R.id.checkBox3) {
            if (checked) {
                imageview3.setVisibility(View.VISIBLE);
            } else {
                imageview3.setVisibility(View.INVISIBLE);
            }
        }}
}