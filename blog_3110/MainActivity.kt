package com.example.mysample

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import okhttp3.*
import org.json.JSONObject
import java.io.IOException

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val intentText = intent.getCharSequenceExtra(Intent.EXTRA_PROCESS_TEXT)?.toString()
        val baseURL = "https://my-api/?word="

        if (intentText != null) {
            if(intentText.isNotEmpty()) {

                val client = OkHttpClient.Builder().build()
                val request = Request.Builder()
                    .url("$baseURL${intentText.lowercase()}")
                    .build()

                client.newCall(request).enqueue(object : Callback {
                    override fun onFailure(call: Call, e: IOException) {
                        runOnUiThread {
                            val tv = findViewById<TextView>(R.id.hellowworld)
                            tv.text = "error: $e"
                        }
                    }

                    @SuppressLint("SetTextI18n")
                    override fun onResponse(call: Call, response: Response) {
                        runOnUiThread {
                            val jsonText = response.body!!.string()
                            val tv = findViewById<TextView>(R.id.hellowworld)
                            tv.text = "no data"
                        }
                    }
                })
            }
        }
    }
}
