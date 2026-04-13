---
paper_id: 2026_step_3_5_flash_open_frontier_level_intelligence_with_11b_active_parameters
topic_tags: [training_infra, moe_systems, distributed_training, rl_post_training, agentic_llms]
source_url: "https://arxiv.org/abs/2602.10604"
---

Step 3.5 Flash: Open Frontier-Level Intelligence
with 11B Active Parameters
StepFunTeam
GitHub HuggingFace ModelBlog
## Abstract
WeintroduceStep3.5Flash,asparseMixture-of-Experts(MoE)modelthatbridgesthegapbetween
frontier-level agentic intelligence and computational efficiency. We focus on what matters most
when building agents: reasoning that’s sharp, and execution that’s fast and reliable. Reflecting
thesepriorities,Step3.5Flashpairsa196B-parameterfoundationforhigh-fidelitymodelingwith
11B active parameters for efficient inference, optimized by interleaved 3:1 Sliding Window/Full
Attention and Multi-Token Prediction (MTP-3) to minimize the latency and cost of multi-round
agentic interactions. Toward frontier-level intelligence, we design a scalable RL framework that
integratesverifiablesignalsandpreferencefeedbackwhilemaintainingstabilityduringlarge-scale
off-policytrainingtodriveconsistentself-improvementacrossmathematics,code,andtooluse. Step
3.5Flashdemonstratesstrongintelligenceacrossagent,coding,andmathtasks,achieving85.4%on
IMO-AnswerBenchand86.4%onLiveCodeBench-v6(2024.08–2025.05),88.2%on𝜏2-Bench,69.0%on
BrowseComp(w. ContextManage),and51.0%onTerminal-Bench2.0—performanceonparwith
frontier models such as GPT-5.2 xHigh and Gemini 3.0 Pro. By redefining the efficiency frontier,
Step3.5Flashprovidesahigh-densityfoundationfordeployingsophisticatedagentsinreal-world
industrialenvironments.
ŗŖŖ
ŞŖ
ŜŖ
ŚŖ
ŘŖ
Ŗ

ȱŘŖŘś 
Ȭ  2Ȭ Ȭ   Ȭ
  Ŝ  ǻ ǯȱ¡ȱǼ ȱŘǯŖ
ǼƖǻȱ¢
ȱřǯśȱ ȱřǯŘ 	ȱřǯŖȱ ȱȱŚǯś 	ȬśǯŘȱ¡

ŗŖŖǯŖ
şŝǯř
şśǯŖ
şřǯŗ şŘǯŞ şŘǯś
şŖǯŝ şŖǯŝ
ŞśǯŚ ŞřǯřŞŚǯŖ ŞŜǯř ŞŜǯŚ Şřǯř ŞŚǯŞ Şŝǯŝ ŞŞǯŘ ŞśǯŘ Şśǯś
ŞŖǯşŞŖǯŖ
ŝŞǯř
ŝŚǯŚ ŝŜǯŘ
ŝřǯŗ
ŜşǯŖ
ŜŝǯŜ
ŜśǯŞ
śşǯŘśŝǯŞ
śŜǯş
śşǯř
śŚǯŖ
śŗǯŖ
ŚŜǯŚ
ȱ ȱ
Figure 1: Step 3.5 Flash achieves frontier-level intelligence with only 11B active parameters (196B
MoE),comparabletoleadingclosedandopen-sourcemodels.
beF
]LC.sc[
2v40601.2062:viXra

Contents
## 1 Introduction 4
## 2 Architecture 5
2.1 DesignPhilosophy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5
## 2.2 SparseMoEBackbonewithHybridAttention . . . . . . . . . . . . . . . . . . . . . . . . 6
## 2.3 ArchitectureAblationsandResults . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
## 3 Infrastructure 9
3.1 ComputeCluster . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
## 3.2 TrainingFramework . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
## 3.3 High-ThroughputLightweightMonitoring . . . . . . . . . . . . . . . . . . . . . . . . . 10
## 4 Pre-TrainingandMid-Training 10
4.1 TrainingStability . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
## 4.1.1 NumericalSensitivityofMuon . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
## 4.1.2 ExpertCollapseBeyondRoutingCollapse . . . . . . . . . . . . . . . . . . . . . 12
## 4.1.3 LocalizedActivationBlow-upinMoELayers . . . . . . . . . . . . . . . . . . . . 12
4.2 TrainingCurriculum . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
## 4.2.1 DataMixture . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
## 4.2.2 Schedule . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
## 4.2.3 Hyper-Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15
## 5 Post-Training 15
## 5.1 ExpertModelConstructionandSelf-Distillation . . . . . . . . . . . . . . . . . . . . . . 15
5.2 ScalableRL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
## 5.2.1 MIS-FilteredPolicyOptimization(MIS-PO) . . . . . . . . . . . . . . . . . . . . . 16
## 5.2.2 RewardSystem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
## 5.2.3 Hyper-Parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
## 5.3 DataSynthesis&Curation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
## 5.3.1 GeneralandReasoning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
## 5.3.2 GeneralizedToolLearning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
## 5.3.3 CodeAgents. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20

## 5.3.4 SearchandResearchAgents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20
5.4 AgentInfrastructure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
## 6 Evaluations 21
6.1 Pre-trainingEvaluations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
6.2 Post-trainingEvaluations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
## 7 Limitations 23
A ArchitectureDetails 27
A.1 Head-wiseGatedAttention . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
A.2 SpeedBenchmarkofAttentionEnhancements . . . . . . . . . . . . . . . . . . . . . . . 28
A.3 MetaToken. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
A.4 Pre-trainingAblationsDetails . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
B DetailAnalysisofLocalizedActivationBlow-up 30
C StepPre-trainingDataFoundation 32
C.1 KnowledgeDataConstruction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
C.2 CodeData . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
C.3 Mathematics&STEMData . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
C.4 DataInfrastructure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
C.5 DataAblationsSetting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
D PostTrainingDetails 35
D.1 SFTDetails . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
D.2 RLDetailsandAblations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36
D.3 Tool-integratedReasoningandParallelReasoning . . . . . . . . . . . . . . . . . . . . . 39
E DetailedEvaluationProtocolsandPrompts 40
E.1 EvaluationDetailsofPre-trainedModels . . . . . . . . . . . . . . . . . . . . . . . . . . 40
E.2 EvaluationDetailsofPost-TrainedModels. . . . . . . . . . . . . . . . . . . . . . . . . . 45
E.3 InternalEvaluation-BenchmarksandMethodology . . . . . . . . . . . . . . . . . . . . 52

## 1. Introduction
Whileopen-sourcelargelanguagemodels(LLMs)[1–6]haverapidlynarrowedtheperformancegap
withclosed-sourcefrontiersystems[7–9]acrossverifiabletasks[10–12],newchallengesemergeas
agenticsystemsgainprominence. Inparticular,open-sourcemodelsstilltrailclosed-sourcefrontiersin
complexreasoning. Furthermore,criticalefficiencybottleneckshindertheirapplicationinlong-context
agentictasks[13–21],letalonedeploymentinedgeorresource-constrainedsettings.
IndesigningthearchitectureofStep3.5Flash,wefocusontwocoreaspects: efficiencyandcapacity.
We adopt a sparse Mixture-of-Experts (MoE) [22–26] architecture with 196B total parameters and
only11Bactivatedpertoken,togetherwitha3:1ratioofsliding-windowattention(SWA)[27]tofull
attentionandmulti-tokenprediction(MTP-3)[3,28–30]toreducelong-contextlatency. Toimprove
capacityunderhybridattentionwithminimaloverhead,weincreasethenumberofqueryheadsin
sliding-windowattention(SWA)layersfrom64to96andusehead-wisegatedattention[31]. This
designenableslarge-scaleonlinedeployment,sustaining∼170tokens/sonHopperGPUsduringthe
firstweekonOpenRouter1.
On the pretraining side, we treat stability as a first-class requirement and build a comprehensive
observabilityanddiagnosticstackviaalightweightasynchronousmetricsserverwithmicro-batch-
level continuous logging. This infrastructure enables systematic identification and mitigation of
large-scale MoE failure modes (e.g., Muon-related precision sensitivity, expert collapse [32], and
activation blow-ups [5,33]). Combined with an improved Muon optimizer [34] that offers more
accurateandstableupdates,weachievestabletrainingover17.2Thigh-qualityanddiversetokens
withonlyasingletransientlossspike. Withthisstabletrainingregime,Step3.5FlashBaseachieves
competitiveperformanceagainstlargercounterparts,suchasDeepSeek-V3.2-ExpBase[1]andKimi-
K2-Base[5],onmath,codingandknowledgebenchmarks. Notably,onSimpleQA[35],itscores31.6%,
surpassingDeepSeek-V3.2-ExpBasedespiteusingonlyone-thirdoftheparameters.
Towardfrontier-levelintelligence,currentpost-trainingsystemsfacetwotightlycoupledchallenges:
inefficient iteration of domain-specific experts for self-distillation [1–4] and limited scalability of
ReinforcementLearning(RL)tolong-horizonreasoningforMoEmodels. Trainingasinglegeneralist
to directly cover diverse domains often sacrifices domain-specific expertise, whereas maintaining
separateexpertmodelsleadstofragmentationandanunsustainablecostofcontinualmulti-model
iteration. At the same time, as models are extended to deeper reasoning trajectories, even small
token-level discrepancies in off-policy rollouts can accumulate into high-variance gradients. This
effectisparticularlysevereinMoEmodels,whereexpert-levelroutinginduceslargerdistributional
shiftsanddestabilizesoptimizationinthefrontierperformanceregime[1,36–38].
Toaddressthesechallenges,weproposeaunifiedpost-trainingrecipeforlarge-scaleRLbuiltona
sharedSFTfoundation. Theframeworkalternatesbetweendomain-specificspecializationandglobal
synthesis,enablingefficientexpertiterationwhilemaintainingasingle,high-performinggeneralist. A
dedicatedmid-trainingphasescalesthecontextwindowto128kandstrengthenscoreagenticandrea-
soningcapabilitiesviasyntheticdata,providingastronginitializationfordownstreampost-training.
TosupportstableandscalableRLwithinthisunifiedframework,weintroduceMetropolisIndepen-
dence Sampling-Filtered Policy Optimization (MIS-PO) [39,40], replacing continuous importance
weighting with discrete, distributional filtering at both token and trajectory levels. By restricting
optimizationtosampleswithinastabletrustregion,MIS-POsubstantiallyreducesgradientvariance
whilepreservingeffectivelearningsignals,enablingRLtoscalereliablytolong-horizonreasoning
andagenticbehaviors.
1https://openrouter.ai

Step3.5Flashachievescompetitiveperformancewithleadingfrontiermodelsandsystemsacrossa
broadrangeofreasoningandagenticbenchmarks,despite11Bactiveparameters. Itdeliversstrong
resultsunderstandardinferenceonreasoningtasks,including85.4%onIMO-AnswerBench[41]and
86.4%onLiveCodeBench-v6(2024.08–2025.05)[12],whilealsodemonstratingrobustlong-horizon,
tool-augmented capabilities with 88.2% on 𝜏2-Bench [15], 69.0% on BrowseComp (with context
management) [17], and 51.0% on Terminal-Bench 2.0 [16]. With PaCoRe [42] deep think inference,
Step3.5Flashfurtherimprovesperformanceonreasoning-intensivebenchmarksrequiringextended
deliberation and multi-round synthesis. Taken together, these results indicate that Step 3.5 Flash
substantiallynarrowsthegapbetweenadvancedopenmodelsandfrontierproprietarysystemsin
bothreasoningandagenticsettings.
## 2. Architecture
## 2.1. DesignPhilosophy
ThearchitectureofStep3.5Flashreflectsaparadigmshiftinmodel–systemco-design. Beyondthe
traditionalobjectivesofintelligenceandcost,theeraofautonomousagentselevatesathirdcritical
constraint: inferencelatency. Ininteractiveagenticworkflows[43,44],minimizedlatencytranslates
directlytoreducedwall-clocktimefortaskcompletion,orconversely,allowsforincreasedintelligence
withinafixedtimebudgetviatest-timescaling[42,45–47].
Agenticworkloadstypicallyexhibitadistinctprofile: extensivecontextprefillingfollowedbypro-
longed,multi-turninteractivedecoding. Accordingly,weco-designStep3.5Flashforlowwall-clock
latencyalongthreecoupledaxes: attention(toacceleratelong-contextprocessingandhavegoodaffin-
itywithMTP),sparseMoE(topreventstragglersindistributeddeploymentsthatreducethroughput),
andmulti-tokenprediction(MTP;tofacilitatefastgenerationthroughspeculativedecoding).
Attention. To accelerate prefilling, we employ a hybrid attention mechanism [33,48,49] to miti-
gatethequadraticcomplexityoflong-contextprocessing. Fordecoding,weprioritizearchitectural
compatibilitywithspeculativedecoding[50],sinceverificationefficiencyisthedominantleveron
bandwidth-boundhardware. Theseconsiderationsmotivatetwoattentiondesigndecisions:
• Sliding-WindowAttention(SWA).WeselectSWA[27]overlinearattention[10,51]tomaximize
decodingefficiency. Althoughbothhavelinearcomplexity,thestate-updatemechanismoflinear
attention complicates efficient draft tree generation and parallel tree verification needed for
speculative decoding [52–54]. In contrast, SWA preserves standard attention semantics and
remainsinherentlyamenabletoparallelverificationvia 𝐾𝑉 masking. Moreover,intheabsenceof
robustempiricalevidencethatlinearattentionyieldssuperiorlong-contextmodelingforagentic
tasks,wefindthatSWAwithwindowsize𝑊=512strikesafavorablebalancebetweenkernel
efficiencyandcapturinglocaldependencies.
• Hardware-Aligned Grouped-Query Attention (GQA-8). Targeting deployment on standard
8-GPUservernodes,weconfigurethemodelwitheight 𝐾𝑉 heads(GQA-8)[55]. Thisaligns 𝐾𝑉-
cacheshardingwith8-waytensorparallelismandimprovesmemoryaccesspatterns. Crucially,
whileGQA-8makesattentionmorememory-bandwidthbound,italsocreatescomputational
slackthatcanabsorbspeculativedraftingandverificationoverhead,enablingaggressivemulti-
tokenspeculationwithoutaproportionallatencypenalty.
SparseMoE. Onthefeed-forwardside,weemployfine-grainedMoE[22–26]toreducetheaverage
FFNcomputewhilemaintainingcapacity. Expertparallelism(EP)[25]isutilizedtoenablescalable

𝑥 𝑥 𝑥
! !$# !$%
LM Head MTP head 1 MTP head 2
Enable only during the
final post-training stage
Main Stream MTP module 1 MTP module 2
Gated FullAttn
Gated SWA Gated SWA
Block
Block Block
. . .
𝐿x
SSSF Block Linear Linear
SSSF Block
x L
Ga x te L d SWA concatenation concatenation
Block x 3
H-Norm E-Norm H-Norm E-Norm
Embedding Embedding(Shared) Embedding(Shared)
𝑥 𝑥 𝑥
!"# ! !$#
Figure2: IllustrationofStep3.5Flash. Themodeluseshead-wisegatedattention[31]withaleading
FullAttentionlayerfollowedby 𝐿 =11HybridBlocks,eachinterleaving3SlidingWindowAttention
(SWA)layerswithoneFullAttentionlayer(forvisualclarity,thefirstlayerisomittedinthefigure). We
applyzero-centeredRMSNorm[57]throughout. ThefirstthreeblocksusedenseFFNs;laterblocks
employsparseMoEFFNs. MTPmodulesuseSWAanddenseFFNs. Tolimitoverhead,onlyMTP
module1istrainedduringmaintraining;MTPmodules2–3areclonedfromitandjointlyfine-tuned
inalightweightfinalphase.
deployment. However, under EP, end-to-end latency can be dominated by stragglers induced by
routingimbalance: tokenassignmentskewconcentratesworkloadonasmallsubsetofexpertsand
their hosting GPUs, throttling throughput at synchronization points. We therefore introduce an
EP-GroupBalancedMoERoutingstrategy.
Multi-Token Prediction (MTP). To further reduce autoregressive latency, we incorporate Multi-
Token Prediction (MTP) [29,56] as a complementary lever to speculative decoding [50]. To keep
speculationlightweight,westreamlinetheMTPheadsbyleveragingSWAanddenseFFNs[3].
Wefurtherconstrainthemodelsizetounder200Bparameters,enablinghigh-performanceinference
withinthe128GBmemorybudgetofhigh-endworkstations.
## 2.2. SparseMoEBackbonewithHybridAttention
AsillustratedinFigure2,Step3.5Flashadoptsa45-layersparse-MoETransformerbackbone(3dense
layersand42MoElayers)pairedwithaspecializedhybridattentionlayerlayout. EachMoElayer
contains 288 routed experts plus one shared expert, with a top-𝑘 router activating 𝑘=8 experts per
token. Thisconfigurationmaintainsanextensiveknowledgecapacity(196Btotalparameters)while
restrictingper-tokenactivationtojust11B,ensuringinferencelatencyremainslowenoughforhighly

responsiveagentinteraction. Table6summarizeskeyarchitecturehyperparametersofStep3.5Flash.
HybridAttentionLayerLayout. Tobalancelong-contextefficiencywithrobustlong-rangeconnec-
tivity, Step 3.5 Flash leverages an interleaved attention layout at a 3 : 1 ratio (SWA : Full) inspired
by[33,49,58],denotedas𝑆3𝐹1. Thisconfigurationrepeatsafour-layermotifconsistingofthreeSWA
layers(𝑊=512)followedbyasinglefullGQA-8layer. However,inourinitialexperiments,anaive
interleavingstrategyconsistentlyunderperformsadenseattentionbaselineacrossvariousbenchmarks
(Table 10). To bridge this performance gap without adding practical overheads, we leverage two
complementaryenhancements: (i)anincreasedSWAquery-headcount,and(ii)adoptinghead-wise
gatedattention[31].
AugmentedQueryHeadsinSWA. Usingahigherquery-headnumber(from64to96)effectively
mitigates performance drop typically observed when transitioning from a uniform full-attention
architecture to the𝑆3𝐹1 layout (Table 10). We consider this to be nearly a “free lunch”. Because in
long-text scenarios, the overhead of naive SWA is very small, even though our solution scales up
significantly.
Head-wiseGatedAttention. AlimitationofnaiveSWAisitsinabilitytoeffectivelyabsorbunused
attention weights when there is no useful information in the input window [31,59–61]. Previous
work [3,33] introduce learnable, data-independent sink tokens into the window to address this
issue. Instead,weoptforadifferentapproachbyintegratingaparameter-efficienthead-wisegating
mechanism[31,62,63],whichcanbeviewedasintegratingdata-dependentsinktokens. Pleasereferto
AppendixA.1forimplementationdetailsandfurtherdiscussion. Head-wisegatingisalsonegligible
toboththeoreticalFLOPsandpracticallatency. Wereportmoreperformanceanalysisandbenchmarks
forgatingandaugmentingthenumberofSWAheadsinAppendixA.2.
MoEExpert-parallelLoadBalancing. Weuseloss-freeload-balancing[29,64]toencourageglobal
tokenbalanceacrossexperts. However,thisapproachdoesnotguaranteebalancedloadsacrossEP
ranksatthemicro-batchlevel,potentiallyleadingtostragglersandreducedthroughput. Wetherefore
introduceanEP-levelbalancinglossthatexplicitlypromotesuniformrank-levelutilization[26].
EPpartitionsexpertsE into𝐺 disjointgroups {E 𝑔 }𝐺 𝑔=1 acrossranks. Fortoken𝑡,let𝑆 𝑡 denotethetop-𝐾
experts(mask𝑠 𝑡,𝑒 =1[𝑒 ∈ 𝑆 𝑡 ])and 𝑝 𝑡,· theroutingprobabilities. Then,theEPloadbalancinglossL 𝐸𝑃 is:
𝑇 𝑇 𝐺
1 ∑︁ 1 ∑︁ ∑︁ ∑︁ ∑︁
𝑝 𝑒 = 𝑇 𝑝 𝑡,𝑒, 𝑓 𝑒 = 𝑇𝐾 𝑠 𝑡,𝑒, 𝑝 𝑔 = 𝑝 𝑒, 𝑓 𝑔 = 𝑓 𝑒, L EP =𝐺 𝑓 𝑔 𝑝 𝑔. (1)
𝑡=1 𝑡=1 𝑒∈E𝑔 𝑒∈E𝑔 𝑔=1
Multi-tokenPrediction(MTP). Tospeedupspeculativedecodingonlong-contextagenticworkloads,
weattachthreelightweightmulti-tokenprediction(MTP)heads. EachMTPheadconsistsofaSWA
andadenseFFN,addingonly0.81Bparameters(∼0.41%). Weindextheseheadsbytheiradditional
prediction offset beyond the standard LM head: for ℎ ∈ {1,2,3}, MTP-ℎ predicts the token 𝑥 𝑡+1+ℎ
conditionedonthebackbonehiddenstatesatposition𝑡. Tocontroltrainingoverhead,weactivateand
optimizeonlyMTP-1inmosttrainingstages. Oncethebackboneiswell-trained,weinitializeMTP-2
andMTP-3fromMTP-1andjointlytrainallMTPheadsinalightweightpost-trainingphase. Inspired
byFast-MTP[65], weadoptposition-dependentlossreweightingacrosspredictionoffsetsinMTP
headstopreventover-optimizingfordistant-tokenpredictions.

SWA Rel.FLOPs Pre-train DownstreamPerformance
Layout
Heads Avg.
Decode/Prefill Reasoning Math Code Sci General LongCtx Avg.
𝐹𝐹𝐹𝐹 32 ∼2.68/2.90 54.1 40.8 40.9 19.6 42.7 26.5 28.8 33.2
𝑆1𝐹1 32 ∼1.58/1.65 54.6 42.1 42.3 19.3 44.5 26.8 29.6 34.1
𝑆3𝐹1 32 1.00/1.00 53.6 40.2 40.4 18.9 42.4 25.4 27.5 32.5
𝑆3𝐹1 +Head 48 ∼1.01/1.02 55.7 40.6 40.3 18.3 44.0 26.0 28.2 32.9
Table1: Downstreamresultson30B-A3B. 𝐹 denotesfullattentionand𝑆denotesSWA.𝑆3𝐹1indicates
three𝑆 layersfollowedbyone 𝐹 layerinthehybridlayout. Rel. FLOPsarenormalizedtothe𝑆3𝐹1
configurationandaveragedover64k/256kcontexts(Table8). Pre-trainAvg. aggregatesresultsacross
general,math,andcodebenchmarks(Table16).
## 2.3. ArchitectureAblationsandResults
We conduct extensive experiments to validate key design choices in Step 3.5 Flash, focusing on (i)
attention layouts, including SWA and head scaling, and (ii) head-wise gated attention versus sink
tokens. To ensure our efficiency optimizations do not degrade model performance, we adopt two
complementaryablationprotocols: oneevaluatesfullend-to-endpipelinescoveringpre-training,32k
long-context extension, and 64k context-length supervised fine-tuning (SFT), and the other scales
theanalysisupto100Bparameterstostudyhowthesedesignchoicesbehavewithscale. Detailed
architectureandevaluationsetupsforalltablesareprovidedinAppendixA.4. Keyfindingsfrom
theselarge-scaleexperimentsaresummarizedbelow.
SWAw.r.t. LongContext. Wetraina30B-A3Bmodelthroughthefullpipeline(1.4T-tokenpretraining
followedbySFT)toevaluatetheend-to-endimpactofhybridattentiononreasoningandlong-context
performance. Weablatefourattentionlayouts: all-fullattention(𝐹𝐹𝐹𝐹),alternatingSWA/full(𝑆1𝐹1),
a3:1SWA-to-fulllayout(𝑆3𝐹1),andan𝑆3𝐹1variantwithincreasedSWAqueryheads(𝑆3𝐹1 +Head ).
To isolate attention-structure effects, we fix the SWA window size to𝑊=512 and disable MTP (see
Appendix,Table9andTable10).
Table 1 shows a clear cost–quality trade-off across layouts. 𝑆3𝐹1 achieves the lowest normalized
attention-sideFLOPs(normalizedto1.00forprefilland1.00fordecodeseparately),whereas 𝐹𝐹𝐹𝐹
is∼2.68×/2.90×asexpensiveas𝑆3𝐹1;however,𝑆3𝐹1exhibitsaconsistentqualitydegradation(e.g.,
LongCtxdropsfrom28.8to27.5).
IncreasingthenumberofSWAqueryheadslargelycompensatesforthisloss. Notably,𝑆3𝐹1 +Head
alreadysurpasses 𝐹𝐹𝐹𝐹 duringpretraining(55.7vs.54.1),andremainscompetitiveafterpost-training:
LongCtx improves from 27.5 to 28.2 and Sci from 42.4 to 44.0, closing most of the gap to the 𝐹𝐹𝐹𝐹
baselinewithnegligibleadditionalattentioncost. Theremainingdownsideislimitedandlocalized
(e.g.,amodestdroponCodeto18.3),whileoverallqualitytrendsfavor𝑆3𝐹1 +Head .
Interestingly, the alternating 𝑆1𝐹1 layout delivers the best overall SFT quality and the strongest
LongCtxscore(29.6),butrequiressubstantiallyhigherattention-sideprefill/decodeFLOPs(∼1.58/1.65),
abouta60%costincreaserelativeto𝑆3𝐹1 +Head . Wethereforeadopt𝑆3𝐹1 +Head asthedefaultcon-
figurationforlong-contextagenticworkloads,prioritizingitsmuchlowerprefill/decodecostwith
strongandstablelong-contextperformance.
Head-wise Gated Attention vs. Sink Tokens. We conduct scaled, controlled pretraining experi-
mentsona100B-A10BMoEtostudyattention-sidemechanismsunderrealisticscalingconditions.

Method BBH MMLU GPQA MBPP C-EVAL CMMLU Avg.
SinkToken 70.6 65.1 27.2 61.2 76.2 74.6 62.5
Head-wiseGate 73.7 67.0 28.1 62.6 77.9 77.1 64.4
Table2: Pretraining-onlyevaluationona100B-A10Bmodelunderthe𝑆3𝐹1layout. Head-wisegating
consistentlyoutperformsafixedsinktokenacrossbenchmarks,includingtheoverallaverage.
Specifically,wecomparesinktokensandhead-wisegatedattentionwhileholdingtheattentionlayout
fixed to the same 𝑆3𝐹1 configuration with window size 𝑊=512. As shown in Table 2, head-wise
gatingconsistentlyimprovesquality,raisingtheaverageperformancefrom62.46to64.43(+1.97). We
thereforeadopthead-wisegatedattentionasthedefaultmechanisminsubsequentstudies.
## 3. Infrastructure
## 3.1. ComputeCluster
Step3.5Flashistrainedonalarge-scaleclusterwith4,096NVIDIAH800GPUs. Eachnodecontains8
GPUsinterconnectedthroughNVLinkandNVSwitchforhigh-bandwidthintra-nodecommunica-
tion. Forinter-nodeconnectivity, theclusterrelieson8×200GbpsRoCElinkstomaintainefficient
synchronizationanddataexchangeatscale.
## 3.2. TrainingFramework
The training of Step 3.5 Flash is powered by our internal Steptron framework, a lightweight high-
performance system built on top of PyTorch [66] and Megatron-LM [67]. Steptron unifies the full
modeldevelopmentpipeline,supportinglarge-scalepre-training,post-training,andreinforcement
learning(RL)workloadsunderasingleengineeringstack.
Step3.5Flashemploysahybridparallelizationstrategy,including8-waypipelineparallelism(PP)[68]
withvirtualpipelinestages(VPP),and8-wayexpertparallelism(EP)[25],andZeRO-1DataParallelism
(DP)[69]. InordertofacilitateefficienttrainingofStep3.5Flash,weemploythefollowingengineering
techniques.
DecoupledParallelism. FollowingMegatron-Core[70],weimplementadecoupledparallelization
scheme that allows the attention and MoE modules to use different parallelization strategies. We
assignthemindependentparallelgroupsandperformgradientreductionandscalingwithineach
module’scorrespondingdata-parallelgroup.
CommunicationOptimization. ConcurrentDPcommunicationstreamsfordecoupledattentionand
MoEcansaturateRoCElinks,incurringconsiderableincreasesinDPoverheadsduetocongestion.
Toaddressthis,weproposetwocomplementarycommunicationoptimizationsthatjointlyreduce
iteration time by up to 5%. First, fabric-aware communication scheduling partitions DP traffic into
intra-node NVLink and inter-node RoCE phases, and pipelines them to fully utilize both fabrics.
Second, communication-aware rank placement uses job-level communication profiles to place ranks
acrossswitches,reducinghopcountsandsteeringheavytrafficawayfrominter-switchhotspots.

Muon ZeRO-1 Resharding. Muon [34] requires full (unsharded) per-parameter gradients for
Newton–Schulz orthogonalization, which conflicts with ZeRO-1 [69] reduce-scatter that shards a
parameter’s gradient across DP ranks. The current implementation in Megatron-LM resolves this
mismatchbynaivelyall-reducingFP32gradientstoreconstructfullgradientspriortotheMuonup-
datebutnearlydoublescommunication. WeinsteadassignwholeparameterstoDPranksandrepack
the gradients buffer into a rank-major buffer so a single reduce-scatter delivers each parameter’s
completegradienttoitsowner. Sincepaddingtothefattestrankincursoverheadthatgrowswith
thedata-parallelsize,weapplythisonlytoexpertparametersanduseDPall-reducefornon-expert
parameters. Thishybridstrategyreducesend-to-enditerationtimebyapproximately5%withless
than4GBadditionalmemorycomparedtothenaiveall-reducebaseline.
GPUKernelsOptimization. Wealsoapplykernel-leveloptimizationstoimprovetrainingefficiency.
Inattention,wefuseQKnormalizationwithRoPE.InMoE,wefusemultiplesmalloperatorstoreduce
kernel-launchoverheadandmemorytraffic,andimplementafusedMoEgather/scatterwithgrouped
GEMM,similartoSonicMoE[71].
Fine-grainedSelectiveCheckpointing. Ourtrainingframeworksupportsfine-grainedactivation
recomputationwithper-layer,submodule-leveltoggles(e.g.,attention,FFN,normalization,SiLU,and
MoEpermutation),enablingselectiverecomputationofonlythemostmemory-intensivecomponents
toreducepeakmemorywithminimaloverhead.
## 3.3. High-ThroughputLightweightMonitoring
We collect a comprehensive suite of metrics (e.g., expert distribution within each micro-batch and
gradientnorms)forfine-grainedmonitoringofthetraining. However,thetelemetryscaleisimmense:
a4,096-GPUworkloadgeneratesnearly6millionmessagesperiteration. Conductingasynchronous
global reduction within the main loop would introduce a significant overhead of several seconds,
effectivelydoublingtheiterationtime,whichisclearlyintolerableforhigh-performancetraining. To
mitigatethis,wedevelopaLightweightMetricsServertodecoupletelemetryprocessingfromthe
trainingpath. EachrankutilizesStepRPC,anin-houseasynchronouscommunicationframework,to
asynchronouslyoffloadlocalmetricstotheremoteserver. Thisapproachreducestelemetryoverhead
toapproximately100msperiteration.
TheMetricsServerbuffersincomingmetricsandtriggersreductionanddatabasepersistenceonlyafter
receivingend-of-iterationsignalsfromallparticipatingranks,eliminatingsynchronizationinthemain
loop. Toingestandprocessmillionsofmessageswithlowlatency,theserverisimplementedasahigh-
concurrencymulti-processsystemwithtwodecoupledmodules: (i)aMessageReceiveroptimizedfor
high-throughputingestion,and(ii)aReductionProcessorresponsibleforaggregationandpersistence.
Byexploitingmulti-coreparallelismwithinandacrossthesemodules,theserverkeepspacewiththe
telemetrystreamandensuresthatmetricsmanagementneverlagsbehindtraining.
## 4. Pre-Training and Mid-Training
Overview. Thissectionsummarizesourpre-trainingandmid-trainingprocess,withanemphasis
on the practical stability constraints of large-scale sparse MoE training. We first describe training
stabilitydiagnosticsandmitigations(Section4.1),thendetailthecurriculumusedforpre-trainingand
mid-training,includingthedatamixture,schedule,andkeyhyper-parameters(Section4.2).

2.0
1.8
1.6
1.4
0T 2T 4T 6T 8T 10T 12T 14T
Tokens
ssoL
1.9
1.8
1.7 3
1.6
0.1T 0.2T 0.3T 0.4T 0.5T
The only loss spike
Figure3: Per-steptraininglossofStep3.5Flash,plottedwithoutsmoothingorsub-sampling. We
observemerelyoneisolatedlossspikeacrossthefulltrainingduration. Theinitialtrainingstepsare
① ③
omittedforclarity. Markers – indicatebatchsizeincreasesto8,192,12,288,and16,384,respectively.
④
Marker denotestheactivationofthelossmaskonmetatokens(seeAppendixA.3fordetails).
## 4.1. TrainingStability
Trainingstabilityisafirst-classrequirementforlarge-scalesparseMoEpre-training. Tomakestability
actionable, we build a comprehensive observability and diagnostic stack based on a lightweight
asynchronous metrics server with micro-batch-level continuous logging (described in Section 3.3).
Thisinfrastructureprovidesfine-grainedvisibilityintobothoptimizer-levelandexpert-levelsignals,
enablingsystematicmitigationofrecurringfailuremodesinlarge-scaleMoEtraining.
Inpractice,wefindthreedominantinstabilitiesthatthemetricsstackhelpssurfaceearlyandlocalize
precisely: (i)transientlossspikesandoccasionalstochasticnumericalblow-upscausedbyMuon’s[34]
numericallysensitivepolar-factoriterationunderreducedprecision,(ii)expert-sidecollapse("dead
experts") that can occur even when router dispatch statistics remain apparently healthy, and (iii)
localizedactivationblow-upsconfinedtoasmallsubsetofexperts.
Withthemitigationsguidedbythesediagnostics,thepre-traininglossremainssmooththroughoutthe
run,exhibitingonlyasinglelossspike. Figure3showsthefullcurvepriortolearning-ratecooldown.
## 4.1.1. NumericalSensitivityofMuon
Muon approximates a semi-orthogonal update direction via a Newton–Schulz (NS) iteration [72].
In early experiments, we find modest, consistent loss reduction when using a faster-converging
orthogonalizationapproximation. WethereforeadoptthePolarExpress[73]iterationandrunafixed
𝑇=6stepstobalanceoptimizationqualityandthroughput.
However,weoccasionallyobservesharp,unrecoverablelossspikesdespiteusingtherecommended
safety scaling [73]. The spikes are non-deterministic (often avoided by resuming from a nearby
bfloat16
checkpoint),suggestinganumericalpathology. Simulationsindicatethat PolarExpress
canrarelyyieldextremeintermediateoutliersundercertainupdatestatisticsduetocumulativeerror
float16
inaddition. WethereforecastonlythePolarExpressiteration(stateandintermediates)to

whilekeepingtherestofthetrainingmixed-precision. Afterthischange,thespikesdonotrecur.
## 4.1.2. ExpertCollapseBeyondRoutingCollapse
Step-3 [32], our prior work, reports that MoE training may exhibit "dead experts", often described
as experts receiving negligible token dispatch for extended periods and therefore obtaining little
effectivegradientsignal. Inourpriorinvestigation,wefindthatexpertcollapsecanalsomanifestas
anexpert-sidepathologyevenwhenrouterdispatchremainsstable,i.e.,vanishingexpertactivations
andstagnantordecayingexpertparameternorms.
Weobservethattwofactorsareparticularlyinfluential: (i)Routed-expertaggregationrequiresexplicit
scaling. Whenincorporatingasharedexpert,itisimportanttointroduceanexplicitscalingfactorto
calibratetherelativecontributionofthesharedexpertandtheroutedexperts. Whilesmallermodels
mayimplicitlylearnsuchabalance,largermodelsarelessreliableatself-calibration. Amismatchcan
suppresstheeffectivecontributionofroutedexpertsevenifroutingfrequenciesappearhealthy. (ii)
Micro-batchbalancingcanbeoverlyrestrictiveunderfine-grainedsparsity. Forsparse,fine-grained
MoEdesigns,micro-batch-levelload-balancingconstraints(ascommonlyimplementedinSwitch-style
routing[22])canbecomeoverlystringent. Asanalyzedin[74],micro-batchLBLmayinduceexcessive
cross-expertcompetitionandhindereffectivespecialization.
We therefore prefer broader-scope balancing (e.g., global-batch statistics) [74,75] or loss-free bias
adjustmentbasedonobservedload[29,64]. Inpractice,routerdispatchstatisticsaretypicallystable
andarenotsensitiveindicatorsofexpertcollapse. Werecommendmonitoringexpert-sidesignals,
including per-expert activation norms (e.g., RMS/mean norm at the MoE FFN intermediate) and
parameternorms(e.g.,Frobeniusnormsofexpertprojectionmatrices). Whenasubsetofexpertsdrifts
towardnear-zeroactivations/updateswhilethemedianremainsstable(e.g.,decreasingmin-to-median
ratios),itprovidesanearlywarningofexpert“death”.
## 4.1.3. LocalizedActivationBlow-upinMoELayers
As expert specialization matures during the main training phase, we observe a localized stability
pathology in the deeper MoE layers. Specifically, the activation norm of a small subset of experts
(oftenjustoneortwoperlayer)growsrapidly,whilethemajorityofexpertsinthesamelayerremain
well-behaved. This disparity results in a heavy-tailed activation distribution: the median expert
activationnormremainstable,butthemaximumactivationnormexplodes,significantlyincreasing
theriskofnumericaloverflowanddownstreaminstability.
Figure4illustratesthisfailuremode. Remarkably,thisinternalinstabilityisentirelymaskedbythe
trainingloss,whichshowsnegligiblevariationdespitetheunderlyingexplosioninnormsshownin
Panel(a). Wetrackthisphenomenonbymonitoringthedispersionofper-expertFFNoutputnorms.
AsobservedinPanels(b)and(c),whilethemiddlelayers(e.g.,Layer38)retainstabledistributions,
thefinallayers(i.e.,Layer45)exhibitarapidlywideninggapbetweenthemaximum(solidlines)and
themedian(dashedlines). Thisindicatesthatactivationenergyisconcentratingdangerouslyinafew
"rogue"expertsinthedeepernetwork. Tomitigatethis,weevaluatetwodistinctinterventions:
• Weightclippingonexpertprojections: WeconstrainthenormoftheMoEFFNexpertprojection
matrices. For each expert projection matrix 𝑊, if its maximum activation norm max𝑥 ∥𝑊𝑥∥
exceeds a threshold 𝜏, we rescale it via 𝑊 ← 𝑊 · 𝜏 . This is similar to MuonClip in
max𝑥∥𝑊𝑥∥
attention[5],butweperformclippingofflineonthecheckpointratherthanon-the-fly.
• Activationclippinginsideexperts: Weapplyelement-wiseclippingdirectlytotheMoEFFN
intermediateactivationspriortotheoutputprojection,asin[33].

1.50
1.49
1.48
96k 100k 104k 108k
ssoL
96k 100k 104k 108k
(a) Loss vs. Steps
)goL(
mroN
tuptuO
Solid: max 103
Dashed: Median
96k 100k 104k 108k
(b) Expert Output (Layer 38)
)goL(
mroN
tuptuO
NNoo cclliippppiinngg WWeeiigghhtt cclliippppiinngg AAccttiivvaattiioonn cclliippppiinngg
Solid: max
Dashed: Median
(c) Expert Output (Layer 45)
Figure 4: Analysis of expert activation stability and mitigation strategies. In Panels (b)–(c), solid
lines represent the maximum expert output norm, while dashed lines represent the median. (1)
Depth-Dependent Instability: While training loss appears identical across methods (Panel a) and
middlelayersremainstable(e.g.,Layer38inPanelb),thefinallayers(i.e.,Layer45inPanelc)suffer
fromcatastrophicnormexplosionintheNoclippingbaseline. (2)Mitigation: Weightclippingmerely
delaysthisexplosion. Incontrast,Activationclippingeffectivelyboundsmaximumnorms,ensuring
stabilityacrossalllayers.
AlthoughthetraininglossappearsindistinguishableacrossdifferentmitigationstrategiesinFigure4
(a),themax-to-medianratioreliablyunmasksunderlyinginstability. AsevidencedinPanels(b)and
(c),activationclippingensuresastabletrajectoryforinternalnorms,whereasweightclippingalone
failstopreventtherecurrenceofoutlierexperts. Consequently,weestablishthemax-to-medianratio
ofper-expertactivationnormsasarobustandnecessarymetricformonitoringtrainingstability.
The activation blow-up is driven by several factors. We observe that high-frequency bi-grams can
trigger expert specialization. When using pre-norm [76,77], a single expert can amplify its output
boundlesslyanddominatethefinaloutputnorm,leadingtonear-deterministicpredictionbehavior.
ThisriskisexacerbatedbySwiGLU[78],wherestrongalignmentbetweenthegateandup-projection
branchesproducessparseactivationswithextrememagnitudes. Muonfurtheracceleratesthiscollapse
byamplifyingpersistentlow-rankupdates. AdetailedanalysisisprovidedinAppendixB.
## 4.2. TrainingCurriculum
Thetrainingproceedsfrombroadopen-domaincoveragetoincreasinglyagenticandlong-context
specialization. Wefirstpre-trainat4kcontextonabroadopen-domainmixturetoestablishgeneral-
purposecapabilities,thenannealthemixturetowardhigher-qualityknowledgeandmoresoftware-
developmentdata(code,PRs,issues,andcommits)whileextendingthecontextwindowto32k. Next,
a dedicated mid-training stage expands the context window from 32k to 128k to strengthen long-
horizonreasoningandimproveinitializationfordownstreampost-trainingandagenticworkloads.
Overall,wetrainonapproximately17.6Ttokensforpre-trainingand750Btokensformid-training.
## 4.2.1. DataMixture
Ourcorpuscombinesgeneralopen-domaindatawithagentic-orienteddata. Wesummarizethekey
sourcesbelow,moredetailscanbereferedinAppendixC.

GeneralKnowledgeData. Tosupportbroadworldknowledge,webuildStepCrawl(AppendixC.1.1),
anin-housecrawlingandcurationinfrastructurebeyondstandardCommonCrawl[79],toharvest
trillionsofhigh-qualitytokensatscalefromwebpages(HTML)andbook-/document-likesources
(ePub/PDF).Allcontentisprocessedwithmulti-stagequalityfiltering,site/categorytagging,dedu-
plication,andsanitization.
CodeData. Strongcodecapacityisfoundationalforagenticmodels. Ourcodecorpusiscurated
andrefinedusingamodifiedOpenCoder[80]pipeline. Werelaxfilteringfromazero-tolerancepolicy
toallowing0–6heuristicviolations(AppendixC.2.1)perdocument,balancingqualityanddiversity,
and upsample code-centric data during annealing and mid-training to strengthen agent-related
programming.
PR/Issue/CommitData. Tobettermatchrealsoftware-engineeringworkflows,wecurateacompre-
hensivePR/Issue/Commitdataset(AppendixC.2.2)fromGitHubrepositorieswith10+stars. This
git diff
includes(1)BaseDatavalidatedagainst (deduplicatedagainstbenchmarks[14,81]); (2)
PR-DialogueDataderivedfromPRthreadsandcommitsusingAgentless-styletemplates[82]forfile
localizationandcoderepair;and(3)derivativesoftware-engineeringcorporausedinmid-training
andpost-training.
Tool-UseandReasoningData. Toimprovetool-userobustnessandmulti-stepreasoning,weadd
syntheticandsemi-syntheticdataspanningmath/code/science/generalknowledge,anddomain-
specific samples targeting search agent, SWE agent, and tool execution. During mid-training, we
furtherintroducelong-contextsamples(naturallongdocumentsandlong-formsynthetictasks)to
reinforceplanningandreasoningoverextendedcontexts.
## 4.2.2. Schedule
Pre-trainingschedule. Pre-trainingconsistsoftwostages:
## 1. Pre-trainingStage1: Open-domainpre-training(14.6Ttokens,4kcontext). Broadopen-domain
trainingtomaximizecoverageandfoundationalcapability.
## 2. Pre-trainingStage2: Annealing+long-contextinitialization(3Ttokens,4kto32kcontext). We
annealthedatamixturetowardcodeandPR/Issue/Commit-centricsources,whileincreasingthe
shareofhigher-qualityknowledgeandreasoning-densesamples. Thisstagestartswith2Ttokens
at 4k context, then transitions to 1T tokens at 32k context under the same annealed mixture to
initializelong-contexttraining.
Mid-trainingschedule. Mid-trainingalsoconsistsoftwostages:
## 1. Mid-trainingStage1: Specializationat32k(386Btokens,32kcontext). Wereplay81Btokens(21%)
from pre-training to mitigate distribution shift and stabilize specialization, while emphasizing
software-engineerandtool-use-centricmixtures.
## 2. Mid-trainingStage2: Long-contextspecialization(364Btokens,128kcontext). Weretain10.5B
replay tokens, and further specialize long-context capability with a mixture of synthetic long-
horizonreasoningandnaturallongdocuments(selectedfrompre-trainingdatawithlength> 32k),
plusdomain-specificdataforcodeagent,searchagent,andtool-use.

## 4.2.3. Hyper-Parameters
Pre-traininghyper-parameters. WeusetheMuonoptimizer[34]throughoutpre-training,setweight
decayto0.1andgradeintclipto1.0. Thelearningrateislinearlywarmedupfrom0to2.5×10−4 over
the first 2,000 steps and then cosine-decayed to 5×10−5 over Pre-training Stage 1. In Pre-training
Stage2,weapplyasecondarycosinedecayfrom5×10−5 to2×10−5 overthe4kportion(2Ttokens)
and keep the learning rate fixed at 2×10−5 for the 32k portion (1T tokens). The global batch size
graduallyincreasesfrom4096to16384overthefirst400Btokens,andkeeps16384intheremaining
training, and is set to 2k for the 32k portion of annealing. The MTP loss weight is set to 0.3 in Pre-
trainingStage1and0.1inPre-trainingStage2,following[29]. Forloss-freeloadbalancing,thebias
updaterateis0.001forthefirst14.6Ttokensanddecaysto0.0duringannealing,andanEP-group
balancelosswithcoefficient0.001isappliedthroughoutpre-training. ForRoPE[83],weuse𝜃 =10,000
forbothfullattentionandslidingwindowattention(SWA)during4ktraining,andset𝜃 =1,000,000
Full
onlyforfullattentionandmaintain𝜃 =10,000forthe32kportionofannealing.
SWA
Mid-traininghyper-parameters. WecontinuetouseMuon[34]duringmid-training. Wefreezethe
MoErouterweightsanddisabletheEP-groupbalancelossandfixtheMTPlossweightto0.1forboth
mid-trainingstages. Thelearningrateiswarmedupfrom0to2×10−5 overthefirst3%ofiterations,
keptconstantinMid-trainingStage1,anddecayedto7.3×10−6 inMid-trainingStage2. ForRoPE
selectivescaling,weset𝜃 =1,000,000at32k(Mid-trainingStage1)andincreaseto𝜃 =5,000,000
Full Full
at128k(Mid-trainingStage2),whilekeeping𝜃 =10,000throughoutmid-training[84].
SWA
## 5. Post-Training
Inthissection,weintroduceaunifiedpost-trainingrecipeforlarge-scaleReinforcementLearning(RL),
whichbeginswithaunifiedSupervisedFine-Tuning(SFT)model. Thisframeworkenablesconsistent
self-improvementby combiningverifiablereward signalswithhumanpreferencefeedback, while
maintainingstabilityevenduringlarge-scaleoff-policytrainingforMixture-of-Experts(MoE)models.
Theprocessfollowsatwo-phaseapproachsimilartopriorworks[2,85]. First,weconstructExpert
ModelsbyenhancingtheunifiedSFTbaselinewithdomain-specificRLacrossMath,Code,STEM,
Tool-use,LongContextUnderstanding,HumanPreference,andAgenticReasoning. Thesespecialized
expertsarethendistilledintoageneralistmodelusingSelf-DistillationandScalableRL,ensuring
thefinalmodelremainscompetitivewithspecializedbaselinesacrossdiversetasks. Bysystematically
alternatingbetweentargetedspecializationandbroadsynthesis,weachieverobustgeneralization
withoutcompromisingexpert-levelperformance.
## 5.1. ExpertModelConstructionandSelf-Distillation
Weemployatwo-stageSFTpipelinetobuildarobustfoundationforsubsequentRL.Thefirststage
executeslarge-scalemulti-domainSFTspanningMath,Code,STEM,Logic,GeneralQA,CodeAgent,
Tool-use, Search Agent, and Long Context Understanding. Difficulty-aware filtering and strategic
balancingareappliedtofosterbroadagenticbehaviors. Thesecondstageexplicitlymaximizesrea-
soningdensitybyinjectingout-of-distribution(OOD)signals[46,86],comprising∼30kexpert-level
chemistrytrajectoriesandsyntheticarithmetictasks. Thistargetedexposuretodistinctreasoningpat-
ternsunlockslatentcapabilitieswithinjustthreeepochs,equippingthemodelwiththesophisticated
structuralcomplexitynecessarytoinitializethesubsequentdomain-specificRLphase.
Followingdomain-specificRL,weconsolidatethedivergentexpertcapabilitiesintoaunifiedstudent
model, initialized from the mid-train checkpoint. In this phase, the expert models generate high-

0.55
0.50
0.45
0.40
0.35
0 1000 2000 3000 4000
Training Step
draweR
1.50
1.25
1.00
0.75
0.50
0.25
0.00
0 1000 2000 3000 4000
Training Step
mroN
darG
rotcA
0.4
0.3
0.2
0.1
0 1000 2000 3000 4000
Training Step
yportnE
MIS-PO PPO
Figure5: ScalabilitycomparisonbetweenMIS-POandPPOonourinternalmodel. (1)Efficiency:
MIS-POdemonstratessuperiorsampleefficiency,achievinghigherrewardplateauswithanaccelerated
convergencetrend. (2)Stability: MIS-POsignificantlystabilizestrainingdynamicsbysuppressing
gradientnoiseandeliminatingthelargespikesinthepolicygradientnorm. (3)ExplorationPersis-
tence: MIS-POexhibitsslowerentropydecay,enablingabetterexploration–exploitationbalance.
qualitytrajectoriesusingapromptdistributionsharedwiththefirst-stageSFTcorpus,offeringamore
stableandefficientalternativetodirectRLintegration. Thisapproachemploysrejectionsampling
to eliminate undesirable patterns such as language mixing or overthinking, centralizing expert
knowledgeintoasinglestudentmodel. Byestablishingthishigh-qualityfoundation,self-distillation
significantlyreducestheoptimizationburdenonsubsequentRLstages.
Hyper-Parameters. TheMuonoptimizer[34]isemployedwitha3%warmupandacosinedecay
from1.0×10−5 to5.0×10−6. WefreezetheMoErouterweightsanddisabletheEP-groupbalanceloss
similartomid-training. TheSFTtrainingisexecutedwithanMTPlossweightof0.1,aglobalbatch
sizeof32,andaglobalsequencelengthof128k. RegardingRotaryPositionEmbeddings(RoPE)[83],
wemaintain𝜃
𝑆𝑊𝐴
=10,000andadjust𝜃
𝐹𝑢𝑙𝑙
=5,000,000toaccommodatethe128kcontextlength[84].
## 5.2. ScalableRL
In RL for LLMs, we optimize a policy 𝜋 𝜃 to maximize terminal rewards over trajectories 𝜏 =
(𝑠 0 ,𝑎 0 ,...,𝑠 𝑇 ), where 𝑎 𝑡 denotes the token generated at state 𝑠 𝑡. For reasoning tasks, however, this
processfacessevereinstabilityarisingfromhighgradientvariance,furtheramplifiedbyextremely
longhorizonsandmodelscale(Figure5(2)). Thisvarianceprimarilyfrominfrastructuredivergence
betweenhigh-throughputinferenceenginesandtrainingframeworks,aswellastheoff-policymis-
alignmentinherenttoiterativeupdates. Insuchsettings,importancesamplingisinherentlyunstable,
asminortoken-levelprobabilityshiftscompoundintonoisygradientsthatimpedeconvergence.
## 5.2.1. MIS-FilteredPolicyOptimization(MIS-PO)
Toaddressthesestabilitychallenges,weproposeMIS-PO,amethodinspiredbyMetropolisIndepen-
denceSampling(MIS)[39,40]. Wetreattheinferencepolicyasaproposaldistributionandthetraining
policyasthetarget,restrictingupdatestosamplesthatremainsufficientlyclosetothetargetdistribu-
tion. Unlikeimportancesampling,whichscalesgradientsbyboundedratiosandoftensuffersfrom
highvariance,MIS-POappliesbinarymaskingtofilteroff-distributionsamplesandtreatsretained
trajectories as effectively on-policy, resulting in significantly reduced gradient variance and stable
optimization.

Formally,wedefineabinaryindicatorfunction I(𝑥) =1[𝜌 ≤ 𝑥 ≤ 𝜌 ] andapplyitattwodistinct
min max
granularities. Atthetokenlevel,thefunctionfilterstheprobabilityratio 𝑥 𝑡 =𝜋 𝜃 (𝑎 𝑡 |𝑠 𝑡 )/𝜋 𝜃 (𝑎 𝑡 |𝑠 𝑡 )
old vllm
tosuppresslocalizedmismatchesbetweenthetrainingandinferencepolicies[37]. Atthetrajectory
level,weapplythesameindicatortothegeometricmeanratio 𝜌¯(𝜏) = ((cid:206) 𝑡 𝑥 𝑡 )𝑇 1 ,effectivelydiscarding
entiretrajectoriesthathavedriftedsignificantlyfromthetargetdistribution. Thereformulatedactor
lossreplacescontinuousimportanceweightswiththesedual-leveldiscretemasks:
L 𝑎𝑐𝑡𝑜𝑟 =−E 𝜏∼𝜋
𝜃
(cid:2)I(𝑥 𝑡 )·I(𝜌¯(𝜏))·log𝜋 𝜃 (𝑎 𝑡 |𝑠 𝑡 )·𝐴ˆ 𝑡 (cid:3) . (2)
vllm
Bytreatingvalidsamplesaseffectivelyon-policy,thisobjectivesubstantiallyreducesgradientvariance
forlong-horizonreasoningtasksunderatrust-regionconstraint. Figure5presentsanablationstudy
overapproximately5,000trainingsteps,whereMIS-POexhibitssignificantlylowernoiseintheactor
gradientnormthanPPO,indicatingimprovedscalability. MoreablationsareshowninAppendixD.2.3.
To further stabilize training dynamics, we employ several techniques: Truncation-Aware Value
Bootstrapping[87]tocorrecttheambitiousrewardbiasintroducedbycontext-lengthtruncationand
RoutingConfidencemonitoringtopredictinstabilityspecifictoMoEarchitectures.
Truncation-AwareValueBootstrapping. Assigningzerorewardstocontext-truncatedtrajectories
conflates truncation with task failure. This ambiguity penalizes long-chain reasoning by failing to
distinguishbetweenincompleteandincorrectoutcomes. Toaddressthis,wereplacethezeroreward
with a bootstrapped value estimate of the final state, effectively treating truncation as a horizon
interruptionratherthanaterminalfailure. Themodifiedrewardfortrajectory𝜏 𝑖 isdefinedas:
(cid:40)
𝑉 𝜙 (𝑠 𝑇 ) iftheresponseistruncated,
𝑅ˆ 𝑖 = (3)
𝑅 𝑖 otherwise.
Empirically,thistruncation-awarevaluebootstrappingstabilizestrainingevenattruncationratesas
highas20%,preventingtherewarddegradationtypicallytriggeredbyincompletetrajectories[88,89].
Ablationstudiesconfirmthatthistechniqueisparticularlybeneficialforcompetition-levelbenchmarks,
wherelong-horizonreasoningmakestruncationeffectsmostprevalent.
Routing Confidence as a Stability Proxy. Recent studies [36,38] bridge RL stability with MoE
routingconsistency. Buildingonthis,weproposetheRoutingConfidence(Σ 𝑘)asaproxyforstability,
whichistheaverageprobabilitymassofactivatedexperts. LowΣ 𝑘 implieshighroutinguncertainty,
whichamplifiesthetraining-inferencemismatch. Throughpreliminaryexperiments,weidentifya
distinctstabilityphasetransition: modelswithlowroutingconfidencearebrittleandrequireextreme
stabilization(e.g.,RouterReplay[1,36,38],stricton-policyupdates[90]). Incontrast,modelswithhigh
routingconfidencemaintainrobustness,enablingoff-policytrainingwithoutcomplexinterventions.
RL Training Dynamics. To provide a holistic view of our method, we illustrate the RL with ver-
ifiable rewards (RLVR) training dynamics and downstream evaluation improvements of Step 3.5
FlashinFigure6. Thesteadyriseintrainingrewardssuggestsastableandeffectivelearningprocess.
Furthermore,Step3.5Flashachievesconsistentperformancegainsacrossdiverseevaluationbench-
marks. Specifically,weobservesubstantialimprovementsof+3.2%onIMO-AnswerBench[91],+6.1%
on CF-Div2-Stepfun-cpp (Appendix E.2.1: our custom CodeForces2 Div.2 Benchmark), +10.6% on
ARC-AGI-1[92],and+3.4%onHLE [93].
text
2https://codeforces.com/

0.700
0.675
0.650
0.625
0.600
50 100 150 200 250
Training Step
draweR
IMO-Answer CF-Div2- ARC-AGI-1 HLEText
Bench Stepfun-cpp
)%(
ycaruccA
+3.2 +6.1
85.5 86.4 Init Model
82.3 80.3 RL Model
+10.6
56.8
46.2
+3.4
23.3
19.9
Figure6: RLtrainingdynamicsandcross-domainimprovementsofStep3.5Flash. RLdrivessteady
rewardgrowth(left)anddeliversconsistentaccuracyboostsacrossmultiplebenchmarks(right).
## 5.2.2. RewardSystem
We decouple the RL framework into RL with verifiable rewards (RLVR [94]) and RL with non-
verifiablerewards(e.g.,RLHF[95]),eachsupportedbyadistinctrewardtailoredtoitssupervision
characteristics.
Verifiable Rewards. For RLVR, each prompt is paired with a task-specific verifier that outputs a
reward. Therule-basedcheckersareusedforlogic,instructionfollowing,andcode,whilemodel-based
verifiersareemployedforSTEMtasks. Inablationstudiesover450RLtrainingstepsonourinternal
model, using model-based verifiers for STEM tasks outperforms direct vanilla math-verify by an
averageof2.0%;additionaldetailsareprovidedinAppendixD.2.2.
Non-VerifiableReward. Weaddressnon-verifiabletasksusingapairwisegenerativerewardmodel
(GenRM[96])thatbenchmarksresponsesagainstafixedreference. GenRMisareasoningmodelthat
outputsaconfidencescoreindicatingthelikelihoodofaresponsewinning. Thisscoreissubsequently
convertedintoaBradley–Terrywinrate[97]toserveastherewardsignal. Lengthcontrolismodeled
within GenRM as a confidence score penalty and propagated to the win-rate reward, effectively
suppressingexcessivelengthgrowthduringRLtraining. Wefurtherensurerobustnessbyassigning
zerorewardtoresponseswithfabricatedcitations,overconfidentclaims,orlanguageinconsistencies.
AgentReward. SearchtasksareevaluatedusinganLLMbasedonentity-matchingscores. Forreport
generation,arubric-basedLLMjudgeevaluatestheresearchquery,rubricspecifications,andcandidate
reports,producingternaryjudgments(satisfied,partiallysatisfied,unsatisfied)[98]. Astheintermediate
categoryoftenmisalignswithexpertpreferences,wemaptheoutputstoasymmetricbinaryrewards,
yieldingclearerlearningsignalsandfasterconvergencetowardexpert-alignedbehaviors.
GenRM Training and MetaRM. We initialize the GenRM by fine-tuning our SFT model with
RM-specificprompts. ForRLtraining,weusecuratedpairwisepreferencedatawithalogsigmoid
loss similar to the scalar reward model formulation. To improve the robustness of GenRM, we
penalizeresponsesexhibitingspuriousreasoning(i.e.,correctpreferencederivedfromflawedlogic)
byintegratingMetaRM,anadditionalverifierthatreducesthetrainingrewardwhensuchpatterns

Domain NumSamples Tokens CorpusContribution
Math 68055 0.98B 11.19%
Code 86421 1.23B 21.10%
STEM 120399 0.55B 6.31%
Logic 93323 0.81B 13.87%
General 314495 0.80B 9.16%
CodeAgent 37240 0.90B 17.70%
Tool-use 114507 0.76B 8.72%
SearchAgent 20256 0.50B 8.75%
LongContext 15565 0.70B 4.00%
Total 870687 7.23B 100.00%
Table3: DataStatisticsoffirst-stageSFT.
are detected. In ablation studies spanning 200 RL training steps on our internal model, MetaRM-
augmentedGenRMoutperformsvanillaGenRMby0.5%-3%oneverybenchmark.
## 5.2.3. Hyper-Parameters
Forrollout,wesetboththesamplingtemperatureandtop-𝑝to1.0withamaximumsequencelengthof
128ktokens. Pergeneration,wesample256uniquepromptswith16responseseachforreasoningtasks,
512uniquepromptswith8responseseachforhumanpreferencetasks,and128uniquepromptswith
8responseseachfortool-usetasks. Afterrollout,completedsamplesarepartitionedintomini-batches
andusedfortrainingoverasingleepoch,with4mini-batchesfortheactorand12mini-batchesfor
thecritic. OptimizationisperformedusingtheMuonoptimizerwithaweightdecayof0.1. Theactor
istrainedwithalearningrateof2×10−6 and20warmupsteps,whilethecriticusesalearningrateof
5×10−6 with50warmupsteps. FollowingORZ[90],wesetboth𝛾 and 𝜆 to1. Wefurtheradoptan
unbiasedKLloss[85]withacoefficientof0.001inthefinalstage. ForEquation(2),thetoken-level
andtrajectory-levelmaskingboundsaresetto [0.5,2] and [0.996,1.001],respectively.
## 5.3. DataSynthesis&Curation
Weconstructadiverseanddifficulty-balancedpromptpoolbyaggregatingopen-sourcedata,synthetic
generations,andusertrajectories. Aunifiedsynthesisandcurationpipelineisapplied,combining
strictglobalfilteringwithdomain-specificrefinementtomaximizereasoningdensity. Dataquality
isensuredthroughahybridofrule-basedheuristicsandmodel-basedfidelitychecks. Theresulting
datasetcontains871ksamples(7.23Btokens),withdetailedstatisticssummarizedinTable3.
## 5.3.1. GeneralandReasoning
Ourtrainingcorpusaggregatescommunityprompts,expertresponses,andsyntheticdatafromdiverse
open-source,includingMathematics[90,99–110],Coding[111–113],andScienceandOpen-ended
QA[114–117]. Tomaximizereasoningdensity,weemployaunifiedpipelinethatcouplesstrictglobal
filteringwithdomain-specificrefinement,enforcingqualityviaahybridofrule-basedheuristicsand
model-based fidelity checks. Specifically, in mathematics, we ensure numerical stability through
specialist-guidedrejectionsamplingandsyntheticlarge-numberarithmetic. Forprogramming,we
prioritize offline executability by selecting rigorous algorithmic challenges while strictly purging
RAG-relatedhallucinations. Inparticular,wemitigatethemodel’stendencytofalselyclaimaccessto

externalsearchenginesorpretendtoretrieveonlinesolutions. Furthermore,werestrictscientificdata
tounambiguousquestionswithunique,determinablesolutions.
Toenablegeneralizationacrosspracticalscenarios,weexpandopen-sourcecheckers3 andaugment
sampleswithseveralreal-worldconstraints. Inparallel,wecollectgeneralpromptsfromopen-source,
synthetic, and user trajectories to form a diverse, difficulty-balanced pool. This process yields a
high-fidelitydatasetcomprisingmillionsofsamplesatthebillion-tokenscale.
## 5.3.2. GeneralizedToolLearning
Weproposeanexecution-drivendatagenerationframeworkforlearningreliabletool-usebehaviorsin
intelligentagents,addressingkeylimitationsofexistingsyntheticpipelinessuchasdatainconsistency,
lackofverifiability, andmodelhallucinations. Insteadofrelyingonrandomexploration[118,119]
ormodel-basedsimulation[5,120],ourapproachdecomposestool-usebehaviorintoatomicintents
andmodelsthemusingafinitestatemachine(FSM),explicitlyseparatingabstracttool-calllogicfrom
parameterizedexecutionconstraints. Dataisgeneratedthroughasample–execute–verifyloopwith
rejectionsampling,whereallcandidatetrajectoriesareexecutedinrealenvironmentsandvalidatedby
deterministicfeedback,ensuringfidelityandeliminatinghallucinatedbehaviors. Bycompositionally
combiningatomicintents,theframeworksupportsscalablegenerationofcomplex,controllabletool-
usescenarios. Usingthisparadigm,weconstructover100Khigh-qualitytrajectoriestotalingbillions
oftokens,providingprecisesupervisionfortool-basedplanning,reasoning,andexecution.
## 5.3.3. CodeAgents
Codeagentscanself-improvethroughaclosed-loopinterventionbetweenverifiableenvironment
constructionandsolutiongeneration,whereexecutablefeedbackcontinuouslyrefinesbothcapabil-
ities. Wetreatenvironmentconstructionasafirst-classcapabilityalongsidebugfixingandfeature
implementation,synthesizingitunderverifiablerewardsignals. Tothisend,wedevelopaspecialized
agenticpipelineevolvedfromtheSWE-factory[121]framework,incorporatingacross-taskmemory
poolthatretrieveshistoricalbuildsuccessesasfew-shotdemonstrationsandaloop-detectionmecha-
nismtopreventredundantexploration. Thispipelineachievesa40%environment-buildingsuccess
rate,formingapositivefeedbackloopformodelself-evolutionthroughdensesupervisionfromcon-
structiontrajectories,includingshellcommandsanderrorrecovery. Tofurtherimprovesignalquality,
we normalize environment construction trajectories by abstracting and masking transient failures
and redundant execution patterns that do not contribute to the final resolution. The bootstrapped
environmentsfunctionasdynamictestbeds,leveragingexecutionfeedbackandunitteststogenerate
high-qualitysyntheticdataandrewardsignalsforcontinuousalignment. Empirically,weobservea
bidirectionaltransfer: constructionexpertiseacceleratescodingperformance,whilecodingwithin
theseenvironmentsfurtherimprovesconstructionaccuracy,asshowninDockSmith[122]. Leveraging
thisevolutionpipeline,wecurate50kverifiedenvironmentsspanningover15kGitHubrepositories
and more than 20 programming languages. This diverse collection captures a broad spectrum of
real-world scenarios, providing a robust foundation for training generalist code agents. Further-
more, we incorporate several prominent open-source environments, including SWE-smith [123],
SWE-Gym[124],R2E-Gym[125],SWE-rebench[126],andSETA[127].
## 5.3.4. SearchandResearchAgents
Tofacilitateadvancedinformation-seeking,ourpipelineintegratesgraph-basedandmulti-document
synthesistoenforcemulti-hopreasoning. Byperformingtopologicalexpansionsonknowledgegraphs
3https://github.com/allenai/open-instruct/tree/main/open_instruct/IFEvalG

(e.g., Wikidata5m [128]) and simulating cross-website browsing trajectories, we generate data that
reflectsreal-worldresearchcomplexity. Crucially,toguaranteethenecessityofexternalretrieval,we
validategeneratedqueriesagainstDeepSeek-R1[129],systematicallyexcludinginstancessolvableby
thisstrongreasoningmodelwithouttoolinteraction. Theresultingtrajectoriesarerefinedthrougha
structuredreportgenerationpipeline[98]thatenforcesrigorousinstructioncomplianceandstructural
integrity. Specifically,weenforcestrictadherencetopresetresearchplans,discardinganytrajectories
thatdeviatefromthestructure. Subsequently, validoutputsundergoiterativecleaningviamodel-
basedjudgersandheuristicrulestoresolvefine-grainedissuessuchasinformalwriting,temporal
hallucinations,andmixed-languageartifacts. Thisend-to-endapproachachievesindustry-leading
performanceonthe RESEARCHRUBRICS [21]benchmark.
## 5.4. AgentInfrastructure
ReasoningwithTool-UseTemplateDesign. Toeffectivelyintegratereasoningandagenticcapa-
bilities into a single foundation model, it is crucial to determine the appropriate templates for the
thinkingprocessandtoolusage. Regardingthereasoningtemplate,weevaluatethreemanagement
strategies. The approach of discarding reasoning history at every turn [129], while incentivizing
independentgeneration,leadstotaskfailureinlong-horizontasks(e.g.,codingsessionsexceeding100
turns). Conversely,retainingthefullreasoninghistoryincursprohibitivecontextconsumption,which
rapidlysaturatesthemodel’scapacityandblockssubsequenttoolinvocations. Toresolvethis,we
adoptaselectiveretentionstrategy: preservingreasoningtracesexclusivelyforthetool-usetrajectory
triggered by the most recent user instruction. This design achieves an optimal trade-off between
reasoningcoherenceandcontextefficiency,apracticealignedwithrecentfrontiermodels[85,130].
Regarding the tool-use template, we compared the prevalent JSON and XML formats. The rigid
syntaxofJSON,includingescapesequencesanddelimiters,frequentlyinducesparsingerrorsinsmall,
under-trained models. In contrast, the XML format allows for flat string output with significantly
lowergrammaticaloverhead. Therefore,weselecttheXMLformattoensurerobustnessincomplex,
real-worldagenticcodingscenarios.
ScalableCodeAgentInfrastructure. Ourintegratedarchitecturefocusesonscalablesessionman-
agementandcross-frameworkgeneralizationtofacilitatehigh-throughputagenticcoding. Centralto
thisisaproprietarySession-RouterthatorchestratescontainerlifecyclesviaKubernetesandensures
interactionconsistencythroughTmux. Thisarchitecturesupportsthousandsofconcurrentenviron-
ments with seamless state persistence, eliminating the need for manual, scaffold-specific Docker
configurations. Toensurehighgeneralizationacrossdiverseagenticworkflows,wetrainedthemodel
toadapttoawidespectrumofinteractionframeworks,rangingfromacademicstandards(e.g.,Open-
Hands[131],SWE-agent[132],andTerminus-2[16])toenterprisegradeprotocols(e.g.,Kilocode[133],
Roocode[134],andClaudeCode[135]). Byexposingthemodeltothesevariedinteractionparadigms
during training, we effectively prevent it from overfitting to specific pipeline patterns, ensuring it
remainsrobustregardlessoftheunderlyingexecutionenvironment.
## 6. Evaluations
## 6.1. Pre-trainingEvaluations
Evaluation Setup. We evaluate Step 3.5 Flash on a series of benchmarks, encompassing various
capabilities: (1)Generallanguageunderstandingandreasoning,includingBBH[136],MMLU[137],
MMLU-Redux[138],MMLU-Pro[139],HellaSwag[140],WinoGrande[141],GPQA[142],SuperG-
PQA[143],andSimpleQA[144]. (2)Mathematicsreasoning,includingGSM8K[145]andMATH[146].

Step3.5Flash MiMo-V2Flash GLM-4.5 DeepSeekV3.1 DeepSeekV3.2 Kimi-K2
Benchmark #Shots
Base Base Base Base ExpBase Base
#ActivatedParams - 11B 15B 32B 37B 37B 32B
#TotalParams - 196B 309B 355B 671B 671B 1043B
GENERAL
BBH 3-shot 88.2 88.5 86.2 88.2† 88.7† 88.7
MMLU 5-shot 85.8 86.7 86.1 87.4† 87.8† 87.8
MMLU-Redux 5-shot 89.2 90.6 - 90.0† 90.4† 90.2
MMLU-Pro 5-shot 62.3 73.2 - 58.8† 62.1† 69.2
HellaSwag 10-shot 90.2 88.5 87.1 89.2† 89.4† 94.6
WinoGrande 5-shot 79.1 83.8 - 85.9† 85.6† 85.3
GPQA 5-shot 41.7 43.5* 33.5* 43.1* 37.3* 43.1*
SuperGPQA 5-shot 41.0 41.1 - 42.3† 43.6† 44.7
SimpleQA 5-shot 31.6 20.6 30.0 26.3† 27.0† 35.3
MATHEMATICS
GSM8K 8-shot 88.2 92.3 87.6 91.4† 91.1† 92.1
MATH 4-shot 66.8 71.0 62.6 62.6† 62.5† 70.2
CODE
HumanEval 3-shot 81.1 77.4* 79.8* 72.5* 67.7* 84.8*
MBPP 3-shot 79.4 81.0* 81.6* 74.6* 75.6* 89.0*
HumanEval+ 0-shot 72.0 70.7 - 64.6† 67.7† -
MBPP+ 0-shot 70.6 71.4 - 72.2† 69.8† -
MultiPL-EHumanEval 0-shot 67.7 59.5 - 45.9† 45.7† 60.5
MultiPL-EMBPP 0-shot 58.0 56.7 - 52.5† 50.6† 58.8
CHINESE
C-EVAL 5-shot 89.6 87.9 86.9 90.0† 91.0† 92.5
CMMLU 5-shot 88.9 87.4 - 88.8† 88.9† 90.9
C-SimpleQA 5-shot 63.2 61.5 70.1 70.9† 68.0† 77.6
Table 4: Pre-training evaluation results. * denotes cases where the original score was unavailable;
wereportresultsevaluatedunderthesametestconditionsasStep3.5Flashforfaircomparison. †
indicatesDeepseekscoresquotedfromtheMiMo-V2-Flashreport[30].
(3)Coding,includingHumanEval[147],MBPP[148],HumanEval+,MBPP+[149]andMultiPL-E[150].
(4)Chineseunderstanding,includingC-Eval[151],CMMLU[152],andC-SimpleQA[153].
EvaluationResults. Table4summarizesthepre-trainingevaluationofStep3.5Flashacrossgeneral
reasoning, mathematics, code, and Chinese benchmarks. Despite activating only 11B parameters
(196B total), Step 3.5 Flash remains broadly competitive with substantially larger sparse baselines
(15–37Bactivated; 309–1043Btotal),demonstratingastrongaccuracy–efficiencytrade-off. Oncore
generalbenchmarks,Step3.5Flashachieves88.2onBBH(within0.5ofthebest)and85.8onMMLU.
Notably, Step 3.5 Flash reaches 31.6 on SimpleQA, outperforming DeepSeek-V3.2-Exp Base (27.0)
whileusingonly196Btotalparametersversus671B(i.e.,∼3.4×totalparameters),highlightingstronger
capabilitydensityperparameterbudget. Step3.5Flashfurtherdemonstratesstrongcodingcapabilities,
including81.1onHumanEval,67.7onMultiPL-EHumanEvaland58.0onMultiPL-EMBPP.Overall,
these results show that Step 3.5 Flash delivers high strong performance per activated compute,
providingasolidfoundationfordownstreamreasoningandagenticpost-training.

## 6.2. Post-trainingEvaluations
We evaluate Step 3.5 Flash on representative benchmarks, including the reasoning oritend HLE
(text subset) [154], MMLU-Pro [139], GPQA-Diamond [142], AIME2025 [10], HMMT [11], IMO-
AnswerBench[91];thecodingrelatedLiveCodeBench-v6(2024.08-2025.05)[12],CF-Div2-Stepfun4,
SWE-BenchVerified[13]andSWE-BenchMultilingual[14];theagentseries𝜏2-Bench[15],Terminal-
Bench 2.0 [16], GAIA [19], BrowseComp [17], xbench-DeepSearch [20], BrowseComp-zh [18], and
RESEARCHRUBRICS [21]; the general related ArenaHard v2 [155], IFBench [156] and MultiChal-
lenge [157]; and the long-context related LongBench v2 [158], MRCR [159] 5, FRAMES [160] and
RepoQA[161].
We further investigate the test-time scaling properties of Step 3.5 Flash on reasoning, general, and
long-contextbenchmarksbyadoptingtheParallelCoordinatedReasoning(PaCoRe)paradigm[42].
LeveragingStep3.5Flash’sextremeinferenceefficiency,thisapproachdecouplesreasoningcapacity
fromcontextlimitationsbylaunchingparallelreasoningtrajectoriesandsynthesizingtheirinsights
intohigher-fidelitysolutionsviamultiroundcoordination. Specifically, weemployamulti-round
PaCoRetrajectoryconfigurationas 𝐾(cid:174) = [4,4,4,4],yieldingsignificantgainsacrossbenchmarks.
We maintain a maximum sequence length of 256k, using the default decoding configuration with
decodingtemperatureandtop-pof1.0. AndweapplyYaRN[162]withascalingfactorof2.0ontopof
theoriginal128kpositionalembeddings,restrictingittofull-attentionlayersonly. Wereportpass@1
accuracyforallapproachesbasedonaverageperformanceofmultipleindependentgenerationsper
problem: 64 for AIME 2025, HMMT 2025 Feb., and HMMT 2025 Nov.; 8 for IMO-AnswerBench,
LiveCodeBench,GPQA-Diamond,andMultiChallenge;1forHLEand4runsforallotherbenchmarks.
MoredetailsareprovidedinAppendixE.2.
EvaluationResults. Table5presentsacomprehensivecomparisonofStep3.5Flashagainstabroad
setofstrongbaselinesacrossreasoning,codeagents,generalagents,long-contextunderstanding,and
generalcapabilitybenchmarks. Despiteactivatingonly11Bparameters(196Btotal),Step3.5Flash
demonstratesstrongperformanceacrossawiderangeoftasks,particularlyexcellingonreasoning-
intensivebenchmarkssuchasAIME2025,HMMT2025Feb.,HMMT2025Nov.,IMO-AnswerBench,
andLiveCodeBench-v6. Itconsistentlyoutperformsopen-sourcemodelswithlargerparametercounts
andachievesperformanceonparwithfrontiermodelssuchasGPT-5.2xHighandGemini3.0Pro.
Notably,Step3.5Flashachievesstrongresultsonagenticevaluations,includingSWE-BenchVerified,
Terminal-Bench2.0,BrowseComp(withContextManager),GAIA,and𝜏2-Bench,highlightingrobust
tool-useandlong-horizondecision-makingcapabilities.
## 7. Limitations
Token Efficiency. Step 3.5 Flash achieves frontier-level intelligence but currently requires longer
generationtrajectoriesthanGemini3.0Protoreachcomparablequality. Nextstepwewillpruneand
compressthethinkingforbetterefficiencywhilemaintainingthesamecompetitiveperformance.
EfficientUniversalMastery. Weaimtounifygeneralistversatilitywithdeepdomainexpertise. To
achieve this efficiently, we are advancing variants of on-policy distillation, allowing the model to
internalizeexpertbehaviorswithhighersampleefficiency.
4https://huggingface.co/datasets/stepfun-ai/CF-Div2-Stepfun
5https://huggingface.co/datasets/openai/mrcr

Claude
MiniMax MiMoV2 GLM DeepSeek Gemini GPT-5.2
Benchmark Step3.5Flash KimiK2.5 Opus
M2.1 Flash 4.7 V3.2 3.0Pro xHigh
Vanilla PaCoRe 4.5
#Activatedparams 11B 10B 15B 32B 37B 32B - - -
#Totalparams 196B 230B 309B 355B 671B 1T - - -
REASONING
AIME2025 97.3 99.9 83.0 95.1* 95.7 93.1 96.1 95.0 92.8 100.0
HMMT2025Feb. 98.4 100.0 71.0* 95.4* 97.1 92.5 95.4 97.5† 92.9† 99.4
HMMT2025Nov. 94.0 97.8 74.3* 91.0* 93.5 90.2 91.1 94.5† 91.7* 97.1*
IMO-AnswerBench 85.4 88.8 60.4* 80.9* 82.0 78.3 81.8 83.3† 84.0† 86.3†
LiveCodeBench-v6 86.4 88.9 75.4* 81.6* 84.9 83.3 85.0 90.7† 84.8† 87.7†
CF-Div2-Stepfun-cpp 86.1 93.3 59.0* 46.9* 74.1* 81.6* 73.6* 83.5* 72.2* -
MMLU-Pro 84.4 84.8 88.0 84.9 84.3 85.0 87.1 90.1† 89.5† 87.4†
GPQA-Diamond 83.5 85.0 83.0 84.1* 85.7 82.4 87.6 91.9 87.0 92.4
HLEtext 23.1 27.9 22.2 22.1 24.8 25.1 31.5 37.7† 30.8† 35.5†
CODEAGENT
SWEVerified 74.4 - 74.0 73.4 73.8 73.1 76.8 76.2 80.9 80.0
SWEMultilingual 67.4 - 72.5 71.7 66.7 70.2 73.0 65.0† 77.5† 72.0†
Terminal-Bench2.0 51.0 - 47.9 38.5 41.0 46.4 50.8 56.9† 59.3† 54.0†
GENERALAGENT
BrowseComp 51.6 - 47.4 45.4 52.0 51.4 60.6 37.8† 37.0† -
BrowseComp(w.CtxManage) 69.0 - 62.0 58.3 67.5 67.6 74.9 59.2† 57.8† 65.8
BrowseComp-ZH 66.9 - 47.8* 51.2* 66.6 65.0 62.3* 66.8* 62.4* 76.1*
GAIA 84.5 - 64.3* 78.2* 61.9* 75.1* 75.9* 76.6* 76.1* 83.5*
xbench-DeepSearch-2505 83.7 - 68.7* 69.3* 72.0* 78.0* 76.7* 78.3* 77.0* 83.0*
xbench-DeepSearch-2510 56.3 - 43.0* 44.0* 52.3* 55.7* 40.0† 57.7* 59.3* 67.0*
RESEARCHRUBRICS 65.3 - 60.2* 54.3* 62.0* 55.8* 59.5* 50.1* 61.6* 57.8*
𝜏2-Bench 88.2 - 86.6* 84.1* 87.4 85.2* 85.4* 90.7 92.5 85.5*
GENERAL
Arena-Hard-v2.0 74.0 93.1 63.1* 68.2* 73.1* 66.0* 85.8* 81.7† 76.7† 80.6†
MultiChallenge 55.7 60.8 50.5* 44.3* 67.8* 57.1* 73.6* 71.8* 65.8* 71.9*
IFBench 67.4 56.8 70.0 64.0† 68.0† 61.0† 72.8* 70.4† 58.0† 75.4†
LONGCONTEXT
LongBenchv2 57.5 62.0 53.9* 60.6† 59.1* 58.4† 61.0 70.0* 67.8* 62.4*
MRCR-8needle 28.8 26.3 20.0† 19.9† 25.4† 27.2† 36.5* 73.0† 54.0* 88.2*
FRAMES-Oracle 76.5 77.2 76.5* 78.0* 75.1* 80.1* 77.4* 79.7* 85.8* 87.3*
RepoQA 88.5 88.7 88.2* 91.2* 89.5* 91.9* 89.8* 91.5* 95.7* 93.8*
Table5: ComparisonbetweenStep3.5Flashandclosed/openmodels. *denotescaseswheretheorigi-
nalscorewasunavailableorinferiortoourreproducedresult;wethereforereportresultsevaluated
underthesametestconditionsasStep3.5Flashforfaircomparison. †indicatesscoresquotedfrom
non-officialsources,includingtechnicalreports,orindependentevaluationplatforms. Ourevaluation
on HLE focuses on the text-only subset. BrowseComp (w. Ctx Manage) denotes the evaluation of
BrowseCompwithaContextManagementenabled.
RLforOpen-WorldAgenticTasks. WhileStep3.5Flashdemonstratescompetitiveperformance
onacademicagenticbenchmarks,thenextfrontierofagenticAInecessitatestheapplicationofRLto
intricate,expert-leveltasksfoundinprofessionalwork,advancedengineering,andscientificresearch.
Solvingthesechallengesisaprerequisitefordeployingagentscapableofgenuineautonomy.
OperationalScopeandConstraints. Step3.5Flashistailoredforcodingandwork-centrictasks,but
mayexperiencereducedstabilityduringdistributionshifts. Thistypicallyoccursinhighlyspecialized
domainsorlong-horizon,multi-turndialogues,wherethemodelmayexhibitrepetitivereasoning,
mixed-languageoutputs,orinconsistenciesintimeandidentityawareness.

Contributors
Thelistingofauthorsisinalphabeticalorderbasedontheirfirstnames.
AilinHuang HongyuanWang MichaelLi XiangfengWang
AngLi HouyongChen MingLi XiangwenKong
AoboKong HuangxiZhu MingliangLi XiangyuLiu
BinWang HuiminWu MingmingZhang XiangyuZhang
BinxingJiao HuiyongGuo MingruiChen XiaoboYang
BoDong JiaWang MittHuang XiaojiaLiu
BojunWang JianZhou NaWang XiaolanYuan
BoyuChen JianjianSun PengLiu XiaoranJiao
BrianLi JiaorenWu QiHan XiaoxiaoRen
BuyunMa JiaranZhang QianZhao XiaoyunZhang
ChangSu JiashuLv QinglinHe XinLi
ChangxinMiao JiashuoLiu QinxinDu XinLiu
ChangyiWan JiawenLuo QiupingWu XinWu
ChaoLou JiayiFu QuanSun XingChen
ChenHu JiayuLiu RongqiuYang XingpingYang
ChenXu JieCheng RuihangMiao XinranWang
ChenfengYu JieLuo RuixinHan XuZhao
ChengtingFeng JieYang RuosiWan XuanHe
ChengyuanYao JieZhou RuyanGuo XuantiFeng
ChunruiHan JieyiHou ShanWang XuedanCai
DanMa JingBai ShaoliangPang XuqiangZhou
DapengShi JingchengHu ShaowenYang YanboYu
DaxinJiang JingjingXie ShengjieFan YangLi
DehuaMa JingweiWu ShijieShang YangXu
DeshanSun JingyangZhang ShiliangYang YanlinLai
DiQi JishiZhou ShiweiLi YanmingXu
EnleLiu JunfengLiu ShuangshuangTian YaoyuWang
FajieZhang JunzheLin SiqiLiu YeqingShen
FanqiWan KaManLo SiyeWu YiboZhu
GuanzheHuang KaiLiang SiyuChen YichenLv
GulinYan KaiboLiu SongYuan YichengCao
GuoliangCao KaijunTan TianchengCao YifengGong
GuopengLi KaiwenYan TianchiYue YijingYang
HanCheng KaixiangLi TianhaoCheng YikunYang
HangyuGuo KangAn TianningLi YinZhao
HanshanZhang KanghengLin TingdanLuo YingxiuZhao
HaoNie LeiYang WangYou YinminZhang
HaonanJia LiangLv WeiJi YitongZhang
HaoranLv LiangZhao WeiYuan YixuanZhang
HebinZhou LiangyuChen WeiZhang YiyangChen
HekunLv LieyuShi WeiboWu YongchiZhao
HengWang LiguoTan WeihaoXie YongshenLong
Heung-YeungShum LinLin WenSun YongyaoWang
HongboHuang LinaChen WenjinDeng YousongGuan
HongboPeng LuckMa WenzhenZheng YuZhou
HongyuZhou MengqiangRen WuxunXie YuangPeng

YuanhaoDing YulingZhao ZexiLi ZhihengHu
YuantaoFan YunzhouJu ZheXie ZidongYang
YuanweiLu YurongZhang ZhengGe ZiliWang
YuanzhenYang YushengLi ZhengGong ZiqiRen
YuchuLuo YuxiangYang ZhengZeng ZixinZhang
YudiZhao YuyangChen ZhenyiLu ZixuanWang
YuePeng YuzhuCai ZheweiHuang
YueqiangLin ZejiaWeng ZhichaoChang
YufanLu ZetaoHong ZhiguoHuang

## Appendix
A. Architecture Details
Table6summarizeskeyarchitecturehyper-parametersofStep3.5Flash.
Hyper-Parameter Value
BACKBONE
Vocabularysize(𝑉) 128,896
Modelwidth(𝑑 ) 4096
model
Transformerblocks 45(3dense+42MoE)
MOE FFN
ExpertsperMoEblock 288+1shared
Routing top-𝑘=8
DenseFFNhiddensize 11,264
MoEexperthiddensize 1,280
ATTENTION
Hybridblockstructure 3SWAblocks+1fullattentionblock
SWAwindowsize 512
KVheads(GQA) 8
Queryheads(full/SWA) 64/96
GateType head-wiseonoutput
Headdimension 128
RoPE𝜃 10,000
RoPEdims(full/SWA) 64/128
MULTI-TOKEN PREDICTION
MTPblocks 3(DenseSWA)
PARAMETER COUNTS
Totalparams(backbone) 196B
Activatedparams/token(backbone) 11B
Totalparams(withMTP3) 198B
Activatedparams/token(withMTP3) 13B
Table6: Keyarchitecturehyper-parametersofStep3.5Flash. “Activatedparams”arereportedper
tokenandexcludeembedding/outputmatrices.
A.1. Head-wiseGatedAttention
Eachattentionheadisassignedalightweight, input-dependentscalargate, allowingthemodelto
dynamically modulate information flow across the hybrid layout with negligible computational
overhead.
Formally,fora(single)headofdimension𝑑,let𝒒
𝑖
,𝒌𝑗,𝒗𝑗 ∈ R𝑑 denotethequeryvectoratposition𝑖and
thekeyandvaluevectorsatposition 𝑗,thescaleddot-productscores𝑠,thecorrespondingattention
weights𝛼andtheoutputs 𝒚 arecomputedasfollows:
√
∑︁ ∑︁
𝑠 𝑖,𝑗 =⟨𝒒 𝑖 ,𝒌𝑗 ⟩/ 𝑑, 𝑍 𝑖 = exp(𝑠 𝑖,𝑗′ ), 𝛼 𝑖,𝑗 =exp(𝑠 𝑖,𝑗 )/𝑍 𝑖, 𝒚 𝑖 = 𝛼 𝑖,𝑗𝒗𝑗. (4)
𝑗′ 𝑗

Giventheinputrepresentation 𝒙𝑖 atposition𝑖,wecomputeahead-wisegate𝑔 𝑖 tomodulatethehead
output:
𝑔 𝑖 =𝜎(𝒘 ⊤ 𝑔𝑎𝑡𝑒 𝒙𝑖 ), 𝑜g 𝑖 ate =𝑔 𝑖 𝒚 𝑖 , (5)
where𝜎(·) isthesigmoidfunctionand𝒘𝑔𝑎𝑡𝑒 isalearnablevector.
Head-wisegatedattentioncanbeviewedasintroducinganinput-dependentsinktoken[33]intothe
attentionmechanism. Substituting𝜎(𝑔) = 1 intoEquation5,wehave
1+exp(−𝑔)
𝒐 g
𝑖
ate = ∑︁
𝑍
e
𝑖
x
+
p
𝑒
(
−
𝑠 𝑖
𝑔
,
𝑖
𝑗
𝑍
)
𝑖
𝒗𝑗, (6)
𝑗
whereexp(−𝑔 𝑖 )𝑍 𝑖actsasaninput-dependentsinkmassinthesoftmaxnormalizer. AsshowninSection2.3,
thisadaptiveformulationconsistentlyoutperformsfixed(input-independent)sinktokens.
A.2. SpeedBenchmarkofAttentionEnhancements
WeconductsimulationswithMTP-3toevaluatethelatencyoverheadsofthetwoenhancementsunder
anidealworkload. Table7presentstherelativeincrementoftheoreticalFLOPsandlatency. Increasing
thenumberofqueryheadsinSWAslightlyraisestheFLOPsbuthaslessimpactonlatency. Thisisdue
toaquery-to-𝑘𝑣ratioof12,whichkeepsSWAintheIO-boundregion,evenwhenconsideringMTP-3.
Forhead-wisegating,neitherFLOPsnorlatencyhasnoticeabledifferencebecauseofitslightweight.
SWA Decode(FLOPs/Lat.) Prefill(FLOPs/Lat.)
Backbone Setting
Heads
64k 256k 64k 256k
## 64 nogate 1.00/1.00 1.00/1.00 1.00/1.00 1.00/1.00
Step3.5Flash 96 nogate 1.02/1.01 1.01/1.00 1.08/1.06 1.04/1.03
(𝑆3𝐹1layout) 64 head-wise 1.00/1.00 1.00/1.00 1.00/1.02 1.00/1.01
## 96 head-wise 1.02/1.02 1.01/1.00 1.08/1.08 1.04/1.05
Table7: RelativeincrementunderdifferentSWAheadcountsandgatingstrategies. Themetricsare
presentedasFLOPs/Latency. Thebaselineconfiguration(firstline)isnormalizedto1.0.
SWA Decode Prefill
Backbone Layout
Heads
64K 256K 64K 256K
𝑆3𝐹1 64 1.00 1.00 1.00 1.00
𝑆3𝐹1+Head
96 1.02 1.01 1.08 1.04
Step3.5Flash
𝑆1𝐹1 64 1.18 1.47 1.38 1.71
𝐹𝐹𝐹𝐹 64 1.51 2.33 2.07 3.00
𝑆3𝐹1 32 1.00 1.00 1.00 1.00
𝑆3𝐹1+Head
48 1.02 1.01 1.05 1.02
Internal30B-A3B
𝑆1𝐹1 32 1.42 1.74 1.50 1.80
𝐹𝐹𝐹𝐹 32 2.21 3.16 2.47 3.34
Table8: RelativeFLOPscostacrossdifferentbackbonesandattentionpatterns. Theheadcountrefers
toSWAheads. Foreachbackbone,theconfigurationwithminimumFLOPs(𝑆3𝐹1withreducedheads)
isthebaseline(1.0).

A.3. MetaToken
Recentliterature[163–165]hasshownboththeoreticallyandempiricallythatpre-pendingstructured
metadata to pre-training sequences can improve data efficiency and accelerate convergence: by
exposinghigh-levelattributes(e.g.,modality,language,domain),metadataprovidesglobalcuesthat
reduceuncertaintyabouttheupcomingcontentandthusmakesnext-tokenpredictioneasier.
Motivated by this paradigm, we associate each training example with a metadata string M in a
human-readableformat,includingcontenttype(e.g.,Code,Book,Paper,Web),language(e.g.,EN,ZH),
domain,andsource. WethenprependMtotheoriginaltokensequencex,formingasingletraining
sequences = [M;x]. Duringpre-training,themodelistrainedtomaximizethelikelihoodofs:
|s|
∑︁
L full (𝜃) =− log𝑃 𝜃 (𝑠 𝑡 | s<𝑡 ). (7)
𝑡=1
Afteraninitialphaseofapproximately3.8Ttokens,wekeepMinthecontextbutmaskoutitspositions
fromthelosswhilecontinuingtopredictthepayloadtokens:
|s| |x|
∑︁ ∑︁
L mask (𝜃) =− log𝑃 𝜃 (𝑠 𝑡 | s<𝑡 ) =− log𝑃 𝜃 (𝑥 𝑡 | M,x<𝑡 ). (8)
𝑡=|M|+1 𝑡=1
We hypothesize that by this stage the model has already learned to effectively use metadata as a
conditioningsignal. Maskingthemetadatalossthereforeallocatesoptimizationpressureentirelyto
thepayloadtokens,whilestillbenefitingfromtheexplicitconditioningondatacharacteristics.
A.4. Pre-trainingAblationsDetails
We conduct controlled pre-training ablations to isolate the effects of (i) different hybrid attention
layoutand(ii)sinktokensversushead-wisegatedattention.
Hybridattentionlayout. Weadopta30B-A3BMoEarchitecturetoevaluatethedownstreamimpact
ofdifferenthybridattentionlayoutunderafixedtokenbudget. Thetrainingfollowsastrict,multi-
stage pipeline: a 30B-token warmup phase, followed by 1T tokens of main pre-training, a 300B-
token cooldown phase, and an additional 100B-token long-context specialization stage—totaling
approximately1.4Ttokens. Supervisedfine-tuning(SFT)isthenperformedona0.1×downsampled
dataset. FulltrainingdetailsareprovidedinTable9.
Gatevs. sink(scaledsetting). Wepre-traina100B-A10BMoEmodelfor∼250Btokenstocompare
sinktokensandhead-wisegatingunderalarger-scaleregime.
Pre-training results of the architectural ablations are presented in Tables 2 and 10. We employ the
evaluation protocols detailed in Section 6.1. Specifically, GPQA [142] is evaluated using 5-shot
prompting,whileHumanEval[166]andMBPP[167]utilize3-shotprompting.
Thepost-trainingresultsinTable1areaggregatedasfollows:
• Reasoning: TheaverageofMMLU-Pro[139],GPQA-Diamond[142],LiveCodeBenchv6[12],and
LiveBench[168].
• Math: TheaverageofAIME2024[169],AIME2025[170],HMMT2025Feb.[171],andCNMO20246.
• Code: TheaverageofCF-Div2-StepfunandLiveCodeBenchv6[12].
6https://www.cms.org.cn/Home/comp/comp/cid/12.html

Hyper-Parameter 100B-A10B 30B-A3B
TotalTokens 250B 1.4T
Optimizer Muon[34]
Peaklearningrate 1.31×10−4 1.1×10−3
Batch-sizewarmup - First30Btokens
Layers 43 48
Dimension 4096 2048
LeadingDenseLayers 1 1
RoutedExperts 96 128
ActiveExperts 4 8
SharedExperts 1 1
LoadBalancingMethod LossFree[64]
Attentionmodule GQA8
SequenceLength 4096
VocabSize 129280
BatchSize 8192 16384
WeightDecay 0.1
PartialRoPE Disabled Enabled
MTP Enabled Disabled
Table9: Trainingconfigurationforthe100B-A10Bandthe30B-A3Barchitectureablationsuite.
• Sci: RepresentedbyGPQA-Diamond[142].
• General: The average of IFEval [172], IFBench [156], WildBench [173], Arena-Hard [155], and
MultiChallenge[157].
• LongCtx: Theaverageofsixbenchmark-levelaverages: (i)theaveragescoreacrosscontextlengths
8k-128k on RULER [174], (ii) the average score over the Short and Medium subsets of Long-
Benchv2[158],(iii)theaveragescoreacrosscontextlengths8k-128konHELMET[175],(iv)GSM-
Infinite[176],(v)theoverallscoreonFRAMES[160],and(vi)theoverallscoreonRepoQA[161].
Tables1and10showthatthevanilla𝑆3𝐹1layoutunderperformsthefull-attentionbaselineongeneral
pre-training benchmarks and consistently degrades SFT quality (e.g., BBH: −4.3; SFT Avg: −0.7).
IncreasingthenumberofSWAqueryheadssubstantiallyclosesthisgap(e.g.,MMLU-Pro: +3.7;SFT
Reasoning: +0.4),withonlyaminorregressiononSFTCode(−0.6),whilematchingorexceedingthe
full-attentionbaselineonseveralmetrics. Table2furtherdemonstratesthathead-wisegatedattention
yieldsanaverageimprovementfrom62.5to64.4(+1.9)onthesinktokenmetric.
B. Detail Analysis of Localized Activation Blow-up
Toinvestigatetherootcauseofthelocalizedactivationblow-up,weanalyzethetokensthattrigger
the largest expert activations across all layers, and identify two distinct large activation patterns:
(1) Specific lexical items, such as special tokens and punctuation, commonly elicit large but not
dramaticactivations,particularlyintheshallowerlayers. Thispatternisnotrecognizedasafailure
modebyus,asthereisnorapidincrementanditmayserveasaninternalmechanismforsemantic

SWA Pre-trainEvaluation
Layout
Heads
BBH MMLU MMLU-Redux MMLU-Pro SimpleQA GSM8K MATH HumanEval MBPP C-EVAL CMMLU Avg.
𝐹𝐹𝐹𝐹 32 66.0 64.5 69.7 35.7 7.2 70.0 39.2 48.8 53.4 69.7 70.5 54.1
𝑆1𝐹1 32 64.1 64.7 69.8 37.7 7.5 70.1 43.9 47.0 56.2 69.8 69.8 54.6
𝑆3𝐹1 32 61.7 64.2 69.4 33.7 8.0 67.4 41.5 47.6 56.0 69.5 70.9 53.6
𝑆3𝐹1+Head 48 65.3 65.9 71.0 37.4 7.5 72.2 44.5 48.8 58.6 70.2 71.0 55.7
Table10: Pre-trainingevaluationresultsforhybridattentionlayoutablations(𝑊=512)on30B-A3B.
𝐹 denotes full attention and 𝑆 denotes SWA; 𝑆3𝐹1 indicates three 𝑆 and one 𝐹 in the hybrid layout.
𝑆3𝐹1 +Head increasesthenumberofSWAheadsfrom32to48.
modeling[60,177]. Anotherpatternisthat(2)somehigh-frequencybi-gramstriggerextremelylarge
activationsonthefirsttoken, whichrepresentsthefailuremodeweareinvestigating. Thepattern
istriggeredbyseveralfactors: Thefrequencyofabi-gram’soccurrenceissufficientlyhigh,andthe
MoE FFN is fine-grained enough, allowing an expert to specialize in that bi-gram without being
regulatedbytheloadbalancingmechanism. Thisspecializationservesasashortcut: oncetheexpert
isactivated,theoutputbecomesdeterministic,andothernetworksnolongerinfluencetheprediction.
Whilefindingshortcutsisareasonableapproachtominimizingloss,inaMoEmodelwithapre-norm
architecture[76,77],thereisastraightforward,pathologicalsolutionforachievingsuchdeterministic
predictions,asoutlinednext. Themodel’sfinalrepresentationisthesumoftheoutputsfromalllayers,
followedbyaRMSNorm. Thiscanbeexpressedasacombinationoftheoutputsfromtheexpertsand
theattentionlayers:
𝐿
∑︁ ∑︁
𝒉
final
=RMSNorm(ex
(cid:32)(cid:32)(cid:32)
p
(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)
e
(cid:32)
rt
o(cid:32)u(cid:32)(cid:32)(cid:32)t(cid:32)(cid:32)l(cid:32)(cid:32)i(cid:32)er
+ attn𝑙 + expert
𝑙,𝑒
), (9)
(cid:124) (cid:123)(cid:122) (cid:125) 𝑙=1 𝑙,𝑒
𝒉outlier (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32) ( (cid:32)(cid:32) 𝑙 (cid:32)(cid:32) , (cid:32) 𝑒 (cid:32)(cid:32) ) (cid:32)(cid:32)(cid:32)(cid:32) i (cid:32) s (cid:32)(cid:32) not (cid:32)(cid:32) a (cid:32)(cid:32)(cid:32)(cid:32) o (cid:32)(cid:32)(cid:32) u (cid:32)(cid:32)(cid:32) t (cid:32)(cid:32) l (cid:32) i (cid:32)(cid:32) e (cid:32)(cid:32) r (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)
(cid:124) (cid:123)(cid:122) (cid:125)
𝒉others
whereattn,MoE,expertrepresenttheoutputhiddenstatesoftheirrespectivemodules,while 𝐿and 𝐸
denotethenumberoflayersandexperts,respectively. Thestraightforwardsolutionistoboundlessly
enlargeexpert ,then
outlier
RMSNorm(𝒉 ) = limRMSNorm(𝑐·𝒉ˆ +𝒉 ) =RMSNorm(𝒉 ), (10)
final outlier others outlier
𝑐→∞
wherewedecouple𝒉 tothemagnitude𝑐andtheunitvector𝒉ˆ denotingthedirection.
outlier outlier
SwiGLU[78],theexpertarchitectureinStep3.5Flash,providesawaytogeneratelargeoutputs,even
whentheweightdecayeffectivelysuppressestheweightnorms. SwiGLUisdefinedasfollows:
(cid:0) (cid:1)
SwiGLU(𝒙) =𝑾 SiLU(𝑾 𝒙)·𝑾 𝒙 . (11)
down gate up
We analyze the activation norms of 𝑾 𝒙 and 𝑾 𝒙 and find no significant differences between
gate up
outlierexpertsandnormalexperts. However,theelement-wiseproductproducesabnormaloutputs,
whichhave
∥SiLU(𝑾 𝒙)∥·∥𝑾 𝒙∥ ≈ ∥SiLU(𝑾 𝒙)·𝑾 𝒙∥, (12)
gate up gate up
inoutlierexperts. ItcanbeachievedonlyifSiLU(𝑾 𝒙)and𝑾 𝒙arehighlyalignedandconcentrate
gate up
onaverylimitednumberofdimensions. Consequently,onlyalimitednumberofrowsfrom𝑾 are
up
utilizedduetothesparseinput. Thisobservationleadsustopreferactivationclippingoverweight
clipping,asactivation’snumericalpropertydirectlycontributetotheblow-upandthesparsity,and
activation clipping can promptly address these issues. Besides, activation clipping has negligible
negativeeffects,aswell-behavedactivationsrarelyexceedthethreshold.

WhenusingtheMuonoptimizer,gatedlinearunits,suchasSwiGLU,aresusceptibletologitexplosion.
Thisvulnerabilityarisesfromsimilarmechanismsthatcauseexplosioninattention,asreportedin[5].
Foranoutlierexpertspecializedtosomespecificbi-gram,hiddenstatesroutedtoitareexpectedtobe
closelyalignedtoitsrouterembedding. Wevalidatethisbyinputtingtherouterembeddingintoa
outlierexpertanddirectlypredictingoutputsbasedonthisexpert’soutput. Thepredicteddistribution
aligns with that of the real data and the entire network’s performance. Combined with the overly
singletrainingtarget(topredictthesecondtokeninthebi-gram),wearguethatgradientsw.r.t. the
outlierexpert’sparameters,𝑾 ,𝑾 and𝑾 ,arenotonlyabnormallylowrank(denotedas𝑟),
gate up down
butalsoconsistentlypointinadirectionthatemphasizesthemagnitudeasanalyzedinthefirstfactor,
withoutrotation. Lettheupdatematricesofaparametermatrix𝑾 ∈ R𝑁×𝑁 tobe
𝑟 𝑁
∑︁ ∑︁ ∑︁
Δ𝑾 = 𝜎 𝑖𝒖𝑖𝒗 ⊤
𝑖
= 𝜎 𝑖𝒖𝑖𝒗 ⊤
𝑖
+ 𝜎 𝑗𝒖𝑗𝒗 ⊤
𝑗
(13)
𝑖 𝑖=(cid:32)(cid:32)1(cid:32)(cid:32)(cid:32)(cid:32) (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32) 𝑗= (cid:32) 𝑟 (cid:32)(cid:32) + (cid:32)(cid:32)(cid:32)(cid:32) 1 (cid:32) (cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)(cid:32)
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
lowranksignal noise
Accumulatingupdatesoveroptimizationstepswillrapidlyincreasethesingularvalueofthelow-rank
signals,resultinginanexplosionoftheweightparameter. IntheGLUstructure,∥SiLU(𝑾 𝒙)·𝑾 𝒙∥
gate up
squaresthespectralnorminourstrongalignmentcase,makingtheprogressmoresharp. Additionally,
Muon completely eliminates the influence of gradient magnitudes. During the blow-up process,
RMSNorm reduces the gradients of large inputs. When using the Adam optimizer, its 𝜖 acts as a
threshold to filter out small gradients during the learning rate adaptation, which can hinder the
progress. In contrast, Muon consistently and effectively orthogonalizes the gradients, resulting in
moreaggressiveupdates.
C. Step Pre-training Data Foundation
C.1. KnowledgeDataConstruction
C.1.1. StepCrawl
Beyond standard web-scale datasets (e.g., CommonCrawl), we develop StepCrawl, an in-house
crawlingandcurationsystemdesignedtoacquirehigh-qualityanddiversetokensatscale. StepCrawl
servesasaprimarydatasourceforbothhigh-signalwebpagesanddocument-likecontent(notably
PDFs),whichfrequentlycontainlong-form,high-information-densitymaterial.
AkeycomponentofStepCrawlisasiteandURLselectionlayerpoweredbyaWebOrganizer-style
model[178]. WeadaptthecapabilitiesintroducedinWebOrganizerandfurtherfine-tuneaversion
tailoredtoourpipeline. Duringcrawling,eachfetchedwebpageisanalyzedbythismodel,forming
alightweightLM-in-the-loopfeedbackcyclethat(i)filtersSEO-drivenandotherlow-utilitypages,
and(ii)guidescrawl-budgetallocationbybalancingsitecategories(e.g.,preventingdisproportionate
crawling of tool and e-commerce sites) to preserve corpus diversity and reduce topical skew. In
practice,StepCrawlprocessesontheorderof∼1Bpagesperdayunderthisquality-anddiversity-
awareschedulingpolicy.
robots.txt
Allcrawlingactivitiesstrictlyadhereto andsite-specificaccesspolicies. Thecollected
contentissubsequentlypassedthroughamulti-stagefilteringprocess(qualityscoring,deduplication,
andsanitization),ensuringthatonlyhigh-utilityandpolicy-compliantdataareretainedfortraining.

C.1.2. QualityRefinementandStratification
Qualitystratification. InspiredbyNemotron-CC[179]-stylequalitybucketing,wedividetheinternal
webdataintoqualitytiersandsamplepreferentiallyfromhighertiers. Welabeleachdocumentusing
anensembleofsixlightweightscorers/classifiersandensemblethetierassignmentsacrossscorers.
Inthefinalrecipe,wekeepHigh/Medium-High/MediumanddiscardMedium-Low/Low,which
substantiallyimprovestokenefficiencyinablations. Forbookandpapercorpora,weapplythesame
stratificationbutrestrictretentiontoHigh/Medium-Hightiersexclusivelyduringtheannealingstage
tomaximizediversity. Inadditiontothesharedsix-scorerensemble,weintegrateadditionaldomain-
specific filters targeting STEM and knowledge-dense content, and down-sample overrepresented
domainstoensurebalancedrepresentation.
Embedding-basedclusterrebalancing. Weleverageembedding-basedcorpusbalancingasaprin-
cipled way to further reduce redundancy and mitigate distribution skew. Specifically, we embed
large-scaleChinese/Englishwebdata,runk-meansclustering(100k+clusters),anddown-sample
clusterswithdisproportionatemass. Inablations,thiscluster-levelrebalancinginthecooldownstage
improvesabroadsetofbenchmarks.
Knowledge-Intensive Mining and Augmentation. We construct a dedicated knowledge subset
using a lightweight two-stage pipeline built on the shared embedding representation described
above. First, a curated inventory of high-value entities, concepts, and relations is used to retrieve
knowledge-densedocumentsandpassagesfromthefullcorpusinembeddingspace;thesecandidates
arerankedbyaknowledge-densitymodelandsimplecoverageheuristics. Second,foraportionofthe
retrievedcontent,weapplytargetedtransformationssuchascontrolledrephrasingandQAsynthesis
toimprovelearnability. Theresultingsamplesaremixedbackintothetrainingmixturetoincrease
effectiveknowledgesignaldensity. Weobserveconsistentgainsfromthispipelineinablations,while
adetailedcausalanalysisofitsbenefitsisleftforfuturework.
C.2. CodeData
C.2.1. Pure-Code
We refine our internal programming dataset using a modified version of the OpenCoder filtering
rules[80],introducingacalibratedrelaxationtobalancedataqualityanddiversity. Inourpipeline,
applyingOpenCoderfiltersgeneratesasetof“hits”foreachdocument,whereeachhitrepresentsa
violationofaheuristicrule(signalingpotentialnoise). Wecategorizethecorpusbythesehitcounts:
hit0 hit1
forcleandocuments(zeroviolations), foroneviolation,andsoon.
hit0
Ourinternalablationsrevealaclearquality-diversitytrade-off: strictfiltering(e.g., -only)over-
hit0–6
prunesthecorpus,whilenofilteringintroducesexcessivenoise. Wefindthatthe configuration
(acceptingdocumentswithupto6violations)yieldsthebestoverallbenchmarkperformance,retaining
awidervarietyofhigh-signalcodecomparedtotheoriginalstrictconstraints.
C.2.2. PR/Issue/CommitData
To enhance software engineering capabilities, we construct a comprehensive dataset from GitHub
repositories with over 10 stars, comprising PRs, issues, and commits. We apply strict filtering on
repository popularity and content quality, and use LLMs to generate missing issue descriptions,
resultingina5-million-samplefoundation. Fromthis,wederivefourtrainingsubsets:

(1) Base PR/Issue/Commit Data: We crawl data via GHArchive and GitHub API, including full
git diff
commit histories. We extract changes and validate a small portion of samples against
groundtruth,thenfilterto20+mainstreamlanguages(e.g.,Python,Java,C++). Westrictlydeduplicate
againstSWE-BenchVerified[13]andSWE-BenchMultilingual[14]topreventleakage.
(2)ConcatenatedPR-DialogueData(90Btokens): Wegenerate90Btokensofcode-editingtraining
databyapplyingtwoAgentless-inspiredtemplates[82]: (1)Filelocalization: Givenaproblemdescrip-
tionandrepositorystructure,identifytargetfilepaths;(2)Coderepair: Givenaproblemdescription
andfilecontent,generateprecisemodificationsviaSEARCH/REPLACEblocks.
Weintegratethis90Bcode-editingdataintotwotrainingphaseswithphase-specificmaskingstrategies.
Intheannealingstageofpre-training,onlytemplatescaffoldingismasked;inmid-training,thedatais
convertedtochatdialogswithuserpromptsmasked. Internalablationsshowconsistentgainsover
SWE-BenchVerifiedandSWE-BenchMultilingualinthecooldownstageandmid-training.
(3)RewrittenReasoning-OrientedData(12Btokens): FromthePythonsubsetofourbasedataset,we
derivebug-fixsamplesviaLLMchange-typeannotation. Weapplytwoconciserewritingstrategies:
(1)Reasoningreconstruction: anLLMreconstructsthePRauthor’sproblem-solvingprocess(problem
analysis, root cause identification, solution design, and code implementation), injected into PR-
Dialogueformat. Hallucinated/inconsistenttracesarefilteredviarule-basedandLLMverification.
(2) Active Reading notebooks: PR/issue/commit data is converted into structured learning outlines
(motivation,rootcauses,designdecisions,insights),thensynthesizedintocoherenttechnicalnotes.
Theserewrittendatasets(∼12Btokens)areincorporatedduringmid-training,yieldingfurthergains
onSWE-BenchVerified.
(4)Environment-basedSeedData. WecurateexecutableenvironmentsderivedfromrawPR,issue,
andcommitrecordsusingtheenvironmentbuildingpipelinedescribedinAppendixE.2.2. Candidate
samplesarerigorouslyfilteredtoensuretest-patchinclusionandvalidatedviastrictrule-basedcriteria
toguaranteeenvironmentalreproducibility. Furthermore,selectedissuesundergotargetedrewriting
to augment data quality and coverage. The resulting dataset comprises hundreds of thousands of
seedsamples, includingproblemdescriptions, codechanges, andtestfunctions, andservesasthe
foundationalbedrockforenhancingagenticcodingcapabilities,drivingsignificantperformancegains
indownstreamagenttasks.
C.3. Mathematics&STEMData
To enhance reasoning capabilities and elicit intelligence from knowledge, we curate a large-scale
mathematicsandSTEMdataset. BeyondthestandardCommonCrawldatausedinpriorworks[180,
181],weleverageourin-houseStepCrawlsystemtoharvestamassivescaleofadditionalmathematics-
relateddata. Specifically,weimplementafilteringpipelineinspiredbyMegaMath[181],utilizingan
ensembleofinternalclassifiersalongsideFineMath[182]. Thisallowsustoretainhundredsofbillions
of mathematics-related tokens distinct from Common Crawl. We further collect a diverse 100M-
sampleeducationaldatasetencompassingexercises,quizzes,andinstructionalcontent. Thiscollection
bridgesthegapbetweenacademictheoryandprofessionalapplication,coveringdomainsfromK-12
mathematics/physics/chemistryandhumanitiestoadultvocationalexams(CPA,Legal). Early-stage
experimentsconfirmthatthisproblem-solvingdataiscrucialforoptimizingtokenefficiencyduring
pre-training.

C.4. DataInfrastructure
Ourdataconstructionandcurationpipelinerunsonahigh-throughputin-housedatainfrastructure
system designed for large-scale deduplication, mining, and model-inference filtering. We operate
Spark Ray
hybrid CPU/GPU clusters with distributed frameworks such as and to execute both
large-volumeprocessing(e.g.,minhash-baseddeduplication)andmodel-drivencurationworkloads
(e.g.,embeddinggenerationandclassifier/LMinference),backedbyastoragelayerspanningobject
HDFS JuiceFS
storage(OSS), ,and forefficientreads/writesofrawcorporaandintermediateartifacts.
C.5. DataAblationsSetting
To rigorously assess data quality and the impact of curation strategies, we conduct an extensive
ablation suite using the 30B-A3B MoE architecture trained with the Muon optimizer, consistent
with the mainline settings (Table 9). Adhering to a strict token efficiency protocol, we set a fixed
trainingbudgetforallexperiments. Modelsareevaluatedonthecomprehensivebenchmarkslistedin
Section6.1,alongsideaseriesofcarefullydesignedheld-outcompression(perplexity)testsets. We
observethatcompressionmetricsoftenprovideamoredirectmeasureofknowledgecapacity,offering
signalscomplementarytomainstreambenchmarks.
Internalexperimentsonthe30B-A3BMoEmodeldemonstrateitssuperiorperformanceandstability
compared to smaller proxies. While smaller models are computationally cheaper, they often fail
to capture the nuances of complex reasoning and lack the capacity to memorize long-tail patterns,
leading to an artificial bias towards data repetition. Empirically, the 30B-A3B size offers stronger
stabilityandbetterfidelitytofull-scaletrends.
D. Post Training Details
Thissectiondescribesthepost-trainingprocessthatrefinesthebasemodelintoahigh-performance
agenticsystem,coveringSFTwithrigorousdataprocessingandqualitycontrol,followedbylarge-scale
RLtofurtherimprovereasoning,tooluse,andgeneralization.
D.1. SFTDetails
D.1.1. SFTDataProcessingPipeline
Acrossalldomains,weapplyaunifieddataprocessingpipelinethatemphasizesanswerverifiability,
reasoning quality, and execution realism. To ensure overall data integrity, the aggregated dataset
undergoesastricttwo-stagefiltrationprocess:
## 1. Rule-basedFiltering: Weeliminatelow-qualitydataexhibitingdegeneratepatterns,suchas
infiniterepetition,harmfulcontent,andpersonallyidentifiableinformation.
## 2. Model-based Filtering: We utilize specialized models to detect and filter out linguistically
inconsistentdata. Byidentifyingandremovingsampleswithunnaturallanguagemixing,we
significantlyrefinethedataset’slinguisticpurityandoverallquality.
## 3. Decontamination: Weconductcomprehensivebenchmarkdecontaminationtopreventtestset
leakage. Thisinvolvesbothexactmatching(withdigitmaskingtocatchnumericalmodifications)
and 𝑁-grammatching.
Thisprocessyieldsafinalrefineddatasetof871ksamples,totaling7.23Btokens.Thedetaileddistribu-
tionoftheSFTdataispresentedinTable3.

D.2. RLDetailsandAblations
Thissectiondetailsthelarge-scaleRLpost-training,coveringdatacuration,asynchronoussearch-agent
training,andablationsondenseandMoEmodels.
D.2.1. DataCuration
WecuratetheRLtrainingdatasetbyaggregatingproblemsfromopen-sourcecollectionsandcompeti-
tionarchivesspanningcompetitivecoding,STEM,andsyntheticdataforgeneralRLVRtraining. To
preventdatacontamination,westrictlyexcludeproblemsfromcompetitionsheldduring2024–2026.
Thedatasetisfurtheraugmentedwith: (i)syntheticarithmeticproblemsinvolving11–13digitintegers;
(ii) a generator–validator pipeline that synthesizes additional test cases for coding tasks; and (iii)
syntheticenvironmentsforgeneralreasoningtasks,suchaspuzzleandinstructionfollowing.
We apply a two-stage filtering process. First, deterministic rule-based pruning removes prompts
containingimages,externallinks,oropen-endedrequirementswithoutauniquefinalanswer. Second,
an accuracy-based filter excludes trivial or degenerate problems. During training, each batch is
constructedbysamplingfromdifferentdomainsaccordingtopredefinedsamplingprobabilities.
D.2.2. RewardSystem
VerifiableRewards. ForSTEMtasks,weemploygpt-oss-120b[33]astheverifiermodel,usingthe
followingstructuredprompt(originallyinChinese)torigorouslyassessfinal-answercorrectness. For
codingtasks,weutilizesandboxestovalidatecodeexecutionagainsttestcaseswithsoftreward.
You are a strict grader. Below you are given the problem, the student’s answer, and the
reference answer. Please determine whether the student’s answer is correct according to
the rules below.
Grading procedure:
## 1. Overall check: If the student’s response is incomplete, lacks a clear final answer,
or contains repeated content multiple times → mark as incorrect.
## 2. Final-answer match: Extract the student’s explicit final answer and compare it with
the reference answer:
• If they are exactly equivalent semantically or mathematically → proceed to process
check.
• If numerical computation is involved and the discrepancy is solely due to rounding
→ proceed to process check.
• Otherwise → mark as incorrect.
## 3. Process check: Carefully verify each reasoning step:
• If there are errors, contradictions, obvious irrelevance to the problem, or
the student merely copies the prompt without a substantive solution → mark as
incorrect.
• If the solution process is correct, clear, and consistent → mark as correct.
## 4. Format requirements: If the problem requires a specific format (e.g., units,
step-by-step answers, or explicit equations) and the student does not satisfy it → mark
as incorrect.
## 5. Multiple sub-questions: If the problem contains multiple sub-questions, the student
must answer all of them correctly to be marked correct.
## 6. Other cases: If the above rules do not cover the situation, make an overall judgment
from the perspective of whether the student truly knows how to solve the problem.
Output requirement:
Your final output must be strictly one of the following:
• <correct> True </correct>
• <correct> False </correct>
Now begin:
<question>
{question}
</question>
<student_answer>
{student_answer}
</student_answer>
<reference_answer>
{reference_answer}
</reference_answer>

0.48
0.44
0.40
0.36
0.32
0 200 400 600 800 1000 1200
Training Step
draweR
0.20
0.16
0.12
0.08
0.04
0 200 400 600 800 1000 1200
Training Step
oitaR
tpeccA
llA
0.45
0.30
0.15
0.00
0 200 400 600 800 1000 1200
Training Step
mroN
darG
rotcA
MIS-PO GSPO PPO
(a)Comparisononthedensemodel. WhileGSPOalsoeffectivelyreducesthevarianceoftheactorgradient
norm,itsefficiencyisinferiortothatofMIS-PO.Underthesameiterationbudget,MIS-POachieveshigher
rewardsandallacceptanceratio.
0.64
0.56
0.48
0.40
0.32
100 200 300
Training Step
draweR
0.20
0.16
0.12
0.08
100 200 300
Training Step
oitaR
tpeccA
llA
1.0000
0.9975
0.9950
0.9925
0.9900
100 200 300
Training Step
/
mllv
dlo
MIS-PO GSPO
(b)ComparisonontheMoEmodel. (1)Efficiency: MIS-POdemonstratessuperiorsampleefficiency,achieving
higherrewardswithacceleratedconvergence,whereasGSPOplateausarounditeration200. (2)Stability: GSPO
exhibitsanincreasingtraining-inferencediscrepancyduringtraining,quantifiedbythedensityratio𝜋
𝜃
/𝜋
𝜃
old vllm
(where𝜋 𝜃 istherolloutpolicyintheinferencebackendand𝜋 𝜃 isthepre-updatepolicysnapshotinthe
vllm old
trainingbackend). Conversely,MIS-POconsistentlymaintainsthisdiscrepancywithinastablerange.
Figure7: PerformancecomparisonbetweenMIS-POandGSPO.Thetopfigure(a)showsresultson
thedensemodel,andthebottomfigure(b)showsresultsontheMoEmodel. MIS-POconsistently
outperformsGSPOinbothefficiencyandstabilityacrossdifferentarchitectures.
D.2.3. RLAblationDetails
MIS-POvs. GSPO. Torigorouslyvalidatetheeffectivenessofourmethod,webenchmarkMIS-PO
against GSPO [36] on both Dense and MoE architectures. We select GSPO as the primary baseline
becauseitrepresentsacompetitivestrategyforreducingthegradientvarianceinherentinimportance
sampling. Inourimplementation,weextendtheoriginalGSPOestimatortotheactor-criticsetting
byintegratingitsGeneralizedImportanceSamplingmechanismintotheactorloss. Specifically,we
replacethestandardtoken-levelimportancesamplingratiowiththegeometricmeanoftrajectory-level
ratios. Theresultingactorlossisformulatedasfollows(𝛾 =𝜆 =1):
(cid:32) (cid:214) 𝑇−1 𝜋 𝜃 (𝑎 𝑡 |𝑠 𝑡 ) (cid:33) 𝑇 1
𝑟 𝜏 (𝜃) = (14)
𝜋 (𝑎 |𝑠 )
𝜃 𝑡 𝑡
𝑡=0 old
𝐴ˆ 𝑡 =𝑅ˆ −𝑉 𝜙 (𝑠 𝑡 ) (15)
L a G c S to P r O =−E 𝜏∼𝜋 𝜃 (cid:2)I(𝑥 𝑡 )·I(𝜌¯(𝜏))·min(𝑟 𝜏 (𝜃)𝐴ˆ 𝑡,clip(𝑟 𝜏 (𝜃),1−𝜖,1+𝜖)𝐴ˆ 𝑡 ) (cid:3) (16)
vllm

Toensureafaircomparison,weapplythesametoken-andsample-levelmaskingstrategiesusedin
MIS-POtoexcludedatawithsignificanttraining–inferencemismatches. Regardingtheclipratio𝜖,we
conductagridsearchover {1,2,3,4}×10−4. Weadopt𝜖 =10−4 forallexperimentsprimarilybecause
itachievesthebestbenchmarkperformanceafter200RLtrainingsteps. Additionally,weobservethat
thissettingyieldsaclipfractionofapproximately15%,consistentwiththeoriginalGSPO[36].
Figure 7 presents the comparative results. Empirically, MIS-PO demonstrates superior sample ef-
ficiency and scalability compared to GSPO. Crucially, MIS-PO effectively constrains the training-
inferencemismatchwithinastablerange. Thisstabilityprovesparticularlycriticalforthelarge-scale
RLtrainingofMoEmodels,wherethebaselineGSPOfailstomaintainconsistentconvergence.
ExtendedTrainingDynamicsonMoE. Tofurthervalidatethescalabilityofourmethod,weconduct
anextendedtrainingrunofMIS-POontheMoEmodelusingachallengingdataset. Asillustratedin
Figure8,themodelmaintainsacontinuousupwardtrendinrewards,stableactorgradientnorms,
andwell-controlledentropylevels. TheseresultsempiricallyconfirmthatMIS-POisreliabilityfor
large-scaleMoEoff-policyRLtraining.
0.60
0.55
0.50
0.45
0.40
0.35
200 400 600 800
Training Step
draweR
0.040
0.032
0.024
0.016
200 400 600 800
Training Step
mroN
darG
rotcA
0.48
0.40
0.32
0.24
200 400 600 800
Training Step
yportnE
Figure8: ExtendedtrainingdynamicsofMIS-POontheMoEmodel. ThemetricsincludeReward
(left),ActorGradientNorm(middle),andEntropy(right). Notably,themiddlepaneldisplaystheraw
gradientnormwithoutsmoothingordownsamplingtohighlightthestabilityoftheoptimization.
D.2.4. SearchAgent
Regardingthetrainingarchitecture,theearlyclient–serverone-stepoff-policyframeworkisseverely
bottlenecked by long-tail latency: approximately 5% of samples accounted for roughly 80% of the
generation cost. However, our observations indicate that the policy exhibits strong robustness to
staleness, maintaining stable performance even with a latency of approximately 20 steps. Conse-
quently,weadopttheFullyAsyncparadigm,decouplinggenerationandupdatesintoacompletely
asynchronousprocess. Furthermore,tominimizeinferenceoverheadduringmulti-turninteractions,
weimplementstickyscheduling,wherethesamesessionisconsistentlydispatchedtothesamenode
tomaximizeKV-cachereuse. Overall,thisconfigurationachievesanapproximate10×efficiencygain
whilemaintainingtrainingstability.
Throughoutthetrainingprocess,theFullyAsyncparadigmdemonstratesrobuststability,evidenced
by a sustained increase in rewards and a Truncated Importance Sampling (TIS) truncation rate
maintainedwithinacontrollablerange,therebyindicatinglimitedpolicydriftinducedbyasynchrony.
Notably,weobservethatdistinctfromthelimitedscalabilityof“RLfromzero”regardingtraining
budgets,injectingtask-relevantknowledgeandtool-usepriorsduringthemid-trainingphaseelicited
significantlyhigherperformancegainsandamorestableemergenceofcapabilitiesduringtheRL.

xbench xbench
Model BrowseComp BrowseComp-ZH GAIA AvgGain
DeepSearch-2505 DeepSearch-2510
AGENT Δ AVG@3 (METRIC: PASS RATE %)
Step3.5Flash* 1.5 ▲50.1 25.0 ▲41.9 17.0 ▲67.5 26.0 ▲57.7 11.3 ▲42.7 52.0
KimiK2-Thinking* 3.6 ▲37.9 23.8 ▲38.5 18.8 ▲36.6 28.7 ▲39.3 14.3 ▲27.0 35.9
KimiK2.5* 7.4 ▲53.2 40.3 ▲22.0 26.7 ▲49.2 36.0 ▲40.3 19.7 ▲36.6 40.2
DeepSeekV3.2 8.1 ▲43.3 41.2 ▲23.8 23.4 ▲51.7 35.7 ▲41.3 18.7 ▲30.6 38.1
GLM-4.7 3.4 ▲48.6 30.2 ▲36.4 19.6 ▲26.5 29.7 ▲34.6 19.3 ▲23.4 33.9
MiniMaxM2.1 1.3 ▲46.1 10.1 ▲37.7 15.4 ▲30.9 18.7 ▲46.6 6.0 ▲36.3 39.5
MiMo-V2Flash 0.9 ▲44.5 12.9 ▲38.3 12.9 ▲42.3 19.7 ▲49.6 6.3 ▲13.7 37.7
Gemini3.0Pro 25.2 ▲12.6 - 32.1 ▲44.5 45.0 ▲32.0 - 29.7
ClaudeSonnet4.5 1.4 ▲22.7 21.2 ▲19.6 16.2 ▲54.7 24.7 ▲42.6 7.3 ▲37.7 35.5
Table11: ImpactofToolUsageonAgentPerformance. EachcelldisplaystheBaselineScore(internal
knowledgeonly)followedbythe ▲PerformanceGainachievedbyenablingsearchtools. Thefinalscoreis
thesumofbothvalues. AvgGainhighlightsthemodel’sabilitytoleverageexternalinformationto
improveresults. Modelsmarkedwith*denotetoolresultsmeasuredundera256Ksetting;thesetting
forothermodelsisunspecified.
Discussion. Torigorouslyevaluateagenticcompetenceisolatedfromparametricmemorization,we
focusonthetool-usagegain,definedas:
Δ =Score −Score
tool withtools notools
Thismetricdecouplesthemodel’sinherentknowledgefromitsabilitytodynamicallyleverageexternal
tools. As detailed in Table 11, Step 3.5 Flash demonstrates the most robust capability to leverage
externalinformation,achievingthehighestaveragegain(52.0)andleadingsignificantlyoncomplex
benchmarkssuchasGAIAandxbench-DeepSearch.
ThisdistinctioniscriticalbecausehighabsolutescoresonbenchmarkslikeBrowseCompcansome-
times stem from strong internalized knowledge rather than effective search strategies. A smaller
Δ inahigh-performingmodelmayambiguouslyindicateeitherhighefficiency(themodelalready
tool
“knows”theanswer)orafailuretoeffectivelyutilizetoolstoimproveresults. Conversely,alargeΔ
tool
explicitlysignalsthemodel’sproficiencyinbridgingknowledgegapsthroughretrieval. Therefore,we
arguethatfutureoptimizationshouldnotmerelychasehigherabsolutescores(“benchmarkgrind-
ing”),butshouldaimtomaximizethisΔ inlong-context,evidence-criticalscenarios. Thisensures
tool
theagentistrulymasteringtheprocessofinformationretrievalandreasoning,ratherthanoverfitting
tostaticknowledgeorbenchmarkartifacts.
D.3. Tool-integratedReasoningandParallelReasoning
In this section, we introduce two primary methodologies for test-time scaling in Step 3.5 Flash:
tool-integratedreasoningandparallelreasoning.
Tool-integrated Reasoning For complex reasoning tasks, we integrate the model with a Python
interpretertofacilitatetool-assistedreasoning. Inthisframework,themodeloperateswithinasandbox
toiterativelythinkandexecutecodeforcomputational,simulation,andvisualizationpurposes. In
our experiments, we evaluate on AIME 2025, HMMT 2025, IMO-AnswerBench, GPQA, HLE ,
text
andARC-AGI-1witha100-turnlimit. AsshowninTable12,tool-integratedreasoningsignificantly

enhancesperformanceacrosschallengingmathematics,STEM,andpuzzlebenchmarks,highlighting
theadvancedagenticreasoningcapabilitiesofStep3.5Flash.
Benchmark Step3.5Flash Step3.5Flashw. Python
AIME2025 97.3 99.8(+2.5)
HMMT2025Feb. 98.4 98.7(+0.3)
HMMT2025Nov. 94.0 98.0(+4.0)
IMO-AnswerBench 85.4 86.7(+1.3)
GPQA-Diamond 83.5 84.4(+0.9)
HLE 23.1 26.5(+3.4)
text
ARC-AGI-1 54.8 56.5(+1.7)
Table12: ComparisonofStep3.5FlashandStep3.5Flashw. Python.
Tool-integrated Parallel Reasoning We present a preliminary exploration of extending PaCoRe
to a multi-turn interactive environment. By design, PaCoRe preserves the standard LLM message
interface. Thiscompatibilityallowsforseamlessintegrationintoexistingagenticframeworksthat
utilizemulti-turntoolinteraction. ToadaptPaCoRetothissetting,weimplementastate-awareinput
serializationprotocolasshowninTable14.
We evaluate this approach on the GPQA and HLE benchmarks using Step 3.5 Flash equipped
text
withaPythoninterpreter. AsshowninTable13,extendingparallelreasoningtotheseagenticloops
yieldssignificantperformanceimprovementsoverthestandardreasoningbaseline. Thesefindings
demonstrate that PaCoRe effectively generalizes to environments requiring interactive feedback,
highlightingapromisingavenueforagentictest-timescaling.
Benchmarkw. Python Step3.5Flash Step3.5Flash+PaCoRe
GPQA-Diamond 84.4 85.7(+1.3)
HLE 26.5 28.2(+1.7)
text
Table13: ComparisonofStep3.5Flashw. PythonandthesamemodelwithPaCoRetest-timescaling.
E. Detailed Evaluation Protocols and Prompts
This section provides the implementation details for our evaluation suite. We outline the specific
prompttemplates,few-shotconfigurations,andthejudgemodelsemployedacrossdifferentbench-
marks. For complex metrics, such as those used in long-context or reasoning tasks, we also detail
theunderlyingcalculationlogicandscoringcriteriatoensurereproducibility. Inthetemplatespro-
{question}
videdbelow, denotestheplaceholderforthetextualproblemdescription,whileother
{test} {context}
placeholders(e.g., , )representtask-specificinformation.
E.1. EvaluationDetailsofPre-trainedModels
E.1.1. Generallanguageunderstandingandreasoningbenchmarks
BBH. WeusetheofficialCoT-prompts7 ofBBH[136],withonly"Q:"and"A:"replacedby"Problem:"
and"Solution:"asfollows:
7https://github.com/suzgunmirac/BIG-Bench-Hard/tree/main/cot-prompts

PanelA:StandardUserQuery(Lastrole:user)
Youaregivenaproblemandalistofreferenceresponses.Yourjobistoanalyzethesereferencesandprovideyourownresponse.
OriginalProblem:
{{original_content}}
ReferenceResponses:
Note:Somereferencesmaycontain<tool_call>tagsindicatingtoolcallsthereferenceintendedtomake.
ThesetoolcallshaveNOTbeenexecuted-theyareshownonlyasreferenceforyouranalysis.
{%forresponseinref_responses%}
Reference{{loop.index}}:
{{response}}
{%endfor%}
Now,basedontheoriginalproblemandreferenceresponsesabove,pleaseprovideyourowncomprehensivesolution.
PanelB:ToolObservation(Lastrole:tool)
Youaregivenatoolresponseandalistofreferenceresponsesanalyzingit.Yourjobistoanalyzethesereferencesandprovideyourownresponse.
OriginalToolResponse:
{{original_content}}
ReferenceResponses:
[SamepreambleregardingunexecutedtoolcallsasinPanelA]
{%forresponseinref_responses%}
Reference{{loop.index}}:
{{response}}
{%endfor%}
Now,basedontheoriginaltoolresponseandreferenceresponsesabove,pleaseprovideyourowncomprehensiveanalysisandnextsteps.
Table14: InputserializationtemplatesforTool-integratedPaCoRe. Weintroducedistincttemplates
to handle the initial user query (Panel A) and subsequent tool observations (Panel B). Note that
tool_calls
withinreferencebranchesareserializedastextforanalysis.
Problem:
{question}
Solution:
MMLU. WeusetheofficialevaluationmetricofMMLU[137]with5-shot. Weemploythefollowing
task-specificsystemprompt:
The following are multiple choice questions (with answers) about {category}.
Thecorrespondingquestionpromptisstructuredasfollows:
{question}
Answer:
MMLU-Redux. WeusetheofficialevaluationmetricofMMLU-Redux[138]with5-shot. andemploy
thefollowingquestionprompt:
Answer the question and place the option (A/B/C/D...) inside \boxed{}.
{question}

MMLU-Pro. WefollowtheofficialevaluationmetricofMMLU-Pro[139]with5-shot. Allevaluations
usethefollowingsystemprompt:
The following are multiple choice questions (with answers) about {category}.
Think step by step and then output the answer in the format of "The answer is
(X)" at the end.
Thequestionpromptisstructuredasfollows,withadeliberatetrailingspaceafterthefinalperiod:
Question: {question}
Answer: Let’s think step by step.
Notably, we observe that a subset of the original MMLU-Pro dataset (470 out of 12,102 questions)
containedaninconsistentleadingspacebeforetheground-truthoptions. Weexplicitlyremovethese
spacestomitigatepotentialformattingbiasandensureevaluationconsistency.
HellaSwag. WeusetheofficialevaluationmetricofHellaSwag[140]with10-shot. Weemploythe
followingquestionprompt:
Question: {question}
A. {option_0}
B. {option_1}
C. {option_2}
D. {option_3}
Answer:
WinoGrande. WeusetheofficialevaluationmetricofWinoGrande[141]with5-shot. Thequestion
promptisstructuredtopresentthebinarychoicesclearly:
Question: {question}
Options:
A. {option_0}
B. {option_1}
Answer:
GPQA. WeusetheofficialevaluationmetricofGPQA[142]with5-shot. Thequestionpromptis
structuredtopresentthechoicesclearly:
Question: {question}
Options:
A. {option_0}
B. {option_1}
C. {option_2}
D. {option_3}
Answer: Let’s think step by step.

SuperGPQA. WeusetheofficialevaluationmetricofSuperGPQA[143]with5-shot. Thequestion
promptfollowsaChain-of-Thought(CoT)structure,whereeachfew-shotexampleincludesastep-by-
stepderivationleadingtothefinalanswer:
Question:
{question}
Answer: Let’s think step by step.
SimpleQA. We use the official evaluation metric of SimpleQA [144] with 5-shot. As SimpleQA
requiresopen-endedshortanswers,weemployanLLM-basedjudgementforevaluation,specifically
usinggpt-oss-120b[33]asthejudgemodel. Thequestionpromptisformattedasaconcisequery:
Question: {question} Answer:
E.1.2. Mathematicsreasoningbenchmarks
GSM8K. WeusetheofficialevaluationmetricofGSM8K[145]with8-shot. Thequestionpromptis
designedtoelicitCoTreasoningbyusingthefollowingtemplate:
Q: {question}
A: Let’s think step by step.
MATH. WeusetheofficialevaluationmetricofMATH[146]with4-shot. Thequestionpromptis
structuredwithexplicitproblemandsolutiondelimiters:
Problem:
{question}
Solution:
E.1.3. Codingbenchmarks
HumanEval. WeusetheofficialevaluationmetricofHumanEval[147]with3-shot. Thequestion
prompt is structured with three ground-truth examples to provide contextual guidance for code
generation:
# Below are the ground-truth solutions:
def add_two_numbers(a, b):
""" Given two numbers a and b, return the sum of a and b. """
# get the sum of a and b
sum_of_a_and_b = a + b
return sum_of_a_and_b
def reverse_list(some_list: list) -> list:
""" Given a list, return a reversed copy of the list. """

new_list = []
# iterate over the list
for item in some_list:
# insert item into new list
new_list.insert(0, item)
return new_list
def fast_reverse_list(some_list: list) -> list:
""" Given a list, return a reversed copy of the list. Be fast! """
# use faster built-in reverse
some_list.reverse()
return some_list
{question}
MBPP. WefollowtheofficialevaluationmetricofMBPP[148]with3-shot.
HumanEval+. WefollowtheofficialevaluationmetricofHumanEval+[149]with3-shot.
MBPP+. WeusetheofficialevaluationmetricofMBPP+[149]withzero-shot. Weemployastructured
instructionpromptthatspecifiesthetaskrequirementsandincludesasampletestcaseforalignment:
You are an expert Python programmer, and here is your task:
{question}
Your code should pass the test:
{test}
Here is the corresponding code:
```python
MultiPL-E. WeusetheofficialevaluationmetricofMultiPL-E[150]withzero-shot. Wefollowthe
officialtestcasestojudgethegeneratedcode.
E.1.4. Chineseunderstandingbenchmarks
C-Eval. WeusetheofficialevaluationmetricofC-Eval[151]andadda5-shotsetting. Weemploy
thefollowingsystemprompt:
你是一个中文人工智能助手，以下是中国关于{category}考试的单项选择题，请选出其中的正确答案。
Thecorrespondingquestionpromptisstructuredasfollows:
{question}
答案：
CMMLU. We use the official evaluation metric of CMMLU [152] and add a 5-shot setting. We
employthefollowingsystemprompt:

你是一个中文人工智能助手，以下是中国关于{category}考试的单项选择题，请选出其中的正确答案。
Thecorrespondingquestionpromptisstructuredasfollows:
{question}
答案：
C-SimpleQA. WeusetheofficialevaluationmetricandLLM-basedjudgementprotocolsofChinese
SimpleQA[153]. Weadda5-shotsettingandusegpt-oss-120b[33]asthejudgemodel. Weemploy
thefollowingquestionprompt:
问题：{question}
答案：
E.2. EvaluationDetailsofPost-TrainedModels
In this section, we detail the evaluation protocols used to assess the post-trained models across a
diverse set of agentic tasks. Our evaluations span both code-centric and general-purpose agent
settings,coveringsoftwareengineering,terminalinteraction,deepsearch,researchworkflows,and
real-world tool use. We report standardized metrics under carefully controlled environments and
inferencebudgetstoensurefair,stablecomparisonsacrossbenchmarks.
E.2.1. Reasoningbenchmarks
CF-Div2-Stepfun. Recentstudiesandadvancedbenchmarksemphasizethecriticalneedtoevaluate
modelsonfresh, competition-levelproblem[183,184]. Weevaluatethecompetitiveprogramming
capabilitiesofourmodelusingacustomCodeForcesDiv. 2Benchmark8. Thebenchmarkcomprises53
problemssourcedfromofficialCodeForcesDiv.2contestsheldbetweenSeptember2024andFebruary
## 2025. We develop an offline evaluation framework that utilizes a local grading mechanism as an
alternativetoreal-timeonlinesubmissions. Wetrytoconstructtestcasessimilartotheoriginaltest
cases. Specifically,wefirstgenerateenoughsmall-scaletestcasesforevaluationcorrectnesscoverage,
thenaddrandomizeddataforlarge-scaletesting. Finally,weperformedadversarialconstructionof
edgecasesbyanalyzingcommonerrorpatternsand"hacked"submissionsfromactualusers. Some
edgecasesarealsoauto-generatedbythestresstestingtechnique,whichkeepsgeneratingcountless
test cases until one can distinguish failed submissions from correct submissions. To validate the
reliabilityofthisbenchmark,werunbothcorrectandrepresentativefailedsubmissionsselectedfrom
theoriginalcontests. Ourevaluatorcorrectlyidentifies100%oftheacceptedsubmissionsas"Passed",
while92.45%ofthefailedsubmissionsareaccuratelyflagged.
8https://huggingface.co/datasets/stepfun-ai/CF-Div2-Stepfun

Accuracy(avg@8) CodeforcesC++
Model C++ Python Java pass@8Rating
Step3.5Flash 86.1% 81.5% 77.1% 2489
DeepseekV3.2 81.6% 66.5% 80.7% 2319
GLM-4.7 74.1% 63.0% 70.5% 2156
KimiK2-Thinking 67.9% 60.4% 58.5% 1976
Minimax-M2.1 59.0% 46.4% 58.0% 1869
Mimo-V2Flash 46.9% 43.6% 39.6% 1658
Gemini3.0Pro 83.5% 74.1% 81.6% 2397
ClaudeOpus4.5 72.2% 68.4% 68.9% 2100
Table15: FullevaluationresultsofvariablemodelsinCF-Div2-Stepfun.
Wesample8responsesforeachproblemandreporttheaverageaccuracy. Theuserpromptutilized
forthisprocessis:
You are a coding expert. Given a competition-level coding problem, you need to
write a {LANGUAGE} program to solve it. You may start by outlining your thought
process. In the end, please provide the complete code in a code block enclosed
with ``` ```.
{question}
ThecompilationandexecutioncommandsforC++,Python,Javaaregivenbelow:
g++ -std=c++20 -fno-asm -fsanitize=bounds -fno-sanitize-recover=bounds –static
-O2 -DONLINE_JUDGE -o code.exe code.cpp
./code.exe
python3 code.py
javac -J-Xmx544m {JAVA_CLASS_NAME}.java
java -XX:+UseSerialGC -Xmx544m -Xss64m -DONLINE_JUDGE {JAVA_CLASS_NAME}
Tomaintainconsistencywithcompetitiveprogrammingnormsandavoidtheinconsistentoverhead
associatedwithJIT"warm-up"periods,weusethestandardPythoninterpreterwithadoubletime
limitratherthanPyPy9. WeapplythissamedoubletimelimittoallJavasubmissions.
While the Table 15 reports raw accuracy, we recognize that problem difficulty varies significantly.
Therefore,ratingscoresprovidemorerobustmetrics. AlthoughframeworkslikeCodeELO[185]can
calculatecompetitiveratings,currenttop-tiermodelsperformsoeffectivelyinDivision2conteststhat
theirratingsmayresultinstatisticaloutliers. Furthermore,weadoptasimplifiedratingcalculation
thatdisregardssubmissiontimepenaltiesbyassumingallsolutionsaresubmittedattheonsetofthe
contest. Whilethisapproachdeviatesfromempiricalcompetitivescenariosandmayresultinratings
that are not directly comparable to human participants, it provides a standardized benchmark for
consistentcross-modelcomparison.
9https://pypy.org/

LiveCodeBench-v6. WeusetheofficialevaluationmethodofLiveCodeBench[12]. Weemploythe
followingsystemprompt:
You are an expert Python programmer. You will be given a question (problem
specification) and will generate a correct Python program that matches the
specification and passes all tests.
Thecorrespondingquestionpromptisstructuredasfollows:
### Question:
{question}
### Format: You will use the following starter code to write the solution to
the problem and enclose your code within delimiters.
``` python
{starter_code}
```
### Answer: (use the provided format with backticks)
AIME2025. WeusetheofficialevaluationmethodofAIME2025[170]withrepeat@64. Weemploy
thefollowingquestionprompt:
Answer the question and place the answer inside \boxed {} with MathTeX format.
{question}
HMMT2025Feb./Nov. WeusetheofficialevaluationmethodofHMMT2025[11]withrepeat@64.
Weemploythefollowingquestionprompt:
Answer the question and place the answer inside \boxed {} with MathTeX format.
{question}
IMO-AnswerBench. We use the official evaluation method of IMO-AnswerBench [91] with re-
peat@64. Weemploythefollowingquestionprompt:
Answer the question and place the answer inside \boxed {} with MathTeX format.
{question}
MMLU-Pro. WeusetheofficialevaluationmethodofMMLU-Pro[139]. Theprocessingofdataset
remainsconsistentwithourpre-trainingMMLU-Proevaluationmethodology(seeAppendixE.1.1for
details).
Answer the question and place the option (A/B/C/D...) inside \boxed{}.
{question}

GPQA-Diamond. WeusetheofficialevaluationmethodofGPQA-Diamond[142]. Weemploythe
followingquestionprompt:
Answer the question and place the option (A/B/C/D...) inside \boxed{}.
{question}
HLE . WeusetheofficialevaluationmetricandLLM-basedjudgementprotocolsofHLE.Weuse
text
gpt-oss-120b[33]asthejudgemodel.
E.2.2. CodeAgentbenchmarks
SWE-Bench. SWE-BenchVerified[13]isahigh-qualitysubsetoftheoriginalSWE-benchdataset,
consisting of 500 software engineering tasks rigorously validated by human expert developers to
ensurereliableandaccurateevaluation. SWE-BenchMultilingualextendstheoriginalbenchmarktoa
diversesetof300real-worldsoftwareengineeringtasksacross9programminglanguages.
WetestthesoftwareengineeringagentabilityofStep3.5FlashonSWE-BenchVerifiedandSWE-Bench
Multilingualusingourinternalagentinfrastructure,whichisbuiltuponthedescribedsession-router
architecture. For each evaluation instance, we provision a containerized session orchestrated via
Kubernetes. We then perform environment initialization specific to SWE-Bench, which includes
removingfuturecommitstopreventdataleakage,aswellasconfiguringnetworkproxiesandcritical
system settings. Regarding the agent scaffold, we adopted the OpenHands [131] CodeAct Agent
framework,whichiswidelyusedintheresearchcommunity. Weenabledadefaultsuiteoffourtools:
execute_bash,str_replace_editor,finish,andthink. Themaxinteractiveturnsissetto350.
Given the resource-intensive nature of compiled languages, we allocate 12GB of memory for the
multilingual setting, whereas the verified instances are restricted to a 4GB limit. In evaluations,
thetoolexecutiontimeoutissetto1200s, andthemodelinferenceparametersare: temperature=1,
top-p=0.95. Following the above settings, Step 3.5 Flash reach 74.4% on SWE-Bench Verified, and
67.4%onSWE-BenchMultilingualbenchmarkwithanaveragescoreof4repeatofrunnings. Wealso
cross-evaluate Step 3.5 Flash on other popular agent scaffolds: SWE-Agent [132] with the original
agentpipelinesettingsachieving74.2%accuracyonSWE-BenchVerified,andstandardClaudeCode10
environmentscoring72.0%withanextendedtimelimitof4hoursforeachinstanceandnotimelimit
forsingletoolexecution.
Terminal-Bench2.0. WetesttheTerminal-Benchbenchmark[16]withinremotetask-independent
containers. We limit the container memory to 16GB. We have deployed an internal Artifactory
repositoryandupdatethedefaultpackagesourcesforallDockercontainers. Duringsessioncreation
and dependency installation of the testing phases, the system will retry multiple times if an error
occurs. Tostreamlinethesystem-agentinteraction,wemodifytheTerminus2frameworksothatit
automaticallyinterruptstimed-outcommandsandpreventssubsequentcommandsinthesameround
from executing, returning a timeout warning to the agent. Accordingly, we modify the command
durationcontrolpartoftheoriginalsystemprompt:
Keystroke duration sets the command hard timeout. The system automatically
interrupts timed-out commands and prevents subsequent commands in the same
10https://github.com/anthropics/claude-code

round from executing. You can simply continue with your next round - no special
action is required.
Duringinference,wecapthemodel’ssingle-turnoutputat64kandthemaximumcontextwindowat
256kforallinteractions. Thethinkingprocesswillbepreservedinthemulti-roundhistory. Ifthemodel
outputexceedsthe256kcontextwindowlimit,weexecuteapruningcontextmanagement: Keepthe
problemstatementandthelast50%ofhistorybeforeretrying. Weusetheinferenceparametersof
top-p=0.95andtemperature=1. TheinteractionprotocolisprimarilyconductedusingXML-formatted
structuredresponses. Theagentislimitedto200interactionroundsandwillproceeddirectlytothe
testingphaseoncethislimitisreached. Thetotaltimelimitforinteractionandtestingis6hours.
Toensureconsistency,weverifyandrefineeachtask’scheckeragainstitsproblemstatement11,which
improved overall accuracy by approximately 1.5%. Each task is executed across 8 trials. Notably,
88.6%ofsuccessfultrajectoriesarecompletedwithin30interactions. Thefinalpass@8standsat67/89,
withanavg@8of50.98%. Ouragentachievesa100%successrateacrossall8trialsin23outof89tasks.
Inthesuccessfultrajectories,9.41%oftherunstriggeredhistorypruningtomanagecontextlimits.
Setting MaxOutput MaxRound Timeout ContextManagement Avg@8
Baseline 64k 200 6h ✓ 50.98%
Limit16k 16k 200 6h ✓ 48.03%
Limit16kw/oPruning 16k 200 6h × 45.22%
Rounds100 64k 100 6h ✓ 50.42%
Timeout2h 64k 200 2h ✓ 49.72%
Table16: AblationstudyofinferenceconstraintsonTerminal-Bench2.0.
TheablationstudyshowsthatLimit16kcausesthelargestperformancedropbecausethemodel’slong
reasoningforcomplextasksoftenexhauststhetokenlimitbeforeitcanoutputtheterminalcommands.
Thefurtherdeclineto45.22%whendisablingcontextmanagementunderthe16klimit. Meanwhile,
Rounds 100 has minimal impact as most tasks finish early. The Timeout 2h decrease reflects that
certaintasksinvolvingmodeltraining,heavycompilation,orcomplexenvironmentconfiguration
requiremoretimetocomplete.
E.2.3. GeneralAgentbenchmarks
Deep Search. We evaluate our agent’s deep search capabilities on multiple benchmarks (e.g,
BrowseComp [17], BrowseComp-ZH [18], GAIA [19], xbench-DeepSearch [20]). The results re-
portedinTable5arebasedontheavg@3metric;GPT-5.2xHighusesavg@1. Theagentisequipped
withacoretoolsetincluding:
• search: Executesmultiplesearchqueriesinparallel.
• visit: AnalyzesthecontentofthewebpagetoanswerspecificquestionsbasedonLLM.
• google_scholar: Searchforacademicarticlesandtechnicalliterature.
• python_interpreter: RunsPythoncodeforcalculationsanddataanalysis.
• file: DownloadsandsavesfilesfromdirectURLs.
Duringinference,weemploya256k-tokencontextwindowwithnolimitonthemaximumgeneration
length. Inference is conducted with top-p = 0.95, temperature = 1.0, and presence penalty = 1.1,
allowingforanexecutionbudgetofupto400steps.
11https://huggingface.co/datasets/zai-org/terminal-bench-2-verified

ThedetailedsystempromptsfortheagentandtheLLMjudgeareconsistentwiththeconfigurations
providedintheGitHubrepositoryassociatedwith[98].
BrowseComp(w. CtxManage). TheBrowseComp(w. CtxManage)resultof69.0reportedinTable5
correspondstothediscard-allmethodologyevaluatedonthefullBrowseCompdataset. Thisapproach,
sameasDeepSeekV3.2[1],istriggeredwhenthecontextlengthexceedspredefinedthresholds,at
which point the agent discards its entire context and reinitializes the operational loop. Under a
maximumiterationconstraintof1000steps,thisstrategyemploysacontextlengththresholdof72k
tokensforBrowseCompand41ktokensforBrowseComp-ZH.
Wealsoevaluatevariouscontextmanagementstrategiesonasubsetof200instancesfromBrowseC-
omp,includingSummary,Keep-first&last𝐾,Discard-all,andMulti-agentorchestration. Asshown
in Table 17, our model demonstrates robust adaptability across these diverse paradigms. Among
single-agent strategies, Discard-all yields a competitive 66.0% accuracy. We posit that Discard-all
functionsasatest-timepass@𝑘strategy,forcingthemodeltore-reasonfromscratchuntilaself-verified
pathisfound. Theperformancefollowsaclearhierarchy: Multi-agentrankshighestbyleveraginga
masteragenttodecomposetasksanddispatchspecializedagentsforparallelreasoning,followedby
Discard-all,Keep-first&last𝐾 andSummary—closelyalignswiththeincreaseinrealsteps. Thisalign-
mentreflectsadirecttrade-offbetweeninferencecost(numberofsteps)andaccuracy,suggestingthat
intensivecontextmanagementeffectivelyconvertsincreasedcomputationintosuperiorperformance.
Method Accuracy(%) RealSteps
Step3.5Flash 49.5 86
+Summary 57.0 131
+Keep-first&lastK 58.0 244
+Discard-all 66.0 302
+Multi-Agent 68.5 721
Table17: Evaluationresultsofcontextmanagermethods.
RESEARCHRUBRICS. Toevaluatedeepresearchcapabilities,weutilizetheRESEARCHRUBRICS[21]
benchmark. Thisdatasetcomprises101domain-diverseresearchtasks,eachaccompaniedby20–43
expert-written,fine-grainedscoringcriteriathatassessfactualaccuracy,reasoningsoundness,and
clarity. Webenchmarkperformanceagainsttworepresentativesystemfamilies: commercialagent
systemsandReActagents.
Forcommercialagents,wecollectreportsviatheirofficialwebinterfaces(capturedDec2–15,2025)
underdefaultconfigurations. AsshowninTable18,theleadingcommercialsystem(GeminiDeepRe-
search)achievesanaggregatedscoreof63.69.
ForReActagents,detailedperformancecomparisonsarepresentedinTable5. Ourmodelachievesa
scoreof65.3,surpassingthecomplex,proprietarycommercialbaselines. Notably,whenevaluating
Gemini3.0ProwithinourstandardizedReActframework,weobserveascoreof50.1. Weattribute
thisperformancegaptoinsufficientsearchdepthwhenaddressingopen-endedresearchquestions;
the model tends to rely on internal parametric knowledge rather than perform extensive external
retrieval. Consequently,thegeneratedreportslackcomprehensiveness,failingtoadequatelycoverthe
user’simplicitcriteria.
WestandardizetheexecutionenvironmentforReActagentswithamaximumof30reasoningturns
andaper-turnoutputlimitof16ktokens. Forinferenceparameters,otherAPI-basedmodelsusetheir

AgentSystem Score
GeminiDeepResearch 63.69
OpenAIDeepResearch 60.67
KimiResearcher 53.67
MiniMaxAgentPro 51.85
QwenDeepResearch 49.24
Table18: PerformanceofCommercialAgentSystemsonthe RESEARCHRUBRICS benchmark.
defaultsettings,andourmodelisconfiguredwithatemperatureof1andtop-p=0.95. Alloutputsare
subsequentlyappraisedbyanLLMjudgeusingaternarygradingforeachcriterion. Tosupportthe
end-to-endresearchworkflow,ourReActframeworkprovidesaccesstothefollowingsuiteoftools:
• batch_web_surfer: Forconcurrentwebsearchingandmulti-pagebrowsing.
• file: Forrobustfileoperations,includingreading,writing,anditerativeediting.
• file_parser: ForconvertingfilesintoMarkdownformat.
• shell: Forinteractivecommandexecutionandenvironmentinteraction.
• todo: Fordynamictaskstatemanagementandtracking.
• tmux: Forsimulatingamultiplexedterminalenvironmentwithpersistentsessionsandscrollback
history.
𝜏2-Bench. 𝜏2-Bench[15]isanagenticbenchmarkthatevaluatesgeneraltool-usecapabilityinthree
customer service domains: airline, retail, telecom. We evaluate Step 3.5 Flash using the official
settingsintheoriginalcodebase. Specifically,weusethedefaultLLMagentframeworkandsetthe
temperatureto1.0,top-pto0.95,maxsequencelengthto256K.TheusermodelissettoGPT-4.1with
0.0temperaturetoensureastableinteractionduringevaluation. Fortheairlinedomain,sinceithas
incorrectgroundtruthanswers,weusethefixedversionfromClaudeOpus4.5toensureevaluation
reliability12. Fortheretailandtelecomdomains,wealsofollowClaudeOpus4.5toincludeageneral
promptaddendumtotheuserprompttoavoidfailuremodesfromtheuserendingtheinteraction
incorrectly13. Wereportanaveragescoreof8runstoensurestableevaluationresults.
E.2.4. Generalbenchmarks
Arena-Hard-v2.0. We use the official evaluation metric of Arena-Hard-v2.0 [155] and use GPT-
4.1[186]asthejudgemodel.
MultiChallenge. WeusetheofficialevaluationmetricofMultiChallenge[157]witho3-mini[187]
asthejudgemodel. ThisfollowsfindingsfromtheGPT-5[188]releasethatGPT-4o[186]frequently
mis-scorescomplexresponses,leadingtounderestimatedresults.
IFBench. WeusetheofficialevaluationmethodofIFBench[156].
12https://github.com/sierra-research/tau2-bench/pulls/chrisgorgo
13https://github.com/anthropics/model-cards/tree/main/claude-opus-4-5-20251101/tau2

E.2.5. LongContextbenchmarks
LongBenchv2. WeusetheofficialevaluationmethodofLongBenchv2[158].
MRCR-8needle. For MRCR-8needle [159] benchmark, we report the Area Under Curve (AUC)
metric,followingtheprotocolestablishedbyContextArena14. Specifically,weusetheAUC@128k
metric,whichprovidesasingleholisticscoresummarizingperformanceacrosscontextlengthsupto
131,072tokens.
TheAUCiscalculatedbyplottingtheaverageretrievalaccuracyforeachcontextbin(rangingfrom8k
to128k)againstthebin’smaximumcontextlength. Weapplythetrapezoidalruleonalinearscaleto
measuretheareaundertheresultingcurve,whichisthennormalizedbythetotalcontextwidth(128k
minustheinitialbinsize)toyieldapercentagescorebetween0%and100%. Thismetriceffectively
penalizesperformancedegradationasdifficultyincreaseswithlongercontextsequences.
FRAMES-Oracle. We use the official evaluation metric of FRAMES [160]. Since our focus is on
long-contextcapabilities,wespecificallyreportresultsfortheOraclePromptsubset. Inthissetting,
themodelisprovidedwiththequestionalongsideallground-truthWikipediaarticlesusedduring
humanannotation. Thisconfigurationservesasanupperboundformodelperformance,simulatinga
perfectretrievalsystemthatdeliversallrelevantcontexttothemodel.
RepoQA. WeusetheofficialevaluationmethodofREPOQA[161].
E.3. InternalEvaluation-BenchmarksandMethodology
E.3.1. DataAnalysisBenchmark
ToreliablyassessStep3.5Flash’sabilitytoperformpracticaldata-analysistasksintheClaudeCode
environment,wedevelopaninternalDataAnalysisBenchmarkforevaluatingend-to-endanalytical
problemsolvingunderrealisticbusinessconstraints. Thebenchmarkisconstructedbysystematically
distillingseniorpractitioners’tacitexpertiseintoarubric-groundedevaluationsuite. Thisapproach
captures the ambiguity and contextual nuance of real-world analytics while ensuring consistent
evaluationthroughstandardizedrubricsandverifiableground-truthartifacts.
Thebenchmarkisconstructedusinganexpert-driven,rubric-basedprotocoltoensuredomainauthen-
ticityandscoringreliability. TenseniordataanalyticsleadersfrommajorChineseinternetcompanies,
each with over 15 years of experience, contributed real-world business cases through structured
interviewsthatelicitedcoreanalyticalpatternsanddecisionlogic. Thisprocessyieldsrepresentative
taskspairedwithexpert-endorsedsolutionstrategies.
Interview materials are normalized into machine-consumable tasks, each comprising a problem
statement, a CSV dataset, a reference analysis, and a weighted checklist-style scoring rubric. The
resultingbenchmarkcontains50itemsspanningdiverseanalyticalintents,withanaverageof26.9
rubricitemspertask. Qualityisensuredthroughiterativeexpertreview, aligningtaskdefinitions,
data,referencesolutions,andevaluationcriteriatoimprovevalidityandreproducibility.
Wefurtherimplementaunifiedend-to-endevaluationframeworkcoveringtaskexecution,automated
scoring,andreportsynthesis. Theframeworksupportscode-based,research-oriented,andtext-based
14https://contextarena.ai/

analyseswithinasinglepipeline,enablingscalableandreproducibleevaluationacrossheterogeneous
environmentswithlowintegrationoverhead.
EvaluationMethod. Eachtaskisevaluatedbyamodel-basedevaluatorthatscoresgeneratedoutputs
againstexpert-definedrubrics,withresultsaveragedover3identicalrunstoreducestochasticvariance
andensurereliable,comparablecross-modelevaluation.
Model Avg@3(%)
ClaudeOpus4.5 45.0
Step3.5Flash 39.6
GPT-5.2 39.3
Gemini3.0Pro 33.6
DeepseekV3.2 27.9
Table19: EvaluationResultsontheDataAnalysisBenchmark
EvaluationResults. Table19presentstheresultsontheDataAnalysisBenchmark. ClaudeOpus
## 4.5 ranks first overall, while Step 3.5 Flash achieves a strong second place (39.58%) and remains
veryclosetoGPT-5.2(39.31%). Itscompetitiveperformancemaybepartlyrelatedtorelativelygood
adaptation to the Claude Code environment. In addition, Step 3.5 Flash demonstrates a favorable
speed–capabilitytrade-off,maintainingsolidanalyticalqualitywhiledeliveringfasterresponses. The
resultspositionStep3.5Flashasahighlyefficientandcompetitiveoptionforreal-worlddataanalysis
tasks.
E.3.2. ConsultingandRecommendationsBenchmark
TorigorouslyevaluateStep3.5Flashinreal-worldadvisoryscenarios,wecurateabenchmarkof500
diversequeriessourcedfromauthenticsocialplatformssuchasReddit,StackExchange,andvarious
community forums. These queries represent authentic user intent across everyday life, academic
learning,entertainment,andprofessionalworkplacecontexts.
Here, we implement an "Anchor-Based" scoring framework to evaluate candidate models. In this
process,wefirstutilizeleadingmodels,includingGPT-5.2,ClaudeOpus4.5,andDeepSeekV3.2to
generateindependentresponsesforeachquery. Thesehigh-leveloutputsarethensynthesizedand
refinedbyhumanexpertstocreateaReferenceResponseasGroundTruth. Thisreferenceservesasa
high-quality"Anchor"withastandardizedperformancevalueof88/100.
Wethenmeasuretheperformanceofthemodelsacrossfourcriticaldimensions,applyingarigorous
scoring rubric, including Usefulness, Logic, Instruction Following, and Tone. Usefulness assesses
whetherthemodeldeliversaready-to-usesolutionthatmeaningfullyresolvesthetaskwithexpert-
leveldepth,actionablesteps,andfeasiblerecommendations. Logicevaluatesfactualaccuracyand
structuralsoundness,checkingforhallucinations,incorrectcitations,invalidconclusions,orcausal
andtemporalinconsistencies,aswellasoverallcoherenceandargumentflow. InstructionFollowing
measuresadherencetobothexplicitconstraints(e.g.,formatting,length,andstatedrequirements)and
implicitcontextualexpectationsembeddedintheuserquery. Toneassessescommunicativequality,
including appropriateness of language and register, clarity in unpacking complex reasoning, and
calibratedexpressionthatavoidsoverconfidencewhileclearlysignalinguncertaintywhenappropriate.
WeemployaHybridLLM-as-a-Judgesystem. Recognizingthatdifferentfrontiermodelshavedistinct

evaluativestrengths,weassignspecificscoringresponsibilitiesasfollows: Logic,InstructionFollowing,
andUsefulness: ThesethreedimensionsareevaluatedbyGPT-5.2,leveragingitsindustry-leading
capabilities in factual verification, constraint checking, and objective problem-solving. Tone: This
dimensionisevaluatedbyClaudeOpus4.5,utilizingitssuperiornuanceinlinguisticstyle,emotional
calibration,and"human-like"resonance. Judgereliabilityisvalidatedthroughanalignmentstudy
withhumanexperts, yieldingahighPearsoncorrelationbetweenAI-andhuman-assignedscores.
Finalscoresarecomputedusingequalweightingacrossthefourdimensions(25%each),ensuringa
balancedassessmentthatjointlyreflectstechnicalcorrectnessandcommunicativequality.
Model Average Usefulness Logic Tone Instruction-following
GPT-5.2 77.8% 77.2% 81.9% 73.0% 79.6%
KimiK2.5 72.2% 77.1% 62.1% 72.7% 77.3%
Gemini3.0Pro 70.6% 73.9% 61.7% 72.3% 74.4%
Step3.5Flash 70.5% 73.3% 62.1% 72.4% 74.2%
DeepseekV3.2 70.3% 72.5% 64.4% 71.2% 72.9%
GLM-4.7 70.3% 73.5% 61.5% 72.5% 73.6%
ClaudeOpus4.5 68.5% 69.7% 66.5% 65.9% 72.1%
Mimo-V2Flash 67.9% 71.5% 58.0% 70.6% 71.4%
MinimaxM2.1 67.1% 70.7% 60.1% 67.2% 70.4%
Table20: EvaluationresultsontheConsultingandRecommendationsBenchmark
EvaluationResults. Table20showsthatStep3.5FlashachievesanaverageScoreof70.5%onthe
Consulting and Recommendations Benchmark, securing the 4th position overall. Step 3.5 Flash
matchesGemini3.0Properformanceacrossalldimensions,achievingcomparablePro-levelscores
(70.5% vs. 70.6%) while offering substantially lower inference cost and latency. Unlike many fast
modelsthattradespeedfordegradedreasoningquality,Step3.5Flashsurpasseslargermodelsinthe
Logicdimension,reducinghallucinationsandlogicalfailuresandmakingitwellsuitedforautomated
consultingworkflowswherefactualintegrityiscritical.
E.3.3. Step3.5Flash+Step-GUI
TovalidateStep3.5Flash’sefficacyinreal-worldagenticscenarios, weevaluateonAndroidDaily
Hard[189],achallengingbenchmarkdesignedforChinesemobileapplicationenvironments. This
benchmarkcomprisescompositionaltasksspanninge-commercetransactions,multimediainteractions,
and daily mobile operations, offering a naturalistic testbed for assessing GUI agent capabilities in
complex,multi-stepworkflowsrepresentativeofproductiondeployments.
Weempiricallyinvestigatetwoarchitecturalinstantiations: (1)Step-GUI[189],alightweighton-device
agent(EdgeOnly)thatexecutestasksautonomouslyusinglocalcomputationalresources,and(2)Step
3.5Flash+Step-GUI,anedge-cloudcollaborativeframeworkwhereinStep3.5Flashfunctionsas
acloud-basedreasoningorchestratorthatsynthesizeshigh-leveltaskplans,decomposestheminto
executable primitives via the GUI-MCP protocol, and delegates low-level control to the on-device
Step-GUIagent. Thishierarchicalarchitectureexploitsthecomplementarystrengthsofcloud-scale
reasoningandedgeefficiency: Step3.5Flash’s11Bactiveparametersenablesophisticatedmulti-step
planningandcontextualunderstanding,whileStep-GUIensureslow-latencyactionexecutionand
privacy-preservinglocalcontrol.

QuantitativeResults. Theedge-cloudcollaborativeparadigmachievesasuccessrateof57.0%on
AndroidDailyHard,substantiallyoutperformingtheedge-onlybaseline(40.0%). Thisresultsuggests
thatcombiningstrongcloud-sidereasoningwithefficientedgeexecutionisaneffectivestrategyfor
navigatingdeploymentconstraintsinmulti-roundagentinteractions.
ArchitecturalGeneralization. Critically,thiscollaborativepatternextendsbeyondmobileecosys-
temstoheterogeneousplatformsincludingdesktopcomputersandautomotiveinfotainmentsystems.
Bydecouplingcognitiveorchestration(cloud)fromembodiedexecution(edge),theframeworkes-
tablishesascalableparadigmfordeployingsophisticatedagentsinresource-constrainedindustrial
environments—directly aligned with Step 3.5 Flash’s design objective of redefining the efficiency
frontierforproduction-gradeagenticsystems. Theresultsunderscorethateffectivereal-worldagents
requirenotonlyadvancedreasoningcapabilitiesbutalsoarchitecturesthatharmonizecomputational
distributionacrossinfrastructuretiers.
## References
[1] DeepSeek-AI. Deepseek-v3.2-exp: Boostinglong-contextefficiencywithdeepseeksparseatten-
tion,2025.
[2] AohanZeng,XinLv,QinkaiZheng,ZhenyuHou,BinChen,ChengxingXie,CunxiangWang,
DaYin,HaoZeng,JiajieZhang,etal. Glm-4.5: Agentic,reasoning,andcoding(arc)foundation
models. arXivpreprintarXiv:2508.06471,2025.
[3] LLM-CoreXiaomi. Mimo-v2-flashtechnicalreport,2026.
[4] Meituan LongCat Team, Bei Li, Bingye Lei, Bo Wang, Bolin Rong, Chao Wang, Chao Zhang,
Chen Gao, Chen Zhang, Cheng Sun, et al. Longcat-flash technical report. arXiv preprint
arXiv:2509.01322,2025.
[5] KimiTeam,YifanBai,YipingBao,GuanduoChen,JiahaoChen,NingxinChen,RuijueChen,
Yanru Chen, Yuankun Chen, Yutian Chen, et al. Kimi k2: Open agentic intelligence. arXiv
preprintarXiv:2507.20534,2025.
[6] MiniMaxTeam. Minimax-m2.1,2025.
[7] OpenAI. Gpt-5.2,2025.
[8] GoogleDeepMind. Gemini3promodelcard,2025.
[9] Anthropic. Systemcard: Claudeopus4.5,2025.
[10] AngelosKatharopoulos,ApoorvVyas,NikolaosPappas,andFrançoisFleuret. Transformersare
rnns: fastautoregressivetransformerswithlinearattention. InProceedingsofthe37thInternational
ConferenceonMachineLearning,ICML’20.JMLR.org,2020.
[11] HMMT. Hmmt2025feb.,2025.
[12] NamanJain,KingHan,AlexGu,Wen-DingLi,FanjiaYan,TianjunZhang,SidaWang,Armando
Solar-Lezama,KoushikSen,andIonStoica. Livecodebench: Holisticandcontaminationfree
evaluationoflargelanguagemodelsforcode. arXivpreprintarXiv:2403.07974,2024.
[13] OpenAI. Introducing SWE-bench verified we’re releasing a human-validated subset of swe-
benchthatmore,2024.
[14] JohnYang,KilianLieret,CarlosE.Jimenez,AlexanderWettig,KabirKhandpur,YanzheZhang,
BinyuanHui,OfirPress,LudwigSchmidt,andDiyiYang. Swe-smith: Scalingdataforsoftware
engineeringagents,2025.

https://github.com/sierra-research/tau2-bench
[15] SierraResearch. tau2-bench. ,2025.
[16] MikeAMerrill,AlexanderGShaw,NicholasCarlini,BoxuanLi,HarshRaj,IvanBercovich,Lin
Shi,JeongYeonShin,ThomasWalshe,EKellyBuchanan,etal. Terminal-bench: Benchmarking
agentsonhard,realistictasksincommandlineinterfaces. arXivpreprintarXiv:2601.11868,2026.
[17] JasonWei,ZhiqingSun,SpencerPapay,ScottMcKinney,JeffreyHan,IsaFulford,HyungWon
Chung,AlexTachardPassos,WilliamFedus,andAmeliaGlaese. Browsecomp: Asimpleyet
challengingbenchmarkforbrowsingagents,2025.
[18] PeilinZhou,BruceLeon,XiangYing,CanZhang,YifanShao,QichenYe,DadingChong,Zhiling
Jin,ChenxuanXie,MengCao,YuxinGu,SixinHong,JingRen,JianChen,ChaoLiu,andYining
Hua. Browsecomp-zh: Benchmarkingwebbrowsingabilityoflargelanguagemodelsinchinese,
2025.
[19] GrégoireMialon,ClémentineFourrier,CraigSwift,ThomasWolf,YannLeCun,andThomas
Scialom. Gaia: abenchmarkforgeneralaiassistants,2023.
[20] KaiyuanChen,YixinRen,YangLiu,XiaoboHu,HaotongTian,TianbaoXie,FangfuLiu,Haoye
Zhang,HongzhangLiu,YuanGong,etal. xbench: Trackingagentsproductivityscalingwith
profession-alignedreal-worldevaluations. arXivpreprintarXiv:2506.13651,2025.
[21] ManasiSharma,ChenBoCalvinZhang,etal. Researchrubrics: Abenchmarkofpromptsand
rubricsforevaluatingdeepresearchagents. arXivpreprintarXiv:2511.07685,2025.
[22] William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: Scaling to trillion
parametermodelswithsimpleandefficientsparsity. arXivpreprintarXiv:2101.03961,2021.
[23] BarretZoph,IrwanBello,SameerKumar,NanDu,YanpingHuang,JeffDean,NoamShazeer,
andWilliamFedus. St-moe: Designingstableandtransferablesparseexpertmodels,2022.
[24] NanDu,YanpingHuang,AndrewMDai,SimonTong,DmitryLepikhin,YuanzhongXu,Maxim
Krikun,YanqiZhou,AdamsWeiYu,OrhanFirat,BarretZoph,LiamFedus,MaartenPBosma,
ZongweiZhou,TaoWang,EmmaWang,KellieWebster,MariePellat,KevinRobinson,Kathleen
Meier-Hellstern,TojuDuke,LucasDixon,KunZhang,QuocLe,YonghuiWu,ZhifengChen,and
ClaireCui. GLaM:Efficientscalingoflanguagemodelswithmixture-of-experts. InKamalika
Chaudhuri,StefanieJegelka,LeSong,CsabaSzepesvari,GangNiu,andSivanSabato,editors,
Proceedingsofthe39thInternationalConferenceonMachineLearning,volume162ofProceedingsof
MachineLearningResearch,pages5547–5569.PMLR,17–23Jul2022.
[25] DmitryLepikhin,HyoukJoongLee,YuanzhongXu,DehaoChen,OrhanFirat,YanpingHuang,
MaximKrikun,NoamShazeer,andZhifengChen. Gshard: Scalinggiantmodelswithcondi-
tionalcomputationandautomaticsharding,2020.
[26] Damai Dai, Chengqi Deng, Chenggang Zhao, R. X. Xu, Huazuo Gao, Deli Chen, Jiashi Li,
Wangding Zeng, Xingkai Yu, Y. Wu, Zhenda Xie, Y. K. Li, Panpan Huang, Fuli Luo, Chong
Ruan,ZhifangSui,andWenfengLiang. Deepseekmoe: Towardsultimateexpertspecialization
inmixture-of-expertslanguagemodels,2024.
[27] RewonChild,ScottGray,AlecRadford,andIlyaSutskever. Generatinglongsequenceswith
sparsetransformers. CoRR,abs/1904.10509,2019.
[28] FabianGloeckle,BadrYoubiIdrissi,BaptisteRozière,DavidLopez-Paz,andGabrielSynnaeve.
Better&fasterlargelanguagemodelsviamulti-tokenprediction. arXivpreprintarXiv:2404.19737,
2024.
[29] DeepSeek-AI. Deepseek-v3technicalreport. arXivpreprintarXiv:2412.19437,2024.
[30] LLMXiaomi,BingquanXia,BowenShen,DaweiZhu,DiZhang,GangWang,HailinZhang,
Huaqiu Liu, Jiebao Xiao, Jinhao Dong, et al. Mimo: Unlocking the reasoning potential of
languagemodel–frompretrainingtoposttraining. arXivpreprintarXiv:2505.07608,2025.

[31] ZihanQiu,ZekunWang,BoZheng,ZeyuHuang,KaiyueWen,SonglinYang,RuiMen,LeYu,
FeiHuang,SuozhiHuang,DayihengLiu,JingrenZhou,andJunyangLin. Gatedattentionfor
largelanguagemodels: Non-linearity,sparsity,andattention-sink-free,2025.
[32] StepFunTeam. Step3: Cost-effectivemultimodalintelligence.
[33] OpenAI. Gpt-oss-120b&gpt-oss-20bmodelcard,2025.
[34] Keller Jordan, Yuchen Jin, Vlado Boza, Jiacheng You, Franz Cesista, Laker Newhouse, and
JeremyBernstein. Muon: Anoptimizerforhiddenlayersinneuralnetworks,2024.
[35] JasonWei,NguyenKarina,HyungWonChung,YunxinJoyJiao,SpencerPapay,AmeliaGlaese,
JohnSchulman,andWilliamFedus. Measuringshort-formfactualityinlargelanguagemodels.
arXivpreprintarXiv:2411.04368,2024.
[36] Chujie Zheng, Shixuan Liu, Mingze Li, Xiong-Hui Chen, Bowen Yu, Chang Gao, Kai Dang,
Yuqiong Liu, Rui Men, An Yang, et al. Group sequence policy optimization. arXiv preprint
arXiv:2507.18071,2025.
[37] FengYao,LiyuanLiu,DinghuaiZhang,ChengyuDong,JingboShang,andJianfengGao. Your
efficientrlframeworksecretlybringsyouoff-policyrltraining,August2025.
[38] WenhanMa,HailinZhang,LiangZhao,YifanSong,YudongWang,ZhifangSui,andFuliLuo.
Stabilizingmoereinforcementlearningbyaligningtrainingandinferencerouters. arXivpreprint
arXiv:2510.11370,2025.
[39] NicholasMetropolis,AriannaWRosenbluth,MarshallNRosenbluth,AugustaHTeller,and
EdwardTeller. Equationofstatecalculationsbyfastcomputingmachines. Thejournalofchemical
physics,21(6):1087–1092,1953.
[40] WKeithHastings. Montecarlosamplingmethodsusingmarkovchainsandtheirapplications.
1970.
[41] ThangLuong,DawsenHwang,HoangH.Nguyen,GolnazGhiasi,YuriChervonyi,InsukSeo,
JunsuKim,GarrettBingham,JonathanLee,SwaroopMishra,AlexZhai,ClaraHuiyiHu,Henryk
Michalewski,JiminKim,JeonghyunAhn,JunhwiBae,XingyouSong,TrieuH.Trinh,QuocV.
Le,andJunehyukJung. Towardsrobustmathematicalreasoning,2025.
[42] Jingcheng Hu, Yinmin Zhang, Shijie Shang, Xiaobo Yang, Yue Peng, Zhewei Huang, Hebin
Zhou, Xin Wu, Jie Cheng, Fanqi Wan, Xiangwen Kong, Chengyuan Yao, Kaiwen Yan, Ailin
Huang, Hongyu Zhou, Qi Han, Zheng Ge, Daxin Jiang, Xiangyu Zhang, and Heung-Yeung
Shum. Pacore: Learningtoscaletest-timecomputewithparallelcoordinatedreasoning,2026.
https://www.anthropic.com/engineering/building-effec
[43] Buildingeffectiveagents.
tive-agents
.
https://openai.com/index/unrolling-the-codex-a
[44] Unrollingthecodexagentloop.
gent-loop/
.
[45] CharlieVictorSnell,JaehoonLee,KelvinXu,andAviralKumar. ScalingLLMtest-timecom-
puteoptimallycanbemoreeffectivethanscalingparametersforreasoning. InTheThirteenth
InternationalConferenceonLearningRepresentations,2025.
[46] NiklasMuennighoff,ZitongYang,WeijiaShi,XiangLisaLi,LiFei-Fei,HannanehHajishirzi,
Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and Tatsunori B Hashimoto. s1: Simple
test-timescaling. InProceedingsofthe2025ConferenceonEmpiricalMethodsinNaturalLanguage
Processing,pages20286–20332,2025.
[47] XinyuYang,YuweiAn,HongyiLiu,TianqiChen,andBeidiChen. Multiverse: Yourlanguage
models secretly decide how to parallelize and merge generation. In The Thirty-ninth Annual
ConferenceonNeuralInformationProcessingSystems,2025.

[48] IzBeltagy,MatthewE.Peters,andArmanCohan. Longformer: Thelong-documenttransformer.
arXiv:2004.05150,2020.
[49] GemmaTeam,AishwaryaKamath,JohanFerret,etal. Gemma3technicalreport,2025.
[50] Yaniv Leviathan, Matan Kalman, and Yossi Matias. Fast inference from transformers via
speculative decoding. In Proceedings of the 40th International Conference on Machine Learning,
ICML’23.JMLR.org,2023.
[51] Imanol Schlag, Kazuki Irie, and Jürgen Schmidhuber. Linear transformers are secretly fast
weightprogrammers. InInternationalconferenceonmachinelearning,pages9355–9366.PMLR,
2021.
[52] JikaiWang,YiSu,JuntaoLi,QingrongXia,ZiYe,XinyuDuan,ZhefengWang,andMinZhang.
Opt-tree: Speculativedecodingwithadaptivedrafttreestructure. TransactionsoftheAssociation
forComputationalLinguistics,13:188–199,2025.
[53] YunfanXiong,RuoyuZhang,YanzengLi,andLeiZou. Dyspec: Fasterspeculativedecoding
withdynamictokentreestructure. WorldWideWeb,28(3):36,2025.
[54] HaoranYou,YichaoFu,ZhengWang,AmirYazdanbakhsh,andYingyan(Celine)Lin. When
linearattentionmeetsautoregressivedecoding: towardsmoreeffectiveandefficientlinearized
large language models. In Proceedings of the 41st International Conference on Machine Learning,
ICML’24.JMLR.org,2024.
[55] Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebron, and
SumitSanghai. GQA:Traininggeneralizedmulti-querytransformermodelsfrommulti-head
checkpoints. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Proceedings of the 2023
Conference on Empirical Methods in Natural Language Processing, pages 4895–4901, Singapore,
December2023.AssociationforComputationalLinguistics.
[56] Yuhui Li, FangyunWei, Chao Zhang, and Hongyang Zhang. EAGLE: Speculativesampling
requiresrethinkingfeatureuncertainty. InInternationalConferenceonMachineLearning,2024.
[57] GemmaTeam,ThomasMesnard,CassidyHardin,RobertDadashi,SuryaBhupatiraju,Shreya
Pathak,LaurentSifre,MorganeRivière,MihirSanjayKale,JulietteLove,etal. Gemma: Open
modelsbasedongeminiresearchandtechnology,2024.
[58] Team Cohere, :, Aakanksha, Arash Ahmadian, Marwan Ahmed, et al. Command a: An
enterprise-readylargelanguagemodel,2025.
[59] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient stream-
ing language models with attention sinks. In The Twelfth International Conference on Learning
Representations,2024.
[60] MingjieSun,XinleiChen,JZicoKolter,andZhuangLiu. Massiveactivationsinlargelanguage
models. InFirstConferenceonLanguageModeling,2024.
[61] XiangmingGu,TianyuPang,ChaoDu,QianLiu,FengzhuoZhang,CunxiaoDu,YeWang,and
MinLin. Whenattentionsinkemergesinlanguagemodels: Anempiricalview. InTheThirteenth
InternationalConferenceonLearningRepresentations,2025.
[62] JohnJumper,RichardEvans,AlexanderPritzel,TimGreen,MichaelFigurnov,OlafRonneberger,
Kathryn Tunyasuvunakool, Russ Bates, Augustin Žídek, Anna Potapenko, Alex Bridgland,
Clemens Meyer, Simon A. A. Kohl, Andrew J. Ballard, Andrew Cowie, Bernardino Romera-
Paredes,StanislavNikolov,RishubJain,JonasAdler,TrevorBack,StigPetersen,DavidReiman,
EllenClancy,MichalZielinski,MartinSteinegger, MichalinaPacholska, TamasBerghammer,
Sebastian Bodenstein, David Silver, Oriol Vinyals, Andrew W. Senior, Koray Kavukcuoglu,
Pushmeet Kohli, and Demis Hassabis. Highly accurate protein structure prediction with
AlphaFold. Nature,596(7873):583–589,August2021.

[63] ZhixuanLin,EvgeniiNikishin,XuHe,andAaronCourville. Forgettingtransformer: Softmax
attentionwithaforgetgate. InTheThirteenthInternationalConferenceonLearningRepresentations,
2025.
[64] LeanWang,HuazuoGao,ChenggangZhao,XuSun,andDamaiDai. Auxiliary-loss-freeload
balancingstrategyformixture-of-experts. arXivpreprintarXiv:2408.15664,2024.
[65] YuxuanCai,XiaozhuanLiang,XinghuaWang,JinMa,HaijinLiang,JinwenLuo,XinyuZuo,
LishengDuan,YuyangYin,andXiChen. Fastmtp: Acceleratingllminferencewithenhanced
multi-tokenprediction,2025.
[66] JasonAnsel,EdwardYang,HoraceHe,NataliaGimelshein,AnimeshJain,MichaelVoznesensky,
Bin Bao, Peter Bell, David Berard, Evgeni Burovski, Geeta Chauhan, Anjali Chourdia, Will
Constable, Alban Desmaison, Zachary DeVito, Elias Ellison, Will Feng, Jiong Gong, Michael
Gschwind,BrianHirsh,SherlockHuang,KshiteejKalambarkar,LaurentKirsch,MichaelLazos,
MarioLezcano,YanboLiang,JasonLiang,YinghaiLu,CKLuk,BertMaher,YunjiePan,Christian
Puhrsch,MatthiasReso,MarkSaroufim,MarcosYukioSiraichi,HelenSuk,MichaelSuo,Phil
Tillet, Eikan Wang, Xiaodong Wang, William Wen, Shunting Zhang, Xu Zhao, Keren Zhou,
RichardZou,AjitMathews,GregoryChanan,PengWu,andSoumithChintala.PyTorch2: Faster
MachineLearningThroughDynamicPythonBytecodeTransformationandGraphCompilation.
In 29th ACM International Conference on Architectural Support for Programming Languages and
OperatingSystems,Volume2(ASPLOS’24).ACM,April2024.
[67] MohammadShoeybi,MostofaPatwary,RaulPuri,PatrickLeGresley,JaredCasper,andBryan
Catanzaro. Megatron-lm: Training multi-billion parameter language models using model
parallelism. arXivpreprintarXiv:1909.08053,2019.
[68] DeepakNarayanan,MohammadShoeybi,JaredCasper,PatrickLeGresley,MostofaPatwary,
VijayAnandKorthikanti,DmitriVainbrand,PrethviKashinkunti,JulieBernauer,BryanCatan-
zaro,AmarPhanishayee,andMateiZaharia. Efficientlarge-scalelanguagemodeltrainingon
gpuclustersusingmegatron-lm,2021.
[69] Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. Zero: Memory opti-
mizationstowardtrainingtrillionparametermodels. InSC20: InternationalConferenceforHigh
PerformanceComputing,Networking,StorageandAnalysis,pages1–16,2020.
[70] DennisLiu,ZijieYan,XinYao,TongLiu,VijayKorthikanti,EvanWu,ShiqingFan,GaoDeng,
HongxiaoBai,JianbinChang,AshwathAithal,MichaelAndersch,MohammadShoeybi,Jiajie
Yao,ChandlerZhou,DavidWu,XipengLi,andJuneYang. Moeparallelfolding: Heterogeneous
parallelismmappingsforefficientlarge-scalemoemodeltrainingwithmegatroncore,2025.
[71] WentaoGuo,MayankMishra,XinleCheng,IonStoica,andTriDao. Sonicmoe: Accelerating
moewithioandtile-awareoptimizations,2025.
[72] JeremyBernsteinandLakerNewhouse. Oldoptimizer,newnorm: Ananthology,2024.
[73] Noah Amsel, David Persson, Christopher Musco, and Robert M. Gower. The polar express:
Optimalmatrixsignmethodsandtheirapplicationtothemuonalgorithm,2025.
[74] ZihanQiu,ZeyuHuang,BoZheng,KaiyueWen,ZekunWang,RuiMen,IvanTitov,Dayiheng
Liu,JingrenZhou,andJunyangLin. Demonsinthedetail: Onimplementingloadbalancing
lossfortrainingspecializedmixture-of-expertmodels. arXivpreprintarXiv:2501.11873,2025.
[75] AnYang,AnfengLi,BaosongYang,BeichenZhang,BinyuanHui,BoZheng,BowenYu,Chang
Gao,ChengenHuang,ChenxuLv,ChujieZheng,DayihengLiu,FanZhou,FeiHuang,FengHu,
HaoGe,HaoranWei,HuanLin,JialongTang,JianYang,JianhongTu,JianweiZhang,Jianxin
Yang,JiaxiYang,JingZhou,JingrenZhou,JunyangLin,KaiDang,KeqinBao,KexinYang,LeYu,
LianghaoDeng,MeiLi,MingfengXue,MingzeLi,PeiZhang,PengWang,QinZhu,RuiMen,
RuizeGao,ShixuanLiu,ShuangLuo,TianhaoLi,TianyiTang,WenbiaoYin,XingzhangRen,

XinyuWang,XinyuZhang,XuanchengRen,YangFan,YangSu,YichangZhang,YingerZhang,
YuWan,YuqiongLiu,ZekunWang,ZeyuCui,ZhenruZhang,ZhipengZhou,andZihanQiu.
Qwen3technicalreport. arXivpreprintarXiv:2505.09388,2025.
[76] AlecRadford,JeffWu,RewonChild,DavidLuan,DarioAmodei,andIlyaSutskever. Language
modelsareunsupervisedmultitasklearners. 2019.
[77] RuibinXiong,YunchangYang,DiHe,KaiZheng,ShuxinZheng,ChenXing,HuishuaiZhang,
YanyanLan,LiweiWang,andTieyanLiu.Onlayernormalizationinthetransformerarchitecture.
InInternationalconferenceonmachinelearning,pages10524–10533.PMLR,2020.
[78] NoamShazeer. Gluvariantsimprovetransformer,2020.
https://commoncrawl.org
[79] CommonCrawl. Commoncrawl. .
[80] SimingHuang,TianhaoCheng,J.K.Liu,JiaranHao,LiuyihanSong,YangXu,J.Yang,Jiaheng
Liu, Chenchen Zhang, Linzheng Chai, Ruifeng Yuan, Zhaoxiang Zhang, Jie Fu, Qian Liu,
GeZhang,ZiliWang,YuanQi,YinghuiXu,andWeiChu. Opencoder: Theopencookbookfor
top-tiercodelargelanguagemodels,2025.
[81] CarlosEJimenez,JohnYang,AlexanderWettig,ShunyuYao,KexinPei,OfirPress,andKarthikR
Narasimhan. SWE-bench: Canlanguagemodelsresolvereal-worldgithubissues? InTheTwelfth
InternationalConferenceonLearningRepresentations,2024.
[82] ChunqiuStevenXia,YinlinDeng,SorenDunn,andLingmingZhang. Agentless: Demystifying
llm-basedsoftwareengineeringagents. arXivpreprintarXiv:2407.01489,2024.
[83] Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu. Roformer:
Enhancedtransformerwithrotarypositionembedding,2024.
[84] Wenhan Xiong, Jingyu Liu, Igor Molybog, Hejia Zhang, Prajjwal Bhargava, Rui Hou, Louis
Martin,RashiRungta,KarthikAbinavSankararaman,BarlasOguz,etal. Effectivelong-context
scalingoffoundationmodels,2024.
[85] Aixin Liu, Aoxue Mei, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu,
BoweiZhang,ChaofanLin,ChenDong,etal. Deepseek-v3.2: Pushingthefrontierofopenlarge
languagemodels. arXivpreprintarXiv:2512.02556,2025.
[86] YixinYe,ZhenHuang,YangXiao,EthanChern,ShijieXia,andPengfeiLiu. Limo: Lessismore
forreasoning,2025.
[87] FabioPardo,ArashTavakoli,VitalyLevdik,andPetarKormushev. Timelimitsinreinforcement
learning,2022.
[88] MichaelLuo,SijunTan,JustinWong,XiaoxiangShi,WilliamY.Tang,MananRoongta,ColinCai,
JeffreyLuo,LiErranLi,RalucaAdaPopa,andIonStoica. Deepscaler: Surpassingo1-preview
https://pretty-radio-b75.notion.site/DeepScale
witha1.5bmodelbyscalingrl.
R-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468
005bed8ca303013a4e2
,2025. NotionBlog.
[89] QiyingYu,ZhengZhang,RuofeiZhu,YufengYuan,XiaochenZuo,YuYue,WeinanDai,Tiantian
Fan,GaohongLiu,LingjunLiu,etal. Dapo: Anopen-sourcellmreinforcementlearningsystem
atscale. arXivpreprintarXiv:2503.14476,2025.
[90] JingchengHu,YinminZhang,QiHan,DaxinJiang,XiangyuZhang,andHeung-YeungShum.
Open-Reasoner-Zero: An open source approach to scaling up reinforcement learning on the
basemodel. arXivpreprintarXiv:2503.24290,2025.

[91] Minh-ThangLuong,DawsenHwang,HoangHNguyen,GolnazGhiasi,YuriChervonyi,Insuk
Seo, Junsu Kim, Garrett Bingham, Jonathan Lee, Swaroop Mishra, et al. Towards robust
mathematical reasoning. In Proceedings of the 2025 Conference on Empirical Methods in Natural
LanguageProcessing,pages35406–35430,2025.
[92] FrançoisChollet. Onthemeasureofintelligence. arXivpreprintarXiv:1911.01547,2019.
[93] LongPhan,AliceGatti,ZiwenHan,NathanielLi,JosephinaHu,HughZhang,ChenBoCalvin
Zhang,MohamedShaaban,JohnLing,SeanShi,etal. Humanity’slastexam,2025.
[94] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of
mathematicalreasoninginopenlanguagemodels,2024.
[95] Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin,
Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton,
FraserKelton,LukeMiller,MaddieSimens,AmandaAskell,PeterWelinder,PaulChristiano,
Jan Leike, and Ryan Lowe. Training language models to follow instructions with human
feedback,2022.
[96] Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh
Agarwal. Generativeverifiers: Rewardmodelingasnext-tokenprediction,2025.
[97] Ralph Allan Bradley and Milton E Terry. Rank analysis of incomplete block designs: I. the
methodofpairedcomparisons. Biometrika,39(3/4):324–345,1952.
[98] ChenHu,HaikuoDu,HengWang,LinLin,MingruiChen,PengLiu,RuihangMiao,Tianchi
Yue,WangYou,WeiJi,WeiYuan,WenjinDeng,XiaojianYuan,XiaoyunZhang,XiangyuLiu,
XikaiLiu,YanmingXu,YichengCao,YifeiZhang,YongyaoWang,YuboShu,YurongZhang,
YuxiangZhang,ZhengGong,ZhichaoChang,BinyanLi,DanMa,FurongJia,HongyuanWang,
Jiayu Liu, Jing Bai, Junlan Liu, Manjiao Liu, Na Wang, Qiuping Wu, Qinxin Du, Shiwei Li,
WenSun,YifengGong,YonglinChen,YulingZhao,YuxuanLin,ZiqiRen,ZixuanWang,Aihu
Zhang, Brian Li, Buyun Ma, Kang An, Li Xie, Mingliang Li, Pan Li, Shidong Yang, Xi Chen,
XiaojiaLiu,YuchuLuo,YuanSong,YuanHaoDing,YuanweiLiang,ZexiLi,ZhaoningZhang,
ZixinZhang,BinxingJiao,DaxinJiang,JianshengChen,JingLi,XiangyuZhang,andYiboZhu.
Step-deepresearchtechnicalreport,2025.
[99] JiaLi,EdwardBeeching,LewisTunstall,BenLipkin,RomanSoletskyi,ShengyiHuang,Kashif
Rasul,LonghuiYu,AlbertQJiang,ZijuShen,etal. Numinamath: Thelargestpublicdatasetin
ai4mathswith860kpairsofcompetitionmathproblemsandsolutions. 2024.
[100] AlonAlbalaketal. Big-math: Alarge-scale,high-qualitymathdatasetforreinforcementlearning
inlanguagemodels. arXivpreprintarXiv:2502.17387,2025.
[101] ArindamMitra,HamedKhanpour,CorbyRosset,andAhmedAwadallah. Orca-math: Unlock-
ingthepotentialofslmsingradeschoolmath. arXivpreprintarXiv:2402.14830,2024.
https://huggingface.co/datasets/aslawliet/olympiads
[102] aslawliet. Olympiads. ,
## 2024. HuggingFacedataset.
https://huggingface.co/datasets/aslawliet/cn-k12
[103] aslawliet. Cn-k12. , 2024.
HuggingFacedatasetofChineseK-12mathproblems.
https://huggingface.co/datasets/open-r1/Open
[104] Open-R1Team. Openr1-math-220k.
R1-Math-220k
,2025. Open-sourcedistilledmathreasoningdataset.
[105] X. He et al. Deepmath-103k: A large-scale, challenging math qa benchmark. arXiv preprint
arXiv:2504.11456,2025.

[106] Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Tiantian Fan,
GaohongLiu,LingjunLiu,XinLiu,HaibinLin,ZhiqiLin,BoleMa,GuangmingSheng,Yuxuan
Tong,ChiZhang,MofanZhang,WangZhang,HangZhu,JinhuaZhu,JiazeChen,JiangjieChen,
ChengyiWang,HongliYu,WeinanDai,YuxuanSong,XiangpengWei,HaoZhou,JingjingLiu,
Wei-YingMa,Ya-QinZhang,LinYan,MuQiao,YonghuiWu,andMingxuanWang. DAPO:An
open-sourceLLMreinforcementlearningsystematscale,2025.
[107] Etash Guha et al. Openthoughts: Data recipes for reasoning models. arXiv preprint
arXiv:2506.04178,2025.
https://arxiv.org/abs/2501.193
[108] NiklasMuennighoffetal. s1: Simpletest-timescaling.
,2025.
[109] YunjieJi,XiaoyuTian,SitongZhao,HaotianWang,ShuaitingChen,YipingPeng,HanZhao,
andXiangangLi. Am-thinking-v1: Advancingthefrontierofreasoningat32bscale,2025.
[110] LIMO Authors. Less is more for reasoning: Semi-parametric math reasoners. arXiv preprint
arXiv:2502.03387,2025.
[111] RongaoLi,JieFu,Bo-WenZhang,TaoHuang,ZhihongSun,ChenLyu,GuangLiu,ZhiJin,and
GeLi. Taco: Topicsinalgorithmiccodegenerationdataset,2023.
[112] MichaelLuo,SijunTan,RoyHuang,AmeenPatel,AlpayAriyak,QingyangWu,XiaoxiangShi,
RachelXin,ColinCai,MauriceWeber,CeZhang,LiErranLi,RalucaAdaPopa,andIonStoica.
https://www.together.ai/bl
Deepcoder: Afullyopen-source14bcoderato3-minilevel.
og/deepcoder
,2025. TechnicalBlog.
[113] ZihanWang,SiyaoLiu,YangSun,HongyanLi,andKaiShen. Codecontests+: High-qualitytest
casegenerationforcompetitiveprogramming,2025.
[114] Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard
Ghanem. Camel: Communicativeagentsfor"mind"explorationoflargescalelanguagemodel
society,2023.
[115] AkhiadBercovich,ItayLevy,IzikGolan,MohammadDabbah,RanEl-Yaniv,OmriPuny,Ido
Galil,ZachMoshe,TomerRonen,NajeebNabwani,etal. Llama-nemotron: Efficientreasoning
models,2025.
[116] Run-ZeFan,ZengzhiWang,andPengfeiLiu.Megascience: Pushingthefrontiersofpost-training
datasetsforsciencereasoning. arXivpreprintarXiv:2507.16812,2025.
[117] WentingZhao,XiangRen,JackHessel,ClaireCardie,YejinChoi,andYuntianDeng. Wildchat:
1mchatgptinteractionlogsinthewild. arXivpreprintarXiv:2405.01470,2024.
[118] JuntengLiu,YunjiLi,ChiZhang,JingyangLi,AiliChen,KeJi,WeiyuCheng,ZijiaWu,Chengyu
Du,QidiXu,etal. Webexplorer: Exploreandevolvefortraininglong-horizonwebagents. arXiv
preprintarXiv:2509.06501,2025.
[119] KuanLi,ZhongwangZhang,HuifengYin,LiwenZhang,LituOu,JialongWu,WenbiaoYin,
BaixuanLi,ZhengweiTao,XinyuWang,etal. Websailor: Navigatingsuper-humanreasoning
forwebagent. arXivpreprintarXiv:2507.02592,2025.
[120] Yuetai Li, Huseyin A Inan, Xiang Yue, Wei-Ning Chen, Lukas Wutschitz, Janardhan Kulka-
rni,RadhaPoovendran,RobertSim,andSaravanRajmohan. Simulatingenvironmentswith
reasoningmodelsforagenttraining. arXivpreprintarXiv:2511.01824,2025.
[121] Lianghong Guo, Yanlin Wang, Caihua Li, Wei Tao, Pengyu Yang, Jiachi Chen, Haoyu Song,
DuyuTang,andZibinZheng. Swe-factory: Yourautomatedfactoryforissueresolutiontraining
dataandevaluationbenchmarks,2026.

[122] JiaranZhang,LuckMa,YanhaoLi,FanqiWan,DiQi,XuZhao,JieyiHou,ZheXie,Mengqiang
Ren,XinWu,ZheweiHuang,LiangyuChen,YingweiMa,QiHan,andXiangyuZhang. Dock-
smith: Scalingreliablecodingenvironmentsviaanagenticdockerbuilder,2026.
[123] JohnYang,KilianLieret,CarlosEJimenez,AlexanderWettig,KabirKhandpur,YanzheZhang,
BinyuanHui,OfirPress,LudwigSchmidt,andDiyiYang. Swe-smith: Scalingdataforsoftware
engineeringagents. arXivpreprintarXiv:2504.21798,2025.
[124] Jiayi Pan, Xingyao Wang, Graham Neubig, Navdeep Jaitly, Heng Ji, Alane Suhr, and Yizhe
Zhang. Training software engineering agents and verifiers with swe-gym. arXiv preprint
arXiv:2412.21139,2024.
[125] NamanJain,JaskiratSingh,ManishShetty,LiangZheng,KoushikSen,andIonStoica. R2e-gym:
Procedural environments and hybrid verifiers for scaling open-weights swe agents. arXiv
preprintarXiv:2504.07164,2025.
[126] Ibragim Badertdinov, Alexander Golubev, Maksim Nekrashevich, Anton Shevtsov, Simon
Karasik,AndreiAndriushchenko,MariaTrofimova,DariaLitvintseva,andBorisYangel. Swe-
rebench: Anautomatedpipelinefortaskcollectionanddecontaminatedevaluationofsoftware
engineeringagents. arXivpreprintarXiv:2505.20411,2025.
[127] Qijia Shen, Jay Rainton, Aznaur Aliev, Ahmed Awelkair, Boyuan Ma, Zhiqi Huang, Yuzhen
Mao,WendongFan,PhilipTorr,BernardGhanem,ChangranHu,UrmishThakker,andGuohao
Li. SETA:ScalingEnvironmentsforTerminalAgents,January2026.
[128] Xiaozhi Wang, Tianyu Gao, Zhaocheng Zhu, Zhengyan Zhang, Zhiyuan Liu, Juanzi Li, and
Jian Tang. Kepler: A unified model for knowledge embedding and pre-trained language
representation. TransactionsoftheAssociationforComputationalLinguistics,9:176–194,2021.
[129] DayaGuo,DejianYang,HaoweiZhang,JunxiaoSong,RuoyuZhang,RunxinXu,QihaoZhu,
Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1 incentivizes reasoning in llms through
reinforcementlearning. Nature,645(8081):633–638,September2025.
[130] AnYang,AnfengLi,BaosongYang,BeichenZhang,BinyuanHui,BoZheng,BowenYu,Chang
Gao,ChengenHuang,ChenxuLv,ChujieZheng,DayihengLiu,FanZhou,FeiHuang,FengHu,
HaoGe,HaoranWei,HuanLin,JialongTang,JianYang,JianhongTu,JianweiZhang,Jianxin
Yang,JiaxiYang,JingZhou,JingrenZhou,JunyangLin,KaiDang,KeqinBao,KexinYang,LeYu,
LianghaoDeng,MeiLi,MingfengXue,MingzeLi,PeiZhang,PengWang,QinZhu,RuiMen,
RuizeGao,ShixuanLiu,ShuangLuo,TianhaoLi,TianyiTang,WenbiaoYin,XingzhangRen,
XinyuWang,XinyuZhang,XuanchengRen,YangFan,YangSu,YichangZhang,YingerZhang,
YuWan,YuqiongLiu,ZekunWang,ZeyuCui,ZhenruZhang,ZhipengZhou,andZihanQiu.
Qwen3technicalreport,2025.
[131] XingyaoWang,BoxuanLi,YufanSong,FrankFXu,XiangruTang,MingchenZhuge,JiayiPan,
Yueqi Song, Bowen Li, Jaskirat Singh, et al. Openhands: An open platform for ai software
developersasgeneralistagents. arXivpreprintarXiv:2407.16741,2024.
[132] JohnYang,CarlosEJimenez,AlexanderWettig,KilianLieret,ShunyuYao,KarthikNarasimhan,
andOfirPress. Swe-agent: Agent-computerinterfacesenableautomatedsoftwareengineering.
AdvancesinNeuralInformationProcessingSystems,37:50528–50652,2024.
https://kilo.ai/
[133] Inc.KiloCode. Moveatkilospeed. ,2026. KiloCodewebpage.
https://roocode.com/
[134] Roo Code. Your ai software engineering team is here. , 2026. Roo
Codewebpage.
https://clau
[135] ANTHROPICPBC. Autocompletefinisheslines.claudecodefinishesfeatures.
de.com/product/claude-code
,2026. ClaudeCodewebpage.

[136] Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay, Hyung Won
Chung,AakankshaChowdhery,QuocV.Le,EdH.Chi,DennyZhou,andJasonWei.Challenging
big-benchtasksandwhetherchain-of-thoughtcansolvethem,2022.
[137] Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and
JacobSteinhardt. Measuringmassivemultitasklanguageunderstanding,2020.
[138] AryoPradiptaGema,JoshuaOngJunLeang,GiwonHong,AlessioDevoto,AlbertoCarloMaria
Mancino,RohitSaxena,XuanliHe,YuZhao,XiaotangDu,MohammadRezaGhasemiMadani,
ClaireBarale,RobertMcHardy,JoshuaHarris,JeanKaddour,EmilevanKrieken,andPasquale
Minervini. Arewedonewithmmlu?,2024.
[139] Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo,
WeimingRen,AaranArulraj,XuanHe,ZiyanJiang,TianleLi,MaxKu,KaiWang,AlexZhuang,
RongqiFan,XiangYue,andWenhuChen. Mmlu-pro: Amorerobustandchallengingmulti-task
languageunderstandingbenchmark,2024.
[140] Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. Hellaswag: Can a
machinereallyfinishyoursentence?,2019.
[141] KeisukeSakaguchi, RonanLeBras, ChandraBhagavatula, andYejinChoi. Winogrande: An
adversarialwinogradschemachallengeatscale,2019.
[142] DavidRein,BettyLiHou,AsaCooperStickland,JacksonPetty,RichardYuanzhePang,Julien
Dirani, Julian Michael, and Samuel R. Bowman. Gpqa: A graduate-level google-proof q&a
benchmark,2023.
[143] XinrunDu,YifanYao,KaijingMa,BingliWang,TianyuZheng,KingZhu,MinghaoLiu,Yiming
Liang,XiaolongJin,ZhenlinWei,etal. Supergpqa: Scalingllmevaluationacross285graduate
disciplines,2025.
https://github.com/openai/simple-evals
[144] OpenAI. Simpleqa. ,2024.
[145] KarlCobbe,VineetKosaraju,MohammadBavarian,MarkChen,HeewooJun,LukaszKaiser,
MatthiasPlappert,JerryTworek,JacobHilton,ReiichiroNakano,ChristopherHesse,andJohn
Schulman. Trainingverifierstosolvemathwordproblems,2021.
[146] DanHendrycks,CollinBurns,SauravKadavath,AkulArora,StevenBasart,EricTang,Dawn
Song,andJacobSteinhardt. Measuringmathematicalproblemsolvingwiththemathdataset,
2021.
[147] MarkChen,JerryTworek,HeewooJun,QimingYuan,HenriquePondedeOliveiraPinto,Jared
Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri,
GretchenKrueger,MichaelPetrov,HeidyKhlaaf,GirishSastry,PamelaMishkin,BrookeChan,
ScottGray,NickRyder,MikhailPavlov,AletheaPower,LukaszKaiser,MohammadBavarian,
Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert,
FotiosChantzis,ElizabethBarnes,ArielHerbert-Voss,WilliamHebgenGuss,AlexNichol,Alex
Paino,NikolasTezak,JieTang,IgorBabuschkin,SuchirBalaji,ShantanuJain,WilliamSaunders,
ChristopherHesse,AndrewN.Carr,JanLeike,JoshAchiam,VedantMisra,EvanMorikawa,
AlecRadford,MatthewKnight,MilesBrundage,MiraMurati,KatieMayer,PeterWelinder,Bob
McGrew,DarioAmodei,SamMcCandlish,IlyaSutskever,andWojciechZaremba. Evaluating
largelanguagemodelstrainedoncode,2021.
[148] JacobAustin,AugustusOdena,MaxwellNye,MaartenBosma,HenrykMichalewski,David
Dohan,EllenJiang,CarrieCai,MichaelTerry,QuocLe,andCharlesSutton. Programsynthesis
withlargelanguagemodels,2021.
[149] JiaweiLiu,ChunqiuStevenXia,YuyaoWang,andLingmingZhang. Isyourcodegeneratedby
chatgptreallycorrect? rigorousevaluationoflargelanguagemodelsforcodegeneration,2023.

[150] FedericoCassano,JohnGouwar,DanielNguyen,SydneyNguyen,LunaPhipps-Costin,Donald
Pinckney,Ming-HoYee,YangtianZi,CarolynJaneAnderson,MollyQFeldman,ArjunGuha,
Michael Greenberg, and Abhinav Jangda. Multipl-e: A scalable and extensible approach to
benchmarkingneuralcodegeneration,2022.
[151] YuzhenHuang,YuzhuoBai,ZhihaoZhu,JunleiZhang,JinghanZhang,TangjunSu,Junteng
Liu,ChuanchengLv,YikaiZhang,JiayiLei,YaoFu,MaosongSun,andJunxianHe. C-eval: A
multi-levelmulti-disciplinechineseevaluationsuiteforfoundationmodels,2023.
[152] Haonan Li, Yixuan Zhang, Fajri Koto, Yifei Yang, Hai Zhao, Yeyun Gong, Nan Duan, and
TimothyBaldwin. Cmmlu: Measuringmassivemultitasklanguageunderstandinginchinese,
2023.
[153] Yancheng He, Shilong Li, Jiaheng Liu, Yingshui Tan, Weixun Wang, Hui Huang, Xingyuan
Bu,HangyuGuo,ChengweiHu,BorenZheng,etal. Chinesesimpleqa: Achinesefactuality
evaluationforlargelanguagemodels,2024.
[154] LongPhan,TonyCYPang,AdamWecker,YifanXiong,DanHendrycks,etal. Humanity’slast
exam,2025.
[155] TianleLi,Wei-LinChiang,EvanFrick,LisaDunlap,BanghuaZhu,JosephE.Gonzalez,andIon
Stoica. Fromlivedatatohigh-qualitybenchmarks: Thearena-hardpipeline,April2024.
[156] ValentinaPyatkin,SaumyaMalik,VictoriaGraf,HamishIvison,ShengyiHuang,PradeepDasigi,
NathanLambert,andHannanehHajishirzi. Generalizingverifiableinstructionfollowing. arXiv
preprintarXiv:2507.02833,2025.
[157] VedSirdeshmukh,KaustubhDeshpande,JohannesMols,LifengJin,Ed-YeremaiCardona,Dean
Lee,JeremyKritz,WillowPrimack,SummerYue,andChenXing. Multichallenge: Arealistic
multi-turnconversationevaluationbenchmarkchallengingtofrontierllms,2025.
[158] YushiBai,ShangqingTu,JiajieZhang,HaoPeng,XiaozhiWang,XinLv,ShulinCao,JiazhengXu,
LeiHou,YuxiaoDong,JieTang,andJuanziLi. Longbenchv2: Towardsdeeperunderstanding
andreasoningonrealisticlong-contextmultitasks,2024.
[159] KiranVodrahalli,SantiagoOntanon,NileshTripuraneni,KelvinXu,SanilJain,RakeshShivanna,
JeffreyHui,NishanthDikkala,MehranKazemi,BahareFatemi,etal.Michelangelo: Longcontext
evaluationsbeyondhaystacksvialatentstructurequeries. arXivpreprintarXiv:2409.12640,2024.
[160] SatyapriyaKrishna,KalpeshKrishna,AnhadMohananey,StevenSchwarcz,AdamStambler,
ShyamUpadhyay,andManaalFaruqui. Fact,fetch,andreason: Aunifiedevaluationofretrieval-
augmentedgeneration. InProceedingsofthe2025ConferenceoftheNationsoftheAmericasChapter
of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long
Papers),pages4745–4759,2025.
[161] JiaweiLiu,JiaLeTian,VijayDaita,YuxiangWei,YifengDing,YuhanKatherineWang,JunYang,
andLingmingZhang. Repoqa: Evaluatinglongcontextcodeunderstanding,2024.
[162] Bowen Peng, Jeffrey Quesnelle, Honglu Fan, and Enrico Shippole. Yarn: Efficient context
windowextensionoflargelanguagemodels,2023.
[163] TianyuGao,AlexanderWettig,LuxiHe,YiheDong,SadhikaMalladi,andDanqiChen.Metadata
conditioning accelerates language model pre-training. In International Conference on Machine
Learning(ICML),2025.
[164] ZeyuanAllen-ZhuandYuanzhiLi. Physicsoflanguagemodels: Part3.3,knowledgecapacity
scalinglaws. arXivpreprintarXiv:2404.05405,2024.
[165] Dongyang Fan, Diba Hashemi, Sai Praneeth Karimireddy, and Martin Jaggi. Beyond urls:
Metadatadiversityandpositionforefficientllmpretraining,2025.

[166] MarkChen,JerryTworek,HeewooJun,QimingYuan,HenriquePondeDeOliveiraPinto,Jared
Kaplan,HarriEdwards,YuriBurda,NicholasJoseph,GregBrockman,etal. Evaluatinglarge
languagemodelstrainedoncode. arXivpreprintarXiv:2107.03374,2021.
[167] JacobAustin,AugustusOdena,MaxwellNye,MaartenBosma,HenrykMichalewski,David
Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. Program synthesis with large
languagemodels. arXivpreprintarXiv:2108.07732,2021.
[168] Colin White, Samuel Dooley, Manley Roberts, Arka Pal, Ben Feuer, Siddhartha Jain, Ravid
Shwartz-Ziv,NeelJain,KhalidSaifullah,SreemantiDey,Shubh-Agrawal,SandeepSinghSandha,
SiddarthaNaidu,ChinmayHegde,YannLeCun,TomGoldstein,WillieNeiswanger,andMicah
Goldblum. Livebench: Achallenging,contamination-limitedllmbenchmark,2025.
[169] MAA. Americaninvitationalmathematicsexamination-aime. InAmericanInvitationalMathe-
maticsExamination-AIME,2024.
[170] MAA. Americaninvitationalmathematicsexamination-aime. InAmericanInvitationalMathe-
maticsExamination-AIME,2025.
[171] MislavBalunovic´,JasperDekoninck,IvoPetrov,NikolaJovanovic´,andMartinVechev. Math-
arena: Evaluatingllmsonuncontaminatedmathcompetitions. arXivpreprintarXiv:2505.23281,
2025.
[172] JeffreyZhou,TianjianLu,SwaroopMishra,SiddharthaBrahma,SujoyBasu,YiLuan,Denny
Zhou,andLeHou. Instruction-followingevaluationforlargelanguagemodels,2023.
[173] Bill Yuchen Lin, Yuntian Deng, Khyathi Chandu, Faeze Brahman, Abhilasha Ravichander,
ValentinaPyatkin,NouhaDziri,RonanLeBras,andYejinChoi. Wildbench: Benchmarkingllms
withchallengingtasksfromrealusersinthewild,2024.
[174] Cheng-PingHsieh,SimengSun,SamuelKriman,ShantanuAcharya,DimaRekesh,FeiJia,Yang
Zhang,andBorisGinsburg. Ruler: What’stherealcontextsizeofyourlong-contextlanguage
models?,2024.
[175] Howard Yen, Tianyu Gao, Minmin Hou, Ke Ding, Daniel Fleischer, Peter Izsak, Moshe
Wasserblat,andDanqiChen. Helmet: Howtoevaluatelong-contextlanguagemodelseffectively
andthoroughly,2024.
[176] YangZhou,HongyiLiu,ZhuomingChen,YuandongTian,andBeidiChen. Gsm-infinite: How
doyourllmsbehaveoverinfinitelyincreasingcontextlengthandreasoningcomplexity?,2025.
[177] YongqiAn,XuZhao,TaoYu,MingTang,andJinqiaoWang.Systematicoutliersinlargelanguage
models. InTheThirteenthInternationalConferenceonLearningRepresentations,2025.
[178] AlexanderWettig,KyleLo,SewonMin,HannanehHajishirzi,DanqiChen,andLucaSoldaini.
Organizetheweb: Constructingdomainsenhancespre-trainingdatacuration,2025.
[179] Dan Su, Kezhi Kong, Ying Lin, Joseph Jennings, Brandon Norick, Markus Kliegl, Mostofa
Patwary, Mohammad Shoeybi, and BryanCatanzaro. Nemotron-cc: Transforming common
crawlintoarefinedlong-horizonpretrainingdataset,2025.
[180] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. Deepseekmath: Pushing the limits of
mathematicalreasoninginopenlanguagemodels,2024.
[181] FanZhou,ZengzhiWang,NikhilRanjan,ZhoujunCheng,LipingTang,GuoweiHe,Zhengzhong
Liu,andEricP.Xing. Megamath: Pushingthelimitsofopenmathcorpora,2025.

[182] LoubnaBenAllal,AntonLozhkov,ElieBakouch,GabrielMartínBlázquez,GuilhermePenedo,
LewisTunstall,AndrésMarafioti,HynekKydlícˇek,AgustínPiqueresLajarín,VaibhavSrivastav,
Joshua Lochner, Caleb Fahlgren, Xuan-Son Nguyen, Clémentine Fourrier, Ben Burtenshaw,
HugoLarcher,HaojunZhao,CyrilZakka,MathieuMorlon,ColinRaffel,LeandrovonWerra,
andThomasWolf. Smollm2: Whensmolgoesbig–data-centrictrainingofasmalllanguage
model,2025.
[183] ZihanZheng,ZeruiCheng,ZeyuShen,ShangZhou,KaiyuanLiu,HansenHe,DongruixuanLi,
StanleyWei,HangyiHao,JianzhuYao,etal. Livecodebenchpro: Howdoolympiadmedalists
judgellmsincompetitiveprogramming? arXivpreprintarXiv:2506.11928,2025.
[184] Anonymous. Autocode: LLMs as problem setters for competitive programming. In The
FourteenthInternationalConferenceonLearningRepresentations,2026.
[185] Shanghaoran Quan, Jiaxi Yang, Bowen Yu, Bo Zheng, Dayiheng Liu, An Yang, Xuancheng
Ren, Bofei Gao, Yibo Miao, Yunlong Feng, Zekun Wang, Jian Yang, Zeyu Cui, Yang Fan,
YichangZhang,BinyuanHui,andJunyangLin. Codeelo: Benchmarkingcompetition-levelcode
generationofllmswithhuman-comparableeloratings,2025.
[186] OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Floren-
ciaLeoniAleman,DiogoAlmeida,JankoAltenschmidt,SamAltman,ShyamalAnadkat,etal.
Gpt-4technicalreport,2024.
[187] OpenAI. Openaio3-mini,2025.
[188] OpenAI. Introducinggpt-5,2025.
[189] HaolongYan,JiaWang,XinHuang,YeqingShen,ZiyangMeng,ZhiminFan,KaijunTan,Jin
Gao,LieyuShi,MiYang,etal. Step-guitechnicalreport. arXivpreprintarXiv:2512.15431,2025.

## My Notes

- ?????
- ?????
- ?????????
- ???/?????
- ??/???
