function [amax] = freqfiltdetect(z, wlen, elt)

zsel = z(1: wlen * elt);
spec = fft(zsel);
rspec = reshape(spec, wlen, length(spec) / wlen);
out = real(diff(sum(rspec')));

plot(out);

[m, amax] = max(out);

end

