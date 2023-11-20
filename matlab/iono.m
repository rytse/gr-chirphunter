WRI = 1;
%BW = 99951+53.2093-1.87407407407407;
BW = 100000;
Fc = 6043612;
F_tune = 25e6;
F_beat = 20e3;

Fs = 50e6; % Sample frequency (complex)
Ts = 1/Fs;

% Open GUI to select file, load that file
next_t = 0;
[fn, pn] = uigetfile('*.iq');
% fullfile(pn, fn)
fid_in = fopen(fullfile(pn, fn))
% fid_out = fopen(strcat(extractBefore(fullfile(pn, fn),'.iq'),'.spect_100kHz_2e25'),'wb')
fid_out = fopen('../data/out_spect_100kHz_2e25','wb');
fseek(fid_in,0,'eof');
flength = ftell(fid_in);
fclose(fid_in);
fid_in = fopen(fullfile(pn, fn))
%fseek(fid_in, 0, 'bof');
%win = nuttallwin(65536*4*2);
win = ones(2^25,1);
fft_at_a_time = 1;

for kk = 1:floor(flength / 4 / (fft_at_a_time * length(win)))
%for kk = 1:1
    kk
    s = fread(fid_in,fft_at_a_time*length(win) * 2,'int16');
    raw = complex(s(1:2:end),s(2:2:end));
    t = (next_t:Ts:next_t + (length(raw) - 1) * Ts)'; next_t = t(end) + Ts;
    raw = raw .* exp(j * 2 * pi * F_tune * t); % Put DC back to DC
    bb_phase = pi * (BW/WRI .* t) .* t; s_match = exp(j * bb_phase).*exp(j * 2 * pi * Fc .* t); % Make match filter
    s_c = raw .* conj(s_match .* exp(-j * 2 * pi * F_beat .* t)); % Offset match filter by F_beat and mix
    
    %f = int16(zeros(length(win),floor(length(s_c)/length(win)/2)));
    f = int16(zeros(length(win),floor(length(s_c)/length(win))));
    jj = 1;

%     for ii = 1:length(win)/2:length(s_c) - length(win)
%       %f(:,jj) = mag2db(abs(fftshift(fft(s_c(ii:ii+length(win)-1).*win))));
%       f(:,jj) = int16(round(db(abs((fft(s_c(ii:ii+length(win)-1).*win))),'voltage')));
%       jj = jj + 1
%     end
    for ll = 1:length(win):length(s_c)
      f(:,jj) = int16(round(db(abs((fft(s_c(ll:ll+length(win)-1).*win))),'voltage')));
      jj = jj + 1
    end
    count = fwrite(fid_out,f, 'int16')
end
fclose(fid_in);
fclose(fid_out);
% fid = fopen(strcat(extractBefore(fullfile(pn, fn),'.iq'),'.spect'),'rb');
% tmp = fread(fid,fft_at_a_time*length(win),'int16=>int16');
% fclose(fid)1
% imagesc(linspace(0,length(tmp)*Ts,length(tmp)/length(win)),linspace(0,50e6,length(win)),reshape(tmp,length(win),length(tmp)/length(win)))
