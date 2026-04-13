---
paper_id: 2024_deepseek_math
topic_tags: [alignment, grpo, mathematical_reasoning, rl, verifiable_rewards]
source_url: https://github.com/deepseek-ai/DeepSeek-Math
---

DeepSeekMath: Pushing the Limits of Mathematical
Reasoning in Open Language Models
ZhihongShao1,2∗†,PeiyiWang1,3∗†,QihaoZhu1,3∗†,RunxinXu1,JunxiaoSong1
XiaoBi1,HaoweiZhang1,MingchuanZhang1,Y.K.Li1,Y.Wu1,DayaGuo1∗
1DeepSeek-AI,2TsinghuaUniversity,3PekingUniversity
{zhihongshao,wangpeiyi,zhuqh,guoday}@deepseek.com
https://github.com/deepseek-ai/DeepSeek-Math
## Abstract
Mathematicalreasoningposesasignificantchallengeforlanguagemodelsduetoitscomplex
and structured nature. In this paper, we introduce DeepSeekMath 7B, which continues pre-
trainingDeepSeek-Coder-Base-v1.57Bwith120Bmath-relatedtokenssourcedfromCommon
Crawl, together with natural language and code data. DeepSeekMath 7B has achieved an
impressive score of 51.7% on the competition-level MATH benchmark without relying on
externaltoolkitsandvotingtechniques,approachingtheperformancelevelofGemini-Ultra
andGPT-4. Self-consistencyover64samplesfromDeepSeekMath7Bachieves60.9%onMATH.
ThemathematicalreasoningcapabilityofDeepSeekMathisattributedtotwokeyfactors: First,
we harness the significant potential of publicly available web data through a meticulously
engineereddataselectionpipeline. Second,weintroduceGroupRelativePolicyOptimization
(GRPO),avariantofProximalPolicyOptimization(PPO),thatenhancesmathematicalreasoning
abilitieswhileconcurrentlyoptimizingthememoryusageofPPO.
Figure1 | Top1accuracyofopen-sourcemodelson the competition-level MATHbenchmark
(Hendrycksetal.,2021)withouttheuseofexternaltoolkitsandvotingtechniques.
∗ Corecontributors.
† WorkdoneduringinternshipatDeepSeek-AI.
rpA
]LC.sc[
3v00330.2042:viXra

## 1. Introduction
Large language models (LLM) have revolutionized the approach to mathematical reasoning
inartificialintelligence,spurringsignificantadvancementsinboththequantitativereasoning
benchmark(Hendrycksetal.,2021)andthegeometryreasoningbenchmark(Trinhetal.,2024).
Moreover, these models have proven instrumental in assisting humans in solving complex
mathematical problems (Tao, 2023). However, cutting-edge models such as GPT-4 (OpenAI,
2023)andGemini-Ultra(Aniletal.,2023)arenotpubliclyavailable,andthecurrentlyaccessible
open-sourcemodelsconsiderablytrailbehindinperformance.
Inthisstudy,weintroduceDeepSeekMath,adomain-specificlanguagemodelthatsignifi-
cantlyoutperformsthemathematicalcapabilitiesofopen-sourcemodelsandapproachesthe
performancelevelofGPT-4onacademicbenchmarks. Toachievethis,wecreatetheDeepSeek-
MathCorpus,alarge-scalehigh-qualitypre-trainingcorpuscomprising120Bmathtokens. This
datasetisextractedfromtheCommonCrawl(CC)usingafastText-basedclassifier(Joulinetal.,
2016). Intheinitialiteration,theclassifieristrainedusinginstancesfromOpenWebMath(Paster
etal.,2023)aspositiveexamples,whileincorporatingadiverseselectionofotherwebpagesto
serveasnegativeexamples. Subsequently,weemploytheclassifiertomineadditionalpositive
instancesfromtheCC,whicharefurtherrefinedthroughhumanannotation. Theclassifieris
thenupdatedwiththisenhanceddatasettoimproveitsperformance. Theevaluationresults
indicatethatthelarge-scalecorpusisofhighquality,asourbasemodelDeepSeekMath-Base
7Bachieves64.2%onGSM8K(Cobbeetal.,2021)and36.2%onthecompetition-levelMATH
dataset (Hendrycks et al., 2021), outperforming Minerva 540B (Lewkowycz et al., 2022a). In
addition,theDeepSeekMathCorpusismultilingual,sowenoticeanimprovementinChinese
mathematicalbenchmarks(Weietal.,2023;Zhongetal.,2023). Webelievethatourexperience
in mathematical data processing is a starting point for the research community, and there is
significantroomforimprovementinthefuture.
DeepSeekMath-BaseisinitializedwithDeepSeek-Coder-Base-v1.57B(Guoetal.,2024),as
we notice that starting from a code training model is a better choice compared to a general
LLM.Furthermore,weobservethemathtrainingalsoimprovesmodelcapabilityonMMLU
(Hendrycksetal.,2020)andBBHbenchmarks(Suzgunetal.,2022),indicatingitdoesnotonly
enhancethemodel’smathematicalabilitiesbutalsoamplifiesgeneralreasoningcapabilities.
Afterpre-training,weapplymathematicalinstructiontuningtoDeepSeekMath-Basewith
chain-of-thought(Weietal.,2022),program-of-thought(Chenetal.,2022;Gaoetal.,2023),and
tool-integratedreasoning(Gouetal.,2023)data. TheresultingmodelDeepSeekMath-Instruct
7Bbeatsall7Bcounterpartsandiscomparablewith70Bopen-sourceinstruction-tunedmodels.
Furthermore,weintroducetheGroupRelativePolicyOptimization(GRPO),avariantrein-
forcementlearning(RL)algorithmofProximalPolicyOptimization(PPO)(Schulmanetal.,2017).
GRPOforegoesthecriticmodel,insteadestimatingthebaselinefromgroupscores,significantly
reducingtrainingresources. BysolelyusingasubsetofEnglishinstructiontuningdata,GRPO
obtains a substantial improvement over the strong DeepSeekMath-Instruct, including both
in-domain(GSM8K:82.9%→88.2%,MATH:46.8%→51.7%)andout-of-domainmathematical
tasks(e.g.,CMATH:84.6%→88.8%)duringthereinforcementlearningphase. Wealsoprovide
aunifiedparadigmtounderstanddifferentmethods,suchasRejectionSamplingFine-Tuning
(RFT)(Yuanetal.,2023a),DirectPreferenceOptimization(DPO)(Rafailovetal.,2023),PPOand
GRPO.Basedonsuchaunifiedparadigm,wefindthatallthesemethodsareconceptualizedas
eitherdirectorsimplifiedRLtechniques. Wealsoconductextensiveexperiments,e.g.,online
v.s. offlinetraining, outcomev.s. processsupervision, single-turnv.s. iterativeRLandsoon,

todeeplyinvestigatetheessentialelementsofthisparadigm. Atlast,weexplainwhyourRL
booststheperformanceofinstruction-tunedmodels,andfurthersummarizepotentialdirections
toachievemoreeffectiveRLbasedonthisunifiedparadigm.
## 1.1. Contributions
Ourcontributionincludesscalablemathpre-training,alongwiththeexplorationandanalysisof
reinforcementlearning.
MathPre-TrainingatScale
• OurresearchprovidescompellingevidencethatthepubliclyaccessibleCommonCrawl
datacontainsvaluableinformationformathematicalpurposes. Byimplementingametic-
ulously designed data selection pipeline, we successfully construct the DeepSeekMath
Corpus, a high-quality dataset of 120B tokens from web pages filtered for mathemati-
cal content, which is almost 7 times the size of the math web pages used by Minerva
(Lewkowycz et al., 2022a) and 9 times the size of the recently released OpenWebMath
(Pasteretal.,2023).
• Ourpre-trainedbasemodelDeepSeekMath-Base7Bachievescomparableperformance
withMinerva540B(Lewkowyczetal.,2022a),indicatingthenumberofparametersisnot
theonlykeyfactorinmathematicalreasoningcapability. Asmallermodelpre-trainedon
high-qualitydatacouldachievestrongperformanceaswell.
• We share our findings from math training experiments. Code training prior to math
trainingimprovesmodels’abilitytosolvemathematicalproblemsbothwithandwithout
tool use. This offers a partial answer to the long-standing question: does code training
improvereasoningabilities? Webelieveitdoes,atleastformathematicalreasoning.
• AlthoughtrainingonarXivpapersiscommon,especiallyinmanymath-relatedpapers,it
bringsnonotableimprovementsonallmathematicalbenchmarksadoptedinthispaper.
ExplorationandAnalysisofReinforcementLearning
• We introduce Group Relative Policy Optimization (GRPO), an efficient and effective
reinforcement learning algorithm. GRPO foregoes the critic model, instead estimating
the baseline from group scores, significantly reducing training resources compared to
ProximalPolicyOptimization(PPO).
• We demonstrate that GRPO significantly enhances the performance of our instruction-
tunedmodelDeepSeekMath-Instruct,bysolelyusingtheinstruction-tuningdata. Further-
more,weobserveenhancementsintheout-of-domainperformanceduringthereinforce-
mentlearningprocess.
• We provide a unified paradigm to understand different methods, such as RFT, DPO,
PPO,andGRPO.Wealsoconductextensiveexperiments,e.g.,onlinev.s. offlinetraining,
outcomev.s. processsupervision,single-turnv.s. iterativereinforcementlearning,andso
ontodeeplyinvestigatetheessentialelementsofthisparadigm.
• Basedonourunifiedparadigm,weexplorethereasonsbehindtheeffectivenessofrein-
forcementlearning,andsummarizeseveralpotentialdirectionstoachievemoreeffective
reinforcementlearningofLLMs.
## 1.2. SummaryofEvaluationsandMetrics
• EnglishandChineseMathematicalReasoning: Weconductcomprehensiveassessments
of our models on English and Chinese benchmarks, covering mathematical problems

from grade-school level to college level. English benchmarks include GSM8K (Cobbe
etal.,2021),MATH(Hendrycksetal.,2021),SAT(Azerbayevetal.,2023),OCWCourses
(Lewkowyczetal.,2022a),MMLU-STEM(Hendrycksetal.,2020). Chinesebenchmarks
includeMGSM-zh(Shietal.,2023),CMATH(Weietal.,2023),Gaokao-MathCloze(Zhong
et al., 2023), and Gaokao-MathQA (Zhong et al., 2023). We evaluate models’ ability
to generate self-contained text solutions without tool use, and also the ability to solve
problemsusingPython.
OnEnglishbenchmarks,DeepSeekMath-Baseiscompetitivewiththeclosed-sourceMin-
erva540B(Lewkowyczetal.,2022a),andsurpassesallopen-sourcebasemodels(e.g.,Mis-
tral7B(Jiangetal.,2023)andLlemma-34B(Azerbayevetal.,2023)),regardlessofwhether
they’ve undergone math pre-training or not, often by a significant margin. Notably,
DeepSeekMath-BaseissuperioronChinesebenchmarks,likelybecausewedon’tfollow
previousworks(Azerbayevetal.,2023;Lewkowyczetal.,2022a)tocollectEnglish-only
mathpre-trainingdata,andalsoincludehigh-qualitynon-Englishones. Withmathemati-
calinstructiontuningandreinforcementlearning,theresultingDeepSeekMath-Instruct
andDeepSeekMath-RLdemonstratestrongperformance,obtaininganaccuracyofover
50% on the competition-level MATH dataset for the first time within the open-source
community.
• Formal Mathematics: We evaluate DeepSeekMath-Base using the informal-to-formal
theoremprovingtaskfrom(Jiangetal.,2022)onminiF2F(Zhengetal.,2021)withIsabelle
(Wenzeletal.,2008)chosentobetheproofassistant. DeepSeekMath-Basedemonstrates
strongfew-shotautoformalizationperformance.
• Natural Language Understanding, Reasoning, and Code: To build a comprehensive
profile of models’ general understanding, reasoning, and coding capabilities, we eval-
uateDeepSeekMath-BaseontheMassiveMultitaskLanguageUnderstanding(MMLU)
benchmark(Hendrycksetal.,2020)whichencompasses57multiple-choicetaskscovering
diversesubjects,BIG-BenchHard(BBH)(Suzgunetal.,2022)whichconsistsof23chal-
lenging tasks that mostly require multi-step reasoning to solve, as well as HumanEval
(Chenetal.,2021)andMBPP(Austinetal.,2021)whicharewidelyusedtoevaluatecode
languagemodels. Mathpre-trainingbenefitsbothlanguageunderstandingandreasoning
performance.
## 2. Math Pre-Training
## 2.1. DataCollectionandDecontamination
In this section, we will outline the process of constructing the DeepSeekMath Corpus from
CommonCrawl. AsdepictedinFigure2,wepresentaniterativepipelinethatdemonstrates
howtosystematicallygatheralarge-scalemathematicalcorpusfromCommonCrawl,starting
withaseedcorpus(e.g.,asmallbuthigh-qualitycollectionofmath-relateddataset). It’sworth
notingthatthisapproachisalsoapplicabletootherdomains,suchascoding.
First,wechooseOpenWebMath(Pasteretal.,2023),acollectionofhigh-qualitymathematical
webtexts,asourinitialseedcorpus. Usingthiscorpus,wetrainafastTextmodel(Joulinetal.,
2016)torecallmoreOpenWebMath-likemathematicalwebpages. Specifically,werandomly
select 500,000 data points from the seed corpus as positive training examples and another
500,000webpagesfromCommonCrawlasnegativeones. Weemployanopen-sourcelibrary1
fortraining,configuringthevectordimensionto256,learningrateto0.1,themaximumlength
1https://fasttext.cc

## 2. Recall Math-Related Webpages
## 1. Train a FastTextModel
From Common Crawl
Math Seed
Deduplicated Common Crawl Math Corpus
40B HTML pages
## 4. Annotate Math-Related
## 3. Discover Math-Related Domains
URL Path From Labelers
Figure2 | AniterativepipelinethatcollectsmathematicalwebpagesfromCommonCrawl.
of word n-gram to 3, the minimum number of word occurrences to 3, and the number of
trainingepochsto3. ToreducethesizeoftheoriginalCommonCrawl,weemployURL-based
deduplicationandnear-deduplicationtechniques,resultingin40BHTMLwebpages. Wethen
recall mathematical web pages from deduplicated Common Crawl with the fastText model.
Tofilteroutlow-qualitymathematicalcontent,werankthecollectedpagesaccordingtotheir
scorespredictedbythefastTextmodel,andonlypreservethetop-rankingones. Thevolume
ofdatapreservedisassessedthroughpre-trainingexperimentsonthetop40B,80B,120B,and
160Btokens. Inthefirstiteration,wechoosetokeepthetop40Btokens.
After the first iteration of data collection, numerous mathematical web pages remain un-
collected,mainlybecausethefastTextmodelistrainedonasetofpositiveexamplesthatlacks
sufficientdiversity. Wethereforeidentifyadditionalmathematicalwebsourcestoenrichtheseed
corpus,sothatwecanoptimizethefastTextmodel. Specifically,wefirstorganizetheentireCom-
monCrawlintodisjointdomains;adomainisdefinedaswebpagessharingthesamebaseURL.
Foreachdomain,wecalculatethepercentageofwebpagesthatarecollectedinthefirstiteration.
Domainswhereover10%ofthewebpageshavebeencollectedareclassifiedasmath-related
(e.g., mathoverflow.net). Subsequently, we manually annotate the URLs associated with
mathematicalcontentwithintheseidentifieddomains(e.g.,mathoverflow.net/questions).
Web pages linked to these URLs, yet uncollected, will be added to the seed corpus. This ap-
proach enables us to gather more positive examples, thereby training an improved fastText
model capable of recalling more mathematical data in the subsequent iteration. After four
iterations of data collection, we end up with 35.5M mathematical web pages, totaling 120B
tokens. Inthefourthiteration,wenoticethatnearly98%ofthedatahasalreadybeencollected
inthethirditeration,sowedecidetoceasedatacollection.
To avoid benchmark contamination, we follow Guo et al. (2024) to filter out web pages
containingquestionsoranswersfromEnglishmathematicalbenchmarkssuchasGSM8K(Cobbe
et al., 2021) and MATH (Hendrycks et al., 2021) and Chinese benchmarks such as CMATH
(Wei et al., 2023) and AGIEval (Zhong et al., 2023). The filtering criteria are as follows: any
text segment containing a 10-gram string that matches exactly with any sub-string from the
evaluationbenchmarksisremovedfromourmathtrainingcorpus. Forbenchmarktextsthat
are shorter than 10 grams but have at least 3 grams, we employ exact matching to filter out
contaminatedwebpages.

## 2.2. ValidatingtheQualityoftheDeepSeekMathCorpus
Werunpre-trainingexperimentstoinvestigatehowtheDeepSeekMathCorpusiscompared
withtherecentlyreleasedmath-trainingcorpora:
• MathPile (Wang et al., 2023c): a multi-source corpus (8.9B tokens) aggregated from
textbooks, Wikipedia, ProofWiki, CommonCrawl, StackExchange, and arXiv, with the
majority(over85%)sourcedfromarXiv;
• OpenWebMath(Pasteretal.,2023): CommonCrawldatafilteredformathematicalcontent,
totaling13.6Btokens;
• Proof-Pile-2 (Azerbayev et al., 2023): a mathematical corpus consisting of OpenWeb-
Math, AlgebraicStack (10.3B tokens of mathematical code), and arXiv papers (28.0B to-
kens). WhenexperimentingonProof-Pile-2,wefollowAzerbayevetal.(2023)tousean
arXiv:Web:Coderatioof2:4:1.
## 2.2.1. TrainingSetting
Weapplymathtrainingtoageneralpre-trainedlanguagemodelwith1.3Bparameters,which
sharesthesameframeworkastheDeepSeekLLMs(DeepSeek-AI,2024),denotedasDeepSeek-
LLM 1.3B. We separately train a model on each mathematical corpus for 150B tokens. All
experiments are conducted using the efficient and light-weight HAI-LLM (High-flyer, 2023)
trainingframework. FollowingthetrainingpracticeofDeepSeekLLMs,weusetheAdamW
optimizer(LoshchilovandHutter,2017)with 𝛽 = 0.9, 𝛽 = 0.95,andweight_decay = 0.1,along
1 2
with a multi-step learning rate schedule where the learning rate reaches the peak after 2,000
warmupsteps,decreasestoits31.6%after80%ofthetrainingprocess,andfurtherdecreasesto
10.0%ofthepeakafter90%ofthetrainingprocess. Wesetthemaximumvalueoflearningrate
to5.3e-4,anduseabatchsizeof4Mtokenswitha4Kcontextlength.
EnglishBenchmarks ChineseBenchmarks
MathCorpus Size
MMLU Gaokao Gaokao
GSM8K MATH OCW SAT CMATH
STEM MathCloze MathQA
NoMathTraining N/A 2.9% 3.0% 2.9% 15.6% 19.5% 12.3% 0.8% 17.9%
MathPile 8.9B 2.7% 3.3% 2.2% 12.5% 15.7% 1.2% 0.0% 2.8%
OpenWebMath 13.6B 11.5% 8.9% 3.7% 31.3% 29.6% 16.8% 0.0% 14.2%
Proof-Pile-2 51.9B 14.3% 11.2% 3.7% 43.8% 29.2% 19.9% 5.1% 11.7%
DeepSeekMathCorpus 120.2B 23.8% 13.6% 4.8% 56.3% 33.1% 41.5% 5.9% 23.6%
Table1 | PerformanceofDeepSeek-LLM1.3Btrainedondifferentmathematicalcorpora,evalu-
atedusingfew-shotchain-of-thoughtprompting. Corpussizesarecalculatedusingourtokenizer
withavocabularysizeof100K.
## 2.2.2. EvaluationResults
TheDeepSeekMathCorpusisofhighquality,coversmultilingualmathematicalcontent,and
isthelargestinsize.
• High-quality: Weevaluatedownstreamperformanceon8mathematicalbenchmarksusing
few-shotchain-of-thoughtpromptingWeietal.(2022). AsshowninTable1,thereisaclear
performanceleadofthemodeltrainedontheDeepSeekMathCorpus. Figure3showsthat
themodeltrainedontheDeepSeekMathCorpusdemonstratesbetterperformancethan

Figure3 | BenchmarkcurvesofDeepSeek-LLM1.3Btrainedondifferentmathematicalcorpora.
Proof-Pile-2at50Btokens(1fullepochofProof-Pile-2),indicatingtheaveragequalityof
DeepSeekMathCorpusishigher.
• Multilingual: TheDeepSeekMathCorpusencompassesdatainmultiplelanguages,pre-
dominantly featuring English and Chinese as the two most represented languages. As
showninTable1,trainingontheDeepSeekMathCorpusenhancesmathematicalreasoning
performance in both English and Chinese. In contrast, existing mathematical corpora,
which are primarily English-centric, show limited improvement and may even hinder
performanceinChinesemathematicalreasoning.
• Large-scale: TheDeepSeekMathCorpusisseveraltimeslargerthanexistingmathematical
corpora. As depicted in Figure 3, DeepSeek-LLM 1.3B, when trained on the DeepSeek-
MathCorpus,showsasteeperlearningcurvealongwithmorelastingimprovements. In
contrast,thebaselinecorporaaremuchsmaller,andhavealreadybeenrepeatedmultiple
roundsduringtraining,withtheresultingmodelperformancequicklyreachingaplateau.
## 2.3. TrainingandEvaluatingDeepSeekMath-Base7B
In this section, we introduce DeepSeekMath-Base 7B, a base model with strong reasoning
abilities,especiallyinmathematics. OurmodelisinitializedwithDeepSeek-Coder-Base-v1.57B

(Guoetal.,2024)andtrainedfor500Btokens. Thedistributionofthedataisasfollows: 56%
is from the DeepSeekMath Corpus, 4% from AlgebraicStack, 10% from arXiv, 20% is Github
code,andtheremaining10%isnaturallanguagedatafromCommonCrawlinbothEnglishand
Chinese. WemainlyadoptthetrainingsettingspecifiedinSection2.2.1,exceptthatwesetthe
maximumvalueofthelearningrateto4.2e-4anduseabatchsizeof10Mtokens.
WeconductacomprehensiveassessmentofthemathematicalcapabilitiesofDeepSeekMath-
Base7B,focusingonitsabilitytoproduceself-containedmathematicalsolutionswithoutrelying
onexternaltools,solvemathematicalproblemsusingtools,andconductformaltheoremproving.
Beyondmathematics,wealsoprovideamoregeneralprofileofthebasemodel,includingits
performanceofnaturallanguageunderstanding,reasoning,andprogrammingskills.
MathematicalProblemSolvingwithStep-by-StepReasoning WeevaluateDeepSeekMath-
Base’sperformanceofsolvingmathematicalproblemsusingfew-shotchain-of-thoughtprompt-
ing(Weietal.,2022),acrosseightbenchmarksinEnglishandChinese. Thesebenchmarksencom-
passquantitativereasoning(e.g.,GSM8K(Cobbeetal.,2021),MATH(Hendrycksetal.,2021),
andCMATH(Weietal.,2023))andmultiple-choiceproblems(e.g.,MMLU-STEM(Hendrycks
etal.,2020)andGaokao-MathQA(Zhongetal.,2023)),coveringdiversefieldsofmathematics
fromelementarytocollege-levelcomplexity.
AsshowninTable2,DeepSeekMath-Base7Bleadsinperformanceacrossalleightbench-
marksamongtheopen-sourcebasemodels(includingthewidely-usedgeneralmodelMistral
7B (Jiang et al., 2023) and the recently released Llemma 34B (Azerbayev et al., 2023) which
underwentmathtrainingonProof-Pile-2(Azerbayevetal.,2023)). Notably,onthecompetition-
levelMATHdataset,DeepSeekMath-Basesurpassesexistingopen-sourcebasemodelsbyover
10%absolute,andoutperformsMinerva540B(Lewkowyczetal.,2022a),aclosed-sourcebase
model77timeslargerwhichbuildsonPaLM(Lewkowyczetal.,2022b)andisfurthertrained
onmathematicaltexts.
EnglishBenchmarks ChineseBenchmarks
Model Size
MMLU Gaokao Gaokao
GSM8K MATH OCW SAT CMATH
STEM MathCloze MathQA
Closed-SourceBaseModel
Minerva 7B 16.2% 14.1% 7.7% - 35.6% - - -
Minerva 62B 52.4% 27.6% 12.0% - 53.9% - - -
Minerva 540B 58.8% 33.6% 17.6% - 63.9% - - -
Open-SourceBaseModel
Mistral 7B 40.3% 14.3% 9.2% 71.9% 51.1% 44.9% 5.1% 23.4%
Llemma 7B 37.4% 18.1% 6.3% 59.4% 43.1% 43.4% 11.9% 23.6%
Llemma 34B 54.0% 25.3% 10.3% 71.9% 52.9% 56.1% 11.9% 26.2%
DeepSeekMath-Base 7B 64.2% 36.2% 15.4% 84.4% 56.5% 71.7% 20.3% 35.3%
Table2 | ComparisonsbetweenDeepSeekMath-Base7BandstrongbasemodelsonEnglishand
Chinesemathematicalbenchmarks. Modelsareevaluatedwithchain-of-thoughtprompting.
MinervaresultsarequotedfromLewkowyczetal.(2022a).

Mathematical Problem Solving with Tool Use We evaluate program-aided mathematical
reasoningonGSM8KandMATHusingfew-shotprogram-of-thoughtprompting(Chenetal.,
2022;Gaoetal.,2023). ModelsarepromptedtosolveeachproblembywritingaPythonprogram
wherelibrariessuchasmathandsympycanbeutilizedforintricatecomputations. Theexecution
resultoftheprogramisevaluatedastheanswer. AsshowninTable3,DeepSeekMath-Base7B
outperformsthepriorstate-of-the-artLlemma34B.
ProblemSolvingw/Tools Informal-to-FormalProving
Model Size
GSM8K+Python MATH+Python miniF2F-valid miniF2F-test
Mistral 7B 48.5% 18.2% 18.9% 18.0%
CodeLlama 7B 27.1% 17.2% 16.3% 17.6%
CodeLlama 34B 52.7% 23.5% 18.5% 18.0%
Llemma 7B 41.0% 18.6% 20.6% 22.1%
Llemma 34B 64.6% 26.3% 21.0% 21.3%
DeepSeekMath-Base 7B 66.9% 31.4% 25.8% 24.6%
Table3 | Few-shotevaluationofbasemodels’abilitytosolvemathematicalproblemsusingtools
andtheabilitytoconductinformal-to-formaltheoremprovinginIsabelle.
FormalMathematics Formalproofautomationisbeneficialtoensuretheaccuracyandrelia-
bilityofmathematicalproofsandenhanceefficiency,withincreasingattentioninrecentyears.
WeevaluateDeepSeekMath-Base7Bonthetaskofinformal-to-formalprovingfrom(Jiangetal.,
2022)whichistogenerateaformalproofbasedonaninformalstatement,aformalcounterpart
ofthestatement,andaninformalproof. WeevaluateonminiF2F(Zhengetal.,2021),abench-
markforformalOlympiad-levelmathematics,andgenerateaformalproofinIsabelleforeach
problemwithfew-shotprompting. FollowingJiangetal.(2022),weleveragemodelstogenerate
proofsketches,andexecutetheoff-the-shelfautomatedproverSledgehammer(Paulson,2010)
tofillinthemissingdetails. AsshowninTable3,DeepSeekMath-Base7Bdemonstratesstrong
performanceinproofautoformalization.
Model Size MMLU BBH HumanEval(Pass@1) MBPP(Pass@1)
Mistral 7B 62.4% 55.7% 28.0% 41.4%
DeepSeek-Coder-Base-v1.5† 7B 42.9% 42.9% 40.2% 52.6%
DeepSeek-Coder-Base-v1.5 7B 49.1% 55.2% 43.2% 60.4%
DeepSeekMath-Base 7B 54.9% 59.5% 40.9% 52.6%
Table 4 | Evaluation on natural language understanding, reasoning, and code benchmarks.
DeepSeek-Coder-Base-v1.5† isthecheckpointrightbeforelearningratedecay,whichisusedto
trainDeepSeekMath-Base. OnMMLUandBBH,weusefew-shotchain-of-thoughtprompting.
OnHumanEvalandMBPP,weevaluatemodelperformanceunderthezero-shotsettinganda
few-shotsetting,respectively.
NaturalLanguageUnderstanding,Reasoning,andCode Weevaluatemodelperformanceof
naturallanguageunderstandingonMMLU(Hendrycksetal.,2020),reasoningonBBH(Suzgun
etal.,2022),andcodingcapabilitiesonHumanEval(Chenetal.,2021)andMBPP(Austinetal.,

2021). AsshowninTable4,DeepSeekMath-Base7Bexhibitssignificantenhancementsinper-
formanceonMMLUandBBHoveritsprecursor,DeepSeek-Coder-Base-v1.5(Guoetal.,2024),
illustrating the positive impact of math training on language understanding and reasoning.
Additionally,byincludingcodetokensforcontinualtraining,DeepSeekMath-Base7Beffectively
maintainstheperformanceofDeepSeek-Coder-Base-v1.5onthetwocodingbenchmarks. Over-
all,DeepSeekMath-Base7BsignificantlyoutperformsthegeneralmodelMistral7B(Jiangetal.,
2023)onthethreereasoningandcodingbenchmarks.
## 3. Supervised Fine-Tuning
## 3.1. SFTDataCuration
Weconstructamathematicalinstruction-tuningdatasetcoveringEnglishandChineseproblems
fromdifferentmathematicalfieldsandofvaryingcomplexitylevels: problemsarepairedwith
solutionsinchain-of-thought(CoT)(Weietal.,2022),program-of-thought(PoT)(Chenetal.,
2022;Gaoetal.,2023),andtool-integratedreasoningformat(Gouetal.,2023). Thetotalnumber
oftrainingexamplesis776K.
• English mathematical datasets: We annotate GSM8K and MATH problems with tool-
integratedsolutions,andadoptasubsetofMathInstruct(Yueetal.,2023)alongwiththe
training set of Lila-OOD (Mishra et al., 2022) where problems are solved with CoT or
PoT.OurEnglishcollectioncoversdiversefieldsofmathematics,e.g.,algebra,probability,
numbertheory,calculus,andgeometry.
• Chinesemathematicaldatasets: WecollectChineseK-12mathematicalproblemsspanning
## 76 sub-topics such as linear equations, with solutions annotated in both CoT and tool-
integratedreasoningformat.
## 3.2. TrainingandEvaluatingDeepSeekMath-Instruct7B
Inthissection,weintroduceDeepSeekMath-Instruct7Bwhichundergoesmathematicalinstruc-
tiontuningbasedonDeepSeekMath-Base. Trainingexamplesarerandomlyconcatenateduntil
reachingamaximumcontextlengthof4Ktokens. Wetrainthemodelfor500stepswithabatch
sizeof256andaconstantlearningrateof5e-5.
We evaluate models’ mathematical performance both without and with tool use, on 4
quantitativereasoningbenchmarksinEnglishandChinese. Webenchmarkourmodelagainst
theleadingmodelsofthetime:
• Closed-sourcemodelsinclude: (1)theGPTfamilyamongwhichGPT-4(OpenAI,2023)
andGPT-4CodeInterpreter2 arethemostcapableones,(2)GeminiUltraandPro(Anil
etal.,2023),(3)Inflection-2(InflectionAI,2023),(4)Grok-13,aswellasmodelsrecently
releasedbyChinesecompaniesincluding(5)Baichuan-34,(6)thelatestGLM-45 fromthe
GLMfamily(Duetal.,2022). Thesemodelsareforgeneralpurposes,mostofwhichhave
undergoneaseriesofalignmentprocedures.
• Open-sourcemodelsinclude: generalmodelslike(1)DeepSeek-LLM-Chat67B(DeepSeek-
AI,2024),(2)Qwen72B(Baietal.,2023),(3)SeaLLM-v27B(Nguyenetal.,2023),and(4)
2https://openai.com/blog/chatgpt-plugins#code-interpreter
3https://x.ai/model-card
4https://www.baichuan-ai.com
5https://open.bigmodel.cn/dev/api#glm-4

ChatGLM36B(ChatGLM3Team,2023),aswellasmodelswithenhancementsinmathemat-
icsincluding(5)InternLM2-Math20B6 whichbuildsonInternLM2andunderwentmath
trainingfollowedbyinstructiontuning,(6)Math-Shepherd-Mistral7BwhichapplysPPO
training(Schulmanetal.,2017)toMistral7B(Jiangetal.,2023)withaprocess-supervised
rewardmodel,(7)theWizardMathseries(Luoetal.,2023)whichimprovesmathematical
reasoninginMistral7BandLlama-270B(Touvronetal.,2023)usingevolve-instruct(i.e.,
aversionofinstructiontuningthatusesAI-evolvedinstructions)andPPOtrainingwith
trainingproblemsprimarilysourcedfromGSM8KandMATH,(8)MetaMath70B(Yuetal.,
2023)whichisLlama-270Bfine-tunedonanaugmentedversionofGSM8KandMATH,
(9)ToRA34BGouetal.(2023)whichisCodeLlama34Bfine-tunedtodotool-integrated
mathematical reasoning, (10) MAmmoTH 70B (Yue et al., 2023) which is Llama-2 70B
instruction-tunedonMathInstruct.
AsshowninTable5,undertheevaluationsettingwheretooluseisdisallowed,DeepSeekMath-
Instruct 7B demonstrates strong performance of step-by-step reasoning. Notably, on the
competition-level MATH dataset, our model surpasses all open-source models and the ma-
jority of proprietary models (e.g., Inflection-2 and Gemini Pro) by at least 9% absolute. This
is true even for models that are substantially larger (e.g., Qwen 72B) or have been specifi-
callyenhancedthroughmath-focusedreinforcementlearning(e.g.,WizardMath-v1.17B).While
DeepSeekMath-InstructrivalstheChineseproprietarymodelsGLM-4andBaichuan-3onMATH,
itstillunderperformsGPT-4andGeminiUltra.
Undertheevaluationsettingwheremodelsareallowedtointegratenaturallanguagerea-
soningandprogram-basedtooluseforproblemsolving,DeepSeekMath-Instruct7Bapproaches
anaccuracyof60%onMATH,surpassingallexistingopen-sourcemodels. Ontheotherbench-
marks,ourmodeliscompetitivewithDeepSeek-LLM-Chat67B,thepriorstate-of-the-artthatis
10timeslarger.
## 4. Reinforcement Learning
## 4.1. GroupRelativePolicyOptimization
Reinforcementlearning(RL)hasbeenproventobeeffectiveinfurtherimprovingthemathe-
maticalreasoningabilityofLLMsaftertheSupervisedFine-Tuning(SFT)stage(Luoetal.,2023;
Wangetal.,2023b). Inthissection,weintroduceourefficientandeffectiveRLalgorithm,Group
RelativePolicyOptimization(GRPO).
## 4.1.1. FromPPOtoGRPO
ProximalPolicyOptimization(PPO)(Schulmanetal.,2017)isanactor-criticRLalgorithmthatis
widelyusedintheRLfine-tuningstageofLLMs(Ouyangetal.,2022). Inparticular,itoptimizes
LLMsbymaximizingthefollowingsurrogateobjective:
J𝑃𝑃𝑂(𝜃)=E[𝑞∼𝑃(𝑄),𝑜∼𝜋 𝜃𝑜𝑙𝑑 (𝑂|𝑞)] | 1 𝑜| ∑︁ 𝑡 | = 𝑜 1 | min (cid:20) 𝜋 𝜋 𝜃 𝜃 𝑜𝑙𝑑 (𝑜 (𝑜 𝑡| 𝑡 𝑞 |𝑞 , , 𝑜 𝑜 < < 𝑡) 𝑡) 𝐴𝑡,clip (cid:18) 𝜋 𝜋 𝜃 𝜃 𝑜𝑙𝑑 (𝑜 (𝑜 𝑡| 𝑡 𝑞 |𝑞 , , 𝑜 𝑜 < < 𝑡) 𝑡) ,1−𝜀,1+𝜀 (cid:19) 𝐴𝑡 (cid:21) , (1)
where 𝜋 𝜃 and 𝜋 𝜃 are the current and old policy models, and 𝑞,𝑜 are questions and outputs
𝑜𝑙𝑑
sampledfromthequestiondatasetandtheoldpolicy𝜋 𝜃 ,respectively. 𝜀isaclipping-related
𝑜𝑙𝑑
hyper-parameter introduced in PPO for stabilizing training. 𝐴 𝑡 is the advantage, which is
computedbyapplyingGeneralizedAdvantageEstimation(GAE)(Schulmanetal.,2015),based
6https://github.com/InternLM/InternLM-Math

EnglishBenchmarks ChineseBenchmarks
Model Size
GSM8K MATH MGSM-zh CMATH
Chain-of-ThoughtReasoning
Closed-SourceModel
GeminiUltra - 94.4% 53.2% - -
GPT-4 - 92.0% 52.9% - 86.0%
Inflection-2 - 81.4% 34.8% - -
GPT-3.5 - 80.8% 34.1% - 73.8%
GeminiPro - 86.5% 32.6% - -
Grok-1 - 62.9% 23.9% - -
Baichuan-3 - 88.2% 49.2% - -
GLM-4 - 87.6% 47.9% - -
Open-SourceModel
InternLM2-Math 20B 82.6% 37.7% - -
Qwen 72B 78.9% 35.2% - -
Math-Shepherd-Mistral 7B 84.1% 33.0% - -
WizardMath-v1.1 7B 83.2% 33.0% - -
DeepSeek-LLM-Chat 67B 84.1% 32.6% 74.0% 80.3%
MetaMath 70B 82.3% 26.6% 66.4% 70.9%
SeaLLM-v2 7B 78.2% 27.5% 64.8% -
ChatGLM3 6B 72.3% 25.7% - -
WizardMath-v1.0 70B 81.6% 22.7% 64.8% 65.4%
DeepSeekMath-Instruct 7B 82.9% 46.8% 73.2% 84.6%
DeepSeekMath-RL 7B 88.2% 51.7% 79.6% 88.8%
Tool-IntegratedReasoning
Closed-SourceModel
GPT-4CodeInterpreter - 97.0% 69.7% - -
Open-SourceModel
InternLM2-Math 20B 80.7% 54.3% - -
DeepSeek-LLM-Chat 67B 86.7% 51.1% 76.4% 85.4%
ToRA 34B 80.7% 50.8% 41.2% 53.4%
MAmmoTH 70B 76.9% 41.8% - -
DeepSeekMath-Instruct 7B 83.7% 57.4% 72.0% 84.3%
DeepSeekMath-RL 7B 86.7% 58.8% 78.4% 87.6%
Table 5 | Performance of Open- and Closed-Source models with both Chain-of-Thought and
Tool-IntegratedReasoningonEnglishandChineseBenchmarks. Scoresingraydenotemajority
votes with 32 candidates; The others are Top1 scores. DeepSeekMath-RL 7B beats all open-
source models from 7B to 70B, as well as the majority of closed-source models. Although
DeepSeekMath-RL7Bisonlyfurthertrainedonchain-of-thought-formatinstructiontuningdata
ofGSM8KandMATH,itimprovesoverDeepSeekMath-Instruct7Bonallbenchmarks.

Reference
PPO Model
𝐾𝐾𝐾𝐾
Reward
Policy Model ⊕ 𝑟𝑟 GAE
Model
Value
𝐴𝐴 Trained
𝑞𝑞 𝑜𝑜 Model
Models
𝑣𝑣
GRPO Frozen
Reference Models
𝐾𝐾𝐾𝐾
Model
Policy 𝑜𝑜! Reward 𝑟𝑟! Group 𝐴𝐴!
Model … Model … Computation …
𝑜𝑜" 𝑟𝑟" 𝐴𝐴"
𝑞𝑞
Figure 4 | Demonstration o
𝑜𝑜
f
#
PPO and our GRPO. G
𝑟𝑟#
RPO foregoes the
𝐴𝐴#
value model, instead
estimatingthebaselinefromgroupscores,significantlyreducingtrainingresources.
ontherewards{𝑟 ≥𝑡 }andalearnedvaluefunction𝑉 𝜓. Thus,inPPO,avaluefunctionneedsto
betrainedalongsidethepolicymodelandtomitigateover-optimizationoftherewardmodel,
thestandardapproachistoaddaper-tokenKLpenaltyfromareferencemodelintherewardat
eachtoken(Ouyangetal.,2022),i.e.,
𝜋
𝜃
(𝑜
𝑡
|𝑞,𝑜
<𝑡
)
𝑟 𝑡 = 𝑟 𝜑 (𝑞,𝑜 ≤𝑡 )−𝛽log
𝜋
𝑟𝑒𝑓
(𝑜
𝑡
|𝑞,𝑜
<𝑡
)
, (2)
where𝑟 𝜑 istherewardmodel,𝜋 𝑟𝑒𝑓 isthereferencemodel,whichisusuallytheinitialSFTmodel,
and 𝛽 isthecoefficientoftheKLpenalty.
AsthevaluefunctionemployedinPPOistypicallyanothermodelofcomparablesizeas
the policy model, it brings a substantial memory and computational burden. Additionally,
duringRLtraining,thevaluefunctionistreatedasabaselineinthecalculationoftheadvantage
for variance reduction. While in the LLM context, usually only the last token is assigned a
rewardscorebytherewardmodel,whichmaycomplicatethetrainingofavaluefunctionthatis
accurateateachtoken. Toaddressthis,asshowninFigure4,weproposeGroupRelativePolicy
Optimization(GRPO),whichobviatestheneedforadditionalvaluefunctionapproximationas
inPPO,andinsteadusestheaveragerewardofmultiplesampledoutputs,producedinresponse
tothesamequestion,asthebaseline. Morespecifically,foreachquestion𝑞,GRPOsamplesa
groupofoutputs {𝑜 1 ,𝑜 2 ,··· ,𝑜 𝐺 } fromtheoldpolicy𝜋 𝜃 𝑜𝑙𝑑 andthenoptimizesthepolicymodel
bymaximizingthefollowingobjective:
J𝐺𝑅𝑃𝑂(𝜃)=E[𝑞∼𝑃(𝑄),{𝑜 𝑖}𝐺
𝑖=1
∼𝜋
𝜃𝑜𝑙𝑑
(𝑂|𝑞)]
𝐺 1 ∑︁ 𝑖= 𝐺 1 |𝑜 1 𝑖| ∑︁ 𝑡 | = 𝑜𝑖 1 | (cid:26) min (cid:20) 𝜋 𝜋 𝜃 𝜃 𝑜𝑙𝑑 (𝑜 (𝑜 𝑖, 𝑖 𝑡 , | 𝑡 𝑞 |𝑞 , , 𝑜 𝑜 𝑖, 𝑖 < ,< 𝑡) 𝑡) 𝐴ˆ𝑖,𝑡,clip (cid:18) 𝜋 𝜋 𝜃 𝜃 𝑜𝑙𝑑 (𝑜 (𝑜 𝑖, 𝑖 𝑡 , | 𝑡 𝑞 |𝑞 , , 𝑜 𝑜 𝑖, 𝑖 < ,< 𝑡) 𝑡) ,1−𝜀,1+𝜀 (cid:19) 𝐴ˆ𝑖,𝑡 (cid:21) −𝛽D 𝐾𝐿 (cid:2)𝜋 𝜃||𝜋 𝑟𝑒𝑓 (cid:3) (cid:27) , (3)
where 𝜀 and 𝛽 are hyper-parameters, and 𝐴ˆ 𝑖,𝑡 is the advantage calculated based on relative
rewardsoftheoutputsinsideeachgrouponly,whichwillbedetailedinthefollowingsubsec-
tions. ThegrouprelativewaythatGRPOleveragestocalculatetheadvantages,alignswellwith
thecomparativenatureofrewardsmodels,asrewardmodelsaretypicallytrainedondatasets
ofcomparisonsbetweenoutputsonthesamequestion. Alsonotethat,insteadofaddingKL
penalty in the reward, GRPO regularizes by directly adding the KL divergence between the
trainedpolicyandthereferencepolicytotheloss,avoidingcomplicatingthecalculationof 𝐴ˆ 𝑖,𝑡.

Algorithm1IterativeGroupRelativePolicyOptimization
Inputinitialpolicymodel𝜋
𝜃
;rewardmodels𝑟 𝜑;taskpromptsD;hyperparameters𝜀, 𝛽,𝜇
init
1: policymodel𝜋 𝜃 ←𝜋 𝜃
init
2: foriteration=1,...,Ido
3: referencemodel𝜋 𝑟𝑒𝑓 ←𝜋 𝜃
4: forstep=1,...,Mdo
5: SampleabatchD 𝑏fromD
6: Updatetheoldpolicymodel𝜋 𝜃𝑜𝑙𝑑 ←𝜋 𝜃
7: Sample𝐺outputs{𝑜 𝑖 }𝐺 𝑖=1 ∼𝜋 𝜃𝑜𝑙𝑑 (· | 𝑞)foreachquestion𝑞∈ D 𝑏
8: Computerewards{𝑟 𝑖 }𝐺 𝑖=1 foreachsampledoutput𝑜 𝑖 byrunning𝑟 𝜑
9: Compute 𝐴ˆ 𝑖,𝑡 forthe𝑡-thtokenof𝑜 𝑖 throughgrouprelativeadvantageestimation.
10: forGRPOiteration=1,...,𝜇do
11: Updatethepolicymodel𝜋 𝜃bymaximizingtheGRPOobjective(Equation21)
12: Update𝑟 𝜑 throughcontinuoustrainingusingareplaymechanism.
Output𝜋
𝜃
Anddifferentfromthe KLpenalty termused in(2), weestimate theKL divergencewith the
followingunbiasedestimator(Schulman,2020):
D 𝐾𝐿 (cid:2)𝜋 𝜃 ||𝜋 𝑟𝑒𝑓 (cid:3) = 𝜋 𝜋 𝑟 𝜃 𝑒𝑓 ( ( 𝑜 𝑜 𝑖, 𝑖 𝑡 ,𝑡 |𝑞 |𝑞 , , 𝑜 𝑜 𝑖, 𝑖 < ,< 𝑡 𝑡 ) ) −log 𝜋 𝜋 𝑟 𝜃 𝑒𝑓 ( ( 𝑜 𝑜 𝑖, 𝑖 𝑡 ,𝑡 |𝑞 |𝑞 , , 𝑜 𝑜 𝑖, 𝑖 < ,< 𝑡 𝑡 ) ) −1, (4)
whichisguaranteedtobepositive.
## 4.1.2. OutcomeSupervisionRLwithGRPO
Formally, for each question 𝑞, a group of outputs {𝑜 1 ,𝑜 2 ,··· ,𝑜 𝐺 } are sampled from the old
policy model 𝜋 𝜃 . A reward model is then used to score the outputs, yielding 𝐺 rewards
𝑜𝑙𝑑
r = {𝑟 1 ,𝑟 2 ,··· ,𝑟 𝐺 }correspondingly. Subsequently,theserewardsarenormalizedbysubtracting
thegroupaverageanddividingbythegroupstandarddeviation. Outcomesupervisionprovides
thenormalizedrewardattheendofeachoutput𝑜 𝑖 andsetstheadvantages 𝐴ˆ 𝑖,𝑡 ofalltokensin
theoutputasthenormalizedreward,i.e., 𝐴ˆ 𝑖,𝑡 = (cid:101) 𝑟 𝑖 = 𝑟𝑖− s m td e ( a r n ) (r) ,andthenoptimizesthepolicyby
maximizingtheobjectivedefinedinequation(3).
## 4.1.3. ProcessSupervisionRLwithGRPO
Outcome supervision only provides a reward at the end of each output, which may not be
sufficientandefficienttosupervisethepolicyincomplexmathematicaltasks. FollowingWang
et al. (2023b), we also explore process supervision, which provides a reward at the end of
eachreasoningstep. Formally,giventhequestion𝑞and𝐺 sampledoutputs {𝑜 1 ,𝑜 2 ,··· ,𝑜 𝐺 },a
processrewardmodelisusedtoscoreeachstepoftheoutputs,yieldingcorrespondingrewards:
R = {{𝑟𝑖𝑛𝑑𝑒𝑥(1) ,··· ,𝑟𝑖𝑛𝑑𝑒𝑥(𝐾 1 )},··· ,{𝑟𝑖𝑛𝑑𝑒𝑥(1) ,··· ,𝑟𝑖𝑛𝑑𝑒𝑥(𝐾𝐺)}},where𝑖𝑛𝑑𝑒𝑥(𝑗) istheendtokenindex
1 1 𝐺 𝐺
ofthe 𝑗-thstep,and 𝐾 𝑖 isthetotalnumberofstepsinthe𝑖-thoutput. Wealsonormalizethese
rewardswiththeaverageandthestandarddeviation,i.e.,𝑟𝑖𝑛𝑑𝑒𝑥(𝑗)
=
𝑟
𝑖
𝑖𝑛𝑑𝑒𝑥(𝑗)−mean(R)
## . Subsequently,
(cid:101)𝑖 std(R)
theprocesssupervisioncalculatestheadvantageofeachtokenasthesumofthenormalized
rewardsfromthefollowingsteps,i.e., 𝐴ˆ 𝑖,𝑡 = (cid:205) 𝑖𝑛𝑑𝑒𝑥(𝑗)≥𝑡(cid:101) 𝑟 𝑖 𝑖𝑛𝑑𝑒𝑥(𝑗) ,andthenoptimizesthepolicyby
maximizingtheobjectivedefinedinequation(3).

## 4.1.4. IterativeRLwithGRPO
Asthereinforcementlearningtrainingprocessprogresses,theoldrewardmodelmaynotbe
sufficient to supervise the current policy model. Therefore, we also explore the iterative RL
withGRPO.AsshowninAlgorithm1,initerativeGRPO,wegeneratenewtrainingsetsforthe
rewardmodelbasedonthesamplingresultsfromthepolicymodelandcontinuallytrainthe
oldrewardmodelusingareplaymechanismthatincorporates10%ofhistoricaldata. Then,we
set the reference model as the policy model, and continually train the policy model with the
newrewardmodel.
## 4.2. TrainingandEvaluatingDeepSeekMath-RL
We conduct RL based on DeepSeekMath-Instruct 7B. The training data of RL are chain-of-
thought-format questions related to GSM8K and MATH from the SFT data, which consists
of around 144K questions. We exclude other SFT questions to investigate the impact of RL
on benchmarks that lack data throughout the RL phase. We construct the training set of
rewardmodelsfollowing(Wangetal.,2023b). Wetrainourinitialrewardmodelbasedonthe
DeepSeekMath-Base7Bwithalearningrateof2e-5. ForGRPO,wesetthelearningrateofthe
policymodelas1e-6. TheKLcoefficientis0.04. Foreachquestion,wesample64outputs. The
maxlengthissetto1024,andthetrainingbatchsizeis1024. Thepolicymodelonlyhasasingle
updatefollowingeachexplorationstage. WeevaluateDeepSeekMath-RL7Bonbenchmarks
following DeepSeekMath-Instruct 7B. For DeepSeekMath-RL 7B, GSM8K and MATH with
chain-of-thoughtreasoningcanberegardedasin-domaintasksandalltheotherbenchmarks
canberegardedasout-of-domaintasks.
Table5demonstratestheperformanceofopen-andclosed-sourcemodelswithbothchain-
of-thoughtandtool-integratedreasoningonEnglishandChinesebenchmarks. Wefindthat:
1)DeepSeekMath-RL7Battainsaccuraciesof88.2%and51.7%onGSM8KandMATH,respec-
tively,utilizingchain-of-thoughtreasoning. Thisperformancesurpassesthatofallopen-source
models in the 7B to 70B range, as well as the majority of closed-source models. 2) Crucially,
DeepSeekMath-RL 7B is only trained on chain-of-thought-format instruction tuning data of
GSM8KandMATH,startingfromDeepSeekMath-Instruct7B.Despitetheconstrainedscope
of its training data, it outperforms DeepSeekMath-Instruct 7B across all evaluation metrics,
showcasingtheeffectivenessofreinforcementlearning.
## 5. Discussion
Inthissection,wewillshareourfindingsinpre-trainingandRLexperiments.
## 5.1. LessonsLearntinPre-Training
We first share our experience in pre-training. Unless otherwise specified, we will adhere to
the training settings outlined in Section 2.2.1. It is worth noting that, when referring to the
DeepSeekMathCorpusinthissection,weusean89B-tokendatasetfromtheseconditerationof
thedatacollectionprocess.
## 5.1.1. CodeTrainingBenefitsMathematicalReasoning
Apopularyetunverifiedhypothesissuggeststhatcodetrainingimprovesreasoning. Weattempt
toofferapartialresponsetothis,particularlywithinthemathematicaldomain: codetraining

TrainingTokens w/oToolUse w/ToolUse
TrainingSetting
General Code Math GSM8K MATH CMATH GSM8K+Python MATH+Python
NoContinualTraining – – – 2.9% 3.0% 12.3% 2.7% 2.3%
Two-StageTraining
Stage1:GeneralTraining 400B – – 2.9% 3.2% 14.8% 3.3% 2.3%
Stage2:MathTraining – – 150B 19.1% 14.4% 37.2% 14.3% 6.7%
Stage1:CodeTraining – 400B – 5.9% 3.6% 19.9% 12.4% 10.0%
Stage2:MathTraining – – 150B 21.9% 15.3% 39.7% 17.4% 9.4%
One-StageTraining
MathTraining – – 150B 20.5% 13.1% 37.6% 11.4% 6.5%
Code&MathMixedTraining – 400B 150B 17.6% 12.1% 36.3% 19.7% 13.5%
Table 6 | Investigation of how code affects mathematical reasoning under different training
settings. We experiment with DeepSeek-LLM 1.3B, and evaluate its mathematical reasoning
performancewithoutandwithtooluseviafew-shotchain-of-thoughtpromptingandfew-shot
program-of-thoughtprompting,respectively.
improvesmodels’abilitytodomathematicalreasoningbothwithandwithouttooluse.
To study how code training affects mathematical reasoning, we experimented with the
followingtwo-stagetrainingandone-stagetrainingsettings:
Two-StageTraining
• CodeTrainingfor400BTokens→MathTrainingfor150BTokens: WetrainDeepSeek-
LLM1.3Bfor400Bcodetokensfollowedby150Bmathtokens;
• General Training for 400B Tokens → Math Training for 150B Tokens: As a control
experiment,wealsoexperimentwithgeneraltokens(sampledfromalarge-scalegeneral
corpuscreatedbyDeepSeek-AI)insteadofcodetokensinthefirststageoftraining,inan
attempttoinvestigatetheadvantagesofcodetokensovergeneraltokensinimproving
mathematicalreasoning.
One-StageTraining
• MathTrainingfor150BTokens: WetrainDeepSeek-LLM1.3Bfor150Bmathtokens;
• Trainingonamixtureof400BCodeTokensand150BMathTokens: Mathtrainingfol-
lowingcodetrainingdegradescodingperformance. Weinvestigatewhethercodetokens,
whenmixedwithmathtokensforone-stagetraining,wouldstillimprovemathematical
reasoningandalsoalleviatetheproblemofcatastrophicforgetting.
Results Table6andTable7demonstratethedownstreamperformanceunderdifferenttraining
settings.
Codetrainingbenefitsprogram-aidedmathematicalreasoning,bothunderthetwo-stage
training and one-stage training settings. As shown in Table 6, under the two-stage training
setting, code training alone already significantly enhances the ability to solve GSM8K and
MATHproblemsusingPython. Mathtraininginthesecondstageyieldsfurtherimprovements.
Interestingly,undertheone-stagetrainingsetting,mixingcodetokensandmathtokenseffec-
tivelymitigatestheissueofcatastrophicforgettingthatarisesfromtwo-stagetraining,andalso
synergizescoding(Table7)andprogram-aidedmathematicalreasoning(Table6).

TrainingTokens
TrainingSetting MMLU BBH HumanEval(Pass@1) MBPP(Pass@1)
General Code Math
NoContinualTraining – – – 24.5% 28.1% 12.2% 13.0%
Two-StageTraining
Stage1:GeneralTraining 400B – – 25.9% 27.7% 15.2% 13.6%
Stage2:MathTraining – – 150B 33.1% 32.7% 12.8% 13.2%
Stage1:CodeTraining – 400B – 25.0% 31.5% 25.0% 40.0%
Stage2:MathTraining – – 150B 36.2% 35.3% 12.2% 17.0%
One-StageTraining
MathTraining – – 150B 32.3% 32.5% 11.6% 13.2%
Code&MathMixedTraining – 400B 150B 33.5% 35.6% 29.3% 39.4%
Table7 | Investigationofhowdifferentsettingsofcodeandmathtrainingaffectmodelperfor-
manceoflanguageunderstanding,reasoning,andcoding. WeexperimentwithDeepSeek-LLM
1.3B.WeevaluatethemodelsonMMLUandBBHusingfew-shotchain-of-thoughtprompting.
OnHumanEvalandMBPP,weconductzero-shotandfew-shotevaluations,respectively.
EnglishBenchmarks ChineseBenchmarks
Model Size ArXivCorpus
MMLU Gaokao Gaokao
GSM8K MATH OCW SAT CMATH
STEM MathCloze MathQA
NoMathTraining 2.9% 3.0% 2.9% 15.6% 19.5% 12.3% 0.8% 17.9%
DeepSeek-LLM 1.3B
MathPile 2.7% 3.3% 2.2% 12.5% 15.7% 1.2% 0.0% 2.8%
ArXiv-RedPajama 3.3% 3.4% 4.0% 9.4% 9.0% 7.4% 0.8% 2.3%
NoMathTraining 29.0% 12.5% 6.6% 40.6% 38.1% 45.9% 5.9% 21.1%
DeepSeek-Coder-Base-v1.5 7B
MathPile 23.6% 11.5% 7.0% 46.9% 35.8% 37.9% 4.2% 25.6%
ArXiv-RedPajama 28.1% 11.1% 7.7% 50.0% 35.2% 42.6% 7.6% 24.8%
Table8 | EffectofmathtrainingondifferentarXivdatasets. Modelperformanceisevaluated
withfew-shotchain-of-thoughtprompting.
ArXivCorpus miniF2F-valid miniF2F-test
NoMathTraining 20.1% 21.7%
MathPile 16.8% 16.4%
ArXiv-RedPajama 14.8% 11.9%
Table 9 | Effect of math training on different arXiv corpora, the base model being DeepSeek-
Coder-Base-v1.57B.Weevaluateinformal-to-formalprovinginIsabelle.
Codetrainingalsoimprovesmathematicalreasoningwithouttooluse. Underthetwo-stage
training setting, the initial stage of code training already results in moderate enhancements.
It also boosts the efficiency of the subsequent math training, eventually leading to the best
performance. However,combiningcodetokensandmathtokensforone-stagetrainingcom-
promisesmathematicalreasoningwithouttooluse. OneconjectureisthatDeepSeek-LLM1.3B,
duetoitslimitedscale,lacksthecapacitytofullyassimilatebothcodeandmathematicaldata
simultaneously.
## 5.1.2. ArXivPapersSeemIneffectiveinImprovingMathematicalReasoning
ArXivpapersarecommonlyincludedasacomponentofmathpre-trainingdata(Azerbayev
etal.,2023;Lewkowyczetal.,2022a;PoluandSutskever,2020;Wangetal.,2023c). However,

detailedanalysisregardingtheirimpactonmathematicalreasoninghasnotbeenextensively
conducted. Perhaps counter-intuitively, according to our experiments, arXiv papers seem
ineffectiveinimprovingmathematicalreasoning. Weexperimentwithmodelsofdifferentsizes,
includingDeepSeek-LLM1.3BandDeepSeek-Coder-Base-v1.57B(Guoetal.,2024),usingarXiv
corporathatunderwentvariedprocessingpipelines:
• MathPile(Wangetal.,2023c): an8.9B-tokencorpusdevelopedwithcleaningandfiltering
heuristicrules,over85%ofwhicharescientificarXivpapers;
• ArXiv-RedPajama (Computer, 2023): the entirety of arXiv LaTeX files with preambles,
comments,macros,andbibliographiesremoved,totaling28.0Btokens.
In our experiments, we separately train DeepSeek-LLM 1.3B for 150B tokens and DeepSeek-
Coder-Base-v1.57Bfor40BtokensoneacharXivcorpus. ItseemsthatarXivpapersareineffective
inimprovingmathematicalreasoning. WhentrainedonaarXiv-onlycorpus,bothmodelsdis-
playnonotableimprovementsorevendeteriorationacrossvariousmathematicalbenchmarksof
differentcomplexitiesemployedinthisstudy. Thesebenchmarksincludequantitativereasoning
datasetslikeGSM8KandMATH(Table8),multiple-choicechallengeslikeMMLU-STEM(Table
8),andformalmathematicslikeminiF2F(Table9).
However, thisconclusionhasitslimitationsandshouldbetakenwithagrainofsalt. We
havenotyetstudied:
• TheimpactofarXivtokensonspecificmath-relatedtasksnotincludedinthisresearch,
such asinformalization oftheoremswhich is toconvert formalstatements or proofs to
theirinformalversions;
• TheeffectofarXivtokenswhencombinedwithothertypesofdata;
• WhetherthebenefitsofarXivpaperswouldmanifestthemselvesatalargermodelscale.
Thus,furtherexplorationisrequired,whichweleaveforfuturestudies.
## 5.2. InsightsofReinforcementLearning
## 5.2.1. TowardstoaUnifiedParadigm
Inthissection,weprovideaunifiedparadigmtoanalyzedifferenttrainingmethods,suchas
SFT, RFT, DPO, PPO, GRPO, and further conduct experiments to explore the factors of the
unifiedparadigm. Generally,thegradientwithrespecttotheparameter𝜃ofatrainingmethod
canbewrittenas:
|𝑜|
(cid:169) 1 ∑︁ (cid:170)
∇ 𝜃 J A (𝜃) = E[(𝑞 (cid:32)(cid:32)(cid:32) , (cid:32)(cid:32)(cid:32) 𝑜 (cid:32) ) ∼ (cid:32)(cid:32)(cid:32)(cid:32)(cid:32) D (cid:32)(cid:32) ](cid:173) (cid:173)|𝑜| 𝐺 (cid:32) 𝐶 (cid:32)(cid:32)(cid:32)(cid:32) A (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32) ( (cid:32)(cid:32) 𝑞 (cid:32)(cid:32) ,𝑜, (cid:32)(cid:32)(cid:32) 𝑡 (cid:32)(cid:32) , (cid:32)(cid:32)(cid:32) 𝜋 (cid:32)(cid:32)(cid:32)(cid:32) 𝑟 (cid:32)(cid:32)(cid:32) 𝑓 )∇ 𝜃log𝜋 𝜃 (𝑜 𝑡 |𝑞,𝑜 <𝑡 )(cid:174) (cid:174) . (5)
(cid:124) (cid:123)(cid:122) (cid:125) (cid:173) 𝑡=1 (cid:124) (cid:123)(cid:122) (cid:125) (cid:174)
𝐷𝑎𝑡𝑎𝑆𝑜𝑢𝑟𝑐𝑒 𝐺𝑟𝑎𝑑𝑖𝑒𝑛𝑡𝐶𝑜𝑒𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑡
(cid:171) (cid:172)
There exist three key components: 1) Data Source D, which determines the training data; 2)
RewardFunction𝜋 𝑟𝑓,whichisthesourceofthetrainingrewardsignal;3)AlgorithmA: which
processesthetrainingdataandtherewardsignaltothegradientcoefficient𝐺𝐶 thatdetermines
themagnitudeofthepenaltyorreinforcementforthedata. Weanalyzeseveralrepresentative
methodsbasedonsuchaunifiedparadigm:
• SupervisedFine-tuning(SFT):SFTfine-tunespretrainedmodelonhumanselectedSFT
data.

Methods DataSource RewardFunction GradientCoefficient
SFT 𝑞,𝑜∼ 𝑃 𝑠𝑓𝑡 (𝑄,𝑂) - 1
RFT 𝑞∼ 𝑃 𝑠𝑓𝑡 (𝑄),𝑜∼𝜋 𝑠𝑓𝑡 (𝑂|𝑞) Rule Equation10
DPO 𝑞∼ 𝑃 𝑠𝑓𝑡 (𝑄),𝑜+,𝑜− ∼𝜋 𝑠𝑓𝑡 (𝑂|𝑞) Rule Equation14
OnlineRFT 𝑞∼ 𝑃 𝑠𝑓𝑡 (𝑄),𝑜∼𝜋 𝜃 (𝑂|𝑞) Rule Equation10
PPO 𝑞∼ 𝑃 𝑠𝑓𝑡 (𝑄),𝑜∼𝜋 𝜃 (𝑂|𝑞) Model Equation18
GRPO 𝑞∼ 𝑃 𝑠𝑓𝑡 (𝑄),{𝑜 𝑖 }𝐺 𝑖=1 ∼𝜋 𝜃 (𝑂|𝑞) Model Equation21
Table10 | Thedatasourceandgradientcoefficientofdifferentmethods. 𝑃 𝑠𝑓𝑡 denotesthedata
distributionofsupervisedfine-tuningdatasets. 𝜋 𝜃 and𝜋 𝜃 denotethesupervisedfine-tuned
𝑠𝑓𝑡
modelandthereal-timepolicymodelduringtheonlinetrainingprocess,respectively.
0 2000 4000 6000 8000
Steps
)%(
ccA
GSM8K
0 2000 4000 6000 8000
Steps
)%(
ccA
RFT Online RFT GRPO+OS GRPO+PS
MATH
Figure5 | PerformanceoftheDeepSeekMath-Instruct1.3Bmodel,whichwasfurthertrained
usingvariousmethods,ontwobenchmarks.
• Rejection Sampling Fine-tuning (RFT): RFT further fine-tunes the SFT model on the
filtered outputs sampled from the SFT model based on SFT questions. RFT filters the
outputsbasedonthecorrectnessoftheiranswers.
• DirectPreferenceOptimization(DPO):DPOfurtherrefinestheSFTmodelbyfine-tuning
itonaugmentedoutputssampledfromtheSFTmodel,usingpair-wiseDPOloss.
• OnlineRejectionSamplingFine-tuning(OnlineRFT):DifferentfromRFT,OnlineRFT
initiates the policy model using the SFT model and refines it by fine-tuning with the
augmentedoutputssampledfromthereal-timepolicymodel.
• PPO/GRPO:PPO/GRPOinitializesthepolicymodelusingtheSFTmodelandreinforces
itwiththeoutputssampledfromthereal-timepolicymodel.
WesummarizethecomponentsofthesemethodsinTable10. PleaserefertoAppendixA.1fora
moredetailedderivationprocess.
ObservationaboutDataSource Wedividethedatasourceintotwocategories,onlinesam-
pling,andofflinesampling. Onlinesamplingdenotesthatthetrainingdataisfromtheexplo-
ration results of the real-time training policy model, while offline sampling denotes that the

0 1300 2300 3300 4300 5300
Steps
)%(
ccA
GSM8K
0 1300 2300 3300 4300 5300
Steps
)%(
ccA
Iteration-0 Iteration-1 Iteration-2
MATH
Figure6 | PerformanceofiterativereinforcementlearningwithDeepSeekMath-Instruct7Bon
twobenchmarks.
training data is from the sampling results of the initial SFT model. RFT and DPO follow the
offlinestyle,whileOnlineRFTandGRPOfollowtheonlinestyle.
AsshowninFigure5,wefindthattheOnlineRFTsignificantlyoutperformsRFTontwo
benchmarks. Specifically, OnlineRFTiscomparabletoRFTintheearlystageoftrainingbut
gainsanabsoluteadvantageinthelaterstage,demonstratingthesuperiorityofonlinetraining.
Thisisintuitive,asintheinitialstage,theactorandtheSFTmodelexhibitcloseresemblance,
withthesampleddatarevealingonlyminordifferences. Inthelaterstage,however,thedata
sampledfromtheactorwillexhibitmoresignificantdifferences,andreal-timedatasampling
willoffergreateradvantages.
Observation about Gradient Coefficient The algorithm processes the reward signal to the
gradient coefficient to update the model parameter. We divide the reward function as ‘Rule’
and ‘Model’ in our experiments. Rule refers to judging the quality of a response based on
thecorrectnessoftheanswer,andModeldenotesthatwetrainarewardmodeltoscoreeach
response. Thetrainingdataoftherewardmodelisbasedontherulejudgment. Equations10
and21highlightakeydifferencebetweenGRPOandOnlineRFT:GRPOuniquelyadjustsits
gradientcoefficientbasedontherewardvalueprovidedbytherewardmodel. Thisallowsfor
differentialreinforcementandpenalizationofresponsesaccordingtotheirvaryingmagnitudes.
Incontrast,OnlineRFTlacksthisfeature;itdoesnotpenalizeincorrectresponsesanduniformly
reinforcesallresponseswithcorrectanswersatthesamelevelofintensity.
AsdemonstratedinFigure5,GRPOsurpassesonlineRFT,therebyhighlightingtheefficiency
ofalteringpositiveandnegativegradientcoefficients. Inaddition,GRPO+PSshowssuperior
performancecomparedtoGRPO+OS,indicatingthebenefitsofusingfine-grained,step-aware
gradientcoefficients. Furthermore,weexploretheiterativeRL,inourexperiments,weconduct
two rounds of iteration. As shown in Figure 6, we notice that the iterative RL significantly
improvestheperformance,especiallyatthefirstiteration.

1 4 8 16 32 64
K: The number of candidates
)%(
ccA
GSM8K
1 4 8 16 32 64
K: The number of candidates
)%(
ccA
Maj@K-Instruct Maj@K-RL Pass@K-Instruct Pass@K-RL
MATH
Figure 7 | The Maj@K and Pass@K of SFT and RL DeepSeekMath 7B on GSM8K and MATH
(temperature0.7). ItwasnotedthatRLenhancesMaj@KbutnotPass@K.
## 5.2.2. WhyRLWorks?
In this paper, we conduct reinforcement learning based on a subset of instruction tuning
data,anditachievessignificantperformanceenhancementupontheinstructiontuningmodel.
To further explain why reinforcement learning works. We evaluate the Pass@K and Maj@K
accuracyoftheInstructandRLmodelsontwobenchmarks. AsshowninFigure7,RLenhances
Maj@K’sperformancebutnotPass@K.ThesefindingsindicatethatRLenhancesthemodel’s
overallperformancebyrenderingtheoutputdistributionmorerobust,inotherwords,itseems
thattheimprovementisattributedtoboostingthecorrectresponsefromTopKratherthan
the enhancement of fundamental capabilities. Similarly, (Wang et al., 2023a) identified a
misalignmentprobleminreasoningtaskswithintheSFTmodel,showingthatthereasoning
performanceofSFTmodelscanbeimprovedthroughaseriesofpreferencealignmentstrategies
(Songetal.,2023;Wangetal.,2023a;Yuanetal.,2023b).
## 5.2.3. HowtoAchieveMoreEffectiveRL?
WedemonstrateRLworksprettywellinmathematicalreasoningtasks. Wealsoprovideaunified
paradigmtounderstanddifferentrepresentativetrainingmethods. Withinthisparadigm,all
methods are conceptualized as either direct or simplified RL techniques. As summarized in
Equation5,thereexistthreekeycomponents: DataSource,Algorithm,andRewardFunction.
Weprovidesomepotentialfuturedirectionsaboutthethreecomponents.
DataSource Datasourceistherawmaterialofalltrainingmethods. InthecontextofRL,we
specificallyrefertothedatasourceastheunlabeledquestionswiththeoutputssampledfrom
thepolicymodel. Inthispaper,weonlyusethequestionsfromtheinstructiontuningstageand
a naive nucleus sampling to sample outputs. We think this is a potential reason that our RL
pipelineonlyimprovestheMaj@Kperformance. Inthefuture,wewillexploreourRLpipeline
onout-of-distributionquestionprompts,inconjunctionwithadvancedsampling(decoding)
strategies,likethosebasedontree-searchmethods(Yaoetal.,2023). Also,theefficientinference
techniques(Kwonetal.,2023;Leviathanetal.,2023;Xiaetal.,2023,2024),whichdetermines

theexplorationefficiencyofpolicymodels,alsoplayanexceedinglyimportantrole.
Algorithms Algorithmsprocessthedataandrewardsignaltothegradientcoefficienttoupdate
themodelparameter. BasedonEquation5,tosomeextent,allmethodsnowfullyTRUSTthe
signal of the reward function to increase or decrease the conditional probability of a certain
token. However, it is impossible to ensure the reward signal is always reliable, especially in
extremely complex tasks. For example, even the PRM800K datasets (Lightman et al., 2023),
whichhavebeencarefullyannotatedbywell-trainedannotators,stillcontainapproximately20%
ofincorrectlyannotations7. Tothisend,wewillexplorethereinforcementlearningalgorithm
thatisrobustagainstnoisyrewardsignals. WebelievesuchWEAK-TO-STRONG(Burnsetal.,
2023)alignmentmethodswillbringafundamentalchangetothelearningalgorithms.
Reward Function Reward function is the source of the training signal. In RL, the reward
functionisusuallytheneuralrewardmodel. Wethinkthereexistthreeimportantdirectionsfor
rewardmodels: 1)Howtoenhancethegeneralizationabilityoftherewardmodel. Thereward
modelmustbeeffectivelygeneralizedtohandleout-of-distributionquestionsandadvanced
decodingoutputs;otherwise,reinforcementlearningmaymerelystabilizethedistributionof
LLMs rather than improve their fundamental capabilities; 2) How to reflect the uncertainty
ofrewardmodel. Theuncertaintycouldpotentiallyactasalinkingbridgebetweentheweak
rewardmodelandtheweak-to-stronglearningalgorithms;3)Howtoefficientlybuildhigh-
qualityprocessrewardmodelsthatcanprovidefine-grainedtrainingsignalsforthereasoning
process(Lightmanetal.,2023;Wangetal.,2023b).
## 6. Conclusion, Limitation, and Future Work
We present DeepSeekMath, which outperforms all open-source models on the competition-
levelMATHbenchmarkandapproachestheperformanceofclosedmodels. DeepSeekMathis
initializedwithDeepSeek-Coder-v1.57Bandundergoescontinualtrainingfor500Btokens,with
asignificantcomponentofthetrainingdatabeing120BmathtokenssourcedfromCommon
Crawl. Ourextensiveablationstudyshowswebpagesoffersignificantpotentialforhigh-quality
mathematical data, while arXiv may not as beneficial as we expected. We introduce Group
RelativePolicyOptimization(GRPO),avariantofProximalPolicyOptimization(PPO),which
cannotablyimprovemathematicalreasoningcapabilitieswithlessmemoryconsumption. The
experimentresultsshowthatGRPOiseffectiveevenifDeepSeekMath-Instruct7Bhasreached
a high score on benchmarks. We also provide a unified paradigm to understand a series of
methodsandsummarizeseveralpotentialdirectionsformoreeffectivereinforcementlearning.
AlthoughDeepSeekMathachievesimpressivescoresonquantitativereasoningbenchmarks,
its capability on geometry and theorem-proof are relatively weaker than closed models. For
instance, in our dry run, the model cannot handle problems related to triangles and ellipses,
whichmayindicatedataselectionbiasinpre-trainingandfine-tuning. Inaddition,restricted
bythemodelscale,DeepSeekMathisworsethanGPT-4onfew-shotcapability. GPT-4could
improveitsperformancewithfew-shotinputs,whileDeepSeekMathshowssimilarperformance
in zero-shot and few-shot evaluation. In the future, we will further improve our engineered
dataselectionpipelinetoconstructmorehigh-qualitypre-trainedcorpus. Inaddition,wewill
explorethepotentialdirections(Section5.2.3)formoreeffectivereinforcementlearningofLLMs.
7https://github.com/openai/prm800k/issues/12#issuecomment-1728491852

## References
R. Anil, S. Borgeaud, Y. Wu, J. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth,
K.Millican,D.Silver,S.Petrov,M.Johnson,I.Antonoglou,J.Schrittwieser,A.Glaese,J.Chen,
E.Pitler,T.P.Lillicrap,A.Lazaridou,O.Firat,J.Molloy,M.Isard,P.R.Barham,T.Hennigan,
B.Lee,F.Viola,M.Reynolds,Y.Xu,R.Doherty,E.Collins,C.Meyer,E.Rutherford,E.Moreira,
K. Ayoub, M. Goel, G. Tucker, E. Piqueras, M. Krikun, I. Barr, N. Savinov, I. Danihelka,
B. Roelofs, A. White, A. Andreassen, T. von Glehn, L. Yagati, M. Kazemi, L. Gonzalez,
M. Khalman, J. Sygnowski, and et al. Gemini: A family of highly capable multimodal
models. CoRR, abs/2312.11805, 2023. doi: 10.48550/ARXIV.2312.11805. URL https:
//doi.org/10.48550/arXiv.2312.11805.
J.Austin,A.Odena,M.Nye,M.Bosma,H.Michalewski,D.Dohan,E.Jiang,C.Cai,M.Terry,
Q.Le,etal. Programsynthesiswithlargelanguagemodels. arXivpreprintarXiv:2108.07732,
2021.
Z.Azerbayev,H.Schoelkopf,K.Paster,M.D.Santos,S.McAleer,A.Q.Jiang,J.Deng,S.Bider-
man, and S. Welleck. Llemma: An open language model for mathematics. arXiv preprint
arXiv:2310.10631,2023.
J. Bai, S. Bai, Y. Chu, Z. Cui, K. Dang, X. Deng, Y. Fan, W. Ge, Y. Han, F. Huang, et al. Qwen
technicalreport. arXivpreprintarXiv:2309.16609,2023.
C. Burns, P. Izmailov, J. H. Kirchner, B. Baker, L. Gao, L. Aschenbrenner, Y. Chen, A. Ecoffet,
M.Joglekar,J.Leike,etal. Weak-to-stronggeneralization: Elicitingstrongcapabilitieswith
weaksupervision. arXivpreprintarXiv:2312.09390,2023.
ChatGLM3Team. Chatglm3series: Openbilingualchatllms,2023. URLhttps://github.c
om/THUDM/ChatGLM3.
M.Chen,J.Tworek,H.Jun,Q.Yuan,H.P.deOliveiraPinto,J.Kaplan,H.Edwards,Y.Burda,
N.Joseph,G.Brockman,A.Ray,R.Puri,G.Krueger,M.Petrov,H.Khlaaf,G.Sastry,P.Mishkin,
B.Chan,S.Gray,N.Ryder,M.Pavlov,A.Power,L.Kaiser,M.Bavarian,C.Winter,P.Tillet,
F.P.Such,D.Cummings,M.Plappert,F.Chantzis,E.Barnes,A.Herbert-Voss,W.H.Guss,
A.Nichol,A.Paino,N.Tezak,J.Tang,I.Babuschkin,S.Balaji,S.Jain,W.Saunders,C.Hesse,
A.N.Carr,J.Leike,J.Achiam,V.Misra,E.Morikawa,A.Radford,M.Knight,M.Brundage,
M.Murati,K.Mayer,P.Welinder,B.McGrew,D.Amodei,S.McCandlish,I.Sutskever,and
W.Zaremba. Evaluatinglargelanguagemodelstrainedoncode. CoRR,abs/2107.03374,2021.
URLhttps://arxiv.org/abs/2107.03374.
W.Chen,X.Ma,X.Wang,andW.W.Cohen. Programofthoughtsprompting: Disentangling
computationfromreasoningfornumericalreasoningtasks. CoRR,abs/2211.12588,2022. doi:
10.48550/ARXIV.2211.12588. URLhttps://doi.org/10.48550/arXiv.2211.12588.
K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek,
J.Hilton, R.Nakano, etal. Trainingverifierstosolvemathwordproblems. arXivpreprint
arXiv:2110.14168,2021.
T.Computer. Redpajama: anopendatasetfortraininglargelanguagemodels,Oct.2023. URL
https://github.com/togethercomputer/RedPajama-Data.
DeepSeek-AI. DeepseekLLM:scalingopen-sourcelanguagemodelswithlongtermism. CoRR,
abs/2401.02954,2024. doi: 10.48550/ARXIV.2401.02954. URLhttps://doi.org/10.485
50/arXiv.2401.02954.

Z. Du, Y. Qian, X. Liu, M. Ding, J. Qiu, Z. Yang, and J. Tang. Glm: General language model
pretrainingwithautoregressiveblankinfilling. InProceedingsofthe60thAnnualMeeting
of the Association for Computational Linguistics (Volume 1: Long Papers), pages 320–335,
2022.
L.Gao,A.Madaan,S.Zhou,U.Alon,P.Liu,Y.Yang,J.Callan,andG.Neubig. PAL:program-
aided language models. In A. Krause, E. Brunskill, K. Cho, B. Engelhardt, S. Sabato, and
J. Scarlett, editors, International Conference on Machine Learning, ICML 2023, 23-29 July
2023, Honolulu, Hawaii, USA, volume 202 of Proceedings of Machine Learning Research,
pages10764–10799.PMLR,2023. URLhttps://proceedings.mlr.press/v202/gao23f.
html.
Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, M. Huang, N. Duan, and W. Chen. Tora: A tool-
integratedreasoningagentformathematicalproblemsolving. CoRR,abs/2309.17452,2023.
doi: 10.48550/ARXIV.2309.17452. URLhttps://doi.org/10.48550/arXiv.2309.1745
2.
D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. K. Li, F. Luo,
Y.Xiong,andW.Liang. Deepseek-coder: Whenthelargelanguagemodelmeetsprogramming
–theriseofcodeintelligence,2024.
D.Hendrycks,C.Burns,S.Basart,A.Zou,M.Mazeika,D.Song,andJ.Steinhardt. Measuring
massivemultitasklanguageunderstanding. arXivpreprintarXiv:2009.03300,2020.
D.Hendrycks,C.Burns,S.Kadavath,A.Arora,S.Basart,E.Tang,D.Song,andJ.Steinhardt.Mea-
suringmathematicalproblemsolvingwiththemathdataset. arXivpreprintarXiv:2103.03874,
2021.
High-flyer. Hai-llm: 高效且轻量的大模型训练工具,2023. URLhttps://www.high-flyer.c
n/en/blog/hai-llm.
InflectionAI. Inflection-2,2023. URLhttps://inflection.ai/inflection-2.
A.Q.Jiang,S.Welleck,J.P.Zhou,W.Li,J.Liu,M.Jamnik,T.Lacroix,Y.Wu,andG.Lample.Draft,
sketch, and prove: Guiding formal theorem provers with informal proofs. arXiv preprint
arXiv:2210.12283,2022.
A.Q.Jiang,A.Sablayrolles,A.Mensch,C.Bamford,D.S.Chaplot,D.d.l.Casas,F.Bressand,
G.Lengyel,G.Lample,L.Saulnier,etal. Mistral7b. arXivpreprintarXiv:2310.06825,2023.
A.Joulin,E.Grave,P.Bojanowski,M.Douze,H.Jégou,andT.Mikolov. Fasttext.zip: Compress-
ingtextclassificationmodels. arXivpreprintarXiv:1612.03651,2016.
W.Kwon,Z.Li,S.Zhuang,Y.Sheng,L.Zheng,C.H.Yu,J.E.Gonzalez,H.Zhang,andI.Stoica.
Efficient memory management for large language model serving with pagedattention. In
ProceedingsoftheACMSIGOPS29thSymposiumonOperatingSystemsPrinciples,2023.
Y. Leviathan, M. Kalman, and Y. Matias. Fast inference from transformers via speculative
decoding. In International Conference on Machine Learning, pages 19274–19286. PMLR,
2023.
A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone,
C. Anil, I. Schlag, T. Gutman-Solo, et al. Solving quantitative reasoning problems with
languagemodels. AdvancesinNeuralInformationProcessingSystems,35:3843–3857,2022a.

A.Lewkowycz,A.Andreassen,D.Dohan,E.Dyer,H.Michalewski,V.V.Ramasesh,A.Slone,
C.Anil,I.Schlag,T.Gutman-Solo,Y.Wu,B.Neyshabur,G.Gur-Ari,andV.Misra. Solving
quantitativereasoningproblemswithlanguagemodels.InS.Koyejo,S.Mohamed,A.Agarwal,
D.Belgrave,K.Cho,andA.Oh,editors,AdvancesinNeuralInformationProcessingSystems
35: AnnualConferenceonNeuralInformationProcessingSystems2022,NeurIPS2022,New
Orleans, LA, USA, November 28 - December 9, 2022, 2022b. URL http://papers.nips.
cc/paper_files/paper/2022/hash/18abbeef8cfe9203fdf9053c9c4fe191-Abstr
act-Conference.html.
H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman,
I.Sutskever,andK.Cobbe. Let’sverifystepbystep. arXivpreprintarXiv:2305.20050,2023.
I. Loshchilov and F. Hutter. Decoupled weight decay regularization. arXiv preprint
arXiv:1711.05101,2017.
H. Luo, Q. Sun, C. Xu, P. Zhao, J. Lou, C. Tao, X. Geng, Q. Lin, S. Chen, and D. Zhang.
Wizardmath: Empoweringmathematicalreasoningforlargelanguagemodelsviareinforced
evol-instruct. arXivpreprintarXiv:2308.09583,2023.
S.Mishra,M.Finlayson,P.Lu,L.Tang,S.Welleck,C.Baral,T.Rajpurohit,O.Tafjord,A.Sab-
harwal, P. Clark, and A. Kalyan. LILA: A unified benchmark for mathematical reasoning.
In Y. Goldberg, Z. Kozareva, and Y. Zhang, editors, Proceedings of the 2022 Conference on
EmpiricalMethodsinNaturalLanguageProcessing,EMNLP2022,AbuDhabi,UnitedArab
Emirates,December7-11,2022,pages5807–5832.AssociationforComputationalLinguistics,
## 2022. doi: 10.18653/V1/2022.EMNLP-MAIN.392. URLhttps://doi.org/10.18653/v1/
2022.emnlp-main.392.
X. Nguyen, W. Zhang, X. Li, M. M. Aljunied, Q. Tan, L. Cheng, G. Chen, Y. Deng, S. Yang,
C. Liu, H. Zhang, and L. Bing. Seallms - large language models for southeast asia. CoRR,
abs/2312.00738,2023. doi: 10.48550/ARXIV.2312.00738. URLhttps://doi.org/10.485
50/arXiv.2312.00738.
OpenAI. GPT4technicalreport. arXivpreprintarXiv:2303.08774,2023.
L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal,
K.Slama,A.Ray,etal. Traininglanguagemodelstofollowinstructionswithhumanfeedback.
AdvancesinNeuralInformationProcessingSystems,35:27730–27744,2022.
K.Paster,M.D.Santos,Z.Azerbayev,andJ.Ba. Openwebmath: Anopendatasetofhigh-quality
mathematicalwebtext. CoRR,abs/2310.06786,2023. doi: 10.48550/ARXIV.2310.06786. URL
https://doi.org/10.48550/arXiv.2310.06786.
L. C. Paulson. Three years of experience with sledgehammer, a practical link between auto-
matic and interactive theorem provers. In R. A. Schmidt, S. Schulz, and B. Konev, editors,
Proceedingsofthe2ndWorkshoponPracticalAspectsofAutomatedReasoning,PAAR-2010,
Edinburgh, Scotland, UK,July14, 2010, volume9ofEPiCSeriesinComputing, pages1–10.
EasyChair,2010. doi: 10.29007/TNFD. URLhttps://doi.org/10.29007/tnfd.
S.PoluandI.Sutskever. Generativelanguagemodelingforautomatedtheoremproving. CoRR,
abs/2009.03393,2020. URLhttps://arxiv.org/abs/2009.03393.
R.Rafailov,A.Sharma,E.Mitchell,S.Ermon,C.D.Manning,andC.Finn. Directpreference
optimization: Yourlanguagemodelissecretlyarewardmodel. 2023.

J.Schulman. Approximatingkldivergence,2020. URLhttp://joschu.net/blog/kl-app
rox.html.
J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel. High-dimensional continuous
controlusinggeneralizedadvantageestimation. arXivpreprintarXiv:1506.02438,2015.
J.Schulman,F.Wolski,P.Dhariwal,A.Radford,andO.Klimov. Proximalpolicyoptimization
algorithms. arXivpreprintarXiv:1707.06347,2017.
F.Shi,M.Suzgun,M.Freitag,X.Wang,S.Srivats,S.Vosoughi,H.W.Chung,Y.Tay,S.Ruder,
D.Zhou,D.Das,andJ.Wei. Languagemodelsaremultilingualchain-of-thoughtreasoners.
In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali,
Rwanda,May1-5,2023.OpenReview.net,2023. URLhttps://openreview.net/pdf?id=
fR3wGCk-IXp.
F.Song,B.Yu,M.Li,H.Yu,F.Huang,Y.Li,andH.Wang. Preferencerankingoptimizationfor
humanalignment. arXivpreprintarXiv:2306.17492,2023.
M.Suzgun,N.Scales,N.Schärli,S.Gehrmann,Y.Tay,H.W.Chung,A.Chowdhery,Q.V.Le,
E.H.Chi,D.Zhou,etal. Challengingbig-benchtasksandwhetherchain-of-thoughtcansolve
them. arXivpreprintarXiv:2210.09261,2022.
T.Tao. Embracingchangeandresettingexpectations,2023. URLhttps://unlocked.micro
soft.com/ai-anthology/terence-tao/.
H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra,
P.Bhargava,S.Bhosale,D.Bikel,L.Blecher,C.Canton-Ferrer,M.Chen,G.Cucurull,D.Esiobu,
J.Fernandes,J.Fu,W.Fu,B.Fuller,C.Gao,V.Goswami,N.Goyal,A.Hartshorn,S.Hosseini,
R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. Kloumann, A. Korenev, P. S. Koura,
M.Lachaux,T.Lavril,J.Lee,D.Liskovich,Y.Lu,Y.Mao,X.Martinet,T.Mihaylov,P.Mishra,
I.Molybog,Y.Nie,A.Poulton,J.Reizenstein,R.Rungta,K.Saladi,A.Schelten,R.Silva,E.M.
Smith,R.Subramanian,X.E.Tan,B.Tang,R.Taylor,A.Williams,J.X.Kuan,P.Xu,Z.Yan,
I.Zarov,Y.Zhang,A.Fan,M.Kambadur,S.Narang,A.Rodriguez,R.Stojnic,S.Edunov,and
T.Scialom. Llama2: Openfoundationandfine-tunedchatmodels. CoRR,abs/2307.09288,
## 2023. doi: 10.48550/arXiv.2307.09288. URLhttps://doi.org/10.48550/arXiv.2307.
09288.
T.H.Trinh,Y.Wu,Q.V.Le,H.He,andT.Luong. Solvingolympiadgeometrywithouthuman
demonstrations. Nature,625(7995):476–482,2024.
P.Wang,L.Li,L.Chen,F.Song,B.Lin,Y.Cao,T.Liu,andZ.Sui. Makinglargelanguagemodels
betterreasonerswithalignment. arXivpreprintarXiv:2309.02144,2023a.
P.Wang,L.Li,Z.Shao,R.Xu,D.Dai,Y.Li,D.Chen,Y.Wu,andZ.Sui. Math-shepherd: Verify
andreinforcellmsstep-by-stepwithouthumanannotations. CoRR,abs/2312.08935,2023b.
Z. Wang, R. Xia, and P. Liu. Generative AI for math: Part I - mathpile: A billion-token-scale
pretrainingcorpusformath. CoRR,abs/2312.17120,2023c. doi: 10.48550/ARXIV.2312.17120.
URLhttps://doi.org/10.48550/arXiv.2312.17120.
J.Wei,X.Wang,D.Schuurmans,M.Bosma,B.Ichter,F.Xia,E.H.Chi,Q.V.Le,andD.Zhou.
Chain-of-thoughtpromptingelicitsreasoninginlargelanguagemodels. InNeurIPS,2022.
URL http://papers.nips.cc/paper_files/paper/2022/hash/9d5609613524ecf
4f15af0f7b31abca4-Abstract-Conference.html.

T.Wei,J.Luan,W.Liu,S.Dong,andB.Wang. Cmath: Canyourlanguagemodelpasschinese
elementaryschoolmathtest?,2023.
M.Wenzel,L.C.Paulson,andT.Nipkow. Theisabelleframework. InO.A.Mohamed,C.A.
Muñoz, and S. Tahar, editors, Theorem Proving in Higher Order Logics, 21st International
Conference,TPHOLs2008,Montreal,Canada,August18-21,2008.Proceedings,volume5170
ofLectureNotesinComputerScience,pages33–38.Springer,2008. doi: 10.1007/978-3-540-7
1067-7\_7. URLhttps://doi.org/10.1007/978-3-540-71067-7_7.
H. Xia, T. Ge, P. Wang, S.-Q. Chen, F. Wei, and Z. Sui. Speculative decoding: Exploiting
speculativeexecutionforacceleratingseq2seqgeneration. InH.Bouamor,J.Pino,andK.Bali,
editors,FindingsoftheAssociationforComputationalLinguistics: EMNLP2023,pages3909–
3925,Singapore,Dec.2023.AssociationforComputationalLinguistics. doi: 10.18653/v1/20
23.findings-emnlp.257. URLhttps://aclanthology.org/2023.findings-emnlp.257.
H.Xia,Z.Yang,Q.Dong,P.Wang,Y.Li,T.Ge,T.Liu,W.Li,andZ.Sui. Unlockingefficiency
inlargelanguagemodelinference: Acomprehensivesurveyofspeculativedecoding. arXiv
preprintarXiv:2401.07851,2024.
S.Yao,D.Yu,J.Zhao,I.Shafran,T.L.Griffiths,Y.Cao,andK.Narasimhan. Treeofthoughts:
Deliberate problem solving with large language models. arXiv preprint arXiv:2305.10601,
2023.
L. Yu, W. Jiang, H. Shi, J. Yu, Z. Liu, Y. Zhang, J. T. Kwok, Z. Li, A. Weller, and W. Liu.
Metamath: Bootstrapyourownmathematicalquestionsforlargelanguagemodels. CoRR,
abs/2309.12284,2023. doi: 10.48550/ARXIV.2309.12284. URLhttps://doi.org/10.485
50/arXiv.2309.12284.
Z. Yuan, H. Yuan, C. Li, G. Dong, C. Tan, and C. Zhou. Scaling relationship on learning
mathematicalreasoningwithlargelanguagemodels. arXivpreprintarXiv:2308.01825,2023a.
Z. Yuan, H. Yuan, C. Tan, W. Wang, S. Huang, and F. Huang. Rrhf: Rank responses to align
languagemodelswithhumanfeedbackwithouttears. arXivpreprintarXiv:2304.05302,2023b.
X.Yue, X.Qu, G.Zhang, Y.Fu, W.Huang, H.Sun, Y.Su, andW.Chen. Mammoth: Building
mathgeneralistmodelsthroughhybridinstructiontuning. CoRR,abs/2309.05653,2023. doi:
10.48550/ARXIV.2309.05653. URLhttps://doi.org/10.48550/arXiv.2309.05653.
K.Zheng,J.M.Han,andS.Polu. Minif2f: across-systembenchmarkforformalolympiad-level
mathematics. arXivpreprintarXiv:2109.00110,2021.
W.Zhong,R.Cui,Y.Guo,Y.Liang,S.Lu,Y.Wang,A.Saied,W.Chen,andN.Duan. AGIEval: A
human-centricbenchmarkforevaluatingfoundationmodels. CoRR,abs/2304.06364,2023.
doi: 10.48550/arXiv.2304.06364. URLhttps://doi.org/10.48550/arXiv.2304.06364.

A. Appendix
A.1. AnalysisofReinforcementLearning
Weprovidethedetailedderivationofthedatasourceandgradientcoefficient(algorithmand
reward function) across various methods, including SFT, RFT, Online RFT, DPO, PPO, and
GRPO.
A.1.1. SupervisedFine-tuning
TheobjectiveofSupervisedFine-tuningismaximizingthefollowingobjective:
(cid:32) |𝑜| (cid:33)
1 ∑︁
J 𝑆𝐹𝑇 (𝜃) = E[𝑞,𝑜 ∼ 𝑃 𝑠𝑓𝑡 (𝑄,𝑂)] log𝜋 𝜃 (𝑜 𝑡 |𝑞,𝑜 <𝑡 ) . (6)
|𝑜|
𝑡=1
Thegradientof J 𝑆𝐹𝑇 (𝜃) is:
(cid:32) |𝑜| (cid:33)
1 ∑︁
∇ 𝜃 J 𝑆𝐹𝑇 = E[𝑞,𝑜 ∼ 𝑃 𝑠𝑓𝑡 (𝑄,𝑂)] ∇ 𝜃log𝜋 𝜃 (𝑜 𝑡 |𝑞,𝑜 <𝑡 ) . (7)
|𝑜|
𝑡=1
DataSource: ThedatasetemployedforSFT.RewardFunction: Thiscanberegardedashuman
selection. GradientCoefficient: alwayssetto1.
A.1.2. RejectionSamplingFine-tuning
RejectionSamplingFine-tuningfirstsamplesmultipleoutputsfromthesupervisedfine-tuned
LLMsforeachquestion,andthentrainsLLMsonthesampledoutputswiththecorrectanswer.
Formally,theobjectiveofRFTistomaximizethefollowingobjectives:
(cid:32) |𝑜| (cid:33)
1 ∑︁
J 𝑅𝐹𝑇 (𝜃) = E[𝑞 ∼ 𝑃 𝑠𝑓𝑡 (𝑄),𝑜 ∼ 𝜋 𝑠𝑓𝑡 (𝑂|𝑞)] I(𝑜)log𝜋 𝜃 (𝑜 𝑡 |𝑞,𝑜 <𝑡 ) . (8)
|𝑜|
𝑡=1
Thegradientof J 𝑅𝐹𝑇 (𝜃) is:
(cid:32) |𝑜| (cid:33)
1 ∑︁
∇ 𝜃 J 𝑅𝐹𝑇 (𝜃) = E[𝑞 ∼ 𝑃 𝑠𝑓𝑡 (𝑄),𝑜 ∼ 𝜋 𝑠𝑓𝑡 (𝑂|𝑞)] I(𝑜)∇ 𝜃log𝜋 𝜃 (𝑜 𝑡 |𝑞,𝑜 <𝑡 ) . (9)
|𝑜|
𝑡=1
DataSource: questioninSFTdatasetwithoutputssampledfromSFTmodel. RewardFunction:
Rule(whethertheansweriscorrectornot). GradientCoefficient:
(cid:40)
## 1 theanswerofoiscorrect
𝐺𝐶 𝑅𝐹𝑇 (𝑞,𝑜,𝑡) = I(𝑜) = (10)
## 0 theanswerofoisincorrect
A.1.3. OnlineRejectionSamplingFine-tuning
TheonlydifferencebetweenRFTandOnlineRFTisthattheoutputsofOnlineRFTaresampled
fromthereal-timepolicymodel𝜋 𝜃,ratherthanfromtheSFTmodel𝜋 𝜃 . Therefore,thegradient
𝑠𝑓𝑡
ofonlineRFTis:
(cid:32) |𝑜| (cid:33)
1 ∑︁
∇ 𝜃 J 𝑂𝑛𝑅𝐹𝑇 (𝜃) = E[𝑞 ∼ 𝑃 𝑠𝑓𝑡 (𝑄),𝑜 ∼ 𝜋 𝜃 (𝑂|𝑞)] I(𝑜)∇ 𝜃log𝜋 𝜃 (𝑜 𝑡 |𝑞,𝑜 <𝑡 ) . (11)
|𝑜|
𝑡=1

A.1.4. DirectPreferenceOptimization(DPO)
TheobjectiveofDPOis:
J𝐷𝑃𝑂(𝜃)=E[𝑞∼𝑃 𝑠𝑓𝑡(𝑄),𝑜+ ,𝑜− ∼𝜋 𝑠𝑓𝑡(𝑂|𝑞)]log𝜎(cid:169)
(cid:173)
𝛽
|𝑜
+|
∑︁ |
𝑡
𝑜
=
+
| log
𝜋
𝜋
r
𝜃
ef
(
(
𝑜
𝑜
+ 𝑡
+ 𝑡
|𝑞
|𝑞
,
,
𝑜
𝑜
+ <
+ <
𝑡
𝑡
)
)
−𝛽
|𝑜
−|
∑︁ |
𝑡
𝑜
=
−
| log
𝜋
𝜋
r
𝜃
ef
(
(
𝑜
𝑜
< −
< −
𝑡
𝑡
|𝑞
|𝑞
,
,
𝑜
𝑜
< −
< −
𝑡
𝑡
)
)
(cid:170)
(cid:174)
(12)
(cid:171) (cid:172)
Thegradientof J 𝐷𝑃𝑂 (𝜃) is:
|𝑜+|
∇𝜃J𝐷𝑃𝑂(𝜃)=E[𝑞∼𝑃 𝑠𝑓𝑡(𝑄),𝑜+ ,𝑜− ∼𝜋 𝑠𝑓𝑡(𝑂|𝑞)](cid:169)
(cid:173)|𝑜
+|
∑︁ 𝐺𝐶𝐷𝑃𝑂(𝑞,𝑜,𝑡)∇𝜃log𝜋 𝜃(𝑜+
𝑡
|𝑞,𝑜+
<𝑡
)
𝑡=1
(cid:171) (13)
|𝑜−|
−
|𝑜
−|
∑︁ 𝐺𝐶𝐷𝑃𝑂(𝑞,𝑜,𝑡)∇𝜃log𝜋 𝜃(𝑜
𝑡
−|𝑞,𝑜
<
−
𝑡
)(cid:170)
(cid:174)
𝑡=1
(cid:172)
DataSource: questioninSFTdatasetwithoutputssampledfromSFTmodel. RewardFunction:
human preference in the general domain (can be ‘Rule’ in mathematical tasks). Gradient
Coefficient:
𝐺𝐶𝐷𝑃𝑂(𝑞,𝑜,𝑡)=𝜎 (cid:18) 𝛽log
𝜋
𝜋
r
𝜃
ef
(
(
𝑜
𝑜
𝑡 −
𝑡 −
|𝑞
|𝑞
,
,
𝑜
𝑜
< −
< −
𝑡
𝑡
)
)
−𝛽log
𝜋
𝜋
r
𝜃
ef
(
(
𝑜
𝑜
+ 𝑡
+ 𝑡
|𝑞
|𝑞
,
,
𝑜
𝑜
+ <
+ <
𝑡
𝑡
)
)
(cid:19) (14)
A.1.5. ProximalPolicyOptimization(PPO)
TheobjectiveofPPOis:
J𝑃𝑃𝑂(𝜃)=E[𝑞∼𝑃 𝑠𝑓𝑡(𝑄),𝑜∼𝜋 𝜃𝑜𝑙𝑑 (𝑂|𝑞)] | 1 𝑜| ∑︁ 𝑡 | = 𝑜 1 | min (cid:20) 𝜋 𝜋 𝜃 𝜃 𝑜𝑙𝑑 (𝑜 (𝑜 𝑡| 𝑡 𝑞 |𝑞 , , 𝑜 𝑜 < < 𝑡) 𝑡) 𝐴𝑡,clip (cid:18) 𝜋 𝜋 𝜃 𝜃 𝑜𝑙𝑑 (𝑜 (𝑜 𝑡| 𝑡 𝑞 |𝑞 , , 𝑜 𝑜 < < 𝑡) 𝑡) ,1−𝜀,1+𝜀 (cid:19) 𝐴𝑡 (cid:21) . (15)
Tosimplifytheanalysis,itisassumedthatthemodelonlyhasasingleupdatefollowingeach
explorationstage,therebyensuringthat𝜋 𝜃 = 𝜋 𝜃. Inthiscase,wecanremovetheminandclip
𝑜𝑙𝑑
operation:
|𝑜|
J𝑃𝑃𝑂(𝜃)=E[𝑞∼𝑃 𝑠𝑓𝑡(𝑄),𝑜∼𝜋 𝜃𝑜𝑙𝑑 (𝑂|𝑞)] | 1 𝑜| ∑︁ 𝑡=1 𝜋 𝜋 𝜃 𝜃 𝑜𝑙𝑑 (𝑜 (𝑜 𝑡| 𝑡 𝑞 |𝑞 , , 𝑜 𝑜 < < 𝑡) 𝑡) 𝐴𝑡. (16)
Thegradientof J 𝑃𝑃𝑂 (𝜃) is:
|𝑜|
1 ∑︁
∇𝜃J𝑃𝑃𝑂(𝜃)=E[𝑞∼𝑃 𝑠𝑓𝑡(𝑄),𝑜∼𝜋 𝜃𝑜𝑙𝑑 (𝑂|𝑞)] |𝑜| 𝐴𝑡∇𝜃log𝜋 𝜃(𝑜𝑡|𝑞,𝑜<𝑡) (17)
𝑡=1
DataSource: questioninSFTdatasetwithoutputssampledfrompolicymodel. RewardFunction:
rewardmodel. GradientCoefficient:
𝐺𝐶 𝑃𝑃𝑂 (𝑞,𝑜,𝑡,𝜋 𝜃𝑟𝑚 ) = 𝐴 𝑡, (18)
where 𝐴 𝑡 istheadvantage,whichiscomputedbyapplyingGeneralizedAdvantageEstimation
(GAE)(Schulmanetal.,2015),basedontherewards{𝑟 ≥𝑡 } andalearnedvaluefunction𝑉 𝜓.
A.1.6. GroupRelativePolicyOptimization(GRPO)
TheobjectiveofGRPOis(assume𝜋 𝜃 = 𝜋 𝜃 forsimplifiedanalysis):
𝑜𝑙𝑑
J𝐺𝑅𝑃𝑂(𝜃)=E[𝑞∼𝑃 𝑠𝑓𝑡(𝑄),{𝑜 𝑖}𝐺
𝑖=1
∼𝜋
𝜃𝑜𝑙𝑑
(𝑂|𝑞)]
𝐺
1 ∑︁
𝑖=
𝐺
1 |𝑜
𝑖|
∑︁
𝑡
|
=
𝑜𝑖
| (cid:20)
𝜋
𝜋
𝜃
𝜃
𝑜𝑙𝑑
(𝑜
(𝑜
𝑖,
𝑖
𝑡
,
|
𝑡
𝑞
|𝑞
,
,
𝑜
𝑜
𝑖,
𝑖
<
,<
𝑡)
𝑡)
𝐴ˆ𝑖,𝑡−𝛽(
𝜋
𝜋
𝑟
𝜃
𝑒𝑓
(
(
𝑜
𝑜
𝑖,
𝑖
𝑡
,𝑡
|𝑞
|𝑞
,
,
𝑜
𝑜
𝑖,
𝑖
<
,<
𝑡
𝑡
)
)
−log
𝜋
𝜋
𝑟
𝜃
𝑒𝑓
(
(
𝑜
𝑜
𝑖,
𝑖
𝑡
,𝑡
|𝑞
|𝑞
,
,
𝑜
𝑜
𝑖,
𝑖
<
,<
𝑡
𝑡
)
)
−1)
(cid:21)
.
(19)

Thegradientof J 𝐺𝑅𝑃𝑂 (𝜃) is:
∇𝜃J𝐺𝑅𝑃𝑂(𝜃)=E[𝑞∼𝑃 𝑠𝑓𝑡(𝑄),{𝑜 𝑖}𝐺
𝑖=1
∼𝜋
𝜃𝑜𝑙𝑑
(𝑂|𝑞)]
𝐺
1 ∑︁
𝑖=
𝐺
|𝑜
𝑖|
∑︁
𝑡
|
=
𝑜𝑖
| (cid:20)
𝐴ˆ𝑖,𝑡+𝛽
(cid:18)𝜋
𝜋
𝑟
𝜃
𝑒𝑓
(
(
𝑜
𝑜
𝑖,
𝑖
𝑡
,𝑡
|𝑜
|𝑜
𝑖,
𝑖
<
,<
𝑡
𝑡
)
)
−1
(cid:19)(cid:21)
∇𝜃log𝜋 𝜃(𝑜 𝑖,𝑡|𝑞,𝑜 𝑖,<𝑡).
(20)
DataSource: questioninSFTdatasetwithoutputssampledfrompolicymodel. RewardFunction:
rewardmodel. GradientCoefficient:
𝐺𝐶𝐺𝑅𝑃𝑂(𝑞,𝑜,𝑡,𝜋 𝜃𝑟𝑚 )= 𝐴ˆ𝑖,𝑡+𝛽
(cid:18)𝜋
𝜋
𝑟
𝜃
𝑒𝑓
(
(
𝑜
𝑜
𝑖,
𝑖
𝑡
,𝑡
|𝑜
|𝑜
𝑖,
𝑖
<
,<
𝑡
𝑡
)
)
−1
(cid:19)
, (21)
where 𝐴ˆ 𝑖,𝑡 iscomputedbasedonthegrouprewardscores.

## My Notes
- 
- 
- 
- 
-