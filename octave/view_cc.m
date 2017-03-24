



[far, fs] = audioread('../audio/alexa-01.wav');
[near, fs] = audioread('../audio/alexa-02.wav');

% 0.14 m is the distance of the two microphones 
% 340 m/s as the sound speech 
max_tau = 0.14 / 340;
audio_length = length(far);
block_length = floor(fs / 2);
n = floor(audio_length / block_length);
samples = floor(max_tau * fs) * 2 + 1;
z = zeros(samples, n);
window = hanning(block_length);

for k = 1:n
  i = (k - 1) * block_length + 1;
  sig = near(i:(i + block_length - 1)) .* window;
  refsig = far(i:(i + block_length - 1)) .* window;
  [tau, cc] = gcc_phat(sig, refsig, fs, max_tau);
  z(:,k) = abs(cc);
end

surf(z);
colormap(hot)

