function [out] = deinterleve(interleved)
%DEINTERLEVE Split an interleved complex vector into
% a Matlab complex vector
out = complex(interleved(1:2:end), interleved(2:2:end));
end

