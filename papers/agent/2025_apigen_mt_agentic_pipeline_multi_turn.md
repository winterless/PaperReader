---
paper_id: 2025_apigen_mt_agentic_pipeline_multi_turn
topic_tags: [agent, multi_turn, synthetic_data, function_calling, tau_bench, bfcl]
source_url: https://arxiv.org/abs/2504.03601
---

APIGen-MT: Agentic PIpeline for Multi-Turn Data
Generation via Simulated Agent-Human Interplay
AksharaPrabhakar∗ ZuxinLiu∗ MingZhu† JianguoZhang† TulikaAwalgaonkar†
ShiyuWang ZhiweiLiu HaolinChen ThaiHoang JuanCarlosNiebles
ShelbyHeinecke‡‡ WeiranYao‡ HuanWang‡ SilvioSavarese‡ CaimingXiong‡
SalesforceAIResearch
## Abstract
TrainingeffectiveAIagentsformulti-turninteractionsrequireshigh-qualitydata
thatcapturesrealistichuman-agentdynamics,yetsuchdataisscarceandexpensive
tocollectmanually. WeintroduceAPIGen-MT,atwo-phaseframeworkthatgen-
eratesverifiableanddiversemulti-turnagentdata. Inthefirstphase,ouragentic
pipelineproducesdetailedtaskblueprintswithground-truthactions,leveraginga
committeeofLLMreviewersanditerativefeedbackloops. Theseblueprintsare
thentransformedintocompleteinteractiontrajectoriesthroughsimulatedhuman-
agentinterplay. Wetrainafamilyofmodels—thexLAM-2-fc-rserieswithsizes
rangingfrom1Bto70Bparameters. Ourmodelsoutperformfrontiermodelssuch
asGPT-4oandClaude3.5onτ-benchandBFCLbenchmarks,withthesmaller
models surpassing their larger counterparts, particularly in multi-turn settings,
while maintaining superior consistency across multiple trials. Comprehensive
experimentsdemonstratethatourverifiedblueprint-to-detailsapproachyieldshigh-
quality training data, enabling the development of more reliable, efficient, and
capable agents. We open-source 5K synthetic data trajectories and the trained
xLAM-2-fc-rmodelstoadvanceresearchinAIagents.
Model https://huggingface.co/Salesforce/xLAM-2
Dataset https://huggingface.co/Salesforce/APIGen-MT-5k
Website https://apigen-mt.github.io
## 1 Introduction
The growth of Large Language Model (LLM) agents has been accelerating at an unprecedented
rate, driven by advancements in AI capabilities and increasing demand across various industries
[21,1,10,5,30,54,23,7,25]. TheirrolehasevolvedbeyondsimpleconversationalchatbotstoAI
agentscapableofexecutingreal-worldtasks,suchasmanagingfinancialtransactions,scheduling
appointments,andhandlingcustomerservicerequests. Theseapplicationsdemandnotonlylinguistic
fluencybutalsopreciseexecution,reliability,andadherencetodomain-specificpolicies. Realistic
enterpriseusecasesinvolvehavinganassistant(alsoreferredtoasagentinthisdocument)thatis
capableoffluentlyconversingwithhumansofdifferentpersonalities,incrementallyunderstanding
theirintent,extractingthebackgrounddetailsneeded,accuratelyinvokeAPIs,andoperateovera
complexbusinesslogicstructure.
∗Co-firstAuthors
†CoreContributors
‡CorrespondingAuthors
Preprint.Underreview.
luJ
]LC.sc[
4v10630.4052:viXra

BFCL v3 -Retail -Airline
xLAM-2-70b-fc-r 78.2 67.1 45.2
xLAM-2-32b-fc-r 75.8 64.3 45.0
xLAM-2-8b-fc-r 72.8 58.2 35.2
gpt-4o 72.1 62.8 43.0
claude 3.5 (new) 56.5 71.5 48.8
llama 3.1 70b 54.2 50.4 20.6
qwen 2.5 32b 62.8 24.4 25.0
0 25 50 75 100 0 25 50 75 100 0 25 50 75 100
Figure1: ComparativeperformanceoflargerxLAM-2-fc-r models(8B-70B,trainedwithAPIGen-MT data)
againststate-of-the-artbaselinesonfunction-calling(BFCLv3[45])andagentic(τ-bench[49])capabilities.
Despitetheirpotential,buildingrobustandreliableAIagentspresentssignificantchallenges[49].
RecentbenchmarksrevealthatevenadvancedLLMsstrugglewithmulti-turninteractions,particularly
whenrequiredtoperformcomplexfunctioncalls,tracklong-termdependencies,orrequestmissing
information[50,28,46,45,19]. Althoughframeworkdesignandpromptengineeringhaveshown
promise,theunderlyingmodelcapabilitiesremaintheprimarybottleneck,largelyduetotwofunda-
mentalobstacles: (1)thescarcityofhigh-qualityagentinteractiondatainpublicpretrainingcorpora,
and(2)theprohibitivecostandtimerequiredtomanuallycollectandlabelsuchdata,especiallyfor
domain-specificapplicationsrequiringspecializedknowledge.
Severalapproacheshaveattemptedtoaddressthesechallenges. APIGen[26]introducedtechniques
forgeneratingsingle-turnfunctioncallingdata,while[41]exploredmethodsforknowledgedistilla-
tioninagenttraining. However,theseapproachesprimarilyfocusonsingle-turninteractions,failing
tocapturethecomplexityofreal-worldagentusage,wheremultipleturnsareoftenrequired. Other
effortslike[51,50,11],whileincorporatingmulti-turnaspects,lackhuman-agentinterplay–crucial
forrealisticdatageneration. Theverificationandsynthesisofhigh-qualitymulti-turntrajectoriescon-
tainingbothlinguisticdiversityandgroundedactionsremainslargelyunsolved,creatingasignificant
barriertoadvancingagentcapabilities.
Toaddresstheselimitations,weintroduceAPIGen-MT,anagenticdatasynthesispipelineforgenerat-
inghigh-qualitymulti-turnagentdata. Itoperatesintwomainsteps: first,adataagentgeneratesa
detailedandverifiedtask"blueprint",andsecond,thisblueprintguidesthegenerationofrealistic
multi-turninteractionsthroughsimulatedagent-humaninterplay(Subsection4.2). Theblueprint
generation includes sampling relevant APIs, policies, domain data, and user personas to create
groundedgeneraltasksconfigurations,andusingreversetaskrecombination(SubSubsection4.1.3)
toenhancecomplexity. Theseblueprintsarevalidatedthroughformat/executionchecksandanLLM
committeereviewusingareflection-basedmechanism[39]. Subsequently,thevalidatedblueprint
seedsasimulatedinteractionbetweenahumanLMandanagent(e.g.,gpt-4o),producingacomplete
interactiontrajectorywithdialogue,actions,andenvironmentfeedbackfortraining.
Themaincontributionsofourworkaresummarizedasfollows:
• WeproposeAPIGen-MT,anagenticdatasynthesispipelinethatleveragesenvironmentexecution
feedbackandareviewcommitteetoensurethehigh-qualityofgeneratedmulti-turnagentdata.
• We develop a two-phase framework that first creates detailed task blueprints with verifiable
groundtruthactions,thentransformstheseblueprintsintorealisticmulti-turnconversationalagent
trajectorieswithtool-usagethroughsimulatedhuman-agentinterplay.
• Wetrainaseriesofmodelsacrossmultiplearchitecturesandscales(Llama3.1/3.2andQwen
## 2.5 at 1B to 70B parameters), demonstrating superior performance on two popular agentic
benchmarks: τ-benchandBFCL,surpassingmanyfrontiermodelsincludinggpt-4o(Figure1).
• Weopen-source5Khigh-qualitysyntheticdata(APIGen-MT-5k)andtrainedmodels,i.e.,the
xLAM-2-fc-rseries,toadvanceresearchinAIagentspace.

## 2 RelatedWork
Tool-UseAgents. Tool-usecapabilitiesenhanceLLMsbyenablinginteractionwithexternaltools,
extendingtheirreasoningandfunctionality[44,33,24]. Function-callingframeworksallowLLMsto
parsequeries,selecttools,andinterpretresults,butoftenrequirepredefinedtools,limitingadaptability
[26,43]. Effortsweremadetoaddressthisbycreatingreusabletoolsfromscratchonthefly[9],
builtuponbyToolMaker[44]whichleveragestoolsfromexistingcoderepositories. Otherscompose
workflowsorlearnfromdemonstrations[33,36]. Recently,severalworkshaveadoptedspecialized
approachesforagenttraining—critique-informedplanning[13],fine-tuningonselectivesteps[48],
teasingapartreasoningfromformatfollowing(Agent-FLAN)[12],andautonomouslyinvokingtools
withoutexplicitpost-training(ToRL)[22].
InteractiveConversationalBenchmarks. EvaluatingLLMagentsinmulti-turnsettingsrequires
specializedbenchmarks.MultiChallenge[40]andToolDial[38]assessagentsoncontextmaintenance
andtool-augmenteddialogue. InterCode[47]andCRMArena[19]evaluateiterativeproblem-solving
andcustomermanagement. ToolSandbox[28]providesastateful,interactivebenchmarkfortool
use. User simulations have become essential in these benchmarks, offering systematic, realistic
interactions[49,28,31]. Ourworkcomplementstheseeffortsbygeneratingsyntheticmulti-turn
conversationstotrainandevaluateagentsinsuchrealisticsettings.
SyntheticDataGeneration. Thescarcityofhigh-qualitytrainingdatadrivessyntheticdatagenera-
tion. Multi-agentframeworkslikeMAG-V[37],AgentInstruct[29],MATRIX[42],andIntellAgent
[20]createrealisticdatasetsbysimulatingagentinteractions. Otherapproachesutilizeinstruction
composition[18,11],intermediategraphs[6]andmulti-turnplanningtoproducecomplexdialogues
[55]. Relatedtooureffortingeneratingmulti-turntrainingdata,BUTTON[11]generatessynthetic
compositional instruction tuning data by combining 2-3 atomic tasks and conducting trajectory
collectionviaamulti-agentsetup. However,thisinvolvesconstructionofAPIsbasedonthetask
generatedandlackssystematicqualitycontrolandfilteringduringtaskcompositionlimitingdata
verification. MAGNET[50]proposedagraph-basedmethodtogeneratefunctionsignaturepaths
whichareiterativelytransformedtoasequenceofqueriesandfunctioncalls.
Whilemanyofthesepriorapproacheshavebeentestedmainlyonreasoningorsingle-turninteraction
scenarios,ourframework,APIGen-MT,advancesthislineofwork,beingapplicabletoanyexisting
environmentbygeneratinghigh-qualitymulti-turndataforrealisticagent-humaninteractions,focus-
ingonreliabletoolselectionandparametergeneration. Bysystematicallypreparingthecontext,we
firstgeneratetasksadheringtoanydomainconstraintsandthecorrespondingexecutablegroundtruth
functioncallsinanagenticfashionwithiterativerefinementviafeedbackloops.Further,thesimulated
agent-humaninterplaymechanismallowsustogenerateverifiablelonginteractiontrajectories.
## 3 APIGen-MTMethodforSynthesizingHigh-QualityMulti-TurnData
Inthissection,wepresentAPIGen-MT,anagenticpipelineforgeneratingmulti-turndatathrough
simulatedagent-humaninterplay. Wefirstformalizethemulti-turninteractionproblemandthen
describeourtwo-phaseframeworkforgeneratinghigh-quality,verifiablemulti-turndata.
## 3.1 Multi-TurnInteractionProblemFormulation
Multi-turninteractionsbetweenanAIassistantandahumanuserpresentuniquechallengesthatgo
beyondsingle-turnexchanges. WeformalizethisinteractionasaPartiallyObservableMarkovDeci-
sionProcess(POMDP)definedbythetuple(U,S,A,O,T,R),whereU representstheinstruction
spacecontainingpossibleuserintents;S denotesthestatespaceoftheenvironmentandconversation
history;A={tool_call,response}istheactionspaceavailabletotheassistant;O =O ∪O is
E H
theobservationspacecomprisingobservationsfromtheenvironment(O )andresponsefromthe
E
human(O );T :S×A→S×Oisthetransitionfunction;andRistherewardfunctionevaluating
H
interactionsuccess. TheAIassistantmustengageinamulti-turnconversationwiththehumanuserto
incrementallyunderstandtheirintentq ∈ U andsolveitthroughappropriateinteractionswiththe
environmentwhileadheringtoanydomainrules. Atturnt,theassistantpredictsanactionat ∈A
basedontheinteractionhistoryandunderstandingofqthusfar. Whenat isatool_callcompliant
withtherules,ittriggersastatetransition(st ,tool_call)→(st+1,o ),whereo ∈O isthetool
E E E E E
output(typicallyinstructuredformatlikeJSON).Whenatisaresponsetothehuman,itcausesa

Phase 1: Task Configuration and Groundtruth Generation
APIGen-MT
Feedback Generator
Summarized feedback Aggregate Reviews, Reflect & Summarize
and improvement plan
fail
Validated Tasks
Context LLM G e b n a e s r e a d t o D r ata
Task Config Exec F u o t r io m n a C t h & e cker pass
R d e o v e i s e w m a C j o o m rit m y i v t o te te e
pass
Task Intent
{intent, actions, outputs}
APIs Rules Domain Groundtruth
Phase 2: Human-Agent-Environment Interaction Trajectory Collection
Task Intent Agent Interacts in Simulation Groundtruth Actions
Environments with Executable APIs & Outputs
Simulated Test Environment Config
Can you return Sure, but I would
Human my order? need your email to Agent Compare
authenticate you get_user_info(...)
and order info.
User information ...
Interaction Traces
My email is xxx
and the order is I have found your get_order_info(...)
about xxx.... info in our database, pass
your order id is xxx,
would like to Order information ...
proceed?
respond_to_user(I have found ....)
More inter.a.c.tion turns Successful Trajectory
Figure 2: OverviewoftheAPIGen-MTframework. Phase1generatestaskconfigurationsandgroundtruth
actionsthroughanagenticprocesswithfeedbackloops.Phase2collectshuman-agent-environmentinteraction
trajectories by simulating realistic conversations between a human user and a test agent in an executable
environment.
statetransition(st ,response)→(st+1,o ),whereo ∈O isthehuman’sfollow-upmessage.
H H H H H
Importantly, the environment state st+1 remains latent to both the assistant and the human. The
E
interaction completes when the human sends a terminating message or the maximum number of
turnsisreached. TherewardR(∆S ,a)iscalculatedbasedonthecumulativestatechangeinthe
E
environment∆S andthesequenceofresponsesa={a |a ∈responsetohuman}providedby
E i i
theassistantthroughouttheepisode. Theassistant’sobjectiveistomaximizethisreward.
## 3.2 APIGen-MTFrameworkOverview
Generatinghigh-qualitymulti-turndatathatcapturesthecomplexitiesofagent-humaninteractions
presentssignificantchallenges. Directlysynthesizingmulti-turnconversationsinoneshotisdifficult
fortwokeyreasons: (1)asingleerrororhallucinationinanyintermediatestepcanleadtocomplete
failure,and(2)thecontentofeachturndependsonpreviousfunctioncallsandtheiroutputs,creating
complexdependenciesthataredifficulttomaintainconsistently.
To address these challenges, we introduce APIGen-MT, a two-phase framework for generating
verifiable and diverse multi-turn data (Figure 2). Our approach extends the APIGen framework
[26]byaddinganagenticfeedbackloopandsimulatedhuman-agentinterplaytogeneraterealistic
multi-turnconversations.
Thecoreinsightofourapproachistoseparatethetaskgenerationprocessintotwodistinctphases:
firstcreatingadetailed"blueprint"ofthetask(Phase1),andthenusingthisblueprinttoguidethe
generationofrealisticmulti-turninteractionsthatfillintheconversationaldetails(Phase2). This
separationallowsustoensureboththecorrectnessoftheunderlyingtaskstructureandthenaturalness
oftheresultingconversations.
## 3.2.1 Phase1: TaskConfigurationandGroundtruthGeneration
TheinitialphaseofAPIGen-MT focusesonsystematicallygeneratingwell-definedtaskconfigurations,
eachcomprisingauserinstruction(q),acorrespondingsequenceofverifiablegroundtruthactions
(a ),andtheexpectedfinaloutputs(o ). Thisphaseestablishesasolid,verifiablefoundationfor
gt gt

eachinteractionscenariobeforethecomplexitiesofconversationaldynamicsareintroduced. As
depictedinFigure2,thisisachievedthroughanagenticworkflowincorporatingmulti-stagevalidation
andrefinementloops. Morespecifically,ithasthefollowingsteps:
## 1. ContextPreparation: RelevantinformationsuchasavailableAPIs,domain-specificrulesor
policies,andreferencedataisassembled. Thiscontextgroundsthesubsequentgenerationstepin
thespecificconstraintsandcapabilitiesofthetargetenvironment.
## 2. LLM-based Data Generator: An LLM utilizes the prepared context to propose initial task
configurations. Eachconfigurationconsistsof:
• Adetaileduserinstructionqdescribingthehigh-levelintent.
• Asequenceofgroundtruthactionsa requiredtofulfilltheintent.
gt
• Expectedfinaloutputso tobeprovidedtotheuser.
gt
## 3. Format&ExecutionChecker: Proposedconfigurationsundergoautomatedtechnicalvalidation.
Thiscomponentperformsmultiplechecks:
• Verifiesthestructuralcorrectnessofgeneratedactions(e.g.,validAPIcallformats)andoutputs.
• Confirms the executability of each action in a within a simulated target environment E
gt
(checkingAPInames,arguments,types).
## 4. ReviewCommittee: Configurationspassingrule-basedchecksproceedtosemanticevaluation
byacommitteeofmultipleLLMreviewers. Thiscommitteeassessesqualityaspectslikethe
coherencebetweenqanda ,completeness,andoveralltasksensibility. Weusemajorityvoting
gt
toachieveamorestableassessment.
## 5. FeedbackGenerationandRefinement: Ifataskfailsateitherthevalidation(Step3)orreview
(Step4)stage,aFeedbackGeneratoraggregatesfailurereasonsandreviews,reflectsuponthem,
andproducesasummarizedimprovementplan. ThisplanguidestheDataGenerator(Step2)in
refiningthetaskproposalinasubsequentiteration. Successfullyvalidatedtasksexitthisloop.
Thisagenticdesignwithfeedbackloopsiscrucialforgeneratinghigh-qualitytasksefficiently. By
incorporating reflection and improvement based on validation results, the system can learn from
failuresandprogressivelygeneratebettertasks.
## 3.2.2 Phase2: Human-Agent-EnvironmentInteractionTrajectoryCollection
Buildinguponthevalidatedtaskconfigurationsq,a ,o fromPhase1,thesecondphasegenerates
gt gt
realisticmulti-turninteractiondatabysimulatingdynamicconversationsbetweenanLLM-based
human user and a test agent operating within an executable environment. Guided by the task
instructionqandoftenaspecificpersona,thesimulatedhumannaturallyrevealsinformationorsub-
goalsincrementally,whiletheagentinterpretstheevolvingcontext,interactswiththeenvironment
viaAPIcallswhenneeded,andrespondscoherently. Importantly,thesimulateduserisunawareof
theunderlyingenvironmentandavailableAPIsmimickingareal-worlduser.
Thesimulationproducescompleteinteractiontrajectoriesthatcapturedialogueturns,agentactions,
and environment responses. Each trajectory is validated by comparing its outcome against the
groundtruth actions (a ) and expected outputs (o ) from Phase 1. Only those trajectories that
gt gt
verifiably achieve the task using both state-based and output-based checks are accepted into the
dataset,ensuringthatinteractionsarebothdynamicallyplausibleandgroundedinacorrectsolution.
Thistwo-phasedesignoffersseveralbenefits. First,itprovidesverifiabilitybygroundinginteraction
datainpre-validatedtaskconfigurations. Second,itenhancesrealismbyfocusingthesimulation
on natural turn-by-turn dynamics without the simultaneous burden of task solution generation.
Lastly,themodularapproachisolatesissuesintaskdesignfromthoseinconversationalmodeling,
facilitatingdebuggingandscalabilityacrossdiverseinteractionpatterns. Inessence,byintegrating
agenticgenerationofverifiabletask"blueprint"withrealisticsimulationofconversationaldynamics,
APIGen-MTproduceshigh-quality,multi-turninteractiondatathatbalancesstructuralcorrectness
withthenaturalnessrequiredfortrainingagentmodels.
## 4 ACaseStudyofAPIGen-MTonτ-bench
ThissectiondetailstheinstantiationoftheAPIGen-MTframework(Subsection3.2)withτ-bench
[49]. Generating high-quality, multi-turn interaction data with nuanced human-agent dynamics

Reflect &
sample sample Score
sample sample
Examples
add
Task Generation Task Validation Simulated Agent-Human
Interplay
API
## 1. Action Validation 2. Alignment Validation
Policies graph E Fo xe rm cu a t t i o C n h e C c h k
eck
{Task Data, Intent, Diff Patch} r P e i r n v o t e m e a n p l t u t s i t n e o r Hu L m M an
A T g e e s n t
t
Policy Check turns
Examples
Persona T P e r m o p m la p t t
e & D m o d e m a t t a a a
d in a ta
@
--++
@ - 6 0 6 3 1 ,{
D
"""""" npipip i
+
artrtr f
moeiei f
edmcmc
"u_e_e
:ci"i" P
td:d:
,
"_" " a
Si:3:3
md 2 1 t a""8"5 c
@
r:1.2.
@
t 7686 h "0761 W66,
0, a96 9 t42 5 c52 6 h25 9 "31 0 ,
20 7 0" " 5,
,
2",
F A in gg a r l e R ga e t v e i ew av th g r _ e s s c h o o r l e d V >
alidated Task S O t u a t t p E e u n b t v a b s a e s d e r d e w re a w rd
ard
Regenerate task Reflections
Task = {Intent,Actions,Outputs} using feedback & Summarize Successful Trajectory
Figure 3: RealizationofAPIGen-MTframeworkforτ-bench. Wefirstgeneraterealistictaskinstancesby
randomwalkdowntheAPIgraphandsampling.Nextthetasksarevalidatedfollowingamulti-stagepipeline.
InstanceswhichfailaresentbacktotheGeneratortoberefinedbasedonthevalidationfeedback. Finally,
trajectoriesaregeneratedbyasimulatedhumanuserthatinteractswithatestagentbysupplyingthequery
detailsinaturn-wisemanner.Trajectorieswhichpassstate-andoutput-basedevaluationsarecollected.
presentschallenges,asdirectconversationsimulationoftenleadstoinconsistenciesortaskdeviations.
Therefore,ourtwo-phaseapproachaddressesthisbyfirstsynthesizingdetailtaskconfigurationsthat
definetheuser’shigh-levelintent(q),groundtruthactions(a ),andtheexpectedfinaloutputs(o ).
gt gt
Byestablishingthisverifiable"blueprint"first(Phase1), wecanthenmorereliablysimulatethe
fine-grained,turn-by-turninteractiondynamicsbetweenahumanandanagentwithintheexecutable
environment (Phase 2), ensuring the collected trajectories are both realistic and grounded in a
verifiablesolutionpath. τ-bench,withitsrealisticdomains,executableAPIs,andspecificpolicies,
providesanidealtestbedforthismethodology. Figure3illustratesthisspecificimplementation.
## 4.1 Phase1Implementation: TaskConfigurationGenerationandValidation
## 4.1.1 APIDependencyGraphandContextSamplers
Generatingrealistictasksforτ-benchrequiresnavigatingitsspecificAPIs,policies,anddatastruc-
tures. Weimplementedthefollowingtechniquesfortaskgenerationandvalidation.
APIGraphModeling. WemodeltheavailableAPIsineachτ-benchdomainasadirectedgraph,
wherenodesrepresentAPIsandedgesrepresentdependenciesbetweenthem. Anedgeexistsfrom
API A to API B if B’s input arguments can depend on A’s output and the co-occurrence of this
tool-callpairispermittedunderdomainpolicies. Thisgraph-basedapproachenablesustogenerate
realistictasksequencesbyperformingrandomwalksthroughtheAPIdependencygraph.
SpecializedContextSamplers. Toensuretaskdiversity,realism,andgrounding,weutilizeseveral
domain-specificsamplersthatprovidecontexttotheLLM-basedtaskgenerator.
• APISampler: Wedistinguishbetweenstate-exploring(‘read’)APIsandstate-changing(‘write’)
APIswhichcanmodifytheenvironmentstates. Thegeneratorfocusesonsamplingthenecessary
’write’APIstoformthecoreofa ,allowingflexibilityinhow‘read’APIsmightbeusedduring
gt
the subsequent interaction phase. This approach encourages exploration while ensuring that
specificstate-changingactionsareincludedinthegroundtruth.
• PolicySampler: Foreachτ-benchdomain, weextractandsamplefromthedomain-specific
policiesandrules. Thesepoliciesareincorporatedintothetaskgenerationprocesstoensure
complianceofreal-worldusecases. Taskcomplexityisinfluencedbythenumberof’write’calls
andtheassociatedpolicyconstraints.
• Domain Data Sampler: To ground tasks in realistic domain data without exceeding context
limits,wesampledomain-specificdatawithadditionalmetadata(e.g.,cost,time,attributes). This
metadataenhancescoverageandenablesmorecreativeanddiversetaskscenarios.
• PersonaSampler: WeincorporateuserpersonadescriptionsfromPersonaHub[17]toinformthe
userintentqandinjectrealistichumanqualitiesandsituationalcontext,enhancingdiversityfor
subsequentPhase2human-agentinteractionsimulation.
• ExampleSampler: Weprovidefew-shotexamplesofwell-formedtasksrelevanttothesampled
APIs,guidingthegeneratoronstructureandformat.

Foreachtaskgenerationiteration,werandomlyvarythesamplingfrequencyforeachsamplerto
enhance diversity and prevent repetitive scenarios. The sampled information is compiled into
a prompt instructing the LLM generator to produce a <thought> (its reasoning process), the
user <instruction> (q), the corresponding groundtruth <actions> (a ), and the expected fi-
gt
nal<outputs>(o ).
gt
## 4.1.2 Multi-StageValidationforτ-bench
Weimplementarigorousthree-stagevalidationprocessfortheτ-benchenvironment:
Stage1: ActionValidation.
• Format Check: Verifies the presence and basic structure of required task components
(<thought>, <instruction>, <actions>, <outputs>) and ensures all tool calls in
<actions>arevalidJSONandoutputsin<outputs>arestrings.
• ExecutionCheck: Simulateseachactionina withintheτ-benchenvironment,validatingAPI
gt
names,argumentnames,anddatatypes. Thecumulativeeffectontheenvironmentstate(∆S )
E
iscapturedasadiff_patch,similartogit diff.
• PolicyComplianceCheck: Leveragestheexecutablenatureofτ-benchbytranslatingdomain
policiesintoPythonunittests. Thesetestsrunagainstthesimulatedexecutiontraceofa to
gt
detectviolations,especiallythosearisingfrominteractionsbetweenmultipleactions(e.g.,action
BisinvalidgiventhestatechangecausedbyprioractionA).Failuresyielddetailedfeedbackon
thespecificpolicyviolation.
Stage2: AlignmentValidation. TaskssuccessfullypassingStage1’sactionvalidationarethen
assessedforsemanticalignment. Specifically,weevaluatewhetherthegroundtruthactions(a ),as
gt
reflectedbytheirenvironmentaleffectssummarizedinthediff_patch,accuratelyandcomprehen-
sivelyfulfilltheuser’sintentexpressedintheinstruction(q). Tomitigatethepotentialbiasesand
inconsistenciesofasingleevaluator,weemployacommitteeofdiverseLLMjudges[54,8]. These
judgesrevieweachtaskbasedonasystematicrubricwithmetricssuchasCorrectness,Completeness,
Satisfaction,andCreativity(referFigure9inAppendixBfordetails).
Eachjudgeprovidesscoresandqualitativefeedback. Weutilizeamajorityvotingstrategyacross
thecommittee’sjudgmentstodeterminethefinalassessmentforeachmetricandtheoveralltask
quality. Thisapproachyieldsmorestableandreliableevaluationresultscomparedtosingle-judge
assessments.
Stage 3: Final Semantic Review & Refinement. Based on the aggregated scores from the
committee(determinedviamajorityvoting),tasksachievinganaveragescoreaboveapredefined
thresholdareacceptedandaddedtothepoolofvalidatedtaskconfigurations. Tasksthatfailthis
reviewtriggerthefeedbackloopmechanism. Consolidatedfeedback,summarizingthepointsraised
bythecommitteemajority,issentbacktotheLLMtaskgenerator. Thisinitiatesareflectionprocess
[39], guiding the generator to revise the task in the subsequent iteration to address the identified
shortcomings.
## 4.1.3 ReverseTaskRecombinationforComplexTaskConstruction
While the iterative refinement process improves task quality and efficiency, directly generating
complex,long-horizontasksinvolvingmultiplestepsremainschallenging. Validationfailurescan
occurduetosubtlepolicyconflictsordifficultiesinensuringperfectalignmentacrossmanysteps.
Toovercomethisandsystematicallyconstructmorecomplicatedscenarios,weimplementReverse
TaskRecombination,atechniquethatleveragestheprincipleofcompositionality[11,18],similar
tomodulardesigninsoftwareengineering. Thecoreideaistobuildcomplextasksfromsimpler,
independentlyvalidated"buildingblocks":
## 1. SelectValidatedTasks: Identifymultiplesimplertasks(T ,T ,...)thathavesuccessfullypassed
1 2
allvalidationstages(Stages1-3)andareassociatedwiththesameuserpersona.
## 2. ConcatenateComponents: Combinetheirrespectivegroundtruthactions(a =a ◦
combined gt,1
a ◦...)andexpectedoutputs(o =o ⊕o ⊕...,where◦denotesactionsequence
gt,2 combined gt,1 gt,2
concatenationand⊕denotesoutputaggregation).

## 3. Re-CheckPolicyCompliance: RerunthePolicyCheckona toensurethatthecumula-
combined
tiveactionsequenceremainslogicallysoundandadherestothedomainrulesascombinations
could cause conflicting actions to appear together, for e.g., returning and canceling the same
order.
## 4. Synthesize Combined Instruction: Instruct the LLM generator to create a new, coherent,
overarchinguserinstruction(q )thatlogicallyintegratesthegoalsandstepsrepresented
combined
bya ando . Thisnewinstructionshouldframethecombinedactionsasasingle,
combined combined
morecomplexuserrequest.
## 5. Re-Validate Semantics: Submit the newly formed complex task T =
combined
{q ,a ,o }forvalidationstartingfromStage2(AlignmentValidation).
combined combined combined
Stage1(ActionValidation)canbesafelyskippedfora becauseeachconstituentaction
combined
sequence(a ,a ,...)hasalreadybeenindividuallycheckedforformatandexecutionwithin
gt,1 gt,2
itsoriginalcontext,andpolicycomplianceinthecurrentcontext.Stage3(FinalSemanticReview)
proceedsbasedontheoutcomeofStage2forthecombinedtask.
Thismethodallowsforthescalablegenerationofcomplex,multi-steptaskswithgreaterreliability,
asitbuildsuponverifiedcomponentswhilefocusingthevalidationeffortonthesemanticcoherence
andalignmentofthecombinedwhole.
## 4.2 Phase2: SimulatedHuman-AgentInterplayandTrajectoryCollection
BuildingontheverifiedtasksfromPhase1—whichincludeadetaileduserintentq, groundtruth
actionsa ,andexpectedoutputso —wesimulatemulti-turninteractiontrajectoriesbetweenan
gt gt
agent(A)andahumanuser(H)modeledbyanLLM.Guidedbytheinstructionqandanassociated
persona,thesimulatedhumanincrementallyrevealstaskdetailstomimicrealisticinteractions. The
agent, instantiated as gpt-4o with its function-calling mode, interprets the evolving intent and
executesthenecessaryactionstocompletethetask.
TrajectoryCollection. Weemployrejectionsamplingtoensurethatonlytrajectoriesachievingthe
taskgoal(r =1)areretained. Successisdeterminedbycomparingthefinalenvironmentstatetoa
gt
andtheagent’sfinalresponsestoo . Forenhanceddatacoverage,eachtaskisattempteduptothree
gt
times,andtheunionofalluniquesuccessfultrajectoriesiscompiledintoanofflinedatasetsuitable
fordownstreamapplicationssuchasbehavioralcloning.
StabilizingSimulatedHuman. Acriticalchallengeinthisphaseismaintainingthestabilityand
fidelityofthesimulatedhuman. Overmultipleconversationalturns,thehumanLLMmaydriftfrom
theoriginalinstructionorbeundulyinfluencedbytheagent’sresponses[32],introducingvariability
thathindersreliableevaluation[49]. Toaddressthis,weadoptaBest-of-N(N=4)samplingstrategy
incombinationwithaself-critiquemechanismforthehumanLLM’sresponses(seeFigure12in
Appendix B for details), allowing it to adhere to the task instruction more accurately and not be
misleadbythetestagentresponses. Itseffectivenesswasvalidatedontheτ-benchtestset,where
improvedconsistencyinagentperformanceevaluationacrossmultipletrialswasobserved(Table3).
## 4.3 DataCollection&Statistics
Data Collection Procedure. We source APIs implemented as Python functions from τ-bench.
Amongthese,wehave15‘read’and13‘write’APIsacrossbothdomains. τ-benchisaccompanied
withdetailedpoliciesanddomainrulesintwosettings-RetailandAirlinewhichweuseasguideline
policies. Weutilizegpt-4oandDeepSeekV3modelsinthetaskgeneration,validationandagent-
humaninterplaystagestocollecttrainingdata. Thepromptsusedineverystageareprovidedin
AppendixB. Wesetthemaximumnumberofreflection-basedfeedbackturnsto3forretailand5for
airlinerespectively.
Statistics. AsummaryofthedatacollectionisshowninFigure4. Figure5showsthatwecan
efficientlycollectlongtrajectoriesrequiringastrongmodellikegpt-4ototakeanaverage12turns
tocompletethetaskusingAPIGen-MT.Ouragenticpipelineinvolvingreviewcommitteeanditerative
refinementviareflectionprovidesa2.5xboosttothetaskcollectionsuccessratetoattain70%.
OurimplementationdemonstratesthattheAPIGen-MTframeworkcansuccessfullygeneratehigh-
qualitymulti-turndataforcomplexdomainswithstrictpolicyconstraints. Thetwo-phaseapproach

Metric Value
0.20
TaskConfig.S.R.(Phase1) 70%
TaskConfig.S.R.w/oAgenticFeedback 28%
0.15
TrajectorySim.S.R.(Phase2) 67%
Min.TurnsperTrajectory 1 0.10
Max.TurnsperTrajectory 29
Avg.ToolCallsperTrajectory 7 0.05
Avg.UserTurnsperTrajectory 6
0.00
Figure4: Statisticsforthedatasetgeneratedusing 0 10 20 30
Number of Turns
APIGen-MT.Successrates(S.R.)arereportedforthe
taskconfiguration(w. andw/oagenticfeedbackin
Phase1)andtrajectorysimulation(Phase2)stages.
ytisneD
Assistant Turns
User Turns
Figure5: Densitydistributionofassistantand
userturnsincollectedtrajectories.
withagenticfeedbackloopsandsimulatedhuman-agentinterplayproveseffectiveincreatingdiverse,
realistic,andverifiabledatasetsfortrainingandevaluatingconversationalagents.
## 5 Experiments
## 5.1 ExperimentalSetup
TrainingDetails. WeperformfilteredBehavioralCloning(BC)usingthecollectedtrajectorieswith
Llama3.1/3.2Instructmodels[16]andQwen2.5Instructmodels[34]. Thecollectedtrajectories
are split at every assistant response and we train to predict only the assistant response tokens by
maskingthepromptandothermessages. Toenhancethedatasetdiversity,wealsojointlytrainour
xLAM-2-fc-rmodelswithfunction-callingdatafrom[26]andotherdomainsofagenticdatafrom
[52,53]. WeutilizetheLLama-Factorylibrary[56]andperformfull-finetuningusingDeepSpeed
ZeRO[35]stage3,FlashAttention2[15]inbfloat16precisionwithAdamWoptimizer[27]andtrain
foratmost3epochsonaNVIDIAH200node.
Benchmarks. Weevaluateontwochallengingbenchmarksdesignedspecificallyforassessingagent
capabilities–(1)BFCLv3[45],aleadingbenchmarkfortool-useevaluation,specificallydesigned
toassessLLMs’functioncallingcapabilitiesand(2)τ-bench[49],acomprehensivebenchmarkfor
evaluatingAIagentsinrealisticscenarios. MoredetailsareinAppendixA. Bothareparticularly
well-suitedforevaluatingtheeffectivenessofourAPIGen-MTapproach,astheyfocusonmulti-turn
interactionsandtoolusecapabilities,whicharecentraltoourdatagenerationmethodology.
## 5.2 ExperimentResults
We compare the performance of our trained models (xLAM-2-fc-r) against state-of-the-art
proprietary models such as gpt models (o1, gpt-4o); claude models (claude-3.5-haiku,
claude-3.5-sonnet,claude-3.5-sonnet (new),andclaude-3.7-sonnet),andopen-source
LLMsincludingDeepSeekv3,andthebaselinesLlama70BandQwen32B.
BFCLv3Results. OntheBFCLv3benchmark,ourmodelsdemonstrateexceptionalperformance.
AsshowninTable1,xLAM-2-70b-fc-randxLAM-2-32b-fc-rachievethetop2positionsonthe
leaderboardwithoverallaccuraciesof78.19%and75.83%respectively,surpassingallproprietary
and open-source models. The most striking advantage appears in multi-turn scenarios, where
our models excel across all parameter scales. xLAM-2-70b-fc-r achieves 75.12% multi-turn
accuracy, while our smaller models show remarkable capabilities with xLAM-2-8b-fc-r at
69.25%, xLAM-2-3b-fc-r at 56.00%, and even xLAM-2-1b-fc-r at 43.12% - all substantially
outperforming o1 (36%) and gpt-4o in function-calling mode (41%). Additionally, our models
demonstratestronghallucinationdetection,withxLAM-2-3b-fc-rachieving94.44%onrelevance
detection,matchingthebestscoreinthiscategory.

Table1:PerformanceofdifferentmodelsonBFCLleaderboard(asofdate04/03/2025).Therankisbasedonthe
overallaccuracy,whichisaweightedaverageofdifferentevaluationcategories.“FC"standsforfunction-calling
modeincontrasttousingacustomized“prompt"toextractthefunctioncalls.Seethebenchmark[45]fordetails.
Single-Turn Multi-Turn Hallucination
Rank OverallAcc Model
Non-live(AST) Non-live(Exec) Live(AST) OverallAcc Relevance Irrelevance
1 78.19 xLAM-2-70b-fc-r(FC) 88.48 85.98 72.63 75.12 66.67 78.74
2 75.83 xLAM-2-32b-fc-r(FC) 89.50 86.48 73.79 66.38 83.33 76.25
3 74.31 watt-tool-70b(FC) 84.06 89.39 77.74 58.75 94.44 76.32
4 72.83 xLAM-2-8b-fc-r(FC) 84.35 85.59 66.73 69.25 83.33 64.11
5 72.08 GPT-4o-2024-11-20(Prompt) 88.1 89.38 79.83 47.62 83.33 83.76
6 69.94 GPT-4.5-Preview-02-27(FC) 86.12 83.98 79.34 45.25 66.67 83.64
7 69.58 GPT-4o-2024-11-20(FC) 87.42 89.2 79.65 41 83.33 83.15
8 68.39 ToolACE-2-8B(FC) 87.58 87.11 80.05 36.88 72.22 90.11
9 67.98 watt-tool-8B(FC) 86.56 89.34 76.5 39.12 83.33 83.15
10 67.88 GPT-4-2024-04-09(FC) 84.73 85.21 80.5 38.12 72.22 83.81
11 67.87 o1-2024-12-17(Prompt) 85.67 87.45 80.63 36 72.22 87.78
12 67.72 BitAgent-8B 86.92 89.52 76.14 38.5 83.33 82.38
13 65.12 o3-mini-25-01-31(Prompt) 86.15 89.46 79.08 28.75 72.22 82.96
14 65.11 xLAM-2-3b-fc-r(FC) 82.94 81.88 58.69 56.00 94.44 57.94
15 64.1 CoALM-405B 90.58 89.07 74.5 28.75 100 71.79
16 64.1 GPT-4o-mini-24-07-18(FC) 85.21 83.57 74.41 34.12 83.33 74.75
... ... ... ...
34 58.93 Gemini-2-Flash-Thinking 87.4 87.07 75.97 14.5 77.78 72.75
35 58.9 Qwen2.5-14B-Instruct(FC) 85.42 84.86 76.68 15.88 55.56 77.69
36 58.90 xLAM-2-1b-fc-r(FC) 76.23 74.86 59.88 43.12 88.89 56.87
37 58.55 DeepSeek-V3(FC) 89.17 92.32 68.41 18.62 88.89 59.36
38 58.45 mistral-large-2407(FC) 86.81 84.38 69.88 23.75 72.22 52.85
39 58.42 ToolACE-8B(FC) 87.54 89.21 78.59 7.75 83.33 87.88
τ-benchResults. Table2presentsresultsunderthedefaultnaiveusersettingonτ-bench. Our
xLAM-2-70b-fc-r model achieves a 56.2% success rate, outperforming Llama 3.1 70B Instruct
(38.2%), DeepSeek v3 (40.6%), and even proprietary models like GPT-4o (52.9%), while ap-
proaching more recent models like Claude 3.5 Sonnet (60.1%). Notably, our smaller variants
likexLAM-2-32b-fc-r(54.6%)andxLAM-2-8b-fc-r(46.7%)surpasslargerbaselines,demon-
stratingthatoursyntheticdataapproachenablesefficientknowledgetransferandstrongperformance
withfewerparameters.
Table 2: SuccessRate(pass@1)ofvariousopen-sourceandproprietarymodelsontheRetailandAirline
settings of τ-bench (averaged across at least 5 trials). The xLAM-2-fc-r models are trained on the data
generatedusingAPIGen-MT.Overallindicatestheaveragescoreacrossbothdomains.1indicatesresultsfrom
[14];2indicatesresultsfrom[2];3indicateresultsfrom[3];4indicatesfrom[4].Note.Weevaluateonlywith
thebenchmark’sthinktoolandnopromptoptimizations.
Model τ-Retail τ-Airline Overall
Open-SourceModels
Qwen2.532BInstruct 24.4 25.0 24.7
Llama3.170BInstruct 50.4 26.0 38.2
DeepSeekv31 58.3 22.8 40.6
xLAM-2-70b-fc-r 67.1 45.2 56.2
xLAM-2-32b-fc-r 64.3 45.0 54.6
xLAM-2-8b-fc-r 58.2 35.2 46.7
xLAM-2-3b-fc-r 44.4 32.0 38.2
xLAM-2-1b-fc-r 22.5 21.0 21.8
ProprietaryModels
Gemini1.5pro1 54.9 25.2 40.1
gpt-4o-2024-11-20 62.8 43.0 52.9
o13 73.5 54.2 63.9
Claude3.5Haiku2 51.0 22.8 36.9
Calude3.5Sonnet2 62.6 36.0 49.3
Claude3.5Sonnet(new)3 71.5 48.8 60.1
Claude3.7Sonnet4 78.3 41.2 59.8
Claude3.7Sonnet+optimizedprompt4 81.2 58.4 69.8

These results across both benchmarks demonstrate that our APIGen-MT approach for generating
syntheticmulti-turndatathroughsimulatedagent-humaninterplayishighlyeffective. Modelstrained
onthisdataconsistentlyoutperformopen-sourcebaselinesandonparwithproprietarymodels,with
particularlystrongperformanceinmulti-turnscenarios. Importantly,ourapproachenablessmaller
modelstoachievecompetitiveorsuperiorperformancecomparedtomuchlargermodels,highlighting
theefficiencyandeffectivenessofourdatagenerationmethodology.
## 5.3 Consistency&StabilityExperiments
Weplotthepassˆkcurves[49]inFigure6onτ-benchinthedefaultnaiveuserLMsetting. passˆk
isdefinedasthechanceofallk i.i.d. tasktrialsbeingsuccessful,averagedacrossalltasks. Ask
increases,weseelessdropinsuccessrate(SR)forourmodels. Notablyonthemorecomplexairline
domain,xLAM-2-70b-fc-rhashigherpassˆ5scorethanClaude,despitehavingaslightlylower
passˆ1suggestinghigherreliabilityandconsistencyacrossmultipletrials. Thisisacriticalproperty
fordeploymentinreal-worldapplications,whereconsistentperformanceisessential.
0.70
0.60
0.50
0.40
1 2 3 4 5
k
k^ssap
0.50
0.40
0.30
0.20
1 2 3 4 5
k
k^ssap
gpt-4o xlam-2-70b-fc-r xlam-2-32b-fc-r claude 3.5 sonnet (new)
Figure6:Passˆkcurvesmeasuringtheprobabilitythatall5independenttrialssucceedforagiventask,averaged
acrossalltasksforτ-retail(left)andτ-airline(right)domains.Highervalueindicatesconsistencyofthemodels.
Next,weadopttheBoNuserLMsetting(introducedinSubsection4.2)toassessitseffectivenessin
producingmorestableresultsacrosstrials. AlthoughthisenhancementisappliedtotheuserLM,
Table3highlightstheimprovedsuccessrateandreducedvarianceinmodelsutilizingtheBoNuser
simulation. Thissuggeststhatenhancingtheusersimulationstrategywithasimpleself-critiquing
mechanismcannotonlyincreasestabilitybutalsoimproveagentperformance.
Table3: TheSuccessRate(SR)measuredacross5trialsontheRetaildomainofτ-benchusinggpt-4oand
xLAM-2-70b-fc-r asthetestassistants. TheaveragesuccessrateishigherwithlowervarianceusingBoN
basedusersimulation,indicativeofamorestableevaluation.
Model(UserLMsetting) t1 t2 t3 t4 t5 SRAverage SRVariance
gpt-4o(Naive) 61.7 57.4 65.2 65.2 64.4 62.8 11.1
gpt-4o(BoN) 65.2 69.6 67.0 66.1 67.0 67.0 2.6
xLAM-2-70b-fc-r(Naive) 69.6 65.2 62.6 68.7 69.6 67.1 9.7
xLAM-2-70b-fc-r(BoN) 66.9 71.3 68.7 66.9 70.4 68.8 4.0
## 5.4 In-DepthAnalysisofModelBehavior
15 10
short medium long
<13 13-18 >18 Task Category
% sseccuS
ksaT
User Turns 14 Success
snoitcaretnI
resU
fo
rebmuN
xlam-2-70b-fc-r claude 3.5 sonnet (new) gpt-4o
Tobetterunderstandthebehaviorofourtrainedmod-
els,weperformanin-depthinvestigationofthetasks
solvedbyxLAM-2-70b-fc-randastate-of-the-art
modelClaude3.5Sonnet(new)onτ-bench. Wecat-
egorizetasksinto‘short’,‘medium’and‘long’based
on the number of turns required by Claude 3.5 to
solveeachtaskacrossaunionof8trials. Thiscat-
egorization is derived by calculating the 33rd and
66thpercentilesofthenumberofturns. FromFig-
Figure 7: Performance/efficiency comparisons
ure7weobservethatparticularlyonthe‘long’task
ofxLAM-2-70b-fc-rwithfrontiermodelsonτ-
category,thesuccessrateforxLAM-2-70b-fc-ris bench.

muchhigherthangpt-4obutlagsbehindClaude. Further,weassesstheefficiencyoftheagentby
measuringthenumberofinteractionsneededwiththesimulateduserfortheagenttofullycompre-
hendtheintentandsuccessfullycompletethetask. TheplotrevealsthatxLAM-2-70b-fc-risat
parwithgpt-4obutrequiresmoreinteractionscomparedtoClaude,whichcanbeattributedtoits
methodofretrievinguserdetailsinstages, necessitatingmoreturns. Theseobservationssuggest
potentialareasforimprovementinfutureiterations.
## 6 Discussion
Conclusion. WeintroducedAPIGen-MT,atwo-phaseframeworkforgeneratinghigh-qualitymulti-
turnagentdatathroughsimulatedhuman-agentinteractions. Bydecouplingthecreationofdetailed
taskblueprintsfromthesimulationofconversationaltrajectories,ourapproachensuresbothstructural
correctness and natural dialogue dynamics. Experiments on τ-bench and BFCL v3 demonstrate
thatmodelstrainedonoursyntheticdataoutperformexistingbaselines,withevensmallermodels
showingcompetitiveperformanceinmulti-turnscenarios. Moreover,ourstabilizationtechniques
yieldmoreconsistentandreliableagentbehavior. Byopen-sourcingoursyntheticdataandtrained
models,weaimtofosterfurtheradvancesinAIagentdevelopment.
Limitationsandfuturedirections. Despiteitsadvantages,APIGen-MThaslimitationsthatpresent
opportunitiesforfutureresearch. First,whileourBest-of-Nsamplingandself-critiquemechanisms
reducehumanusersimulationvariance,somestochasticityinhumanbehaviorremains;moredeter-
ministicsimulationmethodsorrefinedfilteringmetricscouldfurtherstabilizetheprocess. Second,
our current approach discards failed trajectories in the second phase, yet these cases may offer
valuableinsights;futureworkcouldleveragesuchfailuresasadditionalcontrastivesignalduring
modeltraining. Third,themulti-stagevalidationprocess,thougheffective,incurscomputationalover-
head;developingmoreefficientvalidationoradaptivesamplingstrategiescouldimprovescalability.
Finally,extendingourapproachtoadditionaldomainsandincorporatingself-improvementthrough
reinforcementlearningarepromisingdirectionsforfuturework.
## References
[1] S.Agashe,J.Han,S.Gan,J.Yang,A.Li,andX.E.Wang. Agents:Anopenagenticframework
thatusescomputerslikeahuman. arXivpreprintarXiv:2410.08164,2024.
[2] Anthropic. Claude 3.5 sonnet, 2024. URL https://www.anthropic.com/news/
3-5-models-and-computer-use.
[3] Anthropic. Claude 3.7 sonnet, 2025. URL https://www.anthropic.com/news/
claude-3-7-sonnet.
[4] Anthropic. Claudethinktool, 2025. URLhttps://www.anthropic.com/engineering/
claude-think-tool.
[5] A.Antoniades,A.Örwall,K.Zhang,Y.Xie,A.Goyal,andW.Wang. Swe-search: Enhanc-
ing software agents with monte carlo tree search and iterative refinement. arXiv preprint
arXiv:2410.20285,2024.
[6] S. Arcadinho, D. Aparício, and M. Almeida. Automated test generation to evaluate tool-
augmentedllmsasconversationalaiagents. arXivpreprintarXiv:2409.15934,2024.
[7] D.Bahdanau,N.Gontier,G.Huang,E.Kamalloo,R.Pardinas,A.Piché,T.Scholak,O.Shli-
azhko,J.P.Tremblay,K.Ghanem,etal.Tapeagents:aholisticframeworkforagentdevelopment
andoptimization. arXivpreprintarXiv:2412.08445,2024.
[8] Z.Bi,K.Han,C.Liu,Y.Tang,andY.Wang. Forest-of-thought: Scalingtest-timecomputefor
enhancingllmreasoning. arXivpreprintarXiv:2412.09078,2024.
[9] T.Cai,X.Wang,T.Ma,X.Chen,andD.Zhou. Largelanguagemodelsastoolmakers. arXiv
preprintarXiv:2305.17126,2023.

[10] CAMEL-AI.org. Owl: Optimized workforce learning for general multi-agent assistance in
real-worldtaskautomation. https://github.com/camel-ai/owl,2025. Accessed: 2025-
03-07.
[11] M. Chen, sunhaoze, T. Li, F. Yang, H. Liang, KeerLu, B. CUI, W. Zhang, Z. Zhou, and
weipengchen. Facilitatingmulti-turnfunctioncallingforLLMsviacompositionalinstruction
tuning. InTheThirteenthInternationalConferenceonLearningRepresentations,2025. URL
https://openreview.net/forum?id=owP2mymrTD.
[12] Z. Chen, K. Liu, Q. Wang, W. Zhang, J. Liu, D. Lin, K. Chen, and F. Zhao. Agent-flan:
Designingdataandmethodsofeffectiveagenttuningforlargelanguagemodels. arXivpreprint
arXiv:2403.12881,2024.
[13] Z.Chen, M. Li, Y.Huang, Y.Du, M.Fang, andT. Zhou. Atlas: Agenttuningvia learning
criticalsteps. arXivpreprintarXiv:2503.02197,2025.
[14] S.Cognition. Apt-1blog,2025. URLhttps://www.scaledcognition.com/blog/apt-1.
[15] T.Dao. Flashattention-2: Fasterattentionwithbetterparallelismandworkpartitioning,2023.
URLhttps://arxiv.org/abs/2307.08691.
[16] A.Dubey,A.Jauhri,A.Pandey,A.Kadian,A.Al-Dahle,A.Letman,A.Mathur,A.Schelten,
A.Yang,A.Fan,etal. Thellama3herdofmodels. arXivpreprintarXiv:2407.21783,2024.
[17] T. Ge, X. Chan, X. Wang, D. Yu, H. Mi, and D. Yu. Scaling synthetic data creation with
1,000,000,000personas,2024. URLhttps://arxiv.org/abs/2406.20094.
[18] S.A.Hayati, T.Jung, T.Bodding-Long, S.Kar, A.Sethy, J.-K.Kim, andD.Kang. Chain-
of-instructions: Compositionalinstructiontuningonlargelanguagemodels. arXivpreprint
arXiv:2402.11532,2024.
[19] K.-H.Huang,A.Prabhakar,S.Dhawan,Y.Mao,H.Wang,S.Savarese,C.Xiong,P.Laban,and
C.-S.Wu. Crmarena: Understandingthecapacityofllmagentstoperformprofessionalcrm
tasksinrealisticenvironments,2025. URLhttps://arxiv.org/abs/2411.02305.
[20] E.LeviandI.Kadar. Intellagent: Amulti-agentframeworkforevaluatingconversationalai
systems. arXivpreprintarXiv:2501.11067,2025.
[21] G.Li,H.A.A.K.Hammoud,H.Itani,D.Khizbullin,andB.Ghanem. Camel: Communicative
agentsfor"mind"explorationoflargelanguagemodelsociety. InThirty-seventhConferenceon
NeuralInformationProcessingSystems,2023.
[22] X.Li,H.Zou,andP.Liu. Torl: Scalingtool-integratedrl,2025. URLhttps://arxiv.org/
abs/2503.23383.
[23] Y.Li,Y.Li,X.Wang,Y.Jiang,Z.Zhang,X.Zheng,H.Wang,H.-T.Zheng,P.Xie,P.S.Yu,
etal. Benchmarkingmultimodalretrievalaugmentedgenerationwithdynamicvqadatasetand
self-adaptiveplanningagent. arXivpreprintarXiv:2411.02937,2024.
[24] W.Liu,X.Huang,X.Zeng,X.Hao,S.Yu,D.Li,S.Wang,W.Gan,Z.Liu,Y.Yu,etal. Toolace:
Winningthepointsofllmfunctioncalling. arXivpreprintarXiv:2409.00920,2024.
[25] Z. Liu, J. Zhang, K. Asadi, Y. Liu, D. Zhao, S. Sabach, and R. Fakoor. Tail: Task-specific
adaptersforimitationlearningwithlargepretrainedmodels. arXivpreprintarXiv:2310.05905,
2023.
[26] Z. Liu, T. Hoang, J. Zhang, M. Zhu, T. Lan, J. Tan, W. Yao, Z. Liu, Y. Feng, R. RN, et al.
Apigen: Automated pipeline for generating verifiable and diverse function-calling datasets.
AdvancesinNeuralInformationProcessingSystems,37:54463–54482,2024.
[27] I. Loshchilov and F. Hutter. Decoupled weight decay regularization. arXiv preprint
arXiv:1711.05101,2017.

[28] J.Lu, T.Holleis, Y.Zhang, B.Aumayer, F.Nan, F.Bai, S.Ma, S.Ma, M.Li, G.Yin, etal.
Toolsandbox: A stateful, conversational, interactive evaluation benchmark for llm tool use
capabilities. arXivpreprintarXiv:2408.04682,2024.
[29] A. Mitra, S. Patel, T. Chakrabarty, and C. Baral. Agentinstruct: An agentic framework for
generatinghigh-qualitysyntheticinstructiondata. arXivpreprintarXiv:2402.12360,2024.
[30] J. Pan, X. Wang, G. Neubig, N. Jaitly, H. Ji, A. Suhr, and Y. Zhang. Training software
engineeringagentsandverifierswithswe-gym. arXivpreprintarXiv:2412.21139,2024.
[31] J.Pan,R.Shar,J.Pfau,A.Talwalkar,H.He,andV.Chen.Whenbenchmarkstalk:Re-evaluating
codellmswithinteractivefeedback,2025. URLhttps://arxiv.org/abs/2502.18413.
[32] J.S.Park,J.O’Brien,C.J.Cai,M.R.Morris,P.Liang,andM.S.Bernstein. Generativeagents:
Interactivesimulacraofhumanbehavior. InProceedingsofthe36thannualacmsymposiumon
userinterfacesoftwareandtechnology,pages1–22,2023.
[33] Y.Qin,S.Hu,Y.Lin,W.Chen,N.Ding,G.Cui,Z.Zeng,X.Zhou,Y.Huang,C.Xiao,etal.
Toollearningwithfoundationmodels. ACMComputingSurveys,57(4):1–40,2024.
[34] Qwen,:,A.Yang,B.Yang,B.Zhang,B.Hui,B.Zheng,B.Yu,C.Li,D.Liu,F.Huang,H.Wei,
H.Lin, J.Yang, J.Tu, J.Zhang, J.Yang, J.Yang, J.Zhou, J.Lin, K.Dang, K.Lu, K.Bao,
K.Yang,L.Yu,M.Li,M.Xue,P.Zhang,Q.Zhu,R.Men,R.Lin,T.Li,T.Tang,T.Xia,X.Ren,
X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Wan, Y. Liu, Z. Cui, Z. Zhang, and Z. Qiu. Qwen2.5
technicalreport,2025. URLhttps://arxiv.org/abs/2412.15115.
[35] J.Rasley,S.Rajbhandari,O.Ruwase,andY.He. Deepspeed: Systemoptimizationsenable
trainingdeeplearningmodelswithover100billionparameters. InProceedingsofthe26th
ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, KDD
’20, page 3505–3506, New York, NY, USA, 2020. Association for Computing Machinery.
ISBN9781450379984. doi: 10.1145/3394486.3406703. URLhttps://doi.org/10.1145/
3394486.3406703.
[36] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer,
N.Cancedda,andT.Scialom. Toolformer: Languagemodelscanteachthemselvestousetools.
AdvancesinNeuralInformationProcessingSystems,36:68539–68551,2023.
[37] S.Sengupta,K.Curtis,A.Mallipeddi,A.Mathur,J.Ross,andL.Gou. Mag-v: Amulti-agent
frameworkforsyntheticdatagenerationandverification. arXivpreprintarXiv:2412.04494,
2024.
[38] J. Shim, G. Seo, C. Lim, and Y. Jo. Tooldial: Multi-turn dialogue generation method for
tool-augmentedlanguagemodels. InTheThirteenthInternationalConferenceonLearning
Representations,2025. URLhttps://openreview.net/forum?id=J1J5eGJsKZ.
[39] N. Shinn, F. Cassano, A. Gopinath, K. R. Narasimhan, and S. Yao. Reflexion: language
agentswithverbalreinforcementlearning. InThirty-seventhConferenceonNeuralInformation
ProcessingSystems,2023. URLhttps://openreview.net/forum?id=vAElhFcKW6.
[40] V.Sirdeshmukh,K.Deshpande,J.Mols,L.Jin,E.-Y.Cardona,D.Lee,J.Kritz,W.Primack,
S.Yue,andC.Xing. Multichallenge: Arealisticmulti-turnconversationevaluationbenchmark
challengingtofrontierllms. arXivpreprintarXiv:2501.17399,2025.
[41] H. Su, R. Sun, J. Yoon, P. Yin, T. Yu, and S. Ö. Arık. Learn-by-interact: A data-centric
frameworkforself-adaptiveagentsinrealisticenvironments. arXivpreprintarXiv:2501.10893,
2025.
[42] S. Tang, X. Pang, Z. Liu, B. Tang, R. Ye, X. Dong, Y. Wang, and S. Chen. Synthesizing
post-trainingdataforllmsthroughmulti-agentsimulation. arXivpreprintarXiv:2410.14251,
2024.
[43] J.Wang,J.Zhou,M.Wen,X.Mo,H.Zhang,Q.Lin,C.Jin,X.Wang,W.Zhang,andQ.Peng.
Hammerbench: Fine-grainedfunction-callingevaluationinrealmobiledevicescenarios. arXiv
preprintarXiv:2412.16516,2024.

[44] G.Wölflein,D.Ferber,D.Truhn,O.Arandjelovic´,andJ.N.Kather. Llmagentsmakingagent
tools. arXivpreprintarXiv:2502.11705,2025.
[45] F.Yan,H.Mao,C.C.-J.Ji,T.Zhang,S.G.Patil,I.Stoica,andJ.E.Gonzalez.Berkeleyfunction
callingleaderboard. 2024.
[46] J.Yang, A.Prabhakar, S.Yao, K.Pei, andK.R.Narasimhan. Languageagentsashackers:
Evaluating cybersecurity skills with capture the flag. In Multi-Agent Security Workshop @
NeurIPS’23,2023. URLhttps://openreview.net/forum?id=KOZwk7BFc3.
[47] J.Yang,A.Prabhakar,K.Narasimhan,andS.Yao. Intercode: Standardizingandbenchmarking
interactivecodingwithexecutionfeedback.AdvancesinNeuralInformationProcessingSystems,
36,2024.
[48] R.Yang,F.Ye,J.Li,S.Yuan,Y.Zhang,Z.Tu,X.Li,andD.Yang. Thelighthouseoflanguage:
Enhancing llm agents via critique-guided improvement. arXiv preprint arXiv:2503.16024,
2025.
[49] S.Yao,N.Shinn,P.Razavi,andK.Narasimhan. Tau-bench: Abenchmarkfortool-agent-user
interactioninreal-worlddomains. arXivpreprintarXiv:2406.12045,2024.
[50] F.Yin,Z.Wang,I.-H.Hsu,J.Yan,K.Jiang,Y.Chen,J.Gu,L.T.Le,K.-W.Chang,C.-Y.Lee,
H.Palangi,andT.Pfister. Magnet: Multi-turntool-usedatasynthesisanddistillationviagraph
translation,2025. URLhttps://arxiv.org/abs/2503.07826.
[51] Y.Zeng,X.Ding,Y.Wang,W.Liu,W.Ning,Y.Hou,X.Huang,B.Qin,andT.Liu. Boost-
ing tool use of large language models via iterative reinforced fine-tuning. arXiv preprint
arXiv:2501.09766,2025.
[52] J.Zhang,T.Lan,M.Zhu,Z.Liu,T.Hoang,S.Kokane,W.Yao,J.Tan,A.Prabhakar,H.Chen,
et al. xlam: A family of large action models to empower ai agent systems. arXiv preprint
arXiv:2409.03215,2024.
[53] J.Zhang,T.Hoang,M.Zhu,Z.Liu,S.Wang,T.Awalgaonkar,A.Prabhakar,H.Chen,W.Yao,
Z.Liu,etal. Actionstudio: Alightweightframeworkfordataandtrainingofactionmodels.
arXivpreprintarXiv:2503.22673,2025.
[54] K. Zhang, W. Yao, Z. Liu, Y. Feng, Z. Liu, R. Rithesh, T. Lan, L. Li, R. Lou, J. Xu, et al.
Diversityempowersintelligence: Integratingexpertiseofsoftwareengineeringagents. InThe
ThirteenthInternationalConferenceonLearningRepresentations,2024.
[55] Y.Zhang,J.Lu,andN.Jaitly. Probingthemulti-turnplanningcapabilitiesofLLMsvia20
questiongames. InL.-W.Ku,A.Martins,andV.Srikumar,editors,Proceedingsofthe62nd
AnnualMeetingoftheAssociationforComputationalLinguistics(Volume1: LongPapers),
pages1495–1516,Bangkok,Thailand,Aug.2024.AssociationforComputationalLinguistics.
doi: 10.18653/v1/2024.acl-long.82. URLhttps://aclanthology.org/2024.acl-long.
82/.
[56] Y. Zheng, R. Zhang, J. Zhang, Y. Ye, Z. Luo, Z. Feng, and Y. Ma. Llamafactory: Unified
efficientfine-tuningof100+languagemodels. InProceedingsofthe62ndAnnualMeetingof
theAssociationforComputationalLinguistics(Volume3: SystemDemonstrations),Bangkok,
Thailand,2024.AssociationforComputationalLinguistics. URLhttp://arxiv.org/abs/
2403.13372.

A BenchmarksDescription
• BFCL v3: It introduces comprehensive evaluation across single-turn, multi-turn, and multi-
step function calling scenarios. BFCL v3 evaluates models on their ability to understand user
requests,selectappropriatefunctions,generatevalidparameters,andinterpretfunctionoutputs
acrossmultipleinteractionturns. Thebenchmarkusesaweightedaverageofdifferentevaluation
categoriestoprovideanoverallaccuracyscore.
• τ-bench: Itmeasuresanagent’sabilitytointeractwithsimulatedhumanusers(poweredbylan-
guagemodels)andprogrammaticAPIswhilefollowingdomain-specificpolicies.τ-benchemulates
dynamic conversations across multiple domains, including retail and airline customer service,
requiringagentstomaintaincontextacrossturns, understanduserintents, andfollowcomplex
domain-specificrules. Thebenchmarkemphasizestheimportanceofmulti-turninteractionsand
policyadherenceinreal-worldapplications.
B Prompts
ThepromptsusedacrossthevariousstagesofAPIGen-MTimplementedforτ-benchareshownhere–
TaskConfigurationGeneration(Figure8),AlignmentValidation(Figure9),FinalSemanticReview
(Figure10),TrajectoryCollection(Figure11),StabilizedHumanSimulation(Figure12).
Task Configuration Generation Prompt
##Instructions
Generateataskinstructionthatmimicsrealistichumanusersandtheirintentions,suchaswithdifferentpersonalityandgoals.Thetaskinstructionshouldbe
followedby‘actions’whichisalistofthetool_callstobetakentosolvethistaskand‘outputs’whichisalistoftheanswerstospecificinformationrequestsmade
bytheuser.Thinkstepbysteptocomeupwiththeaction(s)andthecorrespondingtool_call(s)translatingthisthoughtthatwouldbenecessarytofulfilltheuser’s
requestorsolvetheirintentions.Focusoncommonretailscenariosfollowingtheprovidedtaskinstructionguidelines.
##GuidelinesforGeneratingTaskInstruction(q)
{task_rules+domain_rules}
###UserData
{sampled_user_details}
###OrderData
{sampled_orders}
##GuidelinesforgeneratingGroundtruthActions(agt)
## 1. Themainfocusistogenerateactionsthatcanmodifytheunderlyingdatabase.
2. Foractionsthatdonotmodifythedatabaselikespecificinformationrequests,scantheprovidedUserDatadirectlyandappendonlytheanswerin‘outputs’
(ogt).Donotmakeseparatetoolcallsforthisin‘actions’.
## 3. Includemultipletoolcallswhenthescenariorequiresmultiplestepsormodifications.
## 4. Provideprecisetoolcallswithallnecessaryparametersforeachaction.
## 5. Ensureallactionsadheretoretailpoliciesandcommonsensepractices.
##Tools
TheavailabletoolcombinationinPythonformatisasfollows:
{sampled_tools}
##OutputFormat
Generateyourresponseaccordingtothefollowingformat.Enclosethethoughtprocesswithin‘<thought></thought>’tags,andthefinalstructuredresponsewithin
‘<answer></answer>’tags.ThestructuredresponseshouldbeinstrictJSONformat,withoutanyadditionalcommentsorexplanations.
##ExampleTasks
{example}
Donotdirectlycopyinstructionandtheactionpatternsfromtheexamples.Groundthegenerationfromtheaboveprovideddata.
Generatethetasknow.
Figure8: Taskconfigurationgenerationpromptforretaildomainofτ-bench.

Task Alignment Validation Prompt
YouareanAIjudgeandyourgoalistojudgethequalityandvalidityoftheprovidedtaskobjectbasedontheguidelines,followingtherubric.
##Guidelines
• Thetaskobjectcontainsan‘intent’(q)fromauser,‘actions’(agt),and‘outputs’(ogt).
• The‘actions’correspondtothetool_callsmadebyanAIassistanttosatisfytheinstruction.
• Adescriptionofthe‘tools’availabletotheAIassistantisprovided.
• The‘diff_patch’isthedifferenceinthedatabasestateafterthetool_callsaremade.Itshouldonlyreflectchangescorrespondingtothe‘intent’.Thereshould
benoextraneouschanges.Ifthe‘diff_patch’isempty,itmeansthatthetool_callsdidnotchangethedatabasestate,whichispossibleiftheinstructionwasto
provideinformationonly.
• PerformabriefreflectiononthetaskbasedonthebelowRubrics.
• Thinkstep-by-steptogenerateascoreof0or1foreachofthesecriteria(1meansfollowscriterionand0meansdoesnot)
##Rubric
• Correctness:Dotheactions(agt)accuratelyimplementtheinstruction(q)?
• Completeness:Istheinstruction(q)sufficientlydetailed,andisitfullyaddressedbytheactions?(Includesrule-basedchecks).
• Satisfaction:Dotheexpectedoutputs(ogt)fulfillanyexplicitorimplicitinformationrequestswithintheinstruction(q)?
• Creativity:Doesthetaskrepresentanon-trivial,plausible,andpotentiallyinterestingscenariowithinthedomain?
##TaskObject
{task}
##ToolsinPythonformat
{tools}
##DiffPatch
{diff_patch}
##Outputformat
<scores>
{{
"reflection":str,<abriefhigh-levelreviewofthetask>
"correctness":int,<0/1>,
"completeness":int,<0/1>,
"satisfaction":int,<0/1>,
"creativity":int,<0/1>,
"total":int,<totalscoreoutof4>
"correction":str,<briefexplanationandsuggestedcorrection(ifneeded)>
}}
</scores>
Figure 9: Task alignment validation prompt for τ-bench. This is sent to each LM in the review
committeetogettheirscores,followingwhichweemploymajorityvoting.
Final Semantic Review Prompt
YouareresponsibleforanalyzingandsummarizingfeedbackfrommultipleAIjudges. Yourprimarygoalistoprovideclear,actionablefeedbackthatwill
helpthegeneratorLLMimproveitsfutureoutputs.Youdonotevaluatethetaskdirectly;instead,youreviewandgroundingtheexistingfeedbackfromtheAIjudges.
##ReviewProcess
• Beginbyanalyzingindividualreflectionsandscoresfromeachjudge.
• Summarizecommonpointsofagreementordisagreement.
• Offeraconcisesummaryofactionablefeedbacktobesentbacktothedatagenerator,whichaimstoimprovethenextroundofdataquality.
###DiffPatch
{diff_patch}
###GeneratedTaskData
{task}
###AIJudges’Feedback
{reviews}
##OutputFormat
Generateyourresponseaccordingtothefollowingformat.Enclosethethoughtprocesswithin‘<thought></thought>’tags,andthefinalsummaryofactionable
feedbackwithin‘<summary></summary>’tags.
Figure10: Finalsemanticreviewpromptforτ-bench.

Trajectory Collection Prompt
Youareadetail-orienteduserinteractingwithanAIagent.
##Intent
{intent}
##Rules
• Generateonelineatatimetosimulatetheuser’smessage.
• Donotgiveawayalltheintentatonce.Onlyprovidetheinformationthatisnecessaryforthecurrentstep.
• Donothallucinateinformationthatisnotprovidedintheintent.
• Iftheintentgoalissatisfied,generate‘###STOP###’toendtheconversation.
• Donotrepeattheexactintentintheconversation.Instead,useyourownwordstoconveythesameinformation.
• Trytomaketheconversationasnaturalaspossibleandsticktothepersonalitiesintheintent.
Figure11: Trajectorycollectionpromptforτ-bench.
BoN User LM Setting Prompt
Youareafairjudgeandanexpertinfollowingdetails.
Ahumanisinteractingwitharetailassistanttogethelponsolvingtheirtask. Youareprovidedwiththedescriptionofthehumanandthetaskthe
humanwantstoaccomplish(wrappedwith<description></description>),andacandidateresponse(wrappedwith<response></response>)thehumanwantsto
givetheassistant.Pleasehelpthehumanevaluatethiscandidateresponse,giveanintegerscore(rangingfrom0to10)toindicatethecorrectnessoftheresponse,
higherscoremeansbetterquality.
1.Iftheresponseincludesspecificitem/order/personaldetails,andtheycorrectlymatchthetaskdescriptionyoushouldgivefullscoreof10.Ifthereissome
changeindetails,giveacorrespondinglowerscore(moreincorrectdetailsgetslowerscore).
2.Theresponsecanincludeanynormalconversationotherwise(e.g.askingdetails,saying###STOP###)etc.whichareallcorrectresponses.
3.Additionally,ifthecandidate_responsekeepstheconversationflowingbydescribingthetaskclearly/givesinformationproperlythengiveahighscoreandifnot
(e.g."Idon’tremember"orunhelpfulresponse)shouldgetacorrespondinglowerscore.
<description>{description}</description>
<response>{response}</response>
Afterscoringusingthementionedguideline,tellmeyourscore,wrapitin<score></score>tags.
Figure12: Best-of-N(BoN)UserLMsettingpromptusedintheretaildomainofτ-bench.

## My Notes

<!-- 5 行笔记追加模板 -->