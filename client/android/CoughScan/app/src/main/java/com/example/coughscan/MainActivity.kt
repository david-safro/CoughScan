package com.example.coughscan

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button

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
    }
}