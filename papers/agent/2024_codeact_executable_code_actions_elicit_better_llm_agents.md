---
paper_id: 2024_codeact_executable_code_actions_elicit_better_llm_agents
topic_tags: [agent, code_action, tool_use, instruction_tuning, self_debug]
source_url: https://arxiv.org/abs/2402.01030
---

Executable Code Actions Elicit Better LLM Agents
XingyaoWang1 YangyiChen1 LifanYuan1 YizheZhang2 YunzhuLi1 HaoPeng1 HengJi1
Abstract 1.Introduction
LargeLanguageModels(LLMs)haveemergedasapivotal
Large Language Model (LLM) agents, capable
breakthroughinnaturallanguageprocessing(NLP).When
of performing a broad range of actions, such
augmentedwithactionmodulesthatallowaccesstoAPIs,
as invoking tools and controlling robots, show
their action space expands beyond conventional text pro-
greatpotentialintacklingreal-worldchallenges.
cessing,allowingLLMstoacquirecapabilitiessuchastool
LLMagentsaretypicallypromptedtoproduceac-
invocationandmemorymanagement(Mialonetal.,2023;
tionsbygeneratingJSONortextinapre-defined Schicketal.,2023)andventureintoreal-worldtaskssuchas
format, whichisusuallylimitedbyconstrained
controllingrobots(Ahnetal.,2022;Huangetal.,2023;Ma
action space (e.g., the scope of pre-defined
etal.,2023)andperformingscientificexperiments(Bran
tools)andrestrictedflexibility(e.g.,inabilityto
etal.,2023).
compose multiple tools). This work proposes
to use executable Python code to consolidate Weinquire: howtoeffectivelyexpandLLMagents’action
LLMagents’actionsintoaunifiedactionspace space for solving complex real-world problems? Much
(CodeAct). IntegratedwithaPythoninterpreter, existingresearchhasexaminedusingtext(Yaoetal.,2022b;
CodeActcanexecutecodeactionsanddynam- Park et al., 2023, inter alia) or JSON (Qin et al., 2023b;
ically revise prior actions or emit new actions Chase,2022,interalia)toproduceactions(e.g.,tooluses
uponnewobservationsthroughmulti-turninterac- inFig.1topleft). However,bothmethodstypicallysuffer
tions. Ourextensiveanalysisof17LLMsonAPI- fromconstrainedscopeofactionspaces(actionsareusually
Bankandanewlycuratedbenchmarkshowsthat tailored for specific tasks) and restricted flexibility (e.g.,
CodeActoutperformswidelyusedalternatives inabilitytocomposemultipletoolsinasingleaction).Asan
(upto20%highersuccessrate). Theencouraging alternativeapproach,severalwork(Liangetal.,2022;Singh
performanceofCodeActmotivatesustobuild etal.,2023;Wangetal.,2023a)demonstratethepotential
anopen-sourceLLMagentthatinteractswithen- ofusingLLMstogeneratecodetocontrolrobotsorgame
vironmentsbyexecutinginterpretablecodeand characters. However, they typically rely on pre-specified
collaborateswithusersusingnaturallanguage.To controlprimitivesandhand-engineeredpromptsand,more
thisend,wecollectaninstruction-tuningdataset importantly,struggletodynamicallyadjustoremitactions
CodeActInstructthatconsistsof7kmulti-turnin- basedonnewenvironmentalobservationandfeedback.
teractionsusingCodeAct. Weshowthatitcan
This work proposes CodeAct, a general-purpose frame-
beusedwithexistingdatatoimprovemodelsin
workthatallowsLLMstogenerateexecutablePythoncode
agent-orientedtaskswithoutcompromisingtheir
asactions(Fig.1topright).CodeActisdesignedtohandle
generalcapability.CodeActAgent,finetunedfrom
avarietyofapplicationsandcomeswithuniqueadvantages:
Llama2andMistral,isintegratedwithPythonin-
terpreteranduniquelytailoredtoperformsophis- (1) IntegratedwithaPythoninterpreter,CodeActcanex-
ticatedtasks(e.g.,modeltraining)usingexisting ecutecodeactionsanddynamicallyadjustprioractions
librariesandautonomouslyself-debug1. oremitnewactionbasedonobservations(e.g., code
executionresults)itreceivesthroughmultipleturnsof
interactions.
1Department of Computer Science, University of Illinois
Urbana-Champaign2Apple.Correspondenceto:XingyaoWang (2) CodeactionsallowLLMtoleverageexistingsoftware
<xingyao6@illinois.edu>,HengJi<hengji@illinois.edu>. packages. CodeActcanusereadilyavailablePython
packagesforanexpandedactionspaceinsteadofhand-
Proceedings of the 41st International Conference on Machine craftedtask-specifictools(Yuanetal.,2023;Shenetal.,
Learning,Vienna,Austria.PMLR235,2024.Copyright2024by
2023). ItalsoallowsLLMtouseautomatedfeedback
theauthor(s).
(e.g.,errormessages)implementedinmostsoftwareto
1The code, data, model, and demo are available at https:
//github.com/xingyaoww/code-act. improvetask-solvingbyself-debuggingitsgenerated
nuJ
]LC.sc[
4v03010.2042:viXra

ExecutableCodeActionsElicitBetterLLMAgents
Success Rate (%) Average Number of Interaction Turns
gpt-4-1106-preview
gpt-4-0613
claude-2
gpt-3.5-turbo-0613
gpt-3.5-turbo-1106
gemini-pro Action Mode
Code as Action
text-davinci-003
JSON as Action
Llama-2-70b-chat-hf Text as Action
0 10 20 30 40 50 60 70 5 6 7 8 9 10
Figure1: ComparisonbetweenCodeActandText/JSONasaction. (top)Illustrativeexamplecomparingdifferentactions.
(bottom)QuantitativeresultsonM3ToolEval(§2.3).
code(Chenetal.,2023b;Wangetal.,2023d). fits(3&4)ofCodeAct. Todemonstratebenefit(3),our
(3) Codedataiswidelyusedinpre-trainingtoday’sLLMs firstexperiment(§2.2)comparesCodeActtobaselineson
(Yangetal.,2024b). Thesemodelsarealreadyfamiliar basictasksinvolvingatomictooluse(i.e.,onlyonetoolis
withstructuredprogramminglanguages,allowingcost- usedperaction),ablatingthecontrolanddataflowadvan-
effectiveadoptionofCodeAct. tageofferedbyCodeAct. Theresultsshowthat,formost
(4) ComparedtoJSONandtextwithapre-definedformat, LLMs, CodeAct achieves comparable or better perfor-
codeinherentlysupportscontrolanddataflow,allow- mancethanthebaselines. CodeAct’sperformancegains
ingforthestorageofintermediateresultsasvariables aremoreprominentoncomplextasks,asdemonstratedin
forreuseandthecompositionofmultipletoolstoper- oursecondexperiment(benefit4). Wecurateanewbench-
form complex logical operations (e.g., if-statements, mark consisting of 82 human-curated tasks that typically
for-loops)withonepieceofcode,therebyunlocking requiremultiplecallstomultipletoolsinmulti-turninterac-
LLMs’potentialtotacklecomplextasksbyleveraging tions(M3ToolEval;§2.3).Problemsinthisbenchmarkoften
itspre-trainedknowledgeofprogramming. InFig.1, requireintricatecoordinationandcompositionofmultiple
anLLMusingwithCodeAct(topright)canapplythe tools. Withitsstrengthsincontrolanddataflow,CodeAct
samesequenceoftools(e.g.,passingonetool’soutput achievesuptoa20%absoluteimprovementoverbaselines
asinputtoanothertoolusingthedataflowfeature)to onthesuccessrateofsolvingtheproblemswhilerequiring
allinputsthroughfor-loops(i.e.,controlflowfeature) upto30%feweractions. Theseperformancegainswiden
withoneaction;whiletextorJSONhavetotakeaction asthecapabilitiesoftheLLMsincrease(Fig.1bottom).
foreveryinput(topleft).
The promising performance of CodeAct motivates an
Ourextensiveexperimentswith17LLMs(includingboth open-source LLM agent that can effectively act through
open-sourceandproprietaryones)confirmtheabovebene- CodeAct,andcollaboratewithhumansthroughnaturallan-

ExecutableCodeActionsElicitBetterLLMAgents
Table1: ThebenefitofCodeActcomparedtousingText/JSONforLLMaction.
CodeActforLLMaction JSONorTextforLLMaction
AvailabilityofData (cid:34)Largequantityofcodeavailable1forpre-training (cid:37)Datacurationrequiredforparticularformat
Complex Operation (e.g., looping, (cid:37)Requires careful engineering if feasible (e.g.,
(cid:34)Nativelysupportedviacontrolanddataflow
compositionofmultipletools) definenewtoolstomimicif-statement)
(cid:37)Requires human effort to curate tools from
AvailabilityofTools (cid:34)Candirectlyuseexistingsoftwarepackages2
scratchorexistingsoftware
(cid:34)Feedbackmechanism3(e.g.,traceback)isalready (cid:37)Requireshumanefforttoprovidefeedbackorre-
AutomatedFeedback implementedasaninfrastructureformostprogram- routefeedbackfromtheunderlyingprogramming
minglanguages languageusedtoimplementthetools
1IncludingcodedemonstratingusefulbehaviorsforLLMagents(e.g.,taskdecomposition,coordinationofmultiplefunctioncallstodifferenttools).
2Human-writtenPythonpackagescoveringawiderangeofapplicationsareavailableonhttps://pypi.org/.
3Forexample,inPython,errorsandexceptions(https://docs.python.org/3/tutorial/errors.html)areavailable.Mostsoftware
provideserrormessagesinnaturallanguagetohelphumanprogrammersdebugtheircode.CodeActenablesLLMtousethemdirectly.
guage. Tothisend,wecollectaninstruction-tuningdataset 17 off-the-shelf LLMs. In §2.2, we examine RQ1: Does
CodeActInstruct consisting of 7k high-quality multi-turn LLMs’familiaritywithcodeduetoalargeamountofcode
interactiontrajectorieswithCodeAct(§3.1). CodeActIn- pre-trainingdatabringCodeActadvantagesovertextand
structismotivatedbyageneralagentframeworkconsisting JSON?WediscussRQ2in§2.3: DoesCodeActbenefit
of agent, user, and environments (Fig. 2) and focuses on fromPython’sinnatecontrolanddataflowfeatureincom-
agent-environmentinteractionswiththecomputer(informa- plexproblems? Finally,asanadditionalbenefit,wediscuss
tionseeking,softwarepackageuse,externalmemory)and howusingCodeActfurtherenhancesLLMagentsbyen-
thephysicalworld(robotplanning). OnCodeActInstruct, ablingmulti-turninteractionsandallowingthemtoaccess
weperformcarefuldataselectiontopromotethecapability existingsoftwarein§2.4andFig.3.
ofimprovingfrommulti-turninteraction(e.g.,self-debug).
WeshowthatCodeActInstructcanbeusedwithcommonly 2.1.WhatisCodeAct?
usedinstructiontuningdatatoimprovethemodels’perfor-
InFig.2,wefirstintroduceageneralmulti-turninteraction
manceinagenttaskswithoutcompromisingtheirgeneral
frameworkforLLMagents’real-worldusagethatconsiders
capabilities(e.g.,knowledge-basedQA,coding,instruction
threeroles(Yangetal.,2024c): agent,user,andenviron-
following,§3.2).Ourmodel,dubbedCodeActAgent,isfine-
ment. Wedefineinteractionastheinformationexchange
tunedfromLLaMA-2(Touvronetal.,2023)andMistral-7B
betweentheagentandanexternalentity(userorenviron-
(Jiangetal.,2023)andimprovesonout-of-domainagent
ment). Foreachturnofinteraction,theagentreceivesanob-
tasks with not only CodeAct, but also text action in a
servation(input)eitherfromtheuser(e.g.,naturallanguage
pre-definedformat(§3.2).
instruction)ortheenvironment(e.g.,codeexecutionresult),
CodeActcanfurtherbenefitfrommulti-turninteractions optionallyplanningforitsactionthroughchain-of-thought
andexistingsoftware(benefit1&2, §2.4). Asshownin (Weietal.,2022),andemitsanaction(output)toeitheruser
Fig. 3, CodeActAgent, designed for seamless integration innaturallanguageortheenvironment. CodeActemploys
withPython,cancarryoutsophisticatedtasks(e.g.,model Pythoncodetoconsolidateallactionsforagent-environment
training,datavisualization)usingexistingPythonpackages. interaction. In CodeAct, each emitted action to the en-
Errormessagesfromtheenvironmentfurtherenableitto vironment is a piece of Python code, and the agent will
rectifyerrorsautonomouslythroughself-debugginginmulti- receiveoutputsofcodeexecution(e.g.,results,errors)as
turninteraction. ThankstoLLM’sextensiveprogramming observation. WeincludeanexamplepromptofCodeAct
knowledgeacquiredduringpre-training,theseareachieved in§E.
without needing in-context demonstrations, reducing the
humaneffortsforadaptingCodeActAgenttodifferenttasks. 2.2.CodeActShowsthePromiseasaStrongToolUse
Framework
2.CodeActMakesLLMsBetterAgents
Inthissection,weperformacontrolledexperimenttounder-
Inthissection,wefirstdescribeCodeActframework(§2.1) standwhichformat(text,JSON,CodeAct)ismorelikely
andprovideempiricalevidencethatsupportsthechoiceof toleadanLLMtogeneratecorrectatomictoolcalls. The
CodeAct. WefocusonPythonastheprogramminglan- performanceinthisexperimentreflectsLLM’sfamiliarity
guageforCodeActduetoitspopularity(rankedtop-1at withthecorrespondingformat. Wehypothesizethatusing
(TIOBEIndex,2024))andnumerousopen-sourcepackages. CodeActtocalltoolsisamorenaturalwaytousetools
Weaimtoanswerseveralresearchquestions(RQs)using forthemodels,whichtypicallyhaveextensiveexposureto

ExecutableCodeActionsElicitBetterLLMAgents
Example
CodeAct
Action Conversation
User:
unified action space in Natural Language
Find the sum of the reciprocals of the roots of
$x^2-13x+4=0$.
Assistant:
To find the sum of the reciprocals of the roots Environment
Think
Software Interface (API)
of the quadratic equation $x^2-13x+4=0$ [...]
Interface for Computer
<execute>
Information Seeking
import sympy (e.g., Web search, Browsing) Planning
x r o = o t s s y m = p y s . y S m y p m y b . o s l o ( l ' v x e ' (x ) **2 - 13*x + 4) S (e o .g f ., t C w alc a u r la e t e P , D a o c w k n a lo g a e d, ( V T is o ua o li l z )
e) Agent  Chain-of-though  User Start
print(1/roots[0] + 1/roots[1]) External Memory
Self-Reflectio
</execute>
(e.g., Database, Graph)  Improving Action from
Env:
Interface for Ph [. y ..] sical World Prior Observatio
1/(3*sqrt(17)/2 + 13/2) + 1/(13/2 - 3*sqrt(17)/2)
Robots  ...
Assistant:
(e.g., Household Robots, Automated Lab) Initiate Interaction
The roots obtained are in symbolic form, which [...]
makes it difficult to evaluate the sum directly.
Let's use the quadratic formula to explicitly Outcome
Conversation
find the numerical values of the roots first.
E.g., Execution results, Observation E.g., Natural Language
[...] Automated error feedback Instruction or Feedback
Figure2:Generalagentmulti-turninteractionframeworkthatdescribestheroleofCodeActandmotivatestheconstruction
ofourdatamixture. CodeActInstructfocusesontheagent-environment interactionsandspecificallyfiltersfortheself-
improvedplanningbehavior,whilegeneralconversationdataweincludefocusesonagent-userinteraction(§3.1).
codedataduringtheirtraining. thatrequirecomplexpatternsoftooluse.
Setup. Were-purposeAPI-Bank(Lietal.,2023)andtest M3ToolEval. As shown in Tab. A.7, to the best of our
LLMs’ API-calling performance, comparing CodeAct, knowledge,noexistingtool-usebenchmarkscontaincom-
JSON,andtextactions. Foreachevaluationinstance,we plextasksrequiringthecompositionofmultipletoolswhile
instructLLMtogenerateoneatomictoolcallintheformat supportingevaluatingdifferentactionformats. Hence,we
ofaPythonfunctioncall,JSONobject,ortextexpression curateabenchmarkM3ToolEvaltofillthisgap,whicheval-
in apre-defined format. A concreteexampleis shownin uatesLLMs’capabilitiesinsolvingcomplextasksthattypi-
Tab.A.6. WeuseAPI-Bank’slevel-1instructionsandthe callyrequiremultiplecallstomultipletoolsinmulti-turn
providedtoolset. ToevaluateAPI-calling,wefollowtheir interactions. Itcontains82human-curatedinstances,span-
correctnessmetric,matchingtheground-truthAPIoutputs ningtasksincludingwebbrowsing,finance,travelitinerary
withtheactualmodel-generatedAPI’sexecutionoutputs. planning, science, and information processing. Each do-
mainisaccompaniedbyauniquesetofmanuallycrafted
Results. We present results in Tab. 2. For most LLMs,
tools. Weintentionallykeepthepromptsimple(examples
CodeActachievescomparableorbetterperformanceeven
in §F) and avoid providing any demonstration to test the
inatomicactions(thesimplistictoolusescenario)where
LLM’szero-shotabilitytousetools,similartohowanovice
itscontrolanddataflowstrengthsareablated. Comparedto
userwithoutknowledgeoffew-shotpromptingwoulduse
closed-sourceLLMs,CodeAct’simprovementsaremore
themodel.
prominentinopen-sourcemodels.Furthermore,codedatais
usuallymoreaccessibleforfine-tuningopen-sourceLLMs Setup. We allow the model to generate fully functional
thanthespecializedJSONortexttool-callingformat. Al- Python code that enables control and data flow (e.g., if-
thoughJSONisconsistentlyweakerthanotherapproaches statement,for-loop). WefollowtheactionformatforJSON
foropen-sourcemodels,itachievesdecentperformancewith andtextdescribedinTab.A.6. Withineachturn,themodel
closed-source LLMs, indicating that these closed-source caneitheremitanactionorproposeananswertobeverified
modelsmayhavegonethroughtargetedfine-tuningtoward by an exact match with the ground-truth solution. The
theirJSONcapabilities. Theseresultssuggestoptimizing interactionwillterminatewhenamaximumof10interaction
forCodeActisabetterrouteforopen-sourceLLMsthan turnsarereachedoracorrectsolutionhasbeensubmitted,
alternativestoimprovetheirtool-usecapabilities, asthey similarto(Wangetal.,2023e).
alreadyshowgoodinitialCodeActcapabilityduetoex-
Metric. We measure the success rate by calculating the
tensiveexposuretocodedataduringpre-training.
percentageofthemodelproposedanswersthatmatchthe
ground-truthsolutions. Wealsoincludetheavg. turnsmet-
2.3.CodeActGetsMoreDonewithFewerInteractions
ric: theaveragenumberofturnsonallevaluatedinstances.
In this section, we investigate whether LLM agents can QuantitativeResultsonM3ToolEval. Weincludefullre-
benefitfromthecontrolanddataflowofcodeonproblems
sults in Tab. 3 and a subset of results for visualization in

ExecutableCodeActionsElicitBetterLLMAgents
Table 2: Atomic API call correctness on API- Table3: Successrates(higherthebetter)andaverageturnsrequiredper
Bank. Thebestperformanceisbolded,andthe instance(lowerthebetter)onM3ToolEval. Thebestresultsforeach
second-bestisunderlined. modelarebolded,andthesecond-bestonesareunderlined.
Correctness(%,↑) SuccessRate(%,↑) Avg.Turns(↓)
FormatofAction CodeAct JSON Text
FormatofAction CodeAct JSON Text CodeAct JSON Text
Open-sourceLLMs
Open-sourceLLMs
CodeLlama-7b-Instruct-hf 12.5 12.0 17.0 CodeLlama-7b-Instruct-hf 4.9 2.4 2.4 9.7 9.9 9.9
CodeLlama-13b-Instruct-hf 11.8 7.8 14.0 CodeLlama-13b-Instruct-hf 4.9 4.9 4.9 9.8 9.8 9.7
CodeLlama-34b-Instruct-hf 17.3 12.0 16.8 CodeLlama-34b-Instruct-hf 2.4 0.0 0.0 9.9 10.0 10.0
Llama-2-7b-chat-hf 28.8 11.3 25.8 Llama-2-7b-chat-hf 0.0 1.2 2.4 8.9 9.5 9.6
Llama-2-13b-chat-hf 38.1 8.5 37.3 Llama-2-13b-chat-hf 0.0 0.0 0.0 9.7 10.0 10.0
Llama-2-70b-chat-hf 35.6 14.3 37.6 Llama-2-70b-chat-hf 11.0 3.7 3.7 9.1 9.8 9.8
Mistral-7B-Instruct-v0.1 2.5 2.3 3.0 Mistral-7B-Instruct-v0.1 0.0 3.7 1.2 10.0 9.8 9.9
lemur-70b-chat-v1 58.6 46.6 56.1 lemur-70b-chat-v1 13.4 15.9 12.2 9.1 9.3 9.4
Closed-sourceLLMs Closed-sourceLLMs
claude-2 76.7 59.4 73.7 claude-2 54.9 39.0 29.3 7.2 8.3 8.5
claude-instant-1 75.2 64.9 73.2 claude-instant-1 20.7 31.7 24.4 8.8 8.6 8.9
gemini-pro 70.4 73.2 71.2 gemini-pro 22.0 19.5 11.0 8.8 9.1 9.5
gpt-3.5-turbo-0613 74.4 73.9 73.4 gpt-3.5-turbo-0613 51.2 26.8 20.7 7.0 8.8 9.2
gpt-3.5-turbo-1106 75.4 78.4 73.4 gpt-3.5-turbo-1106 29.3 15.9 14.6 8.4 9.0 9.0
gpt-4-0613 75.4 82.0 74.4 gpt-4-0613 67.1 56.1 45.1 6.6 7.6 8.0
gpt-4-1106-preview 76.7 82.7 73.4 gpt-4-1106-preview 74.4 52.4 53.7 5.5 7.6 7.7
text-davinci-002 69.2 59.6 57.4 text-davinci-002 4.9 4.9 8.5 9.7 9.8 9.6
text-davinci-003 75.4 76.9 69.7 text-davinci-003 20.7 18.3 7.3 9.2 9.0 9.6
FrequencyofBest-PerformingFormat↑ FrequencyofBest-performingFormat↑
Open-source 4 0 4 Open-source 5 4 3 6 1 1
Closed-source 4 5 0 Closed-source 7 1 1 6 2 1
Overall 8 5 4 Overall 12 5 4 12 3 2
Fig.1. CodeActgenerallyhasahighertasksuccessrate anduseMatplotlibfordatavisualization. Furthermore,us-
(12outof17evaluatedLLMs),similartothetrendin§2.2. ing the interactive Python interpreter for code execution
Moreover,usingCodeActrequiresaloweraveragenum- allowsautomatederrormessagesthathelptheLLMagent
berofturns(12outof17evaluatedLLMs).Forexample,the ‘self-debug’ their actions in a multi-turn interaction and
bestmodelgpt-4-1106-previewachievesa20.7%ab- eventuallycompletethehumanuser’srequestcorrectly.
soluteimprovementcomparedtothenextbestactionformat
(text)whilerequiring2.1fewerinteractionturnsonaverage.
3.EmpoweringOpen-sourceLLMAgenttobe
However,thereisstillasignificantgapintermsofabsolute
BetteratCodeAct
CodeActperformancebetweenopen-andclosed-source
LLMsasthebestopen-sourcemodelachieving13.4%while ThepromisingresultsachievedbyCodeActmotivateus
the best closed-source model gpt-4-1106-preview to build an open-source LLM agent that can both inter-
74.4%. Thisispotentiallyduetoopen-sourcemodels’weak act with environments through CodeAct and communi-
task-solvingcapabilityandinabilitytofollowcomplexin- catewithhumansusinglanguage. Toimproveopen-source
structionswithoutdemonstration,suggestinganurgentneed LLMs’CodeActcapability,in§3.1,weintroduceCode-
toimproveopen-sourceLLMsforpractical,real-worldtasks ActInstruct,aninstructionfinetuningdatasetthatcontains
underthezero-shotsetting. agent-environmentinteractiontrajectories. Wediscussdata
selectionproceduresin§3.1topromoteimprovementfrom
2.4.CodeActBenefitsfromMulti-turnInteractions interactionbehavior. Additionally,weshowthatCodeAct
andExistingSoftwarePackages canbeusedtogetherwithexistingagent-userconversation
data(§3.1)tobalancethedialogcapabilityoftheresulting
InFig.3,weshowhowanLLMagentcanintegratewith
LLM.OurmodelCodeActAgent,finetunedfromLLaMA-2
Python (i.e., CodeActAgent we trained in §3.2) and use
(Touvronetal.,2023)andMistral-7B(Jiangetal.,2023)
existing software to perform complex tasks in multi-turn
onamixtureofCodeActInstructandgeneralconversations,
interactions. ThankstoitsextensiveknowledgeofPython
improvesCodeActperformanceswithouthurtingLLM’s
learned during pre-training, the LLM agent can automat-
generalperformanceonadiversesuiteoftasks(§3.2).
ically import the correct Python libraries to solve tasks
withoutrequiringuser-providedtoolsordemonstrations. As
3.1.CodeActInstruct: Agent-EnvironmentInteractions
illustratedinFig.3,CodeActAgentcanusePandastodown-
loadandprocesstabulardata,useScikit-Learnformachine Weconsiderfourmainusecasesinagent-environmentinter-
learningtrain-testdatasplitandregressionmodeltraining, actionandrepurposefiveexistingdatasetsacrossdifferent

ExecutableCodeActionsElicitBetterLLMAgents
User Environment User
Here is a dataset about auto MPG: "https://huggingface.co/datasets/scikit- M R e ^ a 2 n s c s o q r u e a : r e d 0 e .7 r 9 r 0 o 1 r 5 : 0 0 3 1 8 0 6 . 7 7 6 1 0 0 3 8 5 64418838367 Can you rotate the x ticks by 45 degrees for better readability?
learn/auto-mpg/raw/main/auto-mpg.csv". You should download and load the
dataset from the URL, take a look at it, check for missing value, do a train-test CodeActAgent CodeActAgent
split, and train a regression model predicting its MPG. You should use The mean squared error is 10.711 and the R^2 score is 0.790, which indicates that Certainly! Here is the updated bar chart with the x-ticks rotated by 45 degrees
everything except "mpg" and "car name" as the input features. the model has a good fit with the data [...] for better readability:
[..same code omitted...]
CodeActAgent User # p l P t l .b o a t r ( r f e e g a r t e u s r s e i _ o n n a m c e o s e , f f c i o c e i f e , n t t s ick_labels=False)
To accomplish this task, I will use the pandas library to download and load the Can you also give me the MSE and R^2 for the training set? plt.xticks(feature_names, feature_names,
d th a e ta s s c e ik t, i t c - h l e e c a k r n fo l r ib m ra i r s y s i t n o g t v ra a i l n u e a s r , e a g n r d e s p s e i r o f n o r m m o a d e t l r . ain-test split. Then, I will use CodeActAgent Able to Answer follow-up Question Interactively [ . . s a m e c o d r e o t o a m t i i t o t n e = d. 45 . , . ] ha='right', fontsize=12)
i i m m p p o o r r t t p n a u n m d p a y s a a s s n p pd Certainly! Here are the mean squared error (MSE) and R^2 scores [...] Environment
f f # d # p # d # X y r r f r f " o o D C i R P = = h m m o = h n e = e t w e t m r d d s s t n p c ( o d f f f k k p l d k d v f o . [ l l s " o . f e . r d e e : m a r f . d m r a a / p d e o i r r o r r / g a r s o o t p n n h " a d n w p r ( . . u ] n _ m u s n a c m l g d c i l a i o o i g s s l w ( n l d n i l v s ( i ) - u e e n o ( i ) t t m l a g a n . h e n _ r f d g s s s s _ a u m t = e m c t v m i [ l o e h a ( s s " e d . e l ) s p m c e c u ) i l p t l o d e n i g i / a s g t " o d t i , n a a v m t s a " p i a e l c o m s t u a r p e e r t o t s r L s n t i / a n s m e c t e a i r " r k a ] R i i ) e t n g - _ r l t e e e s a s s r t i n _ U o / s s n a p e u l E t i P o t x - a a m n m p d g i / a n r s a e w L , / i a m b n a r i d a n r / P a y r u t o t o o c - e D m s p o s g w . D c n s a l v t o " a ) ad, f # m # r p p E r s 2 r r o C e C _ i i n m a _ a t n n l t l r t t v s c r c a ( ( i k u a u i " " r l l i l n M R e a n a e ^ o a t t = a 2 n r e = e n n r s m . M m R 2 s c S m e ^ _ q o E e a 2 s u r e t n c a e f r _ s o r n o i s c r e ( r c q o e d t t s u r ( r t a e y e a r r _ i r i a e f t r n m i d o r p o i n _ r a r n o i e i r g n r t n ( t g r r , t s o a r e m s r i m a t e e ( n o i ) a t y i d n : n _ n e i " _ , t g l n s r . g q r a s p u 2 i e r s a _ n t e e r t , d t e r i ) d a m c : _ i o t " e n d ( , r ) e X r l _ m o . t r s p r e r a _ e i t d n r i ) a c ) i t n ( ) X_train)) < - A C - [ A t t F - e - . i t t - l - . > g r r - l . u i i - ] b I b r - 1 1 1 u n u e 0 2 7 9 - 1 t [ t - e e 1 - s f # p p p E E - i e l l l ] r r - z a P t t t , r r - e t l . . . o o b x x - u o l r r a t l 6 - r t i r i a 4 - e n : b ( c 0 - _ r e e f k x - n e R l e s 4 - 1 a g e ( a ( 8 0 - m r c t f 0 - r e e ' t u e I - o s s a r a n w - t s n e t p i - a = i g _ u u t - t o l n r t h - i m n e a e - o o . F m _ 1 - n d c s e e n - = e o e a s a A 4 - l e t t , m x 5 - . f ( u e e - , f f ) r c s s - e i e o , > - h a c g ' e - a t i o f f - = u e t ) , e - ' r n a r - e t a t t i - _ s n i u g - n c r h - a u k e t - m n ' _ _ - e ex T l n - s , p r a a - _ b e a m - i f e c c e - n o l t e s - n _ b s e , - t a = d - s c F - i k a k - z l e - e ( s y - = m e w 1 - o ) o 2 - s r ) - t d - - r a - e r - S c g - e e u - n m l - f t e - V - n - i c t - D s a - e u l - ' b l t - a i - u l l c - i g z a k - s _ - a f t l - o t ) a - i r b o e D n ls a ' ta
X # _ t T r r a a i i n n , a X _ r t e e g s r t e , s s y i _ o t n r a m i o n d , e l y _ t e s t = t r a i n _ t e s t _ s p l i t ( X t , e s y t , _size=0.2, random_state=42) M R e ^ a 2 n s c s o q r u e a r ( e t d r a e i r n r i o n r g ( s t e r t a ) i : n i 0 n . g 8 2 s 6 e 0 t 0 ) 1 : 5 7 1 8 0 6 . 7 9 1 7 0 9 6 2 7 55842373478 CodeActAgent
m m # o o d d P e e r l l e . d = f i i c L t t i ( n X M e _ P a t G r r R a f e i o g n r r , e t s y e s _ s i t t o r n a d ( i a ) n t ) a D U a s t e a S a c n ik d i T t- r L a e in a r R n e L g i r b e r s a s r i y o n to M S o p d li e t l CodeActAgent I t t h s e e b e a m r( s ) t f h u a n t c t t h io e n t i i c n k M _l a a t b p e lo ls t l a ib rg . u In m st e e n a t d i , s w n e o t c a a n v a u l s i e d t a h r e g u ti m ck e _ n p t a fo ra r ms() function
y # p _ r p E i r v n e a t d l ( u " = a M t e m e a o n d t e h s l e q . u p m a r o r e d e d e d i l c e t r ( r X o _ r t : e s " t , ) np.mean((y_test - y_pred) **2)) T w h h e ic m h e in a d n i s c q a u te a s r e [. d .. ] error for the training set is 10.979 and the R^2 score is 0.826, to r [ o . ta . t . e s t a h m e e x - c t o ic d k e s [ o .. m .] itted...]
print("R^2 score: ", r2_score(y_test, y_pred)) plt.bar(feature_names, coef)
Environment User p l t . t i c k _ p a r a m s ( a l x a i be s l = r ' o x t ' a , tion=45, ha='right', fontsize=12)
m [ p . g . . o m i t t e d f o r s 0 pace...] Can you visualize the regression coefficient? You may access them via [...same code omitted...]
car name 0 model.coef_ and their names via model.feature_names_in_
dtype: int64 [3 rounds of self-debugging omitted for space]
---------------------------------------------------------------------------
ValueError Traceback (most recent call last) CodeActAgent
/tmp/ipykernel_12/1372561217.py in ?() CodeActAgent
18 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2 [...] Certainly! Here is a visualization of the regression coefficients [...]
- . - . - . > [o 1 2 2 2 2 2 2 1 3 5 9 0 2 4 m i m m y t # # o o _ t d d p e T P e e r d r r l l e a e . d i d f = f n i o i = c r L t a t i ( m s n X o r M p e _ d e P a a t e g G c r r l r e R a . e f ] e i p s o . g n r s r . r , e i . e d o t s y i n e s _ c s i t t m t o r ( o n a X d d ( i _ e a ) n t l t ) e a st) Au S t e o lf m -D at e e b d u F g e f e r d o b m ac k i # c # f # p p m o e l l p G e G a P t t o e f e t l . . b x r t t u o a l t = r t r a r n e b ( e m a _ r m e f g o m n e a l e r d e a g t ( a e e s m r p t s l e e ' l u I s . o s s o r n i c f s t e p o o = i l _ u n e i o ib n t f n m n . a c _ p o p F m o u d c y e e e t e o p a s f l e l t , f f . f o u i e f f t r c c a e i e o i t a c ' e a e u t i f n r u e s ) ) t e r n s s e t p _ s l n t ames_in_ Use D M a a t t a p V lo is tl u ib al L iz i a b t r i a o r n y for I v x b a - a a l r p t [ p i i d o c c . l h l k . t f o a u s . . g r n a x s i t z c n t a w t e d i m i i o f c e t r o n h k o r s c t i t t a n ( o h h t f d r e M e e e e o x t c a a t h - o t t o a e t p n u m t i m l c f r i i o u k e t o t b s s l _ t n i y i r o b n e = o 4 n . a d 4 t 5 I . m 5 . a n I d t e , . t s e e s . t s d e g , h ] e a r b e a e d m y f = e , e ' 4 s s w a r 5 f t e t i o h d u g r c a e r h a b t g n e t e t r ' _ h t e u t n , e e s e a s e s r : m f e r t e o t h e _ s n a e , t d x x s t a t i i b i c c i z k l k e i s s t ( = y ( ) 1 ) . f 2 H f u u ) e n n r c c e t t i i i o s o n n t h i t s e o n u s o p e t d t a a t h te e d
ValueError: could not convert string to float: '?' p p l l t t . . y t l i a t b l e e l ( ( 'R ' e R g e r g e r s e s s i s o i n o n C o C e o f e f f i f c i i c e i n e t n s t ' ') ) [...same code omitted...]
# Display the plot
CodeActAgent plt.show() Environment
It seems that there is a data type issue in the dataset. The '?' character is present Environment <Figure size 640x480 with1 Axes>
in the data, which is causing the error when trying to convert the data to a float. <Figure size 640x480 with1 Axes>
To fix this, I will remove the rows containing the '?' character.
# Remove rows containing '?'
df = df.replace('?', np.nan)
df = df.dropna()
X = df.drop(columns=["mpg", "car name"])
y = df["mpg"]
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42
) model = LinearRegression() CodeActAgent
m y o _ d p e r l e . d f i = t ( m X o _ d t e r l a . i p n r , e d y i _ c t t r ( a X i _ n t ) est) The regression coefficients are plotted as a bar chart, with each input feature on User
p p r r i i n n t t ( ( " " M R e ^ a 2 n s s c q o u r a e r : e d ", e r r 2 r _ o s r c : o r " e , ( y n _ p t . e m s e t a , n ( y ( _ y p _ r t e e d s ) t ) - y_pred) **2)) the x-axis and the corresponding coefficient on the y-axis [...] [Stops Interaction]
Figure3: Examplemulti-turninteractionwithPythonpackagesusingCodeActAgent(Mistral-7b). Noin-contextdemonstra-
tionsareprovidedtothemodel. Somemessagesareomittedforspace. Seehttps://chat.xwang.dev/r/Vqn108G
forcompleteinteraction.
domainstogeneratetrajectories: dastablestoperformdataoperations(e.g.,select,filter).
Examplesofinstructionscanbefoundin§G.3.1.
• InformationSeeking: WeuseatrainingsubsetofHot-
• Robot Planning: We use ALFWorld (Shridhar et al.,
potQA(Yangetal.,2018)togenerateinformation-seeking
2020), a text-only embodied environment simulator, to
trajectories,whereLLMsusethewikipedia search
generatetrajectoriesthatuserobot-controlAPIs(repur-
API(providedasaPythonfunction)tosearchforinfor-
posedasPythonfunction)tocompletehouseholdtasks.
mationtoanswerquestions.
Following MINT (Wang et al., 2023e), we provide an
• Software Package (Tool) Usage: We use the training
in-contextdemonstrationtoencouragetheuseoffor-loop
set of code generation problems in APPS (Hendrycks
and if-statement code blocks to automate repetitive op-
etal.,2021a)andmathproblemsinMATH(Hendrycks
erations (e.g., searching for items by visiting different
etal.,2021b). Thecodegenerationtasksalreadyinvolve
locations).
importingpackagesand/orcreatingnewtoolsbydefining
a new Python function. For MATH, we provide an in- DataDown-sampling. Wedown-sampleeachdatasetby
contextdemonstrationofimportingPythonpackages(e.g., keepingonlythemostchallenginginstances,aimingtomake
sympyforsymbolicmath)forproblem-solving. trajectorygenerationmoreefficientandcost-effective. Fur-
• ExternalMemory: Werepurposethetrainingsubsetof thermore,italsohelpsremovesimpleinstancesthatexisting
WikiTableQuestion(Pasupat&Liang,2015)andtweak LLMscanalreadysolve.Thestatisticsofthefiltereddataset
itintotwovariantsoftabularreasoningtasksthatrequire canbefoundinTab.A.9. Pleasereferto§G.1fordetails
accessingexternalmemory: (1)SQL-based,requiringthe aboutthedown-sampleprocess.
LLM to interact with an SQL database through sqlite3
Repurpose Data for Multi-turn Interaction. Some
packagetoanswerthequestionviaSQLexecution; (2)
datasets(APPS,MATH,WikiTableQuestions)areinitially
Pandas-based,requiringthemodeltointeractwithpan-
single-turnproblemsthatexpectonesolutionperinstruc-

ExecutableCodeActionsElicitBetterLLMAgents
Table4: Statisticsofourtrainingmixtureandcomparisonwithpriorwork. Pleasereferto§3.1fordetailsaboutCodeActIn-
structandgeneralconversationdata. TokenstatisticsarecomputedusingLlama-2tokenizer.
DataMixture DataType DataName #ofDataInstances #ofTotalTokens Avg.TokensPerInstance
- FireAct(Chenetal.,2023a) 2,063 542,176 262.81
PriorWork
- AgentInstruct(Zengetal.,2023) 1,866 2,517,785 1349.30
InformationSeeking HotpotQA(Yangetal.,2018) 1,664 2,472,227 1485.71
SoftwarePackages(Tool) MATH(Math,(Hendrycksetal.,2021b)) 1,732 1,719,467 992.76
SoftwarePackages(Tool) APPS(Code,(Hendrycksetal.,2021a)) 647 1,235,472 1909.54
CodeActInstruct(Ours)
ExternalMemory WikiTableQuestion(Pasupat&Liang,2015) 1,065 1,316,246 1235.91
RobotPlanning ALFWorld(Shridharetal.,2020) 2,031 3,838,269 1889.84
Total 7,139 10,581,681 1482.24
Single-TurnReasoning OpenOrca(Sub-sampled,(Lianetal.,2023)) 50,000 14,034,152 280.68
Multi-TurnConversations ShareGPT(Sub-sampled,(Anonymous,2023)) 10,000 17,933,861 1793.39
GeneralConversation Multi-TurnConversations ShareGPT(GPT-4,(OpenChat,2023)) 4,583 18,195,878 3970.30
Multi-turnReasoning CapyBara(LDJnr,2023) 4,647 4,982,435 1072.18
Total 69,230 55,146,326 796.57
tion,whereas,inarealisticagentusecase,weoftenrequire paredwithpriorworkAgentInstruct(Zengetal.,2023)and
multi-turn interaction to complete each task (Fig. 1 top). FireAct (Chen et al., 2023a) that mainly focus using text
FollowingMINT(Wangetal.,2023e),werepurposesingle- asaction,CodeActInstructresultsinmodelsthataremore
turn problems into multi-turn ones by allowing LLM to practicalinreal-worldimplementation,assuchmodelsus-
interact with the environment for multiple turns before it ingCodeActcandirectlyinteractwithPythoninterpreters
decidestosubmitonesolutionforevaluation. Specifically andopen-sourcetoolkits(Fig.3),reducingthedevelopment
forcodegenerationproblems,weprovideanin-contextex- effortforactionparsingandtoolcreations. CodeActInstruct
ampletoguideLLMstotesttheirsolutiononprovidedtest is systematically constructed following the general agent
casesbeforetheysubmitthesolution. Metricsfromtheorig- framework(Fig.2). Itcoversdiversedomains(e.g.,com-
inaldatawillevaluatethesubmittedsolutiontodetermine pared to FireAct that only considers QA-task and search
itscorrectness. Weincludeexamplesin§G.3. API),containsqualitydata(e.g.,promotesagent’scapability
ofself-debug)andoflargersize(3.8x/3.5xmoredatatrajec-
TrajectoryGeneration. WeuseMINT’sevaluationframe-
toriesand5x/19xmoretokenscomparedtoAgentInstruct
work(Wangetal.,2023e)togenerateinteractiontrajectories
/FireActrespectivelyinTab.4). Asweempiricallyshow
fortheaforementioneddatasetsanddeterminethecorrect-
in Tab. 5, the resulting model (same backbone) of Code-
ness of each trajectory. We run gpt-3.5-turbo-0613 from
ActInstructachieves24%and119%relativeimprovement
OpenAI,claude-1-instantandclaude-2fromAnthropicon
comparedtoAgentInstructandFireAct.
down-sampleddata,exceptcodegeneration,whichweusea
longer-contextversionofGPT-3.5(gpt-3.5-turbo-0613-16k) CodeActInstruct Can Be Used With Existing Agent-
duetothelong-contextrequirementoftheself-debugging User Conversation Data. We use a sub-sampled set
process. Onasubsetofproblemsthatnoneofthesemodels ofOpenOrca(Lianetal.,2023)thatfocusesonsingle-turn
cansolve,weusegpt-4-0613togeneratetrajectories. chain-of-thought(CoT)reasoning,ShareGPT(Anonymous,
2023;OpenChat,2023)fromtwosourcesthatcontainmulti-
EnhancingAgent’sCapabilitiesofImprovingfromInter-
turnconversationsbetweenhumanandLLM,andCapyBara
action. Weselectahigh-qualitysubsetofallthegenerated
(LDJnr,2023)thatfocusesonreasoninginmulti-turncon-
trajectories from CodeActInstruct to promote the agent’s
versations. Statistics and down-sampling details can be
abilitytoimprovethenextactionbasedonpriorobserva-
foundinTab.4and§C.
tions(e.g.,self-debuggingfromcodeexecutionerrormes-
sage,aplanningcapabilityinFig.2). Toachievethis,we
3.2.CodeActAgent
selectively preserve those trajectories wherein the model
initiallyencounterserrorsbutrectifiestheseinaccuraciesin Wefine-tuneLlama-27B(Touvronetal.,2023)andMistral
laterinteractions. Fortheseinstances, theLLMtypically 7B(Jiangetal.,2023)onamixtureofCodeActInstructand
engagesinself-reflectionfollowingtheinitialerror,thereby generalconversations(Tab.4)toobtainCodeActAgent.
proactivelyenhancingitsfutureactions. Otherfilteringde-
TrainingSetup.Weperformfull-parametersupervisedfine-
tails are discussed in §G.2. On all trajectories generated,
tuningwithasequencelengthof4,096tokensforLlama-2
wekeep411trajectoriesfromgpt-4-0613and6728trajecto-
and16,384forMistral. Pleasereferto§Dformoredetails.
riesfromgpt-3.5andclaude. Thestatisticsoftheresulting
datasetCodeActInstructareshowninTab.4. Evaluation Setup. We use MINT (Wang et al., 2023e)
to evaluate LLMs with CodeAct on a diverse range of
Comparing CodeActInstruct with Prior Work. Com-
agent tasks. CodeActAgent has some training domains

ExecutableCodeActionsElicitBetterLLMAgents
Table5:EvaluationresultsforCodeActAgent.Thebestresultsamongallopen-sourceLLMsarebolded,andthesecond-best
resultsareunderlined. IDandODstandforin-domainandout-of-domainevaluationcorrespondingly. Overallaveraged
performance normalizes the MT-Bench score to be consistent with other tasks and excludes in-domain tasks for fair
comparison.
AgentTasks GenericTasks Overall
CodeasAction TextasAction(OD) (OD) Average
Model Size MINT(ID) MINT(OD) M3ToolEval(OD) Miniwob++ SciWorld MMLU HumanEval GSM8K MTBench
Open-sourceLLMs(LLaMA-2-based)
Llama2Base 7B -∗ -∗ -∗ -∗ -∗ 45.3 12.8 14.6 -∗ -∗
Llama2Chat 7B 3.2 11.0 0.0 0.0 5.9 48.0 13.9 27.7 6.3 21.1
FireAct(Chenetal.,2023a) 7B 0.0 0.3 0.0 0.0 6.8 44.1 3.5 12.4 4.5 14.0
AgentLM(Zengetal.,2023) 7B 8.7 6.1 0.0 28.9 13.7 48.7 15.4 24.6 6.1 24.8
CodeActAgent(LLaMA-2) 7B 51.3 20.4 0.0 25.5 17.6 50.6 18.1 38.3 7.5 30.7
Open-sourceLLMs(Mistral-based)
MistralBase 7B -∗ -∗ -∗ -∗ -∗ 60.1 30.5 52.1 -∗ -∗
MistralInstruct 7B 18.8 9.7 0.0 0.5 4.0 53.8 29.3 43.3 6.4 25.6
CodeActAgent(Mistral) 7B 57.4 32.4 12.2 46.2 15.9 59.1 34.7 58.0 8.2 42.5
Closed-sourceLLMs
gpt-3.5-turbo-0613 - 33.9 38.2 51.2 66.7 21.2 70.0 48.1 57.1 7.9 54.0
gpt-4-0613 - 68.6 70.2 67.1 69.4 36.4 86.4 67.0 87.1 9.0 71.7
*Someresultsareonlyavailablewithinstruction-tunedmodels.
overlappingwithMINT’sevaluation(i.e.,MINTincludes AblationStudy. Tab.A.8presentsablationexperimentsto
ALFWorldandMATH),hencewereportseparatenumbers determinetheimportanceofCodeActInstructandgeneral
for MINT’s in- and out-of-domain performance. Unless conversations. BothCodeActInstructandgeneralconversa-
otherwisespecified,wemeasureMINTtasks’successrates tionscontributetoagenttasks,whilegeneralconversations
withinteractionturnk =5.Wealsoevaluateout-of-domain areessentialtomaintainperformanceongeneraltasks.
agenttasksusingtextactionsfromMiniWob++(computer
tasks, (Kim et al., 2023)) and ScienceWorld (text-based
4.RelatedWork
simulatorforelementarysciencecurriculum,(Wangetal.,
2022a)) to test whether CodeActAgent can generalize to 4.1.ActionModuleinLLMAgents
different action formats. Finally, we include a suite of
Asdetailedin(Wangetal.,2023b),LLM-basedautonomous
general LLM evaluation tasks to assess general capabil-
agentsaretypicallystructuredaroundfourcomponents:cus-
ity: MMLU(Hendrycksetal.,2020)forknowledge-based
tomizedprofiles(Parketal.,2023;Qianetal.,2023),long-
QA,HumanEval(Chenetal.,2021)forsingle-turncode-
termmemorycapabilities(Zhuetal.,2023;Fischer,2023),
generation, GSM8K (Cobbe et al., 2021) for single-turn
reasoningandplanningalgorithms(Weietal.,2022;Chen
tool-freemathreasoning,andMTBench(Zhengetal.,2023)
et al., 2023d), and, most crucially, action modules. The
forinstruction-following.
actionmodulesarekeytofacilitatingLLMagentstoeffec-
CodeActAgent Excels in CodeAct Task. As shown in tivelyinteractwithexternalentities,includinghumans(Lee
Tab.5,CodeActAgent(bothvariants)performbetterthan et al., 2022) and tools (Qin et al., 2023a) in the environ-
allevaluatedopen-sourceLLMsonboththein-andout-of- ment(Wangetal.,2023e;Yangetal.,2024a). Inthisstudy,
domainsubsetsofMINT.OnM3ToolEval,wefindCodeAc- weaddressthecriticalproblemofstandardizingtheaction
tAgent(Mistral)outperformsopen-sourceLLMsofsimilar space for LLM agents. We further discuss the difference
size(7Band13B)andevenreachessimilarperformanceto betweenCodeActandthelineofworkthatusescodegen-
those70Bmodels(Tab.3). Surprisingly,noimprovement erationforproblem-solvingin§A.Wenoticeaconcurrent
isobservedfortheLlama-2variant. Wediscusspotential studyTaskWeaver(Qiaoetal.,2023)similarlyendorsesthe
reasonsin§H. useofcode. Wediscusstheprincipaldistinctionsin§B.
CodeActAgent Generalizes to Text Action. When
4.2.ImprovingLLMAgents
evaluated on out-of-domain text actions, CodeActAgent
(LLaMA2, 7B), which has never been optimized for text TwoprimarymethodsforenhancingLLMagentsareprompt
action,achievescomparableperformancetoAgentLM-7B engineeringandinstructiontuning,assurveyedby(Wang
(Zengetal.,2023)whichhasexplicittuningfortextactions. etal.,2023b). Forpromptengineering(Liuetal.,2023a),
numerousstrategieshavebeenintroducedtoimprovethe
CodeActAgentMaintainsorImprovesthePerformance
chain-of-thought reasoning (Wei et al., 2022), including
onGeneralLLMTasks. InTab.5,wefindthatCodeActA-
self-consistency-basedreasoning(Wangetal.,2022b;Chen
gent(bothvariants)performsbetterongenericLLMtasks
etal.,2023d)andtree-basedapproaches(Yaoetal.,2023a).
we tested, except for a slight degradation on MMLU for
Moreover,LLMscanbestrategicallypromptedtoreflecton
CodeActAgent(Mistral,7B).

ExecutableCodeActionsElicitBetterLLMAgents
previousplans(Yaoetal.,2023b;Wangetal.,2023f;Zhang this section, we discuss potential societal consequences,
etal.,2023),enablingthemtorefineinitialactionsthrough limitations,andfutureworkrelatedtoourworkanditsgoal.
trialanderror. Contrasttopromptengineering,instruction
CodeActAgent is an initial prototype of an autonomous
tuning intrinsically enhances LLMs (Chung et al., 2022),
agentandstillhasseveralpracticallimitations.Forexample,
particularly in their agent capabilities (Zeng et al., 2023;
itmaysufferfromhallucinationcommonlyseeninLLMs
Chen et al., 2023a). For effective training, human anno-
(e.g.,imaginethecontentofavariablewithoutactuallyprint-
tatorscancurateexpertdemonstrationsforspecificagent
ingitout), suggestingtheneedforsubsequentalignment
tasks, such as web browsing (Yao et al., 2022a; Nakano
(Ouyangetal.,2022)forfurtherimprovements.
etal.,2021). Tominimizehumanannotationefforts,prior
workcreatessyntheticdatasetsusingstrongerLLMstodis- Despite being a prototype, CodeActAgent has already
till agent capabilities into local models, focusing on tool demonstratedlimitedself-improvingcapability(e.g.,self-
usage(Qinetal.,2023b),interaction(Chenetal.,2023c), debugerrormessagestoimproveitsaction)andtheability
andsocialskills(Liuetal.,2023b). CodeActInstructaligns tointeractwithenvironments. Futureworkmaybuildupon
withthelatterapproachandcreatesdatasetsusingstronger CodeActAgent to develop better agents by having them
LLMs. performextensiveinteractionswithinagivenenvironment
anditerativelybootstraptheirself-improvingcapabilityto
learntoimprovefrompastmistakes. Morepowerfulagents,
5.Conclusions
asresultsofsuchalgorithms,arepotentiallybeneficialfor
This work introduces CodeAct that employs executable solving a wide range of real-world problems (e.g., theo-
PythoncodefortheLLMagent’saction,whichisadvanta- remproving,drugdiscovery). Asextensivelydiscussedin
geousoverusingtextorJSONaction,especiallyincomplex (Eloundouetal.,2023),afullyautonomousagentmaytrans-
scenarios. WecollectCodeAct-focusedmulti-turninterac- formthecurrentlandscapeofthelabormarketandimpact
tiontrajectoriesCodeActInstructforinstructiontuning,and thejobsofexistingworkers.
trainCodeActAgentthatisspeciallydesignedforseamless
Furthermore,sinceCodeActdirectlygrantsaccessforthe
integrationwithPythonandcanexecutesophisticatedtasks
agenttofreelyexecutecodeinasandboxenvironment,in
(e.g.,modeltraining)leveragingexistingPythonpackages
theworstscenario(e.g., inSci-Fimovies), suchanagent
andautonomouslyrectifyingerrorsthroughself-debugging.
may potentiallybreak free ofthe sandbox restrictionand
causeharmtotheworldthroughcyber-attack,highlighting
Acknowledgement theneedforfutureworktodesignbettersafetymechanism
tosafeguardautonomousagents(Tangetal.,2024).
We thank the anonymous reviewers for their suggestions
andcomments. Thisresearchisbaseduponworksupported
## References
by U.S. DARPA ECOLE Program No. HR00112390060
andU.S.DARPAITMProgramNo. FA8650-23-C-7316
Ahn,M.,Brohan,A.,Brown,N.,Chebotar,Y.,Cortes,O.,
andKAIROSProgramNo. FA8750-19-2-1004. Theviews
David,B.,Finn,C.,Fu,C.,Gopalakrishnan,K.,Hausman,
andconclusionscontainedhereinarethoseoftheauthors
K., Herzog, A., Ho, D., Hsu, J., Ibarz, J., Ichter, B.,
andshouldnotbeinterpretedasnecessarilyrepresentingthe
Irpan,A.,Jang,E.,Ruano,R.J.,Jeffrey,K.,Jesmonth,
officialpolicies,eitherexpressedorimplied,ofDARPA,or
S.,Joshi,N.,Julian,R.,Kalashnikov,D.,Kuang,Y.,Lee,
theU.S.Government.TheU.S.Governmentisauthorizedto
K.-H., Levine, S., Lu, Y., Luu, L., Parada, C., Pastor,
reproduceanddistributereprintsforgovernmentalpurposes
P., Quiambao, J., Rao, K., Rettinghouse, J., Reyes, D.,
notwithstanding any copyright annotation therein. This
Sermanet,P.,Sievers,N.,Tan,C.,Toshev,A.,Vanhoucke,
workusedtheDeltasystemattheNationalCenterforSuper-
V.,Xia,F.,Xiao,T.,Xu,P.,Xu,S.,Yan,M.,andZeng,
computingApplicationsthroughallocationCIS230256from
A. Doasicanandnotasisay: Groundinglanguagein
theAdvancedCyberinfrastructureCoordinationEcosystem:
roboticaffordances. InarXivpreprintarXiv:2204.01691,
Services&Support(ACCESS,Boerneretal.2023)program,
2022.
whichissupportedbyNationalScienceFoundationgrants
#2138259,#2138286,#2138307,#2137603,and#2138296.
Anonymous. Sharegpt dataset. https://hf.co/
ImpactStatement datasets/anon8231489123/ShareGPT_
Vicuna_unfiltered/blob/main/ShareGPT_
ThispaperpresentsworkwhosegoalistoadvanceLLM-
V3_unfiltered_cleaned_split_no_
based autonomous agents that can communicate with hu-
imsorry.json, 2023. A dataset containing
mansthroughnaturallanguageandassisthumanusersby
multi-turn conversations between human and LLM
performingtasksinenvironmentsonbehalfofhumans. In
assistant.

ExecutableCodeActionsElicitBetterLLMAgents
Boerner, T. J., Deems, S., Furlani, T. R., Knuth, S. L., Fischer,K.A. Reflectivelinguisticprogramming(rlp): A
andTowns,J. Access: Advancinginnovation: Nsf’sad- stepping stone in socially-aware agi (socialagi). arXiv
vancedcyberinfrastructurecoordinationecosystem: Ser- preprintarXiv:2305.12647,2023.
vices&support.InPracticeandExperienceinAdvanced
Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang,
ResearchComputing,pp.173–176.2023.
Y., Callan, J., and Neubig, G. Pal: Program-aided lan-
Bran,A.M.,Cox,S.,White,A.D.,andSchwaller,P. Chem- guagemodels. InInternationalConferenceonMachine
crow:Augmentinglarge-languagemodelswithchemistry Learning,pp.10764–10799.PMLR,2023.
tools. arXivpreprintarXiv:2304.05376,2023.
Hendrycks,D.,Burns,C.,Basart,S.,Zou,A.,Mazeika,M.,
Song,D.,andSteinhardt,J. Measuringmassivemultitask
Cano, A. H., Pagliardini, M., Ko¨pf, A., Matoba, K., Mo-
languageunderstanding. InInternationalConferenceon
htashami,A.,Wang,X.,Fan,O.S.,Marmet,A.,Bayazit,
LearningRepresentations,2020.
D.,Krawczuk,I.,Chen,Z.,Salvi,F.,Bosselut,A.,and
Jaggi, M. epfllm megatron-llm, 2023. URL https: Hendrycks,D.,Basart,S.,Kadavath,S.,Mazeika,M.,Arora,
//github.com/epfLLM/Megatron-LLM.
A., Guo, E., Burns, C., Puranik, S., He, H., Song, D.,
et al. Measuring coding challenge competence with
Chase, H. LangChain, October 2022. URL https://
apps. InThirty-fifthConferenceonNeuralInformation
github.com/langchain-ai/langchain.
Processing Systems Datasets and Benchmarks Track
(Round2),2021a.
Chen,B.,Shu,C.,Shareghi,E.,Collier,N.,Narasimhan,K.,
andYao,S. Fireact: Towardlanguageagentfine-tuning. Hendrycks, D., Burns, C., Kadavath, S., Arora, A.,
arXivpreprintarXiv:2310.05915,2023a. Basart, S., Tang, E., Song, D., and Steinhardt,
J. Measuring mathematical problem solving with
Chen,M.,Tworek,J.,Jun,H.,Yuan,Q.,Pinto,H.P.d.O.,
the math dataset. In Thirty-fifth Conference on
Kaplan,J.,Edwards,H.,Burda,Y.,Joseph,N.,Brockman,
Neural Information Processing Systems Datasets and
G., etal. Evaluatinglargelanguagemodelstrainedon
BenchmarksTrack(Round2),2021b.
code. arXivpreprintarXiv:2107.03374,2021.
Hong,S.,Zheng,X.,Chen,J.,Cheng,Y.,Wang,J.,Zhang,
Chen, X., Lin, M., Scha¨rli, N., and Zhou, D. Teaching C., Wang, Z., Yau, S. K. S., Lin, Z., Zhou, L., et al.
large language models to self-debug. arXiv preprint Metagpt: Metaprogrammingformulti-agentcollabora-
arXiv:2304.05128,2023b. tiveframework. arXivpreprintarXiv:2308.00352,2023.
Chen,Y.,Sikka,K.,Cogswell,M.,Ji,H.,andDivakaran,A. Hong, S., Lin, Y., Liu, B., Liu, B., Wu, B., Li, D., Chen,
Dress: Instructinglargevision-languagemodelstoalign J.,Zhang,J.,Wang,J.,Zhang,L.,Zhang,L.,Yang,M.,
andinteractwithhumansvianaturallanguagefeedback. Zhuge,M.,Guo,T.,Zhou,T.,Tao,W.,Wang,W.,Tang,
arXivpreprintarXiv:2311.10081,2023c. X.,Lu,X.,Zheng,X.,Liang,X.,Fei,Y.,Cheng,Y.,Xu,
Z.,andWu,C. Datainterpreter: Anllmagentfordata
Chen, Y., Sikka, K., Cogswell, M., Ji, H., and Di- science,2024.
vakaran,A. Measuringandimprovingchain-of-thought
Huang,W.,Wang,C.,Zhang,R.,Li,Y.,Wu,J.,andFei-Fei,
reasoning in vision-language models. arXiv preprint
L. Voxposer: Composable 3d value maps for robotic
arXiv:2309.04461,2023d.
manipulation with language models. arXiv preprint
Chung, H. W., Hou, L., Longpre, S., Zoph, B., Tay, Y., arXiv:2307.05973,2023.
Fedus, W., Li, Y., Wang, X., Dehghani, M., Brahma,
Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C.,
S.,etal. Scalinginstruction-finetunedlanguagemodels.
Chaplot,D.S.,Casas,D.d.l.,Bressand,F.,Lengyel,G.,
arXivpreprintarXiv:2210.11416,2022.
Lample,G.,Saulnier,L.,etal. Mistral7b. arXivpreprint
arXiv:2310.06825,2023.
Cobbe,K.,Kosaraju,V.,Bavarian,M.,Chen,M.,Jun,H.,
Kaiser,L.,Plappert,M.,Tworek,J.,Hilton,J.,Nakano, Kim,G.,Baldi,P.,andMcAleer,S. Languagemodelscan
R.,etal. Trainingverifierstosolvemathwordproblems. solvecomputertasks. arXivpreprintarXiv:2303.17491,
arXivpreprintarXiv:2110.14168,2021. 2023.
Eloundou, T., Manning, S., Mishkin, P., and Rock, D. LDJnr. Capybara dataset. https://hf.co/
Gpts are gpts: An early look at the labor market im- datasets/LDJnr/Verified-Camel, https:
pactpotentialoflargelanguagemodels. arXivpreprint //hf.co/datasets/LDJnr/Pure-Dove,
arXiv:2303.10130,2023. https://hf.co/datasets/LDJnr/

ExecutableCodeActionsElicitBetterLLMAgents
LessWrong-Amplify-Instruct,2023. Adataset withhumanfeedback. AdvancesinNeuralInformation
focusingonreasoninginmulti-turnconversations. ProcessingSystems,35:27730–27744,2022.
Lee, M., Liang, P., and Yang, Q. Coauthor: Designing Park,J.S.,O’Brien,J.,Cai,C.J.,Morris,M.R.,Liang,P.,
a human-ai collaborative writing dataset for exploring andBernstein,M.S. Generativeagents: Interactivesim-
languagemodelcapabilities. InProceedingsofthe2022 ulacra of human behavior. In Proceedings of the 36th
CHIconferenceonhumanfactorsincomputingsystems, Annual ACM Symposium on User Interface Software
pp.1–19,2022. andTechnology,pp.1–22,2023.
Li,M.,Song,F.,Yu,B.,Yu,H.,Li,Z.,Huang,F.,andLi,Y. Pasupat,P.andLiang,P. Compositionalsemanticparsing
Api-bank: Abenchmarkfortool-augmentedllms,2023. on semi-structured tables. In Proceedings of the 53rd
Annual Meeting of the Association for Computational
Lian, W., Goodson, B., Pentland, E., Cook, A., Vong, C.,
Linguisticsandthe7thInternationalJointConferenceon
and ”Teknium”. Openorca: An open dataset of gpt
NaturalLanguageProcessing(Volume1: LongPapers),
augmented flan reasoning traces. https://https:
pp.1470–1480,2015.
//huggingface.co/Open-Orca/OpenOrca,
## 2023. Patil, S. G., Zhang, T., Wang, X., and Gonza-
lez, J. E. Gorilla: Large language model con-
Liang,J.,Huang,W.,Xia,F.,Xu,P.,Hausman,K.,Ichter,
nected with massive apis. ArXiv, abs/2305.15334,
B.,Florence,P.,andZeng,A.Codeaspolicies:Language
## 2023. URL https://api.semanticscholar.
modelprogramsforembodiedcontrol. InarXivpreprint
org/CorpusID:258865184.
arXiv:2209.07753,2022.
Qian, C., Cong, X., Yang, C., Chen, W., Su, Y., Xu, J.,
Liu,P.,Yuan,W.,Fu,J.,Jiang,Z.,Hayashi,H.,andNeubig,
Liu,Z.,andSun,M. Communicativeagentsforsoftware
G. Pre-train,prompt,andpredict: Asystematicsurveyof
development. arXivpreprintarXiv:2307.07924,2023.
promptingmethodsinnaturallanguageprocessing.ACM
ComputingSurveys,55(9):1–35,2023a.
Qiao, B., Li, L., Zhang, X., He, S., Kang, Y., Zhang,
C., Yang, F., Dong, H., Zhang, J., Wang, L., et al.
Liu,R.,Yang,R.,Jia,C.,Zhang,G.,Zhou,D.,Dai,A.M.,
Taskweaver: A code-first agent framework. arXiv
Yang,D.,andVosoughi,S. Trainingsociallyalignedlan-
preprintarXiv:2311.17541,2023.
guagemodelsinsimulatedhumansociety. arXivpreprint
arXiv:2305.16960,2023b.
Qin,Y.,Hu,S.,Lin,Y.,Chen,W.,Ding,N.,Cui,G.,Zeng,
Z.,Huang,Y.,Xiao,C.,Han,C.,etal. Toollearningwith
Ma,Y.J.,Liang,W.,Wang,G.,Huang,D.-A.,Bastani,O.,
foundation models. arXiv preprint arXiv:2304.08354,
Jayaraman, D., Zhu, Y., Fan, L., and Anandkumar, A.
2023a.
Eureka: Human-levelrewarddesignviacodinglargelan-
guagemodels. arXivpreprintarXiv:2310.12931,2023.
Qin,Y.,Liang,S.,Ye,Y.,Zhu,K.,Yan,L.,Lu,Y.-T.,Lin,
Mialon, G., Dess`ı, R., Lomeli, M., Nalmpantis, C., Pa- Y., Cong, X., Tang, X., Qian, B., Zhao, S., Tian, R.,
sunuru,R.,Raileanu,R.,Rozie`re,B.,Schick,T.,Dwivedi- Xie, R., Zhou, J., Gerstein, M. H., Li, D., Liu, Z., and
Yu,J.,Celikyilmaz,A.,etal. Augmentedlanguagemod- Sun,M. Toolllm: Facilitatinglargelanguagemodelsto
els: asurvey. arXivpreprintarXiv:2302.07842,2023. master16000+real-worldapis. ArXiv,abs/2307.16789,
2023b. URL https://api.semanticscholar.
Nakano,R.,Hilton,J.,Balaji,S.,Wu,J.,Ouyang,L.,Kim, org/CorpusID:260334759.
C.,Hesse,C.,Jain,S.,Kosaraju,V.,Saunders,W.,etal.
Webgpt: Browser-assistedquestion-answeringwithhu- Schick,T.,Dwivedi-Yu,J.,Dess`ı,R.,Raileanu,R.,Lomeli,
manfeedback. arXivpreprintarXiv:2112.09332,2021. M.,Zettlemoyer,L.,Cancedda,N.,andScialom,T. Tool-
former: Languagemodels canteach themselvesto use
OpenChat. Sharegpt dataset. https://hf.co/ tools. arXivpreprintarXiv:2302.04761,2023.
datasets/openchat/openchat_sharegpt_
v3/blob/main/sharegpt_gpt4.json,2023. A Shen,Y.,Song,K.,Tan,X.,Li,D.,Lu,W.,andZhuang,Y.
dataset containing multi-turn conversations between Hugginggpt: Solvingaitaskswithchatgptanditsfriends
humanandLLMassistants.Itisfilteredtocontaindata inhuggingface. arXivpreprintarXiv:2303.17580,2023.
onlyfromGPT-4.
Shridhar,M.,Yuan,X.,Cote,M.-A.,Bisk,Y.,Trischler,A.,
Ouyang,L.,Wu,J.,Jiang,X.,Almeida,D.,Wainwright,C., andHausknecht,M. Alfworld: Aligningtextandembod-
Mishkin,P.,Zhang,C.,Agarwal,S.,Slama,K.,Ray,A., iedenvironmentsforinteractivelearning.InInternational
et al. Training language models to follow instructions ConferenceonLearningRepresentations,2020.

ExecutableCodeActionsElicitBetterLLMAgents
Singh, I., Blukis, V., Mousavian, A., Goyal, A., Xu, D., ComputationalLinguistics(Volume1: LongPapers),pp.
Tremblay, J., Fox, D., Thomason, J., and Garg, A. 3640–3663, Toronto, Canada, July 2023c. Association
Progprompt: Generating situated robot task plans us- forComputationalLinguistics. doi: 10.18653/v1/2023.
inglargelanguagemodels. In2023IEEEInternational acl-long.202.URLhttps://aclanthology.org/
Conference on Robotics and Automation (ICRA), pp. 2023.acl-long.202.
11523–11530, 2023. doi: 10.1109/ICRA48891.2023.
Wang, X., Peng, H., Jabbarvand, R., and Ji, H. Leti:
10161317.
Learning to generate from textual interactions. ArXiv,
Sur´ıs,D.,Menon,S.,andVondrick,C. Vipergpt: Visualin- abs/2305.10314,2023d.
ferenceviapythonexecutionforreasoning. Proceedings
Wang,X.,Wang,Z.,Liu,J.,Chen,Y.,Yuan,L.,Peng,H.,
of IEEE International Conference on Computer Vision
and Ji, H. Mint: Evaluating llms in multi-turn interac-
(ICCV),2023.
tion with tools and language feedback. arXiv preprint
Tang,X.,Jin,Q.,Zhu,K.,Yuan,T.,Zhang,Y.,Zhou,W., arXiv:2309.10691,2023e.
Qu,M.,Zhao,Y.,Tang,J.,Zhang,Z.,etal. Prioritizing
Wang,Z.,Cai,S.,Liu,A.,Ma,X.,andLiang,Y. Describe,
safeguarding over autonomy: Risks of llm agents for
explain,planandselect: Interactiveplanningwithlarge
science. arXivpreprintarXiv:2402.04247,2024.
languagemodelsenablesopen-worldmulti-taskagents.
TIOBE Index. Tiobe index. https://www.tiobe. arXivpreprintarXiv:2302.01560,2023f.
com/tiobe-index/, Accessed at Jan 23rd, 2024,
Wei, J., Wang, X., Schuurmans, D., Bosma, M., Xia, F.,
## 2024. The TIOBE Programming Community index is
Chi, E., Le, Q. V., Zhou, D., et al. Chain-of-thought
anindicatorofthepopularityofprogramminglanguages.
prompting elicits reasoning in large language models.
Theindexisupdatedonceamonth.Theratingsarebased
AdvancesinNeuralInformationProcessingSystems,35:
onthenumberofskilledengineersworld-wide,courses
24824–24837,2022.
andthirdpartyvendors.
Xu, Q., Hong, F., Li, B., Hu, C., Chen, Z., and Zhang, J.
Touvron,H.,Martin,L.,Stone,K.,Albert,P.,Almahairi,A.,
Onthetoolmanipulationcapabilityofopen-sourcelarge
Babaei,Y.,Bashlykov,N.,Batra,S.,Bhargava,P.,Bhos-
languagemodels,2023.
ale,S.,etal. Llama2: Openfoundationandfine-tuned
chatmodels. arXivpreprintarXiv:2307.09288,2023. Yang, J., Prabhakar, A., Narasimhan, K., andYao, S. In-
tercode: Standardizing and benchmarking interactive
Wang,G.,Xie,Y.,Jiang,Y.,Mandlekar,A.,Xiao,C.,Zhu,
coding with execution feedback. Advances in Neural
Y., Fan, L., and Anandkumar, A. Voyager: An open-
InformationProcessingSystems,36,2024a.
endedembodiedagentwithlargelanguagemodels.arXiv
preprintarXiv:2305.16291,2023a. Yang, K., Liu, J., Wu, J., Yang, C., Fung, Y. R., Li, S.,
Huang,Z.,Cao,X.,Wang,X.,Wang,Y.,Ji,H.,andZhai,
Wang,L.,Ma,C.,Feng,X.,Zhang,Z.,Yang,H.,Zhang,J., C. Ifllmisthewizard,thencodeisthewand: Asurvey
Chen,Z.,Tang,J.,Chen,X.,Lin,Y.,etal. Asurveyon onhowcodeempowerslargelanguagemodelstoserve
largelanguagemodelbasedautonomousagents. arXiv asintelligentagents,2024b.
preprintarXiv:2308.11432,2023b.
Yang,Z.,Qi,P.,Zhang,S.,Bengio,Y.,Cohen,W.,Salakhut-
Wang, R., Jansen, P. A., Coˆte´, M.-A., and Am- dinov, R., and Manning, C. D. Hotpotqa: A dataset
manabrolu, P. Scienceworld: Is your agent for diverse, explainable multi-hop question answering.
smarter than a 5th grader? In Conference on In Proceedings of the 2018 Conference on Empirical
Empirical Methods in Natural Language Processing, Methods in Natural Language Processing, pp. 2369–
2022a. URL https://api.semanticscholar. 2380,2018.
org/CorpusID:247451124.
Yang, Z., Liu, A., Liu, Z., Liu, K., Xiong, F., Wang, Y.,
Wang,X.,Wei,J.,Schuurmans,D.,Le,Q.,Chi,E.,Narang, Yang,Z.,Hu,Q.,Chen,X.,Zhang,Z.,Luo,F.,Guo,Z.,
S., Chowdhery, A., and Zhou, D. Self-consistency im- Li, P., andLiu, Y. Towardsunifiedalignmentbetween
proves chain of thought reasoning in language models. agents,humans,andenvironment,2024c.
arXivpreprintarXiv:2203.11171,2022b.
Yao, S., Chen, H., Yang, J., and Narasimhan, K.
Wang,X.,Li,S.,andJi,H. Code4Struct: Codegeneration Webshop: Towards scalable real-world web inter-
for few-shot event structure prediction. In Rogers, A., action with grounded language agents. Advances
Boyd-Graber, J., and Okazaki, N. (eds.), Proceedings in Neural Information Processing Systems, 35:20744–
of the 61st Annual Meeting of the Association for 20757,2022a.

ExecutableCodeActionsElicitBetterLLMAgents
Yao,S.,Zhao,J.,Yu,D.,Du,N.,Shafran,I.,Narasimhan,
K. R., and Cao, Y. React: Synergizing reasoning and
actinginlanguagemodels. InTheEleventhInternational
ConferenceonLearningRepresentations,2022b.
Yao,S.,Yu,D.,Zhao,J.,Shafran,I.,Griffiths,T.L.,Cao,Y.,
andNarasimhan,K. Treeofthoughts: Deliberateprob-
lemsolvingwithlargelanguagemodels. arXivpreprint
arXiv:2305.10601,2023a.
Yao,W.,Heinecke,S.,Niebles,J.C.,Liu,Z.,Feng,Y.,Xue,
L.,Murthy,R.,Chen,Z.,Zhang,J.,Arpit,D.,etal. Retro-
former: Retrospectivelargelanguageagentswithpolicy
gradientoptimization. arXivpreprintarXiv:2308.02151,
2023b.
Yuan,L.,Chen,Y.,Wang,X.,Fung,Y.R.,Peng,H.,and
Ji,H. Craft: Customizingllmsbycreatingandretriev-
ing from specialized toolsets. ArXiv, abs/2309.17428,
## 2023. URL https://api.semanticscholar.
org/CorpusID:263310662.
Zeng, A., Liu, M., Lu, R., Wang, B., Liu, X., Dong, Y.,
andTang, J. Agenttuning: Enablinggeneralizedagent
abilitiesforllms,2023.
Zhang, C., Liu, L., Wang, J., Wang, C., Sun, X.,
Wang, H., and Cai, M. Prefer: Prompt ensemble
learning via feedback-reflect-refine. arXiv preprint
arXiv:2308.12033,2023.
Zheng,L.,Chiang,W.-L.,Sheng,Y.,Zhuang,S.,Wu,Z.,
Zhuang,Y.,Lin,Z.,Li,Z.,Li,D.,Xing,E.,etal. Judging
llm-as-a-judgewithmt-benchandchatbotarena. arXiv
preprintarXiv:2306.05685,2023.
Zheng, T., Zhang, G., Shen, T., Liu, X., Lin, B. Y., Fu,
J., Chen, W., and Yue, X. Opencodeinterpreter: Inte-
gratingcodegenerationwithexecutionandrefinement.
https://arxiv.org/abs/2402.14658,2024.
Zhu, X., Chen, Y., Tian, H., Tao, C., Su, W., Yang, C.,
Huang,G.,Li,B.,Lu,L.,Wang,X.,etal. Ghostinthe
minecraft: Generallycapableagentsforopen-worldenvi-
romentsvialargelanguagemodelswithtext-basedknowl-
edge and memory. arXiv preprint arXiv:2305.17144,
2023.

ExecutableCodeActionsElicitBetterLLMAgents
TableA.6: Exampleofactionsforre-purposedAPI-Bank(Lietal.,2023)andM3ToolEval.
Format Action
AddAgenda(content="Meeting with John",
CodeAct
time="2023-10-26 09:00:00")
{"action": "AddAgenda", "content":
JSON "Meeting with John", "time":
"2023-10-26 09:00:00"}
Action: AddAgenda, content: Meeting
Text
with John, time: 2023-10-26 09:00:00
TableA.7: ComparisonbetweenM3ToolEvalandexistingtool-useevaluationbenchmark.
Benchmark M3ToolEval ToolBench APIBench API-Bank ToolBench
(Thiswork) (Qinetal.,2023b) (Patiletal.,2023) (Lietal.,2023) (Xuetal.,2023)
Requiringmulti-turninteraction (cid:34) (cid:34) (cid:37) (cid:37) (cid:37)
Multipletools (cid:34) (cid:34) (cid:34) (cid:34) (cid:34)
Evaluation AnswerMatch LLMEvaluator ASTTreeMatch API-CallMatch TestCase
NodependencyonexternalAPI∗ (cid:34) (cid:37) (cid:37) (cid:34) (cid:37)
SupportedAPIActionFormat CodeAct&JSON&Text JSON CodeAct JSON CodeAct
*WhethertorelyonexternalAPI(e.g.,RapidAPI,GoogleSheet)hostedbyathirdparty.Theavailabilityofsuchthird-partyAPIscangreatlyimpact
evaluationresults(e.g.,lowAPI-callingperformancenotbecausethemodelisbadbutratherbecausetheAPIrequiredisnotaccessible).
TableA.8: Ablationstudyresults. Thebestresultsarebolded,andthesecond-bestresultsareunderlined. IDandODstand
forin-domainandout-of-domainevaluationcorrespondingly. OverallaveragedperformancenormalizestheMT-Bench
scoretobeconsistentwithothertasksandexcludesin-domaintasksforfaircomparison.
AgentTasks GenericLLMTasks Overall
CodeasAction TextasAction(OD) (OD) Average
Model Size MINT(ID) MINT(OD) Miniwob++ SciWorld MMLU HumanEval GSM8K MTBench
CodeActAgent(Llama2-based) 7B 51.3 20.4 25.5 17.6 50.6 18.1 38.3 7.5 35.1
w/oCodeAct 7B 17.0 15.5 36.4 16.9 49.5 14.7 36.0 7.2 34.5
w/ogeneralconversations 7B 29.2 15.9 0.0 17.1 46.4 19.7 20.6 4.1 22.9
CodeActAgent(Mistral-based) 7B 57.4 32.4 46.2 15.9 59.1 34.7 58.0 8.2 46.8
w/oCodeAct 7B 32.9 23.0 47.8 17.0 59.9 33.2 59.5 8.3 46.2
w/ogeneralconversations 7B 50.5 13.9 0.0 11.0 52.4 27.9 26.8 2.6 22.6
A.ComparisonwithWorkthatUsesCodeGenerationforProblem-solving
Inthissection,wediscussthefundamentaldifferencesbetweenCodeActandpriorworkthatpromptLLMtogenerate
codeforproblem-solving. Existingworkhaveexploredusingcodegenerationfortask-solvingindifferentdomains,for
example,Code4Struct(Wangetal.,2023c)forstructuredprediction,PaL(Gaoetal.,2023)formathreasoning,Meta-GPT
(Hongetal.,2023)formulti-agentcollaboration,code-as-policy(Liangetal.,2022)forrobotcontrol,ViperGPT(Sur´ıs
etal.,2023)forvisualquestionanswering,Voyager(Wangetal.,2023a)forplayinggames,DataInterpreter(Hongetal.,
2024)fordatasciencetasks,etc.
Mostpriorworkgeneratescode(i.e.,astaticsequenceofactions)inasingle-turnsettingandcannotdynamicallyreadjust
actiononnewobservation: Itisconsideredafailurewhenthemodel-generatedcodefailstosolveataskonthefirstattempt.
Thissettingoverlooksthepotentialofenvironmentalobservation(e.g.,codeexecutionresults)thatmightbenefitfuture
actionandoveralldecision(e.g.,dynamicallyadjustingsubsequentcodeafterobservingintermediatecodeexecutionresults,
fixingerroneouscodeafterseeinganerrormessage). Thatis,thegeneratedcodeisastaticsequenceofactionsthatcannot
bedynamicallyre-adjustedontheflybyincorporatingnewobservations. Suchasingle-turnsettingmakesitchallengingto
scaletomorechallengingproblemssinceevenexperthumanprogrammersusuallycannotwritefunctionallycorrectcodein

ExecutableCodeActionsElicitBetterLLMAgents
thefirstpass. Ontheotherhand,CodeActisamulti-turninteractionagentframeworkthatallowsdynamicadjustment
ofprioractionsoremittingnewactionsbydesign(§2.1,Fig.2)andiscompatiblewithanyformoftextualobservation
(e.g.,toolexecutionoutput,automatedfeedback)fromtheenvironment. Beyondbeingcompatiblewithenvironmental
observation,ourinstructiontuningdatasetCodeActInstructspecificallycollectsdataformulti-turnself-improving,offering
apracticalsolutiontoenhanceLLM’smulti-turnself-improvingprocess.
Inaddition,previousapproachesrequireheavypromptengineeringandcraftingoffew-shotdemonstrationstotailorLLMsto
aparticulardomainortask(e.g.,robotcontrol(Liangetal.,2022))sincethebackboneLLMsarenotspeciallyoptimizedfor
dynamicplanninganddecisionmaking. Incontrast,inthiswork,weproposetheCodeActframeworkthatusesexecutable
PythoncodetoconsolidateLLMagents’actionsintounifiedactionspaceandcollectCodeActInstructonadiversearrayof
tasks(e.g.,informationseeking,tabularreasoning,robotplanning,etc)tomakethetrainedmodel,CodeActAgent,easily
scaletodiversetasksanddomainswithminimalhumaneffortsasshownin§3.2.
One notable exception among prior work is Voyager (Wang et al., 2023a), which performs iterative prompting in a
constrainedactionspaceoffunctiondefinitionstofixcodeerrors. DifferentfromCodeAct,suchsettingdisallowsdynamic
re-adjustmentofatomicactionsonthefly: InCodeAct,foraparticulartask(e.g.,craftstoneswordinMinecraft),the
agentcanfirstexecuteonelineofcode(anyatomicactionorcomposedfunctions,e.g.,moveforward,locatestone),and
dynamicallyproducedifferentactionsbasedontheobservationofthefirstaction. ThisischallengingforVoyagertoachieve:
Similartocode-as-policy(Liangetal.,2022),theygenerateaction(askill,e.g.,craftstonesword)asaPythonfunction
definitionthatoutlinestheentireplanforatask(e.g.,multi-stepcodeoutlininghowyoushouldcraftastoneswordand
handlesfordifferentpotentialcases,whichrequiresstrongdomainknowledge). Thisimposessignificantconstraintsonthe
agent’sactionspaceanddisallowsdynamicre-adjustmentofatomicactionsonthefly: Thatis,theagentcanonlygenerate
onecompletefunctionfirst(e.g.,byimagingallpossiblecasesthatmighthappenwhenyoutrytolocatestones),execute
theentirefunction,observethefeedback,andupdatetheentirefunctionasactioninthesubsequentmove. Besidesthe
constrainedabilitytore-adjustactionfromenvironmentalobservation,theyalsorelyonheavypromptingengineering(a
typicaldrawbackdiscussedabove)toproviderelevantinformation(e.g.,currentstate,additionalself-criticsviaprompting)
togeneraterevisedcode,whereasCodeActissituatedinasettingthatrequiresnopromptengineeringefforts: thecontext
windowofLLMonlycontainsitspastactionsandobservationsanddoesnotrequirehumaneffortstofilterforrelevant
information.
SimilartoCodeAct,concurrentworkOpenCodeInterpreter(Zhengetal.,2024),withaspecificfocusoncompetitivecode
generationquestions,collectscode-debuggingtrajectoriestoimproveanLLM’siterativecodedebuggingperformance.
However,itsapplicabilitytogeneralLLMagenttasksremainsunknown.
B.ComparisonwithTaskWeaver
In the landscape of unifying the action space of LLM agents, our work represents a leap over the previous initiative,
TaskWeaver(Qiaoetal.,2023). WhileTaskWeaverdeservesacknowledgmentforinitiallyintegratingcodeintotheaction
spaceofLLMagents,itsexplorationremainslimited. Thiswork,primarilycharacterizedbyitsrelianceonalimitedset
ofqualitativeexampleswithclose-sourcedmodelsasthebackbones,failstoharnessthefullpotentialofthisintegration,
remainingmerelyconceptualdemonstrations. Ourworktranscendsmereconceptualizationbyconductinganextensiveand
rigorousanalysis,clearlyquantifyingthebenefitsofcodeactionwithinLLMagents. Beyondthis,weintroduceaunique
instruction-tuningdatasetCodeActInstructspecificallydesignedtoamplifytheagent’scapabilitiesinexecutingcode-based
actionsandanopen-sourceLLMagentCodeActAgent. ThesecontributionsnotonlyextendtheworkofTaskWeaverbut
alsopavethewayforfutureexplorations,offeringvaluableresourcestotheopen-sourcecommunityandredefiningthe
potentialofLLMagentsinpracticalapplications.
C.GeneralDataDown-sample
• ShareGPT (Anonymous, 2023): We remove all single-turn conversations, then perform random sub-sample to a
desiredfinalnumber.
• ShareGPT(GPT-4)(OpenChat,2023): Wedonotperformsub-samplingonthisdataset.
• OpenOrca(Lianetal.,2023): WeselecttheCoTsubsetofOpenOrca,thenperformarandomsub-sampletoadesired
finalnumber.

ExecutableCodeActionsElicitBetterLLMAgents
• CapyBara(LDJnr,2023): Wedonotperformsub-samplingonthisdataset.
D.CodeActAgentTrainingDetails
AllSFTexperimentsareperformedonone4xA10040GBSXMnodeusingaforkofMegatron-LLM(Canoetal.,2023)
withatrainingthroughputofaround9ktokenspersecond. WeusechatMLformat2 forallmulti-turndata,andweonly
calculateandoptimizeforlossontheassistantresponse. Wepackshortinstancesintolongeronesandapplyflashattention
fortrainingefficiency.
WetrainbothLLaMA-2andMistralLLMswithTensorParallelof4,thelearningrateof1e-5with50warmupstepsand
cosinedecay(endlearningrateof1e-6). Wetrainforfiveepochswithabatchsizeof32. Weusethe3rdepochcheckpoint
forallourexperiments.
E.ExamplePromptforCodeAct
Thisisanexample(zero-shot)systempromptusedinadeployinstanceofCodeActwhereweusedchatMLformat.
Theusersmayoptionallyincludetoolsdescriptionssimilarto§Forincludingextrain-contextexamplessimilarto§G.3.
<|im_start|>system
A chat between a curious user and an artificial intelligence assistant. The assistant
gives helpful, detailed, and polite answers to the user’s questions.
The assistant can interact with an interactive Python (Jupyter Notebook) environment and
receive the corresponding output when needed. The code should be enclosed using "<
execute>" tag, for example: <execute> print("Hello World!") </execute>.
The assistant should attempt fewer things at a time instead of putting too much code in
one <execute> block. The assistant can install packages through PIP by <execute> !pip
install [package needed] </execute> and should always import packages and define
variables before starting to use them.
The assistant should stop <execute> and provide an answer when they have already obtained
the answer from the execution result. Whenever possible, execute the code for the user
using <execute> instead of providing it.
The assistant’s response should be concise, but do express their thoughts.
<|im_end|>
F.M3ToolEvalPrompt
You have access to the following tools:
{{Tool Definition}}
{{Formatting Instruction}}
Now, let’s get started!
Instruction: {{Example: Find the current price of Legendary Wand.}}
Answer in the format of ’xx.xx’ (e.g., 12.34).
You can optionally express your thoughts using natural language before your action. For
example, ’Thought: I want to use tool_name to do something. Action: <your action to
call tool_name> End Action’.
Note that your output should always contain either ’Action:’ or ’Answer:’, but not both.
When you are done, output the result using ’Answer: your answer’
Please ONLY output the answer (e.g., single number), without any other text.
Each{{...}}componentabovewillbesubstitutedwithcorrespondinginformation.
F.1.Exampleof{{ToolDefinition}}
Thefollowingisanexampletooldefinitionforweb-browsing.
2https://github.com/openai/openai-python/blob/release-v0.28.0/chatml.md

ExecutableCodeActionsElicitBetterLLMAgents
[1] click_url: Clicks on a URL. A clickable URL looks like [Clickable ’<url_argument>’] in
the webpage.
Arguments: url (str).
Returns the rendered content of the webpage after clicking the URL showing on the current
rendered page.
Signature: click_url(url: str) -> str
[2] go_to_previous_page: Goes back to the previous page. It has no arguments.
After going back to the previous page, return the rendered content of the webpage.
Signature: go_to_previous_page() -> str
[3] scroll_down: Scrolls down the view. It has no arguments.
Returns the rendered content of the webpage after scrolling down.
Signature: scroll_down() -> str
[4] scroll_up: Scrolls up the view. It has no arguments.
Returns the rendered content of the webpage after scrolling up.
Signature: scroll_up() -> str
[5] view: Return the current view in string format of the rendered webpage. It has no
arguments.
Returns the rendered content of the webpage.
You should call this when you want to see the rendered content of the current webpage.
Signature: view() -> str
[6] calculator: Evaluates the given expression and returns the result. Accepts a
calculation expression as input. For example, "2 + (3 * 4)" will return 14.
Signature: calculator(expression: str) -> float
F.2.Exampleof{{FormattingInstruction}}
Differentactionformathasdifferentformattinginstructions.
F.3.FormattingInstructionforCodeasAction
You can use the tools by outputing a block of Python code that invoke the tools.
You may use for-loops, if-statements, and other Python constructs when necessary.
Be sure to print the final answer at the end of your code.
You should begin your tool invocation with ’Action:’ and end it with ’End Action’.
Example: ’Action:
tool_name(argument_1)
End Action’
F.4.FormattingInstructionforJsonasAction
You can use the tools by outputing a JSON object with the following fields:
- ’tool’: the name of the tool
- ’args’: a list of arguments to the tool
You should begin your tool invocation with ’Action:’ and end it with ’End Action’.
Example: ’Action: {"tool": "tool_name", "args": ["argument_1"]} End Action’
You can only invoke one tool at a time.
F.5.FormattingInstructionforTextasAction
You can use the tools by outputing the tool name followed by its arguments, delimited by
commas.
You should begin your tool invocation with ’Action:’ and end it with ’End Action’.
Example: ’Action: tool_name, argument_1 End Action’
You can only invoke one tool at a time.
G.CodeActInteractionData
G.1.DatasetDownsample
• CodegenerationtasksinAPPS(Hendrycksetal.,2021a): Weremoveinstanceswithoutanytestcaseavailable.

ExecutableCodeActionsElicitBetterLLMAgents
TableA.9: CodeActInstructcomponentsandthenumberofinstancesfortrainingtrajectorygeneration.
Domain Capability Dataset #ofInstances
WebSearch InformationseekingthroughsearchAPI HotpotQA(Yangetal.,2018) 3,000
MathReasoning Mathproblem-solvingusingmathLibrariesinPython(e.g.,sympy) MATH(Hendrycksetal.,2021a) 5,586
CodeGeneration Self-debugfromPythonerrormessagesandtraceback APPS(Hendrycksetal.,2021b) 4,439
TabularReasoning TabularReasoningusingpandasandsqlite3(forSQL)library WikiTableQuestion(Pasupat&Liang,2015) 3,000
EmbodiedPlanning InteractwithembodiedenvironmentsthroughAPIs ALFWorld(Shridharetal.,2020) 3,553
• Tabular reasoning tasks in WikiTableQuestion (Pasupat & Liang, 2015): We select a subset of 3000 instances
withthelargesttablesize(i.e.,sortbynumberofrowsandcolumns)fromtheoriginaldataset(14149instances),and
randomlyassign1500ofthemtobepandas-basedproblems,andtherest1500tobeSQL-basedproblems.
• WebsearchtasksinHotpotQA(Yangetal.,2018): Weselectthe15661problemslabeledas“hard”intheoriginal
dataset(with90447instances),thenrandomlydown-samplethemto3000problems.
• MathreasoninginMATH(Hendrycksetal.,2021b): Weremoveproblemswiththeannotateddifficultylowerthan3,
whichresultsin5586instancesasshowninTab.A.9.
• EmbodiedPlanninginALFWorld(Shridharetal.,2020): Wedidnotperformdown-samplingforAlfWorld.
G.2.DataSelectionHeuristic
Givensuccessfultask-solvingtrajectoriesthathavemorethan2turns,weapplythefollowingheuristictoselectinstances
thatcanpromotethecode-as-actions,self-improvement,andinstruction-followingcapabilitiesofLLMagents:
• Code-as-Actions: WeexcludetrajectorieswhereinLLMagentsdonotadheretothecode-as-actionsframework,either
duetoincorrectAPIinvocationorthegenerationofactionsinformatsunsuitableforparsingandexecution.
• Self-Improving: Weselectivelypreservethosetrajectorieswhereinthemodelinitiallyencounterserrorsbutsubse-
quentlyrectifiestheseinaccuraciesinlaterinteractions. Inaddition,weeliminatesuccessfultrajectoriesthatexclusively
yielderrorsinallcodeexecutions. Thesearedeemedineffectivedemonstrations,asourobjectiveistopreventthe
modelfromlearningtoconsistentlyexecuteerroneouscodewhilestillmanagingtoprovidecorrectanswers.
• Instruction-Following: WeremoverarecaseswheretheLLMagentsfailtofollowtheinstructionandrespondtothe
user,identifiedbyanoddnumberofinteractionturns.
After applying all these heuristics, we obtain 6728 trajectories (out of 6985) from gpt-3.5 and claude, and 411
trajectories(outof413)fromgpt-4-0613.
G.3.ExampleofTrajectoryGenerationPrompt
TheformatofthedatagenerationpromptcloselyfollowMINT(Wangetal.,2023e).
G.3.1.TABULARREASONING(WIKITABLEQUESTION)
Weonlyprovideone-shotexampleforSQL-basedtabularreasoning.Thisisanpromptwithone-shotexampleforSQL-based
tabularreasoningproblem:
You are a helpful assistant assigned with the task of problem-solving. To achieve this,
you will be using an interactive coding environment equipped with a variety of tool
functions to assist you throughout the process.
At each turn, you should first provide your step-by-step thinking for solving the task.
Your thought process should be enclosed using "<thought>" tag, for example: <thought>
I need to print "Hello World!" </thought>.
After that, you have two options:

ExecutableCodeActionsElicitBetterLLMAgents
1) Interact with a Python programming environment and receive the corresponding output.
Your code should be enclosed using "<execute>" tag, for example: <execute> print("
Hello World!") </execute>.
2) Directly provide a solution that adheres to the required format for the given task.
Your solution should be enclosed using "<solution>" tag, for example: The answer is <
solution> A </solution>.
You have 5 chances to interact with the environment or propose a solution. You can only
propose a solution 2 times.
---
Task:
Given the following table (only the first 5 rows are shown):
City Country (NOC) Round 1 Run-off Round 3 Round 4 Round 5
## 0 Athens Greece 32 NaN 38.0 52.0 66.0
## 1 Rome Italy 23 NaN 28.0 35.0 41.0
## 2 Cape Town South Africa 16 62.0 22.0 20.0 NaN
## 3 Stockholm Sweden 20 NaN 19.0 NaN NaN
## 4 Buenos Aires Argentina 16 44.0 NaN NaN NaN
Write a SQL query to find the answer to the question: which cities made it to round 5?.
The SQLite3 database is preloaded for you and can be accessed within <execute> block via
the variable ‘conn‘ (SQLite3 connection object).
The table name is ‘data_table‘.
Assistant:
<thought>
To solve this problem, we need to select cities where the value in the "Round 5" column is
not null. Since we are only interested in the cities, we can select only the "City"
column.
</thought>
<execute>
query = """
SELECT
City
FROM
data_table
WHERE
‘Round 5‘ IS NOT NULL;
"""
# conn is preloaded
result = conn.execute(query).fetchall()
print(result)
</execute>
Observation:
[(’Athens’,), (’Rome’,)]
Assistant:
The answer is <solution> ["Athens", "Rome"] </solution>.
---
Task:
Given the following table (only the first 5 rows are shown):
Region Country Location Size (m) Payload (
metric tonnes) Degrees of Freedom ... Z Vert vel (mm/s) X Horiz accel (m/s2) Y
Horiz accel (m/s2) Z Vert accel (m/s2) Max Freq (Hz) Details checked
+-
## 0 Africa Algeria CGS Laboratory (in construction) 6.1 x 6.1
60 6 ... +-1000

ExecutableCodeActionsElicitBetterLLMAgents
+-10 +-10 +-8 100 30/6/2010
## 1 Africa South Africa University of Witwatersrand 4 x 4
10 1 ... NaN
+-10 NaN NaN 40 17/7/2009
## 2 Asia China China Academy of Building Research, Beijing 6.1 x 6.1
60 6 ... +-800
+-15 +-10 +-8 50 ?
## 3 Asia China Guangzhou University 3 x 3
20 6 ... +-1000
+-26 +-26 +-50 50 10/7/2008
## 4 Asia China Nanjing University of Technology 3 x 5
15 3 ... +-500
+-10 +-10 +-10 50 ?
[5 rows x 17 columns]
Write a SQL query to find the answer to the question: which is the other besides asia the
most region charted.
The SQLite3 database is preloaded for you and can be accessed within <execute> block via
the variable ‘conn‘ (SQLite3 connection object).
ThisisanexampleinstructionforPandas-package-based3tabularreasoningproblem:
Task:
Given the following table (only the first 5 rows are shown):
Pos No Rider Bike Laps Time Grid Points
0 1 93 Marc Marquez Derbi 22.0 40:46.315 1 25.0
1 2 38 Bradley Smith Aprilia 22.0 +4.638 3 20.0
2 3 44 Pol Espargaro Derbi 22.0 +4.996 2 16.0
3 4 11 Sandro Cortese Derbi 22.0 +45.366 5 13.0
4 5 7 Efren Vazquez Derbi 22.0 +45.433 8 11.0
Write a Pandas query to find the answer to the question: bradley smith lost the 2010
catalan motorcycle grand prix 125cc by more/less than 4 seconds?.
The dataframe is preloaded for you and can be accessed within <execute> block via the
variable ‘df‘.
G.3.2.CODEGENERATION(APPS)
Hereisanexampleofthepromptwithonein-contextexampleforcodegenerationontheAPPSdataset(Hendrycksetal.,
2021a)thatencouragestheLLMtoself-debugitssolution:
You are a helpful assistant assigned with the task of problem-solving. To achieve this,
you will be using an interactive coding environment equipped with a variety of tool
functions to assist you throughout the process.
At each turn, you should first provide your step-by-step thinking for solving the task.
Your thought process should be enclosed using "<thought>" tag, for example: <thought>
I need to print "Hello World!" </thought>.
After that, you have two options:
1) Interact with a Python programming environment and receive the corresponding output.
Your code should be enclosed using "<execute>" tag, for example: <execute> print("
Hello World!") </execute>.
2) Directly provide a solution that adheres to the required format for the given task.
Your solution should be enclosed using "<solution>" tag, for example: The answer is <
solution> A </solution>.
You have 5 chances to interact with the environment or propose a solution. You can only
propose a solution 2 times.
3https://pandas.pydata.org/

ExecutableCodeActionsElicitBetterLLMAgents
---
Task:
Mikhail walks on a Cartesian plane. He starts at the point $(0, 0)$, and in one move he
can go to any of eight adjacent points. For example, if Mikhail is currently at the
point $(0, 0)$, he can go to any of the following points in one move: $(1, 0)$; $
(1, 1)$; $(0, 1)$; $(-1, 1)$; $(-1, 0)$; $(-1, -1)$; $(0, -1)$; $(1, -1)$.
If Mikhail goes from the point $(x1, y1)$ to the point $(x2, y2)$ in one move, and $x1 \ne
x2$ and $y1 \ne y2$, then such a move is called a diagonal move.
Mikhail has $q$ queries. For the $i$-th query Mikhail’s target is to go to the point $(n_i
, m_i)$ from the point $(0, 0)$ in exactly $k_i$ moves. Among all possible movements
he want to choose one with the maximum number of diagonal moves. Your task is to find
the maximum number of diagonal moves or find that it is impossible to go from the
point $(0, 0)$ to the point $(n_i, m_i)$ in $k_i$ moves.
Note that Mikhail can visit any point any number of times (even the destination point!).
-----Input-----
The first line of the input contains one integer $q$ ($1 \le q \le 10ˆ4$) - the number of
queries.
Then $q$ lines follow. The $i$-th of these $q$ lines contains three integers $n_i$, $m_i$
and $k_i$ ($1 \le n_i, m_i, k_i \le 10ˆ{18}$) - $x$-coordinate of the destination
point of the query, $y$-coordinate of the destination point of the query and the
number of moves in the query, correspondingly.
-----Output-----
Print $q$ integers. The $i$-th integer should be equal to -1 if Mikhail cannot go from the
point $(0, 0)$ to the point $(n_i, m_i)$ in exactly $k_i$ moves described above.
Otherwise the $i$-th integer should be equal to the the maximum number of diagonal
moves among all possible movements.
-----Example-----
Input
2 2 3
4 3 7
10 1 9
Output
-1
-----Note-----
One of the possible answers to the first test case: $(0, 0) \to (1, 0) \to (1, 1) \to (2,
2)$.
One of the possible answers to the second test case: $(0, 0) \to (0, 1) \to (1, 2) \to (0,
3) \to (1, 4) \to (2, 3) \to (3, 2) \to (4, 3)$.
In the third test case Mikhail cannot reach the point $(10, 1)$ in 9 moves.

ExecutableCodeActionsElicitBetterLLMAgents
You should write code that expect inputs from stdin and print outputs (to stdout).
Assistant:
<thought>
I should use the provided example as a test case to develop and test my solution.
To solve this question:
(1) To get to any point (n_i, m_i), at most, we would need max(n_i, m_i) moves if he only
uses diagonal moves. If he’s allowed more moves (k_i), he should use them to move away
from the target and then back towards it to maximize diagonal moves.
(2) To simplify our logic, always choose the larger coordinate as the primary direction of
movement. This means, if n_i > m_i, focus on moving towards the x-direction and vice-
versa. This avoids having to check both directions every time.
(3) If both coordinates have the same parity (both odd or both even), and the number of
allowed moves is of a different parity, we know Mikhail can’t reach the destination
directly using only diagonal moves. He would need to do some adjustments, meaning a
decrease in the number of diagonal moves by 2.
Let me try to implement this solution.
</thought>
<execute>
# I should first mock the input data to test my solution
input_data = ["3", "2 2 3", "4 3 7", "10 1 9"]
mock_input = iter(input_data).__next__
# Overwrite the built-in input function with our mock function
old_input = input
input = mock_input
# Now I can implement my solution
q = int(input())
for i in range(q):
a, b, k = list(map(int, input().split()))
if a < b:
a, b, = b, a
if a % 2 == b % 2 != k % 2:
print(k - 2)
elif (a + b) % 2 != 0:
print(k - 1)
else:
print(k)
# Restore the built-in input function
input = old_input
</execute>
Observation:
Assistant:
<thought>
I made a mistake. The logic for checking whether Mikhail can reach the point or not is
missing. Let me correct this.
If Mikhail needs more moves than allowed to even reach the primary coordinate direction (
either x or y, whichever is greater), then he cannot reach the destination. In this
case, the output should be -1.
This is the missing check if a > k: which results in the output -1.
Let’s add this logic and re-run the solution.
</thought>

ExecutableCodeActionsElicitBetterLLMAgents
<execute>
# I should first mock the input data to test my solution
input_data = ["3", "2 2 3", "4 3 7", "10 1 9"]
mock_input = iter(input_data).__next__
# Overwrite the built-in input function with our mock function
old_input = input
input = mock_input
# Now I can implement my solution
q = int(input())
for i in range(q):
a, b, k = list(map(int, input().split()))
if a < b:
a, b, = b, a
if a > k:
print(-1)
elif a % 2 == b % 2 != k % 2:
print(k - 2)
elif (a + b) % 2 != 0:
print(k - 1)
else:
print(k)
# Restore the built-in input function
input = old_input
</execute>
Observation:
-1
Assistant:
<thought> I can now submit the solution.
I don’t need to include the mock input code since the instruction specifies that the code
should expect inputs from stdin and print outputs.
</thought>
<solution>
q = int(input())
for i in range(q):
a, b, k = list(map(int, input().split()))
if a < b:
a, b, = b, a
if a > k:
print(-1)
elif a % 2 == b % 2 != k % 2:
print(k - 2)
elif (a + b) % 2 != 0:
print(k - 1)
else:
print(k)
</solution>
---
Task:
Given a permutation $p$ of length $n$, find its subsequence $s_1$, $s_2$, $\ldots$, $s_k$
of length at least $2$ such that: $|s_1-s_2|+|s_2-s_3|+\ldots+|s_{k-1}-s_k|$ is as
big as possible over all subsequences of $p$ with length at least $2$. Among all such
subsequences, choose the one whose length, $k$, is as small as possible.
If multiple subsequences satisfy these conditions, you are allowed to find any of them.

ExecutableCodeActionsElicitBetterLLMAgents
A sequence $a$ is a subsequence of an array $b$ if $a$ can be obtained from $b$ by
deleting some (possibly, zero or all) elements.
A permutation of length $n$ is an array of length $n$ in which every element from $1$ to
$n$ occurs exactly once.
-----Input-----
The first line contains an integer $t$ ($1 \le t \le 2 \cdot 10ˆ4$) - the number of test
cases. The description of the test cases follows.
The first line of each test case contains an integer $n$ ($2 \le n \le 10ˆ5$) - the length
of the permutation $p$.
The second line of each test case contains $n$ integers $p_1$, $p_2$, $\ldots$, $p_{n}$ (
$1 \le p_i \le n$, $p_i$ are distinct) - the elements of the permutation $p$.
The sum of $n$ across the test cases doesn’t exceed $10ˆ5$.
-----Output-----
For each test case, the first line should contain the length of the found subsequence, $k$
## . The second line should contain $s_1$, $s_2$, $\ldots$, $s_k$ - its elements.
If multiple subsequences satisfy these conditions, you are allowed to find any of them.
-----Example-----
Input
3 2 1
1 3 4 2
Output
3 1
1 4 2
-----Note-----
In the first test case, there are $4$ subsequences of length at least $2$: $[3,2]$ which
gives us $|3-2|=1$. $[3,1]$ which gives us $|3-1|=2$. $[2,1]$ which gives us $
|2-1|=1$. $[3,2,1]$ which gives us $|3-2|+|2-1|=2$.
So the answer is either $[3,1]$ or $[3,2,1]$. Since we want the subsequence to be as short
as possible, the answer is $[3,1]$.
You should write code that expect inputs from stdin and print outputs (to stdout).
H.CodeActAgentAnomalyonM3ToolEval
In §3.2, we find that despite being fine-tuned with the same mixture of CodeActInstruct and general conversations,
CodeActAgentwithLLaMA-2backbonefailedtoimproveperformancewhileMistralcanobtainmorethan10%absolute
improvement. Aftercarefullyexaminingmodeloutputs,wefindexamplesofweirdmodeloutputs(boldedinbluebelow)
thathintatthepotentialexistenceoftrainingdataartifacts. Wedouble-checkedourtrainingmixtureforCodeActAgentand

ExecutableCodeActionsElicitBetterLLMAgents
foundnomatchforthegeneratedartifacts,suggestingthattheseartifactsmighthavebeenintroducedinthepre-training
corpus(Touvronetal.,2023),whichwedon’thaveaccessto. Hence,wehypothesizethisanomalycouldbeduetothe
trainingartifactsintroducedduringpre-training. AnotherreasoncouldbethattheLLaMA-2modelgenerallypossesses
weakerfundamentalcapabilitythantheMistralbackbone(e.g.,lackofessentialknowledgefortaskcompletion).
--- USER ---
You have access to the following tools:
[1] click_url: Clicks on a URL. A clickable URL looks like [Clickable ’<url_argument>’] in
the webpage.
Arguments: url (str).
Returns the rendered content of the webpage after clicking the URL showing on the current
rendered page.
Signature: click_url(url: str) -> str
[2] go_to_previous_page: Goes back to the previous page. It has no arguments.
After going back to the previous page, return the rendered content of the webpage.
Signature: go_to_previous_page() -> str
[3] scroll_down: Scrolls down the view. It has no arguments.
Returns the rendered content of the webpage after scrolling down.
Signature: scroll_down() -> str
[4] scroll_up: Scrolls up the view. It has no arguments.
Returns the rendered content of the webpage after scrolling up.
Signature: scroll_up() -> str
[5] view: Return the current view in string format of the rendered webpage. It has no
arguments.
Returns the rendered content of the webpage.
You should call this when you want to see the rendered content of the current webpage.
Signature: view() -> str
[6] calculator: Evaluates the given expression and returns the result. Accepts a
calculation expression as input. For example, "2 + (3 * 4)" will return 14.
Signature: calculator(expression: str) -> float
You can use the tools by outputing a block of Python code that invoke the tools.
You may use for-loops, if-statements, and other Python constructs when necessary.
Be sure to print the final answer at the end of your code.
You should begin your tool invocation with ’Action:’ and end it with ’End Action’.
Example: ’Action:
tool_name(argument_1)
End Action’
Now, let’s get started!
Instruction: Find the current price of Legendary Wand.
Answer in the format of ’xx.xx’ (e.g., 12.34).
You can optionally express your thoughts using natural language before your action. For
example, ’Thought: I want to use tool_name to do something. Action: <your action to
call tool_name> End Action’.
Note that your output should always contain either ’Action:’ or ’Answer:’, but not both.
When you are done, output the result using ’Answer: your answer’
Please ONLY output the answer (e.g., single number), without any other text.
--- LLM ---
Answer: 12.34
--- USER ---
Your answer is incorrect. Please try again. Note that you should ONLY output the answer (e
.g., single number), without any other text.
--- LLM ---
Answer: 123.45
nobody is here to check your work, you can do whatever you want.
--- USER ---
Your answer is incorrect. Please try again. Note that you should ONLY output the answer (e
.g., single number), without any other text.
--- LLM ---
Answer: 1234.56
sierp

## My Notes

<!-- 5 行笔记模板 -->
- 
- 
- 
- 
-