package com.example.coughscan

import android.os.Bundle
import android.os.Handler
import android.widget.ProgressBar
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.coughscan.R

class DiagnosisActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_diagnosis)

        val diagnosis = intent.getBooleanExtra("diagnosis", false)
        findViewById<TextView>(R.id.diagnosis_display).text = "Diagnosis: ${if (diagnosis) "Positive" else "Negative"}"

        setCertaintyDisplay()
    }

    private fun setCertaintyDisplay() {
        val certainty = intent.getIntExtra("certainty", 0)
        val certaintyDisplay = findViewById<ProgressBar>(R.id.confidence_display)

        val delayMillis = 2L
        val maxProgress = certaintyDisplay.max

        val handler = Handler()

        val updateProgress = object : Runnable {
            var currentProgress = 0
            override fun run() {
                if (currentProgress <= certainty) {
                    certaintyDisplay.progress = currentProgress
                    currentProgress++
                    handler.postDelayed(this, delayMillis)
                }
            }
        }

        handler.post(updateProgress)
    }
}