function [out] = readraw(fs, elapsed_time)
% Load an IQ file selected by GUI as a complex vector
%   fs sampling rate (Hz)
%   elapsed_time amount of the file to load (seconds)

[fn, pn] = uigetfile('*.iq');
fid = fopen(fullfile(pn, fn));
raw = fread(fid, fs * elapsed_time * 2, 'int16');
fclose(fid);
out = complex(raw(1:2:end),raw(2:2:end));

end