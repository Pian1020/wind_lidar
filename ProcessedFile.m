%% code for Wind Lidar
% Created date: 2023.07.20
% Created by Zhai Huang
% For plotting the Wind Lidar wind profile
% Use file named "Processed_Wind_Profile_233_YYYYMMDD_hhmmss.hpl"


clear all
close all
clc

cd C:\Users\user\Desktop\code\WindLidar\;

%%
% make colorbar
cmap1 = makeColorMap([1 1 1],[0.92 0.92 0.92], 5);
cmap2 = makeColorMap([0.92 0.92 0.92],[0.460 0.829 1], 20);
cmap3 = makeColorMap([0.460 0.829 1],[0.316 1 0.316],20);
cmap4 = makeColorMap([0.316 1 0.316],[1 1 0],20);
cmap5 = makeColorMap([1 1 0],[1 0 0],20);
cmap= cat(1,cmap1,cmap2,cmap3,cmap4,cmap5);
cmap = [1 1 1;1 1 1;1 1 1;cmap;0 0 0];

%%
% FilN = dir(['.\Data\Processed_Wind_Profile_*.hpl']);
% FilN = dir(['\\140.115.35.65\CALab\Data\Instrument\WindLidar\2022_NCU\202208\20220819\Processed_Wind_Profile_*.hpl']);
FilN = dir(['E:\case2\Processed_Wind_Profile_*.hpl']);

Output.Time = [];
Output.High = []; 
Output.WD   = [];
Output.WS   = [];


for filname = {FilN.name}

%     M = importdata(['\\140.115.35.65\CALab\Data\Instrument\WindLidar\2022_NCU\202208\20220819\' filname{1}],' ',1);
    M = importdata(['E:\case2\' filname{1}],' ',1);
    Time = datenum(filname{1}(28:40),'yyyymmdd_HHMM')
    Height = M.data(:,1);
    WD   = M.data(:,2);
    WS   = M.data(:,3);
   
    Output.Time = [Output.Time Time];
    Output.High = [Output.High Height]; 
    Output.WD   = [Output.WD WD];
    Output.WS   = [Output.WS WS];
    
    filname
end

[Output.U,Output.V] = sd2uv(Output.WS,Output.WD);

for i = 1:size(Output.U,1)
    [MeanHour.Time ,MeanHour.U(i,:)] = STAFUNCS.meanhr(datetime(Output.Time,'ConvertFrom','datenum'),...
                                                       Output.U(i,:),1);
    [~ ,MeanHour.V(i,:)] = STAFUNCS.meanhr(datetime(Output.Time,'ConvertFrom','datenum'),...
                                                       Output.V(i,:),1);
    [~ ,StdHour.V(i,:)] = STAFUNCS.stdhr(datetime(Output.Time,'ConvertFrom','datenum'),...
                                                     Output.V(i,:),1);                                                 
    [~ ,StdHour.U(i,:)] = STAFUNCS.stdhr(datetime(Output.Time,'ConvertFrom','datenum'),...
                                                     Output.U(i,:),1);                                               
end

[MeanHour.WS,MeanHour.WD] = uv2sd(MeanHour.U,MeanHour.V);
MeanHour.Time = datenum(MeanHour.Time)

%%
MaxHigh = 2000
ff = Output.High(:,1) > MaxHigh
Output.High(ff,:) = []
for Valuename = {'WD','WS','U','V'}
    Output.(Valuename{1})(ff,:) = []
    MeanHour.(Valuename{1})(ff,:) = []
end
% 

%%
MeanHr_WS = MeanHour.WS;
MeanHr_U = MeanHour.U;
MeanHr_V = MeanHour.WS;

g_WS = [];
g_WS = gradient(MeanHr_WS')';
[max_gmWS height_gWS] = max(abs(g_WS));

g_U = [];
g_U = gradient(MeanHr_U')';
[max_gmU height_gU] = max(abs(g_U));

g_V = [];
g_V = gradient(MeanHr_V')';
[max_gmV height_gV] = max(abs(g_V));

for ii =1:49
    MeanHour.WS(height_gWS(ii):length(MeanHr_WS), ii) = nan;
    MeanHour.U(height_gU(ii):length(MeanHr_U), ii) = nan;
    MeanHour.V(height_gV(ii):length(MeanHr_V), ii) = nan;
end

%the times of std change case by case
%case1
% gap1_U = nanmean(nanmean(MeanHour.U)+(1.5).*nanstd(MeanHour.U));
% gap2_U = nanmean(nanmean(MeanHour.U)-(1.5).*nanstd(MeanHour.U));
% gap1_V = nanmean(nanmean(MeanHour.V)+(1.5).*nanstd(MeanHour.V));
% gap2_V = nanmean(nanmean(MeanHour.V)-(1.5).*nanstd(MeanHour.V));
%case2
gap1_U = nanmean(nanmean(MeanHour.U)+nanstd(MeanHour.U));
gap2_U = nanmean(nanmean(MeanHour.U)-nanstd(MeanHour.U));
gap1_V = nanmean(nanmean(MeanHour.V)+nanstd(MeanHour.V));
gap2_V = nanmean(nanmean(MeanHour.V)-nanstd(MeanHour.V));


% MeanHour.WS(abs(MeanHr_WS) > gap1_WS) = nan;
MeanHour.U(MeanHour.U > gap1_U) = nan;
MeanHour.V(MeanHour.V > gap1_V) = nan;

MeanHour.U(MeanHour.U < gap2_U) = nan;
MeanHour.V(MeanHour.V < gap2_V) = nan;

% MeanHour.U((MeanHr_U).*(MeanHr_U) == nan) = nan;
% MeanHour.V((MeanHr_U).*(MeanHr_U) == nan) = nan;

% ff = StdHour.U > 10 | StdHour.V >10
% for Valuename = {'U','V'}
%         MeanHour.(Valuename{1})(ff,:) = nan
% end

%%
xtick = MeanHour.Time;
xtick_raw = Output.Time;
ytick = Output.High(:,1); 

xtickL_raw = datestr(Output.Time,'HH:MM');
xtickL = datestr(MeanHour.Time,'HH:MM');
ytickL = num2str(ytick);

FunNom = @(X) (X-min(X)) / (max(X)-min(X))

NomXtick_raw = FunNom(xtick_raw)
NomXtick = FunNom(xtick)
NomYtick = FunNom(ytick)

[XX_raw,YY_raw] = meshgrid(NomXtick_raw,NomYtick);
[XX_hr,YY_hr] = meshgrid(NomXtick,NomYtick);

% [XX_raw,YY_raw] = meshgrid(Output.Time,Output.High(:,1));
% [XX_hr,YY_hr] = meshgrid(MeanHour.Time,Output.High(:,1));


xi = [1:2:size(XX_hr,1)];
yi = [1:size(YY_hr,2)];

XXi = XX_hr(xi,yi);
YYi = YY_hr(xi,yi);

%%
Halo_Lidar = figure
set(gcf,'position',[50,50,1600,900],'paperunits','inches','papersize',[16 9],'paperposition',[0 0 16 9])
set(gca, 'position', [0.10 0.13 0.82 0.8])

% p = pcolor(XX_raw, YY_raw, Output.WS)
% shading flat
axis([-inf inf 0 1]); caxis([0 12]);
hold on
% hq = quiver(XXi+0.01,YYi,MeanHour.U(xi,yi),MeanHour.V(xi,yi),1.5,'color',[0.7 0 0.7])
hq = quiver(XXi+0.01,YYi,MeanHour.U(xi,yi),MeanHour.V(xi,yi),1.5,'color',[1 0 0])
hq.LineWidth = 1
set(hq,'AutoScale','on', 'AutoScaleFactor', 1)


% set up xy axis
xtickL = cellstr(xtickL)
xtickL(2:2:end) = {' '}
temp_ytickL = cellstr(num2str(ytick))
ytickL = cellstr(num2str(ytick))
ytickL(1:end) = {' '}
ytickL(1:10:end) = temp_ytickL(1:10:end)
set(gca, 'xtick', NomXtick, 'XTickLabel', xtickL, 'FontSize', 16, 'FontWeight','b') 
set(gca, 'ytick', NomYtick, 'YTickLabel', ytickL, 'FontSize', 16, 'FontWeight','b')
xlabel('Local Time', 'fontsize', 20)
ylabel('Altitude (m, agl)', 'fontsize', 18)

colormap(cmap)
colorbar
h=colorbar('location','EastOutside','ytick', [0:4:12], 'yticklabel', [0:4:12], 'FontSize', 16, 'FontWeight','b','LineWidth',2);
set(get(h,'ylabel'),'String','Wind Speed (m/s)', 'fontweight', 'b', 'fontsize',18);
set(h,'tickdir', 'out');
title('2023.07.19-20 at Tainan', 'fontweight', 'b', 'fontsize',24)



saveas(Halo_Lidar, ['WindLidar_Tainan_20230719-20-test2' '.png'])

