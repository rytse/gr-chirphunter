FS = 50e6 / 500;

[fn, pn] = uigetfile('../data/out/*.out');
fid = fopen(fullfile(pn, fn));
raw = fread(fid, inf, 'float32');
fclose(fid);

z = complex(raw(1:2:end),raw(2:2:end));
waterfall(z, FS);