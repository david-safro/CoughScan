library(tuneR)
library(seewave)

audio_file <- readWave("path_to_audio_file.wav")

par(mfrow=c(5, 2))

plot(audio_file, main = "Waveform", xlab = "Time (s)", ylab = "Amplitude")

spectrogram(audio_file, main = "Spectrogram", xlab = "Time (s)", ylab = "Frequency (Hz)")

ae <- envelope(audio_file)
plot(ae, main = "Amplitude Envelope", xlab = "Time (s)", ylab = "Amplitude")

pitch_obj <- pitch(audio_file)
plot(pitch_obj, main = "Pitch", xlab = "Time (s)", ylab = "Pitch (Hz)")

freq <- fpeaks(audio_file)
plot(freq, main = "Frequency Distribution", xlab = "Frequency (Hz)", ylab = "Amplitude")

plotWT(audio_file, main = "Wavelet Transform")

plot(zero_cross(audio_file), main = "Zero-Crossings", xlab = "Time (s)", ylab = "Count")

mfcc_obj <- melfcc(audio_file)
image(mfcc_obj$coeff, main = "MFCC", xlab = "Frame", ylab = "Coefficient")

fund_freq <- fundfreq(audio_file)
plot(fund_freq, main = "Fundamental Frequency Contour", xlab = "Time (s)", ylab = "Frequency (Hz)")

sc <- spectralCentroid(audio_file)
plot(sc, main = "Spectral Centroid", xlab = "Time (s)", ylab = "Frequency (Hz)")
