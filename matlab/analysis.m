FS = 50e6;
ELAPSED_TIME = 6;

live = readraw(FS, ELAPSED_TIME);
% signalhound double fftshifted the data we collected, so we shift back
live = ifft(fftshift(fft(live)));
waterfall(live, FS)
figure

% t1 = 0.08547;
% f1 = 5.116e6;
% t2 = 10;
% f2 = 5.602e6;
% 
% ch = chirpgen(t1, f1, t2, f2, FS, ELAPSED_TIME);
% waterfall(ch, FS)