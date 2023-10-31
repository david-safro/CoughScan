package com.example.coughscan

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val coughNavButton = findViewById<Button>(R.id.button_nav_cough)
        val symptomsNavButton = findViewById<Button>(R.id.button_nav_symptoms)

        coughNavButton.setOnClickListener {
            val intent = Intent(this, CoughActivity::class.java)
            startActivity(intent)
        };

        symptomsNavButton.setOnClickListener {
            val intent = Intent(this, DiagnosisActivity::class.java)
            intent.putExtra("certainty", 89)
            intent.putExtra("diagnosis", true)
            intent.putExtra("age", "10-19")
            intent.putExtra("gender", "Male")
            intent.putExtra("fever", "true")
            startActivity(intent)
        };
    }
}