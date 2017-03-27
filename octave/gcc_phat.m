function [tau, cc] = gcc_phat(sig, refsig, fs, max_tau, interp)

n = length(sig) + length(refsig);
max_shift = floor(n / 2);

if nargin < 3
  fs = 1;
end

if nargin >= 4
  max_shift = min(floor(fs * max_tau), max_shift);
end

if nargin < 5
  interp = 1;
end

max_shift = max_shift * interp;

X1 = fft(sig, n);
X2 = fft(refsig, n);
R = X1 .* conj(X2);

cc = ifft(R ./ (abs(R)), n * interp);
N = length(cc);
cc = [cc((N - max_shift + 1):N)(:); cc(1:(max_shift + 1))(:)];
cc = abs(cc);

[max_cc, shift] = max(cc);
shift -= max_shift + 1;

tau = shift / (interp * fs);

end



