---
paper_id: 2023_continual_pretraining_rewarm_your_model
topic_tags: [adaptive_pretraining, continual_pretraining, learning_rate_schedule, warmup, domain_adaptation]
source_url: https://arxiv.org/abs/2308.04014
---

Continual Pre-Training of Large Language Models: How to (re)warm your
model?
KshitijGupta*12 BenjaminThe´rien*12 AdamIbrahim*12 MatsL.Richter12 QuentinAnthony123
EugeneBelilovsky412 IrinaRish12 Timothe´eLesort12
Abstract 1.Introduction
Largepre-trainedmodelshaveenabledmassiveperformance
Largelanguagemodels(LLMs)areroutinelypre- improvementsformanydownstreamtasksinvision(Kir-
trainedonbillionsoftokens, onlytorestartthe illovetal.,2023;Oquabetal.,2023)andlanguage(Brown
processoveragainoncenewdatabecomesavail- etal.,2020;Zhaoetal.,2023).However,trainingthesefoun-
able. Amuchcheaperandmoreefficientsolution dationmodelsisprohibitivelyexpensive. Existingworks
wouldbetoenablethecontinualpre-trainingof aim to reduce the cost of large-scale model development
these models, i.e. updating pre-trained models byenablinglow-costhyperparameteroptimization(Yang
with new data instead of re-training them from et al., 2022) or providing guidelines for maximizing per-
scratch. However,thedistributionshiftinduced formanceunderagivencomputebudget(Hoffmannetal.,
by novel data typically results in degraded per- 2022). However,theseworksassumethatmodelswillbe
formance on past data. Taking a step towards trainedfromscratch.Astheamountofdataavailableforpre-
efficientcontinualpre-training,inthiswork,we trainingisever-growing, newandimproveddatasets(e.g.
examine the effect of different warm-up strate- RedPajamaandSlimPajama(Together.xyz,2023;Soboleva
gies. Ourhypothesisisthatthelearningratemust etal.,2023;Touvronetal.,2023))willcontinuetobecome
be re-increased to improve compute efficiency available. Should practitioners always combine existing
when training on a new dataset. We study the datasets(e.g. Pile(Gaoetal.,2020))andtrainfromscratch
warmupphaseofmodelspre-trainedonthePile toobtainthebestperformance? Doingsowouldquicklybe-
(upstreamdata,300Btokens)aswecontinueto comeprohibitivelyexpensiveandfailstoleverageexisting
pre-trainonSlimPajama(downstreamdata,297B pre-trainedmodels.
tokens), following a linear warmup and cosine
Ourapproachcircumventstheneedforcompletere-training
decayschedule. Weconductallexperimentson
by continuing to pre-train existing models on new data.
thePythia410Mlanguagemodelarchitectureand
Werefertothisas“continualpre-training”andthegoalis
evaluateperformancethroughvalidationperplex-
to minimize the loss on new data while maintaining low
ity. We experiment with different pre-training
loss on previous data. Continual pre-training is a critical
checkpoints,variousmaximumlearningrates,and
challengesinceitcanleadtocatastrophicforgetting(French,
various warmup lengths. Our results show that
1999). Moreover, the potential long sequence of training
whilerewarmingmodelsfirstincreasestheloss
stages may make common continual learning techniques
onupstreamanddownstreamdata,inthelonger
suchasreplay(Rebuffietal.,2017;Ostapenkoetal.,2022)
runitimprovesthedownstreamperformance,out-
orregularisation(Kirkpatricketal.,2017;Farajtabaretal.,
performing models trained from scratch—even
2020)notcomputeefficientenough(Lesortetal.,2023). A
foralargedownstreamdataset.
simple and – from a compute cost perspective – scalable
solution to limit forgetting in such situations is to (only)
progressivelydecreasethelearningrateeverytimenewdata
*Equalcontribution;authorshiporderdeterminedbyacoinflip
1DepartmentofComputerScienceandOperationResearch,Uni- becomes available (Mirzadeh et al., 2020; Winata et al.,
versite´deMontre´al,Montre´al,Canada2Mila,Montre´al,Canada 2023). However,thissolutionislimitedbecauserepeatedly
3EleutherAI4DepartmentofComputerScienceandSoftwareEngi- decreasing the learning rate would cause it to eventually
neering,ConcordiaUniversity,Montre´al,Canada.Correspondence becometoosmallifthenumberoftrainingstagesbecomes
to:BenjaminThe´rien<benjamin.therien@umontreal.ca>.
high.
WorkpresentedattheES-FoMoWorkshopatthe40th Interna- Inthiswork,wetakeasteptowardsefficientcontinualpre-
tionalConferenceonMachineLearning,Honolulu,Hawaii,USA.
training by studying how to re-increase a small learning
PMLR202,2023.Copyright2023bytheauthor(s).
peS
]LC.sc[
2v41040.8032:viXra

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
ratetokeeptrainingapre-trainedlanguagemodelonnew
Table1.Tokencountsandtraindataweightsforoursubsampled
data.Werefertothisasre-warmingthemodel.Re-warming
versionofSlimPajama.
themodelshouldimprovelearningefficiencybyavoiding
Dataset Sampling% Train Val
avanishinglearningrate. Westudywarm-upstrategieson
Pythia410Mmodelwithvariousamountsofdata,maximum StackExchange 2.0 9.95B 13.08M
learningratesanddifferentpre-trainedcheckpoints. This Arxiv 2.5 13.77B 22.73M
wouldallowamodeltrainedinitiallyonalargedatasetto Wikipedia 4.5 11.78B 15.79M
benefit from resuming training on a newer large dataset Book 4.5 14.22B 22.04M
withouthavingtoretrainfromscratch. Inordertosimulate Github 4.5 15.41B 22.42M
thissetting,wefixourinitialpre-trainingdatasettobePile C4 15.0 78.49B 72.49M
andthenewerdatasettobeSlimPajama. Wehopethatthis Commoncrawl 67.0 153.25B 147.28M
mayguidetheadaptationofexistingLLMstofuturenew
Totals 100 296.86B 315.83M
datasets.
Ourresultsshowthat:
theSlimPajamadataset(Sobolevaetal.,2023)toformthe
## 1. Progressivelyincreasingthelearningratetowarm-up
∼297Btokentrainingdatasetand∼316Mvalidationtoken
is not necessary but starting directly from the maxi-
dataset. Wedonotusereplay. Weusethesametokenizeras
mumlearningratecreatesaninitiallargespikeinthe
(Blacketal.,2022)thatistrainedspecificallyonthePile.
loss(chaoticphasea.k.astabilitygap)withnoconse-
quenceslater. Model–Weusethe410MPythiapre-trainedonthePile
## 2. Adjustingthemaximumlearningratecanhelptrade- (Bidermanetal.,2023),i.e. GPT-NeoX(Blacketal.,2022)
offbetweenupstreamanddownstreamperformance; models. Wedonotuseflashattention(Daoetal.,2022).
increasingthemaximumlearningrateleadstostronger
Hyperparameters– WeusetheAdamWoptimizerwith
adaptation to the downstream dataset (SlimPajama), β =0.9,β =0.95,ϵ=10−8,andaweightdecayof0.1.
1 2
while smaller learning rates preserve more perfor-
The maximum learning rate is varied in our experiments
manceontheupstreamdataset(Pile). {1.5·10−4,3·10−4,6·10−4}. Weusecosinelearningrate
## 3. Continualpre-trainingwiththelatestpre-trainedcheck-
decaytoaminimumof0.1·MaxLr. Allwarmuplengths
pointimprovesperformance.
are calculated based on the full downstream dataset size
(297B tokens). We note that our cosine decay schedule
2.Setup reachestheminimumlearningrateat240Btokensandis
constantthereafter.Wesetgradientclippingto1.0.Training
Inoursetup,theupstream(orpre-training)datasetisthePile
isconductedathalf-precision(FP16),withoutdropout.
(Gaoetal.,2020). Thedownstream(orfine-tuning)dataset
isSlimPajama(Sobolevaetal.,2023). SlimPajamaisanex-
3.RelatedWork
tensivelydeduplicatedversionofRedPajama(Together.xyz,
2023)whichisbuiltbasedontheLLamadataset(Touvron
LargeLanguageModels: LLMsareusuallytrainedwith
etal.,2023). Inthiswork,weuse“fine-tuning”anddown-
Adam (e.g., GPT3 (Brown et al., 2020), BLOOM (Scao
streamcontinualpre-traininginterchangeably. However,in
etal.,2022),Gopher(Raeetal.,2021),Pythia(Biderman
ourcontinualpre-trainingsetting, wenotethatthedown-
etal.,2023))orAdamW(e.g.,Chinchilla(Hoffmannetal.,
streamdatasetisonthescaleofthepreviouspre-training
2022), LLaMA (Touvron et al., 2023)). In all the afore-
dataset(i.e. verylarge,unlikemanyfine-tuningdatasets).
mentionedmodels,thelearningratescheduleconsistsofa
TheSlimPajamadatasetisbuiltfromsimilarsourcesasthe warm-upfollowedbyacosinedecayto10%ofthemaxi-
Pile but with a higher quantity of data. Therefore, some mumlearningrate.
upstream data may be repeated during downstream pre-
UnsupervisedContinualLearning: Inthispaper,wein-
training. Ourexperimentalsetupiscomparabletothesetup
vestigatevariouswarm-upstrategiesforthecontinualpre-
of(Ash&Adams,2020),wheretheytrainaclassifieron
training of LLMs. Continual pre-training uses a similar
halfofthesamplesofadatasetfirst,andfine-tuneitlater
typeoftrainingobjectivesascontinualself-supervisedtrain-
on all samples. They show that warm starting for image
ing. Self-supervisedpre-trainingwasalsostudiedinvision
classificationischallenging. Usingamodelpre-trainedon
datasetsforimagegeneration(Seffetal.,2017;Lesortetal.,
thePileandcontinuingthepre-trainingonSlimPajama,we
2019;Zhaietal.,2019;Nguyenetal.,2018;Davarietal.,
followananalogoussetupforcausallanguagemodeling.
2022)orrepresentationlearning(Finietal.,2022;Madaan
Datasets–WeusethePilewiththesameweightsasBlack etal.,2021;Raoetal.,2019). Inlanguage,continualpre-
etal.(2022)forvalidation.Weshuffleandrandomlysample trainingwasstudiedunderthenameofdomainadaptation

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
pre-training(Keetal.,2023a;Scialometal.,2022;Guru- 2.875
ranganetal.,2021;Qinetal.,2022)wherethenewdataset 2.850
comesfromanewdomain. Anothersettingiswherediffer-
2.825
entdatasetsaregeneratedatdifferentpointsintime(Han
2.800
etal.,2021;Jinetal.,2022;Jangetal.,2021;2022;Loureiro
2.775
etal.,2022). Inoursetup,thescenarioisclosertodomain
2.750
adaptationpre-training,becausewedonottakeintoaccount
2.725
thetemporalityofdata.
2.700
Monitoring Learning Rate for Continual Training of
2.675
LanguageModels: Incontinuallearning(CL),modelsare
0 10 20 30 40 50
trained on sequences of datasets. Therefore, the data is Tokens (B)
notindependentandidenticallydistributedwhichcanlead
the model to lose plasticity or forget. In such situations,
particularmonitoringofthelearningrateschedulecanbe
beneficial. InCLoflanguagemodels(Cacciaetal.,2021;
Ke et al., 2023a; Loureiro et al., 2022; Han et al., 2021;
Loshchilov&Hutter,2018;Scialometal.,2022;Winata
etal.,2023)differentapproacheshavebeenevaluated: con-
stantlearningrate(Keetal.,2023a;Scialometal.,2022),
progressivedecrease(Winataetal.,2023)orwarm-upthen
decrease(Cacciaetal.,2021).
However, tothebestofourknowledge, noexistingwork
studiesspecificallytheinfluenceofthewarm-upphaseinthe
contextofcontinualpre-trainingforlargelanguagemodels.
4.ContinualWarm-up
4.1.Howlongtowarmup?
Intheliterature,warm-upisusuallyconductedonatmost
1%ofthedata(Zhaoetal.,2023). Inthisexperiment,we
investigateiftheresultsaresensitivetothishyper-parameter.
Setup: Weexperimentwithdifferentwarm-uplengthsfor
ascheduleof297Btokens: 0%,0.5%,1%,and2%ofthe
dataandmeasuretheperformanceafterthefirst50Btokens.
Fromadifferentperspective,wecouldseethisexperiment
asrunninga1%warm-upondifferentamountsofdata. We
hypothesizethatwarmingupforalargernumberofitera-
tionscouldleadtoasmoothertransitionwithsubsequent
performanceimprovements.
Results: The results of this experiment are provided in
Fig.1. Theyshowthattheamountofdatausedforwarming
upthelearningratedoesnotsignificantlyinfluencetheper-
plexityonthedownstreamtask(learning)ortheupstream
task (forgetting). These results invalidate our hypothesis
thatusingmoretokensforwarm-upcansmooththetransi-
tionandshowthatlinearwarmupisuselessinthissetting.
Nevertheless, the model trained without any progressive
warmupexperiencesaninitial“choaticphase”causinga
spikeinthelossinitsfirstfewiterationsoftraining, this
phenomenonisalsoreferredtoasstabilitygap(Langeetal.,
2023;Cacciaetal.,2022).
)maertsnwod(
ssoL
.laV
amajaPmilS
WU 0.0
WU 0.005
WU 0.01
WU 0.02
2.6
2.5
2.4
2.3
2.2
0 10 20 30 40 50
Tokens (B)
)maertspu(
ssoL
.laV
eliP
WU 0.0
WU 0.005
WU 0.01
WU 0.02
Figure1.(top)EvolutionofperplexityonSlimPajamawhilefine-
tuning with various amounts of tokens for warm-up. (bottom)
perplexity on the same experiments on the Pile validation set
(upstream). MaxLr = 3·10−4, MinLr = 0.1·MaxLr. This
figureshowsthatatthatscale,thelengthofthewarm-upphase
doesnotsignificantlyinfluenceresults.
Takeaway1:
• Thelengthofthewarmupphasedoesnotap-
peartohaveasignificanteffectonthePileand
SlimPajamavalidationlosses.
4.2.Howhightowarmup?
Oneobjectiveofre-warmingthelearningrateistoenable
compute-efficient continual pre-training. A learning rate
that is too small may lead to inefficient learning on the
downstream dataset, whereas, a learning rate that is too
large may lead to catastrophic forgetting of the upstream
dataset. Oneimportantaspectofre-warmingthelearning
rateistodecidehowhightoincreaseit. Therefore,inthis
experiment,wevarythemaximumlearningratetoassess
itseffectonperformance.
Setup:Wefixthelengthofthewarm-upphasetothedefault
amountof1%ofthetrainingdataandvarythemaximum
learning rate. We experiment with the default value of
3·10−4usedforpre-trainingPythia410M(Bidermanetal.,
2023),1.5·10−4,and6·10−4. Forthepost-warmupcosine
decay phase, we set the final learning rate to 10% of the

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
maximumlearningrate. Thelearningratescheduleweused
decays to the minimum learning rate at 240B tokens and
isconstantthereafter. Therunsarereportedtotheendof
240Btokens(theendofdecayperiod).
2.9
2.8
2.7
2.6
2.5
0 50 100 150 200 250
Tokens (B)
)maertsnwod(
ssoL
.laV
amajaPmilS
Constant 3e-05Iter. 143000 MaxLR 1.5e-04 Iter. 143000
MaxLR 3e-04 Iter. 0
MaxLR 3e-04 Iter. 143000
MaxLR 6e-04 Iter. 143000
Figure2.EvolutionoflossonSlimPajamafordifferentmaximum
learningrates.Thebluecurvereportsamodeltrainedfromscratch.
Growingthemaximumlearningrateconsistentlydecreasesthe
finallossondownstreamdata.Atconvergence,themodelsbeing
continuallypre-trainedoutperformthescratchandconstantLR
baselines.However,theconstantlearningratemodelachievesbest
performancewithinthefirst100Btokens.
2.9
2.8
2.7
2.6
2.5
2.4
2.3
0 50 100 150 200 250
Tokens (B)
)maertspu(
ssoL
.laV
eliP
13 14 15 16 17 18
SlimPajama Val PPL (downstream)
Constant 3e-05Iter. 143000
MaxLR 1.5e-04 Iter. 143000
MaxLR 3e-04 Iter. 0
MaxLR 3e-04 Iter. 143000
MaxLR 6e-04 Iter. 143000
Figure3.EvolutionoflossonPilefordifferentmaximumlearning
rates.Thebluecurvereportsamodeltrainedfromscratch.Grow-
ingthemaximumlearningrateconsistentlyincreasesthefinalloss
onupstreamdata,i.e. itincreasesforgetting. Thefrom-scratch
baselineconsistentlyimprovesitsperformanceonPile,whilebeing
trainedonSlimPajama,showingthesignificantsynergybetween
bothdatasets.
Results: Theresultsofthisexperimentareprovidedinfig-
ures 2, 3, and 4. We observe, at the end of training, that
larger maximum learning rates improve performance on
downstreamdata,whiletheyhurtperformanceonupstream
data. Conversely, a smaller maximum learning rate im-
provesperformanceonupstreamdata,whilelimitingadap-
tationtodownstreamdata—causingdecreasedperformance.
Thesefindingsshowthatalteringthemaximumlearningrate
can be an effective way to tradeoff between downstream
andupstreamperformance. Additionally,weobserveagen-
)maertspu(
LPP
laV
eliP
Constant 3e-05 50 MaxLR 1.5e-04
MaxLR 3e-04
MaxLR 6e-04
)B(
snekoT
Figure4.Perplexitydownstreamvsperplexityupstream,RPfine-
tuning.Greenpointsrefertotheendsofthewarm-upphases.The
redpointrepresentstheperplexitybeforestartingthedownstream
fine-tuning.Increasingthemaximumlearningrateimprovesper-
formanceonthedownstreamdata,butcausesforgettingonthe
upstream.Thisplotreportsthesameresultsasfigures2and3.
eral trend: fine-tuning on SlimPajama, causes the model
to forget what has been learned on the Pile leading to an
increaseinthePilevalidationperplexity. Finally,wenote
thatemployingearlystoppingonthemodeltrainedfroma
constantlearningrate(similartotraditionalfine-tuning)is
aneconomicalwayofadaptingtothenewdatadistribution
whileretainingstrongperformanceontheupstreamdataset.
Takeaway2:
• Rewarming then decaying the learning rate
appearsnecessarytolearnwellonthedown-
streamtask. Moreover,whilekeepingacon-
stantlearningisinitiallyadvantageousonPile,
this advantage vanishes when training long
enoughonSlimPajama.
• AmodelthatonlylearnsonSlimPajamaper-
formsworseonSlimPajamathanmodelspre-
trained on Pile in spite of being optimised
solelyforthedownstreamtask,highlighting
positivetransferbetweenthetwodatasets.
4.3.ComparingwithfromScratchTraining
Inthisexperiment,wewanttocomparefinetunedmodels
withmodelstrainedfromscratch.
Setup: Wetrainamodelfromrandominitializationusing
thesamecosinedecayscheduleastheMaxLr = 3·10−4
modelinSection4.2.
Results: As we can see in Fig. 2 and Fig. 3, all the fine-
tunedmodelswithawarm-upperformbetterthanthemodel

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
trainedfromscratch. Thisshowsthatfinetuninginsteadof
retrainingmightimproveperformanceevenwhenthedown-
streamdatasetisonthescaleoftheupstreamdatasetand
overlapswiththeupstreamdataset. Wealsoobservethat,
after200Btokens,themodeltrainedfromscratchperforms
betterthan themodel finetunedusinga constantlearning
rate.
4.4.Re-warmingonthesamedata
Inthepreviousexperimentswehaveseenthatfinetuningon
newdataleadstoaquickincreaseoflossonpastdata,that
decreaselater.Theincreaseishigherwhenthemaxlearning
rateisbigger. Onehypothesisfortheincreaseinlossisthat
thedistributionshiftbetweenupstreamanddownstreamdata
disturbsthetrainingprocess. Toassessthishypothesis,we
applyourwarm-uppolicyinasettingwithnodistribution
shift. Thatis,wereplicateourexperimentsfromfigures3
and4byfine-tuningonPile.
2.40
2.35
2.30
2.25
2.20
0 10 20 30 40 50
Tokens (B)
ssoL
.laV
eliP
)maertspu
& maertsnwod(
11.0
10.5
10.0
9.5
9.0
15.5 16.0 16.5 17.0 17.5 18.0 18.5 19.0 19.5
SlimPajama Val PPL (downstream)
Constant 3e-05
MaxLR 1.5e-04
MaxLR 3e-04
MaxLR 6e-04
Figure5.Pilevalidationlosswhilefine-tuningagainonthePile.
Warm-upphenomenonobservedinSec.4.2isalsoobservedap-
pliedtofine-tuningagainonthesamedatadistribution.Warm-up
token=1%downstreamtokens,MinLr=0.1·MaxLr.
Setup: Inthisexperiment,insteadoffine-tuningonSlimPa-
jamadata,wefine-tuneon50BtokensofthePiledatawith
thesameparametrizationofthewarm-uppolicyasSec.4.2
experiments.
Results: Fig.5,showsthatre-warmingthelearningrate
whilecontinuingtopre-trainonthePilehasasimilareffect
as re-warming on SlimPajama data Fig. 3 when looking
at the downstream validation loss. This suggests that the
distributionshiftbetweenPileandSlimPajamaisnotsolely
toblameforthenegativeimpactofre-warmingthelearning
rateobservedinsec.4.2,andthattheoptimizationdynamics
alsoplaysaroleinthisincreaseofloss.
Fig.6showsthatthetrainingfirstincreasesperplexityon
both the Pile and SlimPajama data but reduces after on
both.Interestingly,Fig.6showalinearrelationshipbetween
SlimPajama perplexity andthe Pile perplexitywhen fine-
tuning on the Pile, while it was not the case while fine-
)maertspu(
LPP
laV
eliP
Constant 3e-05
MaxLR 1.5e-04
MaxLR 3e-04 40
MaxLR 6e-04
)B(
snekoT
Figure6.PerplexityonthePilevsperplexityonSlimPajamawhen
fine-tuning on the Pile with various maximum learning rates.
Warm-uptoken=1%downstreamtokens,MinLr = 0.1·MaxLr.
Greenpointsrefertotheendofthewarm-upphase.
tuningonSlimPajama(Fig.3). Onepossibleexplanation
forthisrelationshipisthatmodelstrainedonPileclimbout
ofaminimumduringwarmupandreturntowardsthesame
minimumasthelearningrateisdecayed,yieldingthelinear
trend.
Takeaway3:
• Rewarmingthelearningrateappearstobea
significantcauseforthedegradationofperfor-
manceseenpreviouslywhenstartingtolearn
onthedownstreamtask,asevidencedbyre-
warmingthendecayingthelearningratewhile
trainingonthesamedataset.
• Themodelsdonotappeartobeabletorecover
from the performance hit due to rewarming
the learning rate when training on the same
dataset.
4.5.EvaluatingEarlierCheckpoints
Setup:Weselectthreecheckpointsfrommodelpre-training
totestifwarm-upstrategiesbenefitfromstartingwithnon-
converged checkpoints. Our hypothesis is that selecting
checkpointsfartherfromconvergencemaybenefitadapta-
tion to the downstream task as these checkpoints may be
locatedatmorefavorablepointsinthelosslandscape.
Toselectsignificantlydifferentcheckpoints,wecomparethe
lastpre-trainingcheckpoint(i.e.Pythia410Mafter143,000
iters),toanearliercheckpointachievingaPilevalidation
lossnearthemaximumPilevalidationlossattainedbyall
modelsinFig.1(bottom)(∼2.5),andathirdcheckpointin
betweenthetwoothercheckpoints.

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
3.1
3.0
2.9
2.8
2.7
0 10 20 30 40 50
Tokens (B)
)maertsnwod(
ssoL
.laV
amajaPmilS
adaptationpre-trainingsetups(Xuetal.,2019;Gururangan
WU 0.0 Iter. 27000
WU 0.0 Iter. 143000 etal.,2020;Keetal.,2023a;Chakrabartyetal.,2019;Ke
WU 0.0 Iter. 10000
etal.,2023b). Nevertheless,comparingFig.4andFig.6,
WU 0.01 Iter. 10000
WU 0.01 Iter. 143000 we see that the results are not identical when fine-tuning
WU 0.01 Iter. 27000
onthePileorwhenfine-tuningonSlimPajama. Apossible
explanationisthatevenaslightshiftindatadistributioncan
leadtoasignificantperturbationofthelearningdynamics.
Forexample,inthecontextofimageclassification,Igletal.
(2020)showhowasuddentransitionof10to20%ofthe
labels in the dataset can have a significant impact on the
downstreamperformance(seeFig. 5of(Igletal.,2020)).
ExperimentsScale:
Figure7.Pilevalidationlossofmodelstrainedfromthefullycon-
AsdescribedinSec.2,ourinvestigationexploresmodels
vergedcheckpoint,theupstreamsaturationpoint,and1/2ofthe
upstream saturation point. Blackcolour designs for the earlier ofsize410Mandfine-tuningdatasetofsize297Btokens.
checkpoint,redcolourthelatestcheckpointandbluecolourthe Whilethisisapreliminarystudy,infuturework,weplan
in-betweenone. toverifywhetherourconclusionsholdatdifferentmodel
scales(e.g.,3Band7B)anddifferentdatasetscales(e.g.,
100B and 600B). Moreover, we plan to test our models
Results: TheevolutionofthevalidationlossesonSlimPa-
throughoutusingbenchmarkssuchasHELM(Liangetal.,
jama are provided in Fig. 7 and the evolution of the vali-
2022) or Harness (Gao et al., 2021) instead of only loss
dation losses on the Pile is provided in appendix A. We
orperplexity,asthesebenchmarkscanprovideimportant
see in Fig. 7 that, in our setup, selecting earlier check-
insightintotheevolutionofmodelcapabilities.
points for later fine-tuning does not lead to improvement
indownstreamperformance. Therefore,selectingthelatest
6.Conclusion
checkpoint is the best option. We can conclude that the
pre-trainingdidnotleadthemodelintoalossofplasticity
Our experiments demonstrate that warming up to higher
thatwouldmakethemodeldifficulttore-warm.
maximum learning rates helps models pre-trained on the
Localconclusion: Theexperimentsconductedinthissec- PileadapttoSlimPajama,whileasmallermaximumlearn-
tionledtotheconclusionthatre-warmingthepre-trained ingraterpreservesperformanceonthepile. Inbothcases,
model on new data is a challenging task, even when the however,modelsthatarerewarmedimproveovermodels
downstreamdataisofsimilarprovenancetotheupstream trainedfromscratch. Theseresultsmotivatetheuseofcon-
data. Ourresultsshowthattheamountoftokensusedfor tinual pre-training on new datasets rather than restarting
warm-up does not significantly alter performance, grow- trainingfromscratch. Moreresearchisneeded, however,
ingthemaximumlearningrateimprovesdownstreamper- to establish similar results for larger model scales, differ-
formanceofthefinalmodelwhiledecreasingitimproves entdistributionshifts,andverifythatthisstrategycanbe
upstream performance, and selecting earlier checkpoints appliedrepeatedlytoupdatemodels.
decreasesperformanceonbothupstreamanddownstream
data.
SoftwareandData
Takeaway4:
GPT-NeoX (Andonian et al., 2021), DeepSpeed (Rasley
• Usinganearliercheckpointwhenpretraining
etal.,2020),nccl(NVIDIA,2016),Apex(NVIDIA,2019),
onthePiledoesnotleadtolearningfasteron
Pytorch(Paszkeetal.,2017),HuggingFaceTransformers
SlimPajama.
library(Wolfetal.,2020).
5.Discussion/Limitation Acknowledgements
Data similarity and overlapping: In our experimental WeacknowledgethesupportfromCanadaCIFARAIChair
setup,upstreamanddownstreamdatahaveahighsimilarity, ProgramandfromtheCanadaExcellenceResearchChairs
notablybecauseofdataoverlap. Sinceincontinuallearning, Program. Wewouldalsoliketoacknowledgefundingfrom
differenttypesofshiftscanleadtovariationsinperformance theFRQNTDoctoral(B2X)scholarship[B.T.],thescholar-
(Lesortetal.,2021),ourresultsmaynotgeneralizetosetups shipforArtificialIntelligenceofUniversite´ deMontre´al’s
withdifferentdistributionshifts,suchaslanguagedomain

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
E´tudesSupe´rieuresetPostdoctorales,andafellowshipof Chakrabarty,T.,Hidey,C.,andMcKeown,K. IMHOfine-
theIFIprogramoftheGermanAcademicExchangeService tuningimprovesclaimdetection. InProceedingsofthe
(DAAD).Thisresearchwasmadepossiblethankstothecom- 2019ConferenceoftheNorthAmericanChapterofthe
putingresourcesontheSummitsupercomputer,providedas AssociationforComputationalLinguistics: HumanLan-
apartoftheINCITEprogramaward“ScalableFoundation guageTechnologies,Volume1(LongandShortPapers),
ModelsforTransferableGeneralistAI”. Theseresources pp.558–563,Minneapolis,Minnesota,June2019.Asso-
were provided by the Oak Ridge Leadership Computing ciation for Computational Linguistics. doi: 10.18653/
Facility at the Oak Ridge National Laboratory, which is v1/N19-1054.URLhttps://aclanthology.org/
supportedbytheOfficeofScienceoftheU.S.Department N19-1054.
ofEnergyunderContractNo. DE-AC05-00OR22725.
Dao,T.,Fu,D.,Ermon,S.,Rudra,A.,andRe´,C. Flashat-
tention: Fastandmemory-efficientexactattentionwith
## References
io-awareness. AdvancesinNeuralInformationProcess-
ingSystems,35:16344–16359,2022.
Andonian, A., Anthony, Q., Biderman, S., Black, S.,
Gali,P.,Gao,L.,Hallahan,E.,Levy-Kramer,J.,Leahy, Davari, M., Asadi, N., Mudur, S., Aljundi, R., and
C., Nestler, L., Parker, K., Pieler, M., Purohit, S., Belilovsky,E. Probingrepresentationforgettinginsuper-
Songz, T., Phil, W., and Weinbach, S. GPT-NeoX: visedandunsupervisedcontinuallearning. InProceed-
LargeScaleAutoregressiveLanguageModelinginPy- ingsoftheIEEE/CVFConferenceonComputerVision
Torch, 8 2021. URL https://www.github.com/ andPatternRecognition,pp.16712–16721,2022.
eleutherai/gpt-neox.
Farajtabar, M., Azizan, N., Mott, A., and Li, A. Or-
Ash,J.andAdams,R.P. Onwarm-startingneuralnetwork thogonal gradient descent for continual learning. In
training. Advancesinneuralinformationprocessingsys- InternationalConferenceonArtificialIntelligenceand
tems,33:3884–3894,2020. Statistics,pp.3762–3773.PMLR,2020. URLhttps:
//arxiv.org/abs/1910.07104.
Biderman, S., Schoelkopf, H., Anthony, Q., Bradley, H.,
Fini, E., da Costa, V. G. T., Alameda-Pineda, X., Ricci,
O’Brien, K., Hallahan, E., Khan, M. A., Purohit, S.,
E., Alahari, K., and Mairal, J. Self-supervised models
Prashanth,U.S.,Raff,E.,etal. Pythia: Asuiteforana-
arecontinuallearners. InProceedingsoftheIEEE/CVF
lyzinglargelanguagemodelsacrosstrainingandscaling.
ConferenceonComputerVisionandPatternRecognition,
arXivpreprintarXiv:2304.01373,2023.
pp.9621–9630,2022.
Black, S., Biderman, S., Hallahan, E., Anthony, Q., Gao, French, R. M. Catastrophic forgetting in con-
L.,Golding,L.,He,H.,Leahy,C.,McDonell,K.,Phang, nectionist networks. Trends in Cognitive Sci-
J.,Pieler,M.,Prashanth,U.S.,Purohit,S.,Reynolds,L., ences, 3(4):128–135, 1999. ISSN 13646613.
Tow,J.,Wang,B.,andWeinbach,S. Gpt-neox-20b: An doi: 10.1016/S1364-6613(99)01294-2. URL
open-sourceautoregressivelanguagemodel,2022. https://www.sciencedirect.com/science/
article/abs/pii/S1364661399012942.
Brown,T.B.,Mann,B.,Ryder,N.,Subbiah,M.,Kaplan,
Gao,L.,Biderman,S.,Black,S.,Golding,L.,Hoppe,T.,
J., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry,
Foster,C.,Phang,J.,He,H.,Thite,A.,Nabeshima,N.,
G., Askell, A., et al. Language models are few-shot
learners. InProceedingsofthe34thInternationalCon- et al. The pile: An 800gb dataset of diverse text for
ferenceonNeuralInformationProcessingSystems,pp. language modeling. arXiv preprint arXiv:2101.00027,
1877–1901,2020. URLhttps://arxiv.org/abs/ 2020.
2005.14165.
Gao, L., Tow, J., Biderman, S., Black, S., DiPofi, A.,
Foster, C., Golding, L., Hsu, J., McDonell, K., Muen-
Caccia, L., Xu, J., Ott, M., Ranzato, M., and Denoyer,
nighoff,N.,Phang,J.,Reynolds,L.,Tang,E.,Thite,A.,
L. On anytime learning at macroscale. arXiv preprint
Wang,B.,Wang,K.,andZou,A. Aframeworkforfew-
arXiv:2106.09563,2021.
shotlanguagemodelevaluation,September2021. URL
https://doi.org/10.5281/zenodo.5371628.
Caccia,L.,Aljundi,R.,Asadi,N.,Tuytelaars,T.,Pineau,
J., and Belilovsky, E. New insights on reducing Gururangan, S., Marasovic´, A., Swayamdipta, S., Lo, K.,
abrupt representation change in online continual learn- Beltagy, I., Downey, D., and Smith, N. A. Don’t stop
ing. In International Conference on Learning Repre- pretraining:Adaptlanguagemodelstodomainsandtasks.
sentations,2022.URLhttps://openreview.net/ arXivpreprintarXiv:2004.10964,2020. URLhttps:
forum?id=N8MaByOzUfb. //arxiv.org/abs/2004.10964.

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
Gururangan, S., Lewis, M., Holtzman, A., Smith, N. A., Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C.,
and Zettlemoyer, L. Demix layers: Disentangling Gustafson,L.,Xiao,T.,Whitehead,S.,Berg,A.C.,Lo,
domains for modular language modeling. arXiv W.-Y., Dolla´r, P., and Girshick, R. Segment anything.
preprint arXiv:2108.05036, 2021. URL https:// arXiv:2304.02643,2023.
arxiv.org/abs/2108.05036.
Kirkpatrick, J., Pascanu, R., Rabinowitz, N., Ve-
Han,R.,Ren,X.,andPeng,N. ECONET:Effectivecon- ness, J., Desjardins, G., Rusu, A. A., Milan, K.,
tinual pretraining of language models for event tempo- Quan, J., Ramalho, T., Grabska-Barwinska, A., et al.
ral reasoning. In Proceedings of the 2021 Conference Overcoming catastrophic forgetting in neural net-
on Empirical Methods in Natural Language Process- works. Proc. of the national academy of sciences,
ing, pp. 5367–5380, Online and Punta Cana, Domini- 2017. URL https://www.pnas.org/content/
can Republic, November 2021. Association for Com- pnas/114/13/3521.full.pdf.
putational Linguistics. doi: 10.18653/v1/2021.emnlp-
main.436. URL https://aclanthology.org/ Lange,M.D.,vandeVen,G.M.,andTuytelaars,T. Con-
2021.emnlp-main.436. tinual evaluation for lifelong learning: Identifying the
stability gap. In The Eleventh International Confer-
Hoffmann,J.,Borgeaud,S.,Mensch,A.,Buchatskaya,E., enceonLearningRepresentations,2023. URLhttps:
Cai,T.,Rutherford,E.,Casas,D.d.L.,Hendricks,L.A., //openreview.net/forum?id=Zy350cRstc6.
Welbl,J.,Clark,A.,etal.Trainingcompute-optimallarge
languagemodels.arXivpreprintarXiv:2203.15556,2022. Lesort,T.,Caselles-Dupre´,H.,Garcia-Ortiz,M.,Goudou,
URLhttps://arxiv.org/abs/2203.15556. J.-F., and Filliat, D. Generative models from the per-
spective of continual learning. In IJCNN - Interna-
Igl, M., Farquhar, G., Luketina, J., Boehmer, W., and tionalJointConferenceonNeuralNetworks,Budapest,
Whiteson, S. The impact of non-stationarity on gen- Hungary,Jul2019. URLhttps://hal.archives-
eralisation in deep reinforcement learning. arXiv ouvertes.fr/hal-01951954.
preprint arXiv:2006.05826, 2020. URL https://
arxiv.org/abs/2006.05826.pdf. Lesort,T.,Caccia,M.,andRish,I. Understandingcontin-
uallearningsettingswithdatadistributiondriftanalysis.
Jang, J., Ye, S., Yang, S., Shin, J., Han, J., Kim, arXivpreprintarXiv:2104.01678,2021.
G., Choi, S. J., and Seo, M. Towards contin-
ual knowledge learning of language models. arXiv Lesort, T., Ostapenko, O., Rodriguez, P., Arefin, M. R.,
preprint arXiv:2110.03215, 2021. URL https:// Misra,D.,Charlin,L.,andRish,I. Challengingcommon
arxiv.org/abs/2110.03215. assumptionsaboutcatastrophicforgetting. 2023.
Jang,J.,Ye,S.,Lee,C.,Yang,S.,Shin,J.,Han,J.,Kim,G., Liang,P.,Bommasani,R.,Lee,T.,Tsipras,D.,Soylu,D.,
and Seo, M. Temporalwiki: A lifelong benchmark for Yasunaga,M.,Zhang,Y.,Narayanan,D.,Wu,Y.,Kumar,
trainingandevaluatingever-evolvinglanguagemodels. A.,etal. Holisticevaluationoflanguagemodels. arXiv
## 2022. preprintarXiv:2211.09110,2022.
Jin, X., Zhang, D., Zhu, H., Xiao, W., Li, S.-W., Wei, Loshchilov,I.andHutter,F. Decoupledweightdecayreg-
X., Arnold, A., and Ren, X. Lifelong pretraining: ularization. In International Conference on Learning
Continuallyadaptinglanguagemodelstoemergingcor- Representations,2018. URLhttps://arxiv.org/
pora. In Proceedings of BigScience Episode #5 – abs/1711.05101.
Workshop on Challenges & Perspectives in Creating
Loureiro,D.,Barbieri,F.,Neves,L.,EspinosaAnke,L.,and
Large Language Models, pp. 1–16, May 2022. doi:
Camacho-collados,J. TimeLMs: Diachroniclanguage
10.18653/v1/2022.bigscience-1.1. URL https://
modelsfromTwitter. InProceedingsofthe60thAnnual
aclanthology.org/2022.bigscience-1.1.
MeetingoftheAssociationforComputationalLinguistics:
Ke, Z., Shao, Y., Lin, H., Konishi, T., Kim, G., and Liu, System Demonstrations, pp. 251–260, Dublin, Ireland,
B. Continual pre-training of language models. In The May 2022. Association for Computational Linguistics.
EleventhInternationalConferenceonLearningRepresen- doi: 10.18653/v1/2022.acl-demo.25. URLhttps://
tations, 2023a. URL https://openreview.net/ aclanthology.org/2022.acl-demo.25.
forum?id=m GDIItaI3o.
Madaan, D., Yoon, J., Li, Y., Liu, Y., and Hwang, S. J.
Ke, Z., Shao, Y., Lin, H., Xu, H., Shu, L., and Liu, B. Representationalcontinuityforunsupervisedcontinual
Adaptingalanguagemodelwhilepreservingitsgeneral learning. InInternationalConferenceonLearningRep-
knowledge. arXivpreprintarXiv:2301.08986,2023b. resentations,2021.

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
Mirzadeh, S. I., Farajtabar, M., Pascanu, R., and onKnowledgeDiscovery&DataMining,pp.3505–3506,
Ghasemzadeh, H. Understanding the role of training 2020.
regimesincontinuallearning. AdvancesinNeuralInfor-
mationProcessingSystems,33:7308–7320,2020. Rebuffi,S.-A.,Kolesnikov,A.,Sperl,G.,andLampert,C.H.
icarl: Incrementalclassifierandrepresentationlearning.
Nguyen, C. V., Li, Y., Bui, T. D., and Turner, R. E.
In Proceedings of the IEEE Conference on Computer
Variationalcontinuallearning. InInternationalConfer-
Vision and Pattern Recognition, pp. 2001–2010, 2017.
enceonLearningRepresentations,2018. URLhttps: URLhttps://arxiv.org/abs/1611.07725.
//arxiv.org/abs/1710.10628.
Scao,T.L.,Fan,A.,Akiki,C.,Pavlick,E.,Ilic´,S.,Hesslow,
NVIDIA. NVIDIA Collective Communication Library
D., Castagne´, R., Luccioni, A. S., Yvon, F., Galle´, M.,
(NCCL). https://docs.nvidia.com/deeplearning/sdk/nccl-
etal.Bloom:A176b-parameteropen-accessmultilingual
developer-guide/docs/index.html, 2016. Accessed:
languagemodel. arXivpreprintarXiv:2211.05100,2022.
September8,2023.
URLhttps://arxiv.org/abs/2211.05100.
NVIDIA. PytorchextensionwithNVIDIA-maintainedutili-
tiestostreamlinemixedprecisionanddistributedtraining. Scialom,T.,Chakrabarty,T.,andMuresan,S. Fine-tuned
https://nvidia.github.io/apex/,2019. Accessed: Septem- languagemodelsarecontinuallearners. InProceedings
ber8,2023. ofthe2022ConferenceonEmpiricalMethodsinNatural
LanguageProcessing,pp.6107–6122,2022.
Oquab, M., Darcet, T., Moutakanni, T., Vo, H. V.,
Szafraniec,M.,Khalidov,V.,Fernandez,P.,Haziza,D., Seff, A., Beatson, A., Suo, D., and Liu, H. Contin-
Massa,F.,El-Nouby,A.,Howes,R.,Huang,P.-Y.,Xu, ual learning in generative adversarial nets. CoRR,
H.,Sharma,V.,Li,S.-W.,Galuba,W.,Rabbat,M.,As- abs/1705.08395, 2017. URL http://arxiv.org/
sran,M.,Ballas,N.,Synnaeve,G.,Misra,I.,Jegou,H., abs/1705.08395.
Mairal, J., Labatut, P., Joulin, A., and Bojanowski, P.
Dinov2: Learningrobustvisualfeatureswithoutsupervi- Soboleva, D., Al-Khateeb, F., Myers, R., Steeves, J. R.,
sion,2023. Hestness, J., and Dey, N. SlimPajama: A 627B
token cleaned and deduplicated version of RedPa-
Ostapenko, O., Lesort, T., Rodr´ıguez, P., Arefin, M. R.,
jama. https://www.cerebras.net/blog/
Douillard,A.,Rish,I.,andCharlin,L. Continuallearning
slimpajama-a-627b-token-cleaned-and-
with foundation models: An empirical study of latent
deduplicated-version-of-redpajama,2023.
replay,2022.
URL https://huggingface.co/datasets/
Paszke,A.,Gross,S.,Chintala,S.,Chanan,G.,Yang,E., cerebras/SlimPajama-627B.
DeVito,Z.,Lin,Z.,Desmaison,A.,Antiga,L.,andLerer,
Together.xyz. Redpajama: An open source recipe
A. AutomaticDifferentiationinPyTorch. 2017.
to reproduce llama training dataset, 2023. URL
Qin,Y.,Zhang,J.,Lin,Y.,Liu,Z.,Li,P.,Sun,M.,andZhou, https://github.com/togethercomputer/
J. Elle: Efficientlifelongpre-trainingforemergingdata. RedPajama-Data.
arXivpreprintarXiv:2203.06311,2022. URLhttps:
//arxiv.org/abs/2203.06311. Touvron,H.,Lavril,T.,Izacard,G.,Martinet,X.,Lachaux,
M.-A.,Lacroix,T.,Rozie`re,B.,Goyal,N.,Hambro,E.,
Rae, J. W., Borgeaud, S., Cai, T., Millican, K., Hoff-
Azhar, F., et al. Llama: Open and efficient foundation
mann, J., Song, F., Aslanides, J., Henderson, S., Ring,
languagemodels.arXivpreprintarXiv:2302.13971,2023.
R., Young, S., et al. Scaling language models: Meth-
URLhttps://arxiv.org/abs/2302.13971.
ods, analysis & insights from training gopher. arXiv
preprint arXiv:2112.11446, 2021. URL https://
Winata,G.I.,Xie,L.,Radhakrishnan,K.,Wu,S.,Jin,X.,
arxiv.org/abs/2112.11446.
Cheng,P.,Kulkarni,M.,andPreotiuc-Pietro,D. Over-
comingcatastrophicforgettinginmassivelymultilingual
Rao, D., Visin, F., Rusu, A. A., Teh, Y. W., Pascanu, R.,
continual learning. arXiv preprint arXiv:2305.16252,
andHadsell,R. Continualunsupervisedrepresentation
learning. 2019. URL https://arxiv.org/pdf/ 2023.
1910.14481.pdf.
Wolf, T., Debut, L., Sanh, V., Chaumond, J., De-
Rasley,J.,Rajbhandari,S.,Ruwase,O.,andHe,Y. Deep- langue, C., Moi, A., Cistac, P., Ma, C., Jernite, Y.,
speed: Systemoptimizationsenabletrainingdeeplearn- Plu, J., Xu, C., Le Scao, T., Gugger, S., Drame,
ingmodelswithover100billionparameters. InProceed- M., Lhoest, Q., and Rush, A. M. Transformers:
ingsofthe26thACMSIGKDDInternationalConference State-of-the-Art Natural Language Processing. pp.

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
38–45.AssociationforComputationalLinguistics,Oc-
tober 2020. URL https://www.aclweb.org/
anthology/2020.emnlp-demos.6.
Xu, H., Liu, B., Shu, L., andYu, P.S. Bertpost-training
forreviewreadingcomprehensionandaspect-basedsen-
timentanalysis. arXivpreprintarXiv:1904.02232,2019.
Yang, G., Hu, E. J., Babuschkin, I., Sidor, S., Farhi, D.,
Pachocki, J., Liu, X., Chen, W., and Gao, J. Tensor
programsv: Tuninglargeneuralnetworksviazero-shot
hyperparameter transfer. In NeurIPS 2021, March
## 2022. URL https://www.microsoft.com/
en-us/research/publication/tuning-
large-neural-networks-via-zero-shot-
hyperparameter-transfer/.
Zhai,M.,Chen,L.,Tung,F.,He,J.,Nawhal,M.,andMori,
G. Lifelonggan: Continuallearningforconditionalim-
agegeneration. InProceedingsoftheIEEE/CVFinter-
nationalconferenceoncomputervision,pp.2759–2768,
2019.
Zhao, W. X., Zhou, K., Li, J., Tang, T., Wang, X.,
Hou, Y., Min, Y., Zhang, B., Zhang, J., Dong, Z.,
et al. A survey of large language models. arXiv
preprint arXiv:2303.18223, 2023. URL https://
arxiv.org/abs/2303.18223.

ContinualPre-TrainingofLargeLanguageModels:Howto(re)warm-upyourmodel?
A.Upstreamlosswhenfine-tuningvariouscheckpoints.
2.7
2.6
2.5
2.4
2.3
2.2
0 10 20 30 40 50
Tokens (B)
)maertspu(
ssoL
.laV
eliP
MaxLR 3e-04 Iter. 27000
MaxLR 3e-04 Iter. 143000
MaxLR 3e-04 Iter. 10000
MaxLR 3e-04 Iter. 10000
MaxLR 3e-04 Iter. 143000
MaxLR 3e-04 Iter. 27000
Figure8.Pilevalidationlossofmodelstrainedfromthefullyconvergedcheckpoint, theupstreamsaturationpoint, and1/2ofthe
upstreamsaturationpoint.TheexperimentsforthisfigurearedescribedinSec.4.5.
2.8
2.7
2.6
2.5
2.4
2.3
2.2
0 10 20 30 40 50
Tokens (B)
)maertspu(
ssoL
.laV
eliP
3.1
3.0
2.9
WU 0.0 Iter. 27000
WU 0.0 Iter. 143000
WU 0.0 Iter. 10000 2.8
WU 0.01 Iter. 0
WU 0.01 Iter. 10000
WU 0.01 Iter. 143000 2.7
WU 0.01 Iter. 27000
0 10 20 30 40 50
Tokens (B)
)maertsnwod(
ssoL
.laV
amajaPmilS
WU 0.0 Iter. 27000
WU 0.0 Iter. 143000
WU 0.0 Iter. 10000
WU 0.01 Iter. 0
WU 0.01 Iter. 10000
WU 0.01 Iter. 143000
WU 0.01 Iter. 27000
Figure9.Trainingfromapre-trainedcheckpointachieveslowerPileandSlimPajamavalidationlossfasterthantrainingfromscratch.

## My Notes

-
-
-
-
-
