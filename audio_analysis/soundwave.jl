using WAV
using Plots
using DSP
using MFCC
using TempoEstimation

function analyze_audio(audio_file::String)
    audio_data, sample_rate = wavread(audio_file)

    time_vector = (0:length(audio_data) - 1) / sample_rate

    plot(time_vector, audio_data, xlabel="Time (s)", ylabel="Amplitude", label="Waveform")

    envelope = abs.(hilbert(audio_data))
    plot!(time_vector, envelope, label="Amplitude Envelope")

    pitch_values = pitch(audio_data, sample_rate=sample_rate)
    time_pitch = (0:length(pitch_values) - 1) * pitchres(audio_data, sample_rate=sample_rate)

    plot!(time_pitch, pitch_values, xlabel="Time (s)", ylabel="Pitch (Hz)", label="Pitch")

    _, _, spec = spectrogram(audio_data, nfft=1024, fs=sample_rate)
    heatmap(time_vector, 0:sample_rate/1024:sample_rate/2, spec, xlabel="Time (s)", ylabel="Frequency (Hz)", color=:auto, label="Spectrogram")

    mfcc_coeffs = mfcc(audio_data, fs=sample_rate)
    time_mfcc = (0:size(mfcc_coeffs, 2) - 1) * (length(audio_data) / sample_rate) / (size(mfcc_coeffs, 2) - 1)

    plot(time_mfcc, mfcc_coeffs', xlabel="Time (s)", ylabel="MFCC Coefficients", label=[f"MFCC $i" for i in 1:size(mfcc_coeffs, 1)])

    tempo, beats = tempo(audio_data, sample_rate)

    plot!(beats, zeros(length(beats)), st=:stem, color=:red, label="Beats")

    println("Estimated tempo: ", tempo, " BPM")

    display(Plots.plot!())
end

audio_file_path = "path/to/your_audio_file.wav"
analyze_audio(audio_file_path)
