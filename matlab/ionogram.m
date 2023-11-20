FS = 50e6 / 500;

[fn, pn] = uigetfile('../data/out/sim_real_raw.out');
fid = fopen(fullfile(pn, fn));
% raw = fread(fid, FS * 2 * 5, 'float32');
raw = fread(fid, inf, 'float32');
fclose(fid);

z = complex(raw(1:2:end),raw(2:2:end));
waterfall(z, FS);figure