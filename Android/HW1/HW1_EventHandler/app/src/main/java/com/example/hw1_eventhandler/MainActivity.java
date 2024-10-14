package com.example.hw1_eventhandler;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    TextView text1;
    TextView text2;
    Button btnOK;
    LinearLayout linearLayout1;
    CheckBox checkBox1, checkBox2, checkBox3;
    ImageView imageView1, imageView2, imageView3;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 위젯을 변수에 대입
        text2 = (TextView) findViewById(R.id.Text2);
        btnOK = (Button) findViewById(R.id.BtnOK);
        linearLayout1 = (LinearLayout) findViewById(R.id.linearLayout1);
        checkBox1 = (CheckBox) findViewById(R.id.checkBox1);
        checkBox2 = (CheckBox) findViewById(R.id.checkBox2);
        checkBox3 = (CheckBox) findViewById(R.id.checkBox3);
        imageView1 = (ImageView) findViewById(R.id.imageView1); // 강아지
        imageView2 = (ImageView) findViewById(R.id.imageView2); // 고양이
        imageView3 = (ImageView) findViewById(R.id.imageView3); // 토끼


        // 선택확인 버튼 클릭시
        btnOK.setOnClickListener(new View.OnClickListener() {
            public void onClick(View arg0) {
                text2.setVisibility(android.view.View.VISIBLE);
                linearLayout1.setVisibility(android.view.View.VISIBLE);
            }        });

        // 체크박스 클릭 리스너
        checkBox1.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (isChecked) {
                imageView1.setVisibility(View.VISIBLE); // 강아지 이미지 보이기
            } else {
                imageView1.setVisibility(View.INVISIBLE); // 강아지 이미지 숨기기
            }
        });

        checkBox2.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (isChecked) {
                imageView2.setVisibility(View.VISIBLE); // 고양이 이미지 보이기
            } else {
                imageView2.setVisibility(View.INVISIBLE); // 고양이 이미지 숨기기
            }
        });

        checkBox3.setOnCheckedChangeListener((buttonView, isChecked) -> {
            if (isChecked) {
                imageView3.setVisibility(View.VISIBLE); // 토끼 이미지 보이기
            } else {
                imageView3.setVisibility(View.INVISIBLE); // 토끼 이미지 숨기기
            }
        });
    }


}