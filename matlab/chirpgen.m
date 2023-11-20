function [out] = chirpgen(t1, f1, t2, f2, fs, elapsed_time)
% Generate complex LFM chirp given a time domain and two points on the line
%   ts time series along which to generate the chirp
%   fs sampling rate
%   t1 time of the first point on the line
%   f1 frequency of the first point on the line
%   t2 time of the second point on the line
%   f2 frequency of the second point on the line

m = (f2 - f1) / (t2 - t1);

start_f = m * (0 - t1) + f1;
stop_f = m * (elapsed_time - t1) + f1;
bw = stop_f - start_f;

% ts = linspace(0, elapsed_time, elapsed_time * fs);
t = 0:1/fs:elapsed_time;
t(end) = [];

bb_phase = 2 * pi * (bw / elapsed_time .* t) .* t;
plot(bb_phase)
figure

s = exp(j * bb_phase) .* exp(2 * pi * j * start_f .* t);
out = s.';

end

