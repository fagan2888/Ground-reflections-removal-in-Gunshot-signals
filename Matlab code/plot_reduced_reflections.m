fldr = '/home/administrator/Tushar/test_data_files/single shots/Glockpistol_6.4_S'; % Path of binary file where gunshot was recorded
fldr1 = '/home/administrator/Tushar/Data_Files'; % Path of pqfile.txt where Events is saved

sampling_rate = 50000; %Hz
wndw_prec = 0.002; %sec , Time for taking readings before event
wndw_post = 0.008; %sec , Time for taking readings after event

fid = fopen(fullfile(fldr1,'pqfile.txt'),'r');

tline = fgetl(fid);
fclose(fid);

while ischar(tline)
    EventId = str2num(tline); %#ok<ST2NM> 
    y = Events_sepfrmpq(sampling_rate,wndw_prec,wndw_post,EventId);
    [y1,grd_dly] = GroundReflectionCorrection(y);
    t = linspace(0,0.01,501);
    plot(t,y);hold all;plot(t,y1);
    title('Muzzle blast signature of glock pistol with reduction of ground reflections')
    xlabel('Time (sec)')
    ylabel('Amplitude')
    legend('original signature','reduced ground reflections signature','FontSize',26,'location','best')
    tline = fgetl(fid);
end

