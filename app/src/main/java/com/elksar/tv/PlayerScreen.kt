package com.elksar.tv

import android.content.Context
import android.net.Uri
import android.view.KeyEvent
import android.view.ViewGroup
import android.widget.FrameLayout
import androidx.compose.foundation.background
import androidx.compose.foundation.focusable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.key.onKeyEvent
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.DefaultLoadControl
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.media3.ui.PlayerView
import androidx.tv.material3.ExperimentalTvMaterial3Api
import androidx.tv.material3.Text

// Sample test streams
val testStreams = listOf(
    "http://sample.vodobox.net/skate_phantom_flex_4k/skate_phantom_flex_4k.m3u8",
    "http://devimages.apple.com/iphone/samples/bipbop/bipbopall.m3u8",
    "https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8"
)

fun provideExoPlayer(context: Context): ExoPlayer {
    val loadControl = DefaultLoadControl.Builder()
        .setBufferDurationsMs(
            1500,  // Min buffer to start
            5000,  // Max buffer
            1000,  // Buffer after pause
            1500   // Buffer to resume
        )
        .build()

    return ExoPlayer.Builder(context)
        .setLoadControl(loadControl)
        .setHandleAudioBecomingNoisy(true)
        .setWakeMode(C.WAKE_MODE_NETWORK)
        .build()
}

@OptIn(ExperimentalTvMaterial3Api::class)
@Composable
fun PlayerScreen() {
    val context = LocalContext.current
    var currentStreamIndex by remember { mutableIntStateOf(0) }

    val exoPlayer = remember { provideExoPlayer(context) }
    val focusRequester = remember { FocusRequester() }

    LaunchedEffect(currentStreamIndex) {
        val mediaItem = MediaItem.fromUri(Uri.parse(testStreams[currentStreamIndex]))
        exoPlayer.setMediaItem(mediaItem)
        exoPlayer.prepare()
        exoPlayer.playWhenReady = true
    }

    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black)
            .focusRequester(focusRequester)
            .focusable()
            .onKeyEvent { keyEvent ->
                if (keyEvent.nativeKeyEvent.action == KeyEvent.ACTION_DOWN) {
                    when (keyEvent.nativeKeyEvent.keyCode) {
                        KeyEvent.KEYCODE_DPAD_UP -> {
                            currentStreamIndex = (currentStreamIndex + 1) % testStreams.size
                            true
                        }
                        KeyEvent.KEYCODE_DPAD_DOWN -> {
                            currentStreamIndex = if (currentStreamIndex - 1 < 0) testStreams.size - 1 else currentStreamIndex - 1
                            true
                        }
                        else -> false
                    }
                } else {
                    false
                }
            }
    ) {
        AndroidView(
            factory = { ctx ->
                PlayerView(ctx).apply {
                    player = exoPlayer
                    useController = false
                    resizeMode = AspectRatioFrameLayout.RESIZE_MODE_FIT
                    layoutParams = FrameLayout.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                }
            },
            modifier = Modifier.fillMaxSize()
        )

        // Simple overlay to show stream index during test phase
        Text(
            text = "Test Stream: ${currentStreamIndex + 1}/${testStreams.size}",
            color = Color(0xFF00E5FF),
            modifier = Modifier
                .align(Alignment.TopStart)
                .padding(16.dp)
        )
    }

    LaunchedEffect(Unit) {
        focusRequester.requestFocus()
    }
}
