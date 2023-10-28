package com.example.coughscan

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.media.MediaRecorder
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.CheckBox
import android.widget.Spinner
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.coughscan.models.ApiModels
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part
import java.io.File
import java.io.IOException

interface ApiService {
    @Multipart
    @POST("upload")
    fun uploadWebMFile(
        @Part file: MultipartBody.Part
    ): Call<ApiModels.ApiResponse>
}
class CoughActivity : AppCompatActivity() {
    private var recording: Boolean = false;
    private var mediaRecorder: MediaRecorder? = null
    private var fileName: String? = null
    private var recordButton: Button? = null;
    private var fever: Boolean = false;
    private var selectedAge: String = "0-9";
    private var selectedGender: String = "Male";

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cough)

        fileName = "${externalCacheDir?.absolutePath}/audiorecordtest.webm"

        val itemsAge = arrayOf("0-9", "10-19", "20-24", "25-59", "60+")
        val adapterAge = ArrayAdapter(this, android.R.layout.simple_spinner_item, itemsAge)
        adapterAge.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        val ageRangeSelector = findViewById<Spinner>(R.id.age_range_selector)
        ageRangeSelector.adapter = adapterAge

        ageRangeSelector.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                selectedAge = itemsAge[position]
            }

            override fun onNothingSelected(p0: AdapterView<*>?) {

            }
        }

        val itemsGender = arrayOf("Male", "Female", "Other")
        val adapterGender = ArrayAdapter(this, android.R.layout.simple_spinner_item, itemsGender)
        adapterGender.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        val genderSelector = findViewById<Spinner>(R.id.gender_selector)
        genderSelector.adapter = adapterGender;

        genderSelector.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                selectedGender = itemsAge[position]
            }

            override fun onNothingSelected(p0: AdapterView<*>?) {

            }
        }

        requestPermissions()
        initializeRecord()
    }

    private fun initializeRecord() {
        recordButton = findViewById<Button>(R.id.button_record)
        mediaRecorder = MediaRecorder()

        recordButton!!.setOnClickListener {
            if (recording) stopRecording() else startRecording()
            recording = !recording;
        }
    }

    private fun requestPermissions() {
        val permissions = arrayOf(
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.MANAGE_EXTERNAL_STORAGE
        )

        val permissionDenied = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_DENIED
        }

        if (permissionDenied.isNotEmpty()) {
            ActivityCompat.requestPermissions(this, permissionDenied.toTypedArray(), 1)
        }
    }

    private fun startRecording() {
        recordButton!!.text = "Recording..."
        mediaRecorder?.setAudioSource(MediaRecorder.AudioSource.MIC)
        mediaRecorder?.setOutputFormat(MediaRecorder.OutputFormat.WEBM)
        mediaRecorder?.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB)
        mediaRecorder?.setOutputFile(fileName)

        try {
            mediaRecorder?.prepare()
            mediaRecorder?.start()
        } catch (e: IOException) {
            e.printStackTrace()
        }
    }

    private fun stopRecording() {
        recordButton!!.text = "Record"
        mediaRecorder?.stop()
        mediaRecorder?.reset()
        mediaRecorder?.release()
        mediaRecorder = null

        postCough()
    }

    private fun webmToWav() {
        val retriever = FFmpegMediaMetadataRetriever()
        retriever.setDataSource(fileName)

        val command = arrayOf(
            "-i", fileName,
            "-vn",
            "-acodec", "pcm_s16le",
            fileName
        )

        val result = FFmpeg.execute(command)
        return result
    }

    private fun postCough() {
        val file = File(fileName)

        fever = findViewById<CheckBox>(R.id.fever_check_box).isActivated

        val requestFile = RequestBody.create("video/webm".toMediaTypeOrNull(), file)

        val filePart = MultipartBody.Part.createFormData("file", file.name, requestFile)

        val retrofit = Retrofit.Builder()
            .baseUrl("https://coughscan.net/upload")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val apiService = retrofit.create(ApiService::class.java)

        val call = apiService.uploadWebMFile(filePart)
        call.enqueue(object : Callback<ApiModels.ApiResponse> {
            override fun onResponse(call: Call<ApiModels.ApiResponse>, response: Response<ApiModels.ApiResponse>) {
                val responseBody = response.body()
                Log.d("main", responseBody.toString())

                val intent = Intent(this@CoughActivity, DiagnosisActivity::class.java)
                intent.putExtra("certainty", 89)
                intent.putExtra("diagnosis", true)
                intent.putExtra("age", selectedAge)
                intent.putExtra("gender", selectedGender)
                intent.putExtra("fever", fever)
                startActivity(intent)
            }

            override fun onFailure(call: Call<ApiModels.ApiResponse>, t: Throwable) {
                t.message?.let { Log.d("main", t.message!!) }
            }
        })
    }
}