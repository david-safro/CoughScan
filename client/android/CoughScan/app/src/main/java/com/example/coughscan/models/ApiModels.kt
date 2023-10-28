package com.example.coughscan.models
public class ApiModels() {
    data class ApiResponse(
        val success: Boolean,
        val message: String?,
        val data: WebMFile?
    )

    data class WebMFile(
        val id: String,
        val filename: String,
        val url: String
    )
}
