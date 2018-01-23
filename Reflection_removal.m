
function [y,delay] = GroundReflectionCorrection(x)

%%	Perform auto-correlation and its identify peaks
[acf,lags] = xcorr(x,'none');	%Autocorrelation (unnormalized)

center = length(x);

% acf = acf(center:end);	lags = lags(center:end);
[pks,locs] = findpeaks(acf);	%Find peaks of auto-correlation
% if locs(1) ~= 1
% 	pks = [acf(1),pks(:)'];
% 	locs = [1,locs(:)'];
% end
[zp,zmp] = max(pks);			% Maximum is located at center
pks(zmp) = 0;
ipks = find(pks > zp*0.1 & pks < zp*0.5);
pks = pks(ipks);
locs = locs(ipks);
[mp,imp] = max(pks);
secondpk = locs(imp);
delay = abs(secondpk - center);


mp = mp/zp;

if mp > 0.5
	y = x;
	return
end

np = (1 - sqrt(1-4*mp.^2))/(2*mp);

y = x;
for iter = 1:4
	
	if iter*delay > length(x)
		break;
	end

	xsub = zeros(size(x));
	xsub(iter*delay+1:end) = (-np).^iter*x(1:end-iter*delay);
	y = y + xsub;
end
