function [f] = fwf(cin, fs, wsize, to_plot)
% Flexible waterfall plot
%   cin: input signal (complex)
%   fs: sampling rate (Hz)

ELAPSED_TIME = length(cin) / fs;
win = nuttallwin(wsize);
f = zeros(length(win),floor(length(cin)/length(win)/2), 'single');
jj = 1;

for ii = 1 : length(win) / 2 : length(cin) - length(win)
  f(:, jj) = cast(db(abs(fft(cin(ii : ii + length(win) - 1) .* win))), 'single');
  jj = jj + 1;
end

if to_plot
    [k,m] = size(f);
    gr = imagesc(linspace(0, ELAPSED_TIME, m),linspace(0, fs, k), f);
    % gr = imagesc(linspace(0, ELAPSED_TIME, m),linspace(0, 50e6 / 4, k), f(1:round(length(f)/4),:));
    % gr = imagesc(linspace(0, ELAPSED_TIME, m),linspace(0, fs / 4, k), f(1:round(length(f)/4),round(m / 2) : round(m / 2 * 1.3)));

    set(gca,'YDir','normal')
    colormap(hsv);
end

end

