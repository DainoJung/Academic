package com.example.hw2_explicitintent_twoway;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;

public class MainActivity extends AppCompatActivity {

    private TextView txtResult; // 결과를 표시할 TextView

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setTitle("사칙연산 앱");

        txtResult = findViewById(R.id.txtResult); // TextView 초기화
        txtResult.setVisibility(View.GONE); // 초기에는 보이지 않도록 설정
    }

    // 메뉴 생성
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater mInflater = getMenuInflater();
        mInflater.inflate(R.menu.menu_main, menu);
        return true;
    }

    // 옵션 클릭시 분기 처리
    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        EditText edtNum1 = (EditText) findViewById(R.id.edtNum1);
        EditText edtNum2 = (EditText) findViewById(R.id.edtNum2);

        // 입력값 검증
        if (edtNum1.getText().toString().isEmpty() || edtNum2.getText().toString().isEmpty()) {
            Toast.makeText(this, "숫자를 입력하세요.", Toast.LENGTH_SHORT).show();
            return false;
        }

        int num1 = Integer.parseInt(edtNum1.getText().toString());
        int num2 = Integer.parseInt(edtNum2.getText().toString());

        int itemId = item.getItemId();

        if (itemId == R.id.plus) {
            // 덧셈 Activity로 이동
            Intent intent = new Intent(getApplicationContext(),
                    AddActivity.class);
            intent.putExtra("Num1",
                    num1);
            intent.putExtra("Num2",
                    num2);
            startActivityForResult(intent, 0);
            return true;
        } else if (itemId == R.id.minus) {
            // 뺄셈 Activity로 이동
            Intent intent = new Intent(this, SubActivity.class);
            intent.putExtra("Num1",
                    num1);
            intent.putExtra("Num2",
                    num2);
            startActivityForResult(intent, 1);
            return true;
        } else if (itemId == R.id.times) {
            // 곱셈 Activity로 이동
            Intent intent = new Intent(this, MulActivity.class);
            intent.putExtra("Num1",
                    num1);
            intent.putExtra("Num2",
                    num2);
            startActivityForResult(intent, 2);
            return true;
        } else if (itemId == R.id.divide) {

            if (num2 == 0) {
                Toast.makeText(this, "0으로 나눌 수 없습니다.", Toast.LENGTH_SHORT).show();
                return false;
            }

            // 나눗셈 Activity로 이동
            Intent intent = new Intent(this, DivActivity.class);
            intent.putExtra("Num1",
                    num1);
            intent.putExtra("Num2",
                    num2);
            startActivityForResult(intent, 3);
            return true;
        } else {
            return super.onOptionsItemSelected(item);
        }

    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (resultCode == RESULT_OK) {

            if (requestCode == 3) {
                // 나눗셈 연산 결과 처리
                float result = data.getFloatExtra("Hap", 0.0f);
                txtResult.setText("연산 결과: " + result); // 실수 결과를 문자열로 설정
            } else {
                // 덧셈/뺄셈/곱셈 연산 결과 처리
                int result = data.getIntExtra("Hap", 0);

                txtResult.setText("연산 결과: " + result); // 정수 결과를 문자열로 설정
            }

            txtResult.setVisibility(View.VISIBLE);

        }

    }

}