WLEN = 2^20;
NW = 128;

fid = fopen('../data/out/real_nofilt_nodecim_adj.out', 'rb');
raw = fread(fid, WLEN * NW * 2, 'float32');
fclose(fid);
raw = complex(raw(1:2:end), raw(2:2:end));

f = fwf(raw, 50e6, WLEN, 0);
figure;

% spec = fft(raw);
% spec = reshape(spec, WLEN, length(spec) / WLEN);
% out = real(diff(sum(spec')));

out = real(diff(sum(f')));

out = out / max(out);
bfs = linspace(0, 50e6, length(f));
plot(bfs(1:end-1)/1e6, out);
xlabel('Beat Frequency (MHz)');
ylabel('Waterfall Row Sum (Normalized)');