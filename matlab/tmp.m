WLEN = 2^20;
NW = 128;

%fid = fopen('../data/out/real_nofilt_nodecim.out', 'rb');
raw = fread(fid, WLEN * NW * 2);
raw = complex(raw(1:2:end), raw(2:2:end));

spec = fft(raw);
spec = reshape(spec, WLEN, length(spec) / WLEN);
out = real(diff(sum(spec')));

plot(out);