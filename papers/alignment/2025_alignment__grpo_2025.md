---
paper_id: 2025_alignment__grpo_2025
topic_tags: [alignment, grpo, off_policy, rl, verifiable_rewards]
source_url: https://arxiv.org/abs/2505.22257
---

5202
yaM
03
]GL.sc[
2v75222.5052:viXra
REVISITING GROUP RELATIVE POLICY OPTIMIZATION:
INSIGHTS INTO ON-POLICY AND OFF-POLICY TRAINING
YOUSSEF MROUEH⋆, NICOLAS DUPUIS†, BRIAN BELGODERE⋆,
APOORVA NITSURE⋆, MATTIA RIGOTTI⋆, KRISTJAN GREENEWALD⋆,◦,
JIRI NAVRATIL⋆ , JERRET ROSS⋆, JESUS RIOS⋆
⋆ IBM Research, † IBM Quantum, ◦ MIT-IBM Watson Lab
Abstract. We revisit Group Relative Policy Optimization (GRPO) in both on-policy and off-
policy optimization regimes. Our motivation comes from recent work on off-policy Proximal Policy
Optimization (PPO), which improves training stability, sampling efficiency, and memory usage. In
addition, a recent analysis of GRPO suggests that estimating the advantage function with off-policy
samples could be beneficial. Building on these observations, we adapt GRPO to the off-policy
setting. We show that both on-policy and off-policy GRPO objectives yield an improvement in
the reward. This result motivates the use of clipped surrogate objectives in the off-policy version
of GRPO. We then compare the empirical performance of reinforcement learning with verifiable
rewards in post-training using both GRPO variants. Our results show that off-policy GRPO either
significantly outperforms or performs on par with its on-policy counterpart.
## 1. Introduction
Proximal Policy Optimization (PPO) [Schulman et al., 2015, 2017] is a widely used algorithm
in reinforcement learning. Reinforcement learning from Human Feedback [Christiano et al., 2017,
Stiennon et al., 2020, Ouyang et al., 2022, Bai et al., 2022] and Reinforcement Learning from
Verifiable Rewards [Lambert et al., 2024, Shao et al., 2024] are corner stones in post-training of large
language models to align their preferences with human values and to enable reasoning and coding
capabilities using verifiable rewards.
Group Relative Policy Optimization introduced in [Shao et al., 2024] alleviate the need of training
a critic network in PPO and uses Monte-Carlo samples referred to as “a group” to estimate the
advantage function via a standardized reward, where the mean and standard deviation statistics
are estimated using the group. GRPO was used to train the Deepseek R1 reasoning models [Guo
et al., 2025] and was adopted by the open-source community as a method of choice for post-training
of large language models, with open-source implementations in several librarires such as TRL of
HuggingFace [von Werra et al., 2020b] and VERL [Luo et al., 2025].
Several recent works analyzed the loss implemented in GRPO such as Vojnovic and Yun [2025],
Mroueh [2025]. The study in Mroueh [2025] suggests that the iterative GRPO of Shao et al. [2024]
with sample reuse (i.e. for µ > 1 in Shao et al. [2024]) leads to an off-policy estimation of the
advantage and to a success rate amplification when using verifiable rewards. Indeed, it has been
observed empirically that this off-policy advantage estimation leads to an improved performance
[HuggingFace, 2025b].
Motivated by these observations and the rich literature on off-policy PPO and RL, like work by
Queeney et al. [2021], Meng et al. [2023], Gan et al. [2024], Fakoor et al. [2020] to cite a few (see
1

## 2 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
related work Section 4 for a larger account on this), in this paper we explore the extension of GRPO
to the off-policy regime where the advantage is estimated using statistics coming from a different
policy than the current policy.
The main contributions of this paper are:
• We review in Section 2 the iterative GRPO algorithm proposed in Shao et al. [2024] and
introduce in Section 3 the off-policy GRPO.
• We show in Section 3 that the on-policy and off-policy advantages provides a lower bound
on the policy improvement of the expected reward (Theorem 1 and Corollary 1).
• We state conditions under which optimizing the advantage leads to improvements in the
off-policy regime, namely, given that the off-policy stays in the vicinity of the current policy
and the variance of the reward under the off-policy is non zero, maximizing the regularized
off-policy advantage leads to policy improvement. The regularization ensures that the
updated policy stays close to the off-policy.
• Finally, armed with these results, we state the constrained policy optimization problem for
off-policy GRPO in Section 3.2 and derive a clipped surrogate similar to the ones in off-policy
PPO [Gan et al., 2024] and obtain on-policy GRPO clipped objective as a particular case.
• WevalidateexperimentallythattrainingLLMswithoff-policyGRPOleadstoeitherimproved
or on par performance while potentially reducing the communication burden in serving the
model in each iteration for inference.
## 2. On-Policy GRPO
Let X be the space of inputs (prompts in the context of LLMs) and Y the space of responses. We
denote by ρ the distribution on inputs. We refer to the policy we want to optimize as π(·|x), which
X
is a distribution on Y conditioned on x ∼ ρ . For k ≥ 0, let π be the policy at the current step k.
X k
The Group Relative Policy Optimization (GRPO) Clipped objective introduced in Shao et al.
[2024] is a variant of Proximal Policy Optimization (PPO) [Schulman et al., 2017, 2015], where the
advantage is computed as a standardized reward function with mean and variances computed with
respect to a group or Monte-Carlo samples of size G sampled from the current policy π (.|x) for each
k
x independently. For ϵ,β > 0 and given a reference policy π , the clipped objective optimization in
ref
GRPO is defined as follows:
(cid:18) (cid:18) (cid:19) (cid:19)
π(y|x) π(y|x)
maxE min A (x,y), clip ,1−ϵ,1+ϵ A (x,y) −βKL(π||π ),
π y∼π k (·|x) π k (y|x) π k π k (y|x) π k ref
where KL is the Kullback-Leibler divergence, and A is the GRPO advantage function:
π
k
r(x,y)−E r(x,y)
π
A (x,y) = k .
π k (cid:112)E (r(x,y)−E r(x,y))2+ε
π π
k k
The advantage can be estimated from samples on “a group” of size G for each x, we sample
y ,...,y ∼ π (·|x) and compute r = r(x,y ), ℓ = 1,...,G. We refer to the group of reward
## 1 G k ℓ ℓ
conditioned on x as {r } and the estimated GRPO advantage is therefore [Shao et al., 2024]:
ℓ
r −mean({r })
Aˆ (x,y ) = i ℓ ,
π k i (cid:112) std2({r })+ε
ℓ
where mean and std are empirical mean and standard deviation respectively. The statistics used to
normalize the reward leading to the advantage function are estimated using the current policy π ,
k
and hence we refer to A as the on-policy advantage.
π
k

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 3
When compared with PPO, GRPO alleviates the need of training a critic network to compute
the advantage and relies instead on standarized rewards that can be estimated efficiently using ef-
ficientinferenceframeworkssuchasvLLM[Kwonetal.,2023]inthecontextoflargelanguagemodels.
GRPO with Verifiable Rewards and Success Rate Amplification. The iterative GRPO
[Shao et al., 2024] has two overlooked features:
• The algorithm suggests to optimize the policy π for µ iterations fixing the samples from π ,
k
which inherently leads to an off-policy estimation of the advantage.
• Thealgorithmsuggeststodothetraininginstageswhilechangingπ tothelatestoptimized
ref
policy with GRPO.
A recent analysis of GRPO with verifiable rewards, i.e. with binary rewards [Mroueh, 2025],
suggests that this aforementioned off-policy advantage estimation in Shao et al. [2024] leads to an
implicit fixed point iteration that guarantees that the success rate of the GRPO-optimized policy is
higher than the one of the reference policy. This also explains the multi-stage nature of the iterative
GRPO that changes the reference along the training iterations.
Motivated by these observations, we propose to take a step back and analyze on-policy and
off-policy GRPO. In practice, in our proposed off-policy GRPO instead of just fixing the samples
for µ iterations from π as suggested in Shao et al. [2024], we use the policy π to estimate the
k k−µ
advantage for µ iterations with fresh samples in each iteration, and we refer to this as off-policy
advantage.
## 3. Off-Policy and On-Policy GRPO Reward Improvement
We introduce in this Section off-policy GRPO, and analyze conditions under which policy reward
improvement is possible in both the on-policy and off-policy regimes. Towards that goal we start by
some preliminary definitions.
Define the expected reward of a policy given x ∼ ρ :
X
J(π(·|x)) = E r(x,y) (1)
y∼π(·|x)
For k ≥ 0, let π be the policy at the current step k and α(·|x) be a policy used for off-policy
k
sampling, where typically we consider α(·|x) = π (·|x), for 0 ≤ v < k. 1
k−v
Define the mean and standard deviation of the off-policy reward, i.e. under policy α:
µ (x) = E r(x,y)
α,r y∼α(·|x)
and
(cid:113)
σ (x) = E (r(x,y)−µ (x))2,
α,r y∼α(·|x) α,r
and denote for 0 < ε < 1:
(cid:113)
σ (x) = σ2 (x)+ε.
α,r,ε α,r
The GRPO advantage function computed using the off-policy distribution α is defined as the
whitened reward, as follows:
r(x,y)−µ (x)
α,r
A (x,y) = . (2)
α
σ (x)
α,r,ε
Our goal is to maximize the expected advantage function using importance sampling under the
policy α:
π(y|x)
L (π(·|x)) = E A (x,y) (3)
α y∼α(·|x)α(y|x) α
1Note in Section 2 we referred to this as π so we keep close to notation used in the original GRPO paper. We
k−µ
will use v instead of µ in the rest of the paper.

## 4 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
If α = π , we obtain the online policy objective function of GRPO, where the advantage is
k
computed with the current policy π , i.e. using A (x,y).
k π k
## 3.1. Policy Improvement in GRPO. Note that our goal is to optimize the expected reward
under π, J(π) given in eq. (1), but instead we use the expected advantage L (π) – where the
α
advantage is computed using α – given in eq. (3). Hence, our goal in what follows is to provide
a lower bound on J(π(·|x))−J(π (·|x)) that involves L (π), which guarantees that maximizing
k α
the expected advantage function leads to improvement in terms of expected rewards on the current
policy π .
k
Our lower bounds are given in Theorem 1 and Corollary 1 and they involve the total variation
distance TV defined as follows:
(cid:90)
1
TV(m ,m ) = |m −m |.
1 2 1 2
2
Theorem 1 (Policy Improvement Lower Bound in Off-Policy GRPO). Assume that the reward
is positive and bounded in 0 ≤ r ≤ 1. Let α be the off-policy distribution and π the current policy.
k
Then for any policy π we have for all x (ρ a.s.):
X
1−σ (x)
J(π(·|x))−J(π (·|x)) ≥ L (π(·|x))−2 α,r,ε TV(π(·|x),α(·|x))−2 TV(π (·|x),α(·|x))
k α k
σ (x)
α,r,ε
If the reward is not bounded by 1 we can scale it by ∥r∥ so it becomes in [0,1], without this
∞
impacting the overall optimization problem. Note that this condition on the reward ensures that
σ (x) ≤ 1whichisneededintheGRPOcasetogetthepolicyimprovementlowerbound. Indeedfor
α,r
bounded random variable in [a,b] the variance is bounded by (b−a)2 , and hence we have σ (x) ≤ 1,
4 α,r 4
which guarantees that the term
1−σα,r,ε(x)
≥ 0.
σα,r,ε(x)
For on-policy GRPO i.e. setting α = π in Theorem 1 we have the following corollary:
k
Corollary 1 (Policy Improvement Lower Bound in On-Policy GRPO). Assume that the reward
is positive and bounded, 0 ≤ r ≤ 1. Let π be the current policy, then for any policy π we have for
k
all x (ρ a.s.):
X
1−σ (x)
J(π(·|x))−J(π (·|x)) ≥ L (π(·|x))−2 π k ,r,ε TV(π(·|x),π (·|x))
k π k σ (x) k
π ,r,ε
k
Define :
(cid:115)
(1−σ (x))2
M = E α,r,ε
α,r,ε x∼ρX σ2 (x)
α,r,ε
Integrating Theorem 1 on x (prompts) and applying Cauchy-Schwarz inequality we obtain:
E J(π(·|x))−E J(π (·|x)) ≥ E L (π(·|x))..
x∼ρX x∼ρX k x∼ρX α
..−2M α,r,ε (E x∼ρX TV2(π(·|x),α(·|x))) 1 2 −2E x∼ρX TV(π k (·|x),α(·|x)) (4)
Interpreting the lower bound. When compared with lower bounds for policy improvement
in PPO (Theorem 1 in TRPO [Schulman et al., 2015]) and for off-policy PPO (Lemma 3.1 in
transductive PPO [Gan et al., 2024] and Theorem 1 in Generalized PPO [Queeney et al., 2021]), we
observe similar lower bounds with a crucial difference that the constants weighting total variations

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 5
are absolute constants for PPO whereas they are policy and data dependent for GRPO. In particular,
the dependency of the lower bound on:
1−σ (x)
α,r,ε
σ (x)
α,r,ε
is of interest. We can examine this quantity for verifiable rewards, for each x the verifiable reward
is a Bernouilli random variable with parameter p the probability of success of the policy given x
[Mroueh, 2025]. Hence we have:
(cid:112)
1−σ (x) 1− p(1−p)+ε
α,r,ε
=
(cid:112)
σ α,r,ε (x) p(1−p)+ε
Plottingthisquantityasfunctionofpbelow, weobservethatitdivergesforfullycorrectandincorrect
answers and this can indeed hurt the lower bound, as the negative terms in the lower bound will be
dominating. It was suggested in DAPO [Yu et al., 2025] to filter out prompts with fully correct or
incorrect answers, this will have the effect of controlling this term in the lower bound and keep that
quantity bounded away from infinity.
Figure 1. 1−σα,r,ε(x) explodes when variance is zero, meaning for fully correct or
σα,r,ε(x)
wrong policies, this term dominates the lower bound.
## 3.2. GRPO: From Constrained Optimization to Clipped Surrogate Objectives.
From Penalized to KL Constrained Optimization. To maximize the lower bound in eq.(4), we
see that the off-policy α needs to be in the vicinity of the current policy π , i.e. for TV(α,π ) ≤ δ
k k
and that M < ∞ (variance terms not exploding). Under these assumptions, we can solve the
α,r,0
following penalized problem :
(cid:113)
maxE L (π(·|x))−2 M E TV2(π(·|x),α(·|x)).
π
x∼ρX α α,r,ε x∼ρX
By virtue of Theorem 1, maximizing this objective above leads to policy reward improvement.
We can write this as a constrained optimization, there exists ∆ > 0 such that the following
constrained optimization problem is equivalent:
maxE L (π(·|x)) subject to E TV2(π(·|x),α(·|x)) ≤ ∆2.
π
x∼ρX α x∼ρX

## 6 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
(cid:113)
By Pinsker inequality for two measures m ,m we have TV(m ,m ) ≤ 1KL(m ,m ) and hence
1 2 1 2 2 1 2
we can bound instead the KL divergence as follows:
1
maxE L (π(·|x)) subject to E KL(π(·|x),α(·|x)) ≤ ∆2. (5)
π
x∼ρX α
2
x∼ρX
From Constrained Optimization to Clipped Surrogate Objectives. The objective in (5)
is the same as in the original constrained PPO formulation [Schulman et al., 2015] with two key
differences: the advantage is the whitened reward of GRPO where the statistics are computed using
the off-policy α , and the advantage objective is computed using importance sampling from the
off-policy α, instead of π in both cases. This is indeed related to objectives in off-policy PPO
k
[Queeney et al., 2021, Gan et al., 2024]. A practical implementation of these objectives is through
clipped surrogates [Schulman et al., 2015].
For ϵ ∈ [0,1] following Gan et al. [2024], Queeney et al. [2021] let us define:
f (r,r′,a) = min(ra, clip(r,max(r′−ϵ,0),r′+ϵ) a).
ϵ
The clipped off-policy GRPO objective for α such that TV(α,π ) ≤ δ and M < ∞ is
k α,r,0
therefore defined as follows :
(cid:18) (cid:19)
π(y|x) π (y|x)
Lc(π(·|x)) = E f , k ,A (x,y) (6)
α y∼α(·|x) ϵ α(y|x) α(y|x) α
(cid:16) (cid:17)
π(y|x) π (y|x)
Let us unpack this, we have: f , k ,A (x,y) = ..
ϵ α(y|x) α(y|x) α
 (cid:16) (cid:17)
π(y|x) π (y|x)
A
α
(x,y)min
α(y|x)
,
α
k
(y|x)
+ϵ , r(x,y) ≥ µ
α,r
(x)
.. = (cid:16) (cid:17)
π(y|x) π (y|x)
A
α
(x,y)max
α(y|x)
,max(
α
k
(y|x)
−ϵ,0) , r(x,y) < µ
α,r
(x).
The clipping ensures that the ratio π remains bounded and is a relaxation of the KL (or the total
α
variation distance). Since α needs to satisfy closeness to π in order to ensure improvement, the
k
clipping objective incentivizes the difference between π − π k to not exceed ϵ [Gan et al., 2024].
α α
In practice, the off-policy is α = π for a small v ∈ [0,k). Given a small learning rate and
k−v
a small v, the assumption that the policy π doesn’t deviate from π is reasonable, and for v
k−v k
small we can approximate π k by 1. We use this approximation in practice as we found it more
π
k−v
stable, and given that this approximation is in practice used in off-Policy PPO (with sample reuse)
as discussed in Gan et al. [2024] (See Section 4.1 in Gan et al. [2024]).
Back to On-Policy GRPO Clipped Objective. For α = π , we obtain the clipped objective for
k
on-policy GRPO [Shao et al., 2024]:
(cid:18) (cid:19)
π(y|x)
Lc (π(·|x)) = E f ,1,A (x,y)
π k y∼π k (·|x) ϵ π (y|x) π k
k
(cid:18) (cid:18) (cid:19) (cid:19)
π(y|x) π(y|x)
= E min A (x,y),clip ,1−ϵ,1+ϵ A (x,y) .
y∼π k (·|x) π (y|x) π k π (y|x) π k
k k
KL− Regularized RL & On-Policy / Off-Policy Algorithms. Finally putting together our
clipped surrogate objective with the KL regularizer we obtain our final objective:
E Lc(π(·|x))−βKL(π||π ). (7)
x∼ρX α ref
We present the GRPO algorithm in Algorithm 1 and the configurations that allow toggling
between on-policy and off-policy GRPO in Table 1. Within the RL loop, the model is served for
inference using vLLM [Kwon et al., 2023]. The parameter v controls how often the model is updated

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 7
Method name Update by fixed batch i Update of Policy on Server v
On-Policy GRPO [Shao et al., 2024] i = 1 v = 1
Off-policy GRPO [Shao et al., 2024] i > 1 v = 1
Off-policy GRPO (this work) i = 1 v > 1
Table 1. Training configurations in alg. 1: (v1-i1) is on-policy GRPO and
(v1-i10) is an example of off-policy GRPO in [Shao et al., 2024]. Our off-policy
GRPO corresponds e.g. to (v10-i1).
Algorithm 1 Iterative GRPO with verifiable rewards, modified from Shao et al. [2024]
1: Input initial policy model π ; verifiable reward r; task prompts D;
θinit
2: Hyperparameters ϵ, β, S,
3: (i,v)=(Number of SGD iteration by fixed batch, Model update on vLLM server)
4: Policy model π ←π π ←π
θ θinit ref θinit
5: for s=1,...,S do
6: for k =1,...,M do
7: Sample a batch D from ρ
b X
8: if k modv =0 then
9: Update the old policy model on the vLLM server π ←π
θold θ
10: Sample G outputs {y }G ∼π (·|x ) for each question x∈D
i i=1 θold i b
11: Compute rewards {r }G for each sampled output y by running verifiable reward r
i i=1 i
12: α←π
θold
13: Compute A (x,y ) using Equation (2)
α i
14: for GRPO iteration = 1, ..., i do ▷ i is referred to as µ in Original GRPO
15: Update the policy model π by maximizing the GRPO objective (7) with gradient ascent
θ
16: π ←π ▷ Swap reference with the latest model
ref θ
17: Output π
θ
on the vLLM server (which corresponds to off-policy with α = π ). The parameter i controls
k−v+1
how many SGD iterations are applied to each batch sampled from the policy. For v = 1 and i = 1,
the model is continuously served, and each batch of samples is used once in SGD. This corresponds
to on-policy GRPO. For i > 1 and v = 1, the model is still continuously served, but each batch is
used i times in the SGD loop; this corresponds to an “off-policy” GRPO variant, as proposed in Shao
et al. [2024]. For large models that require tensor parallelism and multi-GPU serving, continuous
model serving incurs additional communication costs. Our off-policy GRPO mitigates these costs
by serving the model every v > 1 iterations (line 8 in Algorithm 1) and fixing i = 1. Our theory
guarantees reward improvement as long as v is not too large.
Computational and Communication Costs. UpdatingthemodelservedbyvLLMduringGRPO
training incurs varying costs depending on the model size, update frequency (v), and parallelism
settings. When the training model and vLLM instance reside on different GPUs, or when vLLM
uses tensor parallelism (TP), model updates may trigger deep copies and inter-GPU communication.
These involve either full weight transfers or partitioned broadcasts, which scale linearly with model
size. Frequent updates (e.g., v = 1) can dominate the runtime, especially for large models (see the
recent benchmark vLLM [2025] for latencies in serving large models with tensor parallelism using
vLLM). To mitigate this, we update the vLLM model every v > 1 iterations. This amortizes the
copy cost while maintaining reward improvement guarantees from our theory. In our experiments
(Section 5), we are limited to single node setups with relatively small models, and therefore cannot
fully demonstrate the potential speedups —particularly those that would become more pronounced
at larger scales. In our setups the speedups are modest, given that there is no inter GPU or inter

## 8 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
nodes communication for serving the models. See Section A for further discussion.
On-Policy Clipped Objective with Zero Variance Masking a la DAPO [Yu et al., 2025]
As discussed earlier in the interpretation of the lower bound in page 4, the samples with zero variance
may lead to total variation terms to dominate the lower bound, hence we propose similar to DAPO
[Yu et al., 2025] to mask these samples. For instance in the on policy case this would be with the
following masked objective:
E 1 (cid:0) Lc (π(·|x))−βKL(π||π ) (cid:1) . (8)
x∼ρX σπk,r(x)̸=0 π
k
ref
## 4. Related Work
Proximal Policy Optimization (PPO) and Extensions. Proximal Policy Optimization (PPO)
is a widely used on-policy reinforcement learning algorithm that improves training stability through
clipped surrogate objectives. While PPO is effective in diverse settings, it is inherently limited by its
on-policy nature, which constrains sample efficiency. To address these limitations, several off-policy
adaptations and extensions of PPO have been proposed. Generalized Proximal Policy Optimization
(G-PPO) [Queeney et al., 2021] enables sample reuse while maintaining convergence guarantees.
Transductive off-Policy PPO (ToPPO) [Gan et al., 2024] builds on G-PPO by incorporating trans-
ductive learning principles, bridging the gap between off-policy learning and theoretical guarantees
of on-policy methods. Off-Policy PPO (OPPO) [Meng et al., 2023] proposes novel corrections to
integrate replay buffer samples in PPO-style updates.
On-Policy and Off-Policy Actor-Critic Methods. Actor-critic methods blend the strengths of
policy gradients and value function estimation. Off-policy variants aim to improve sample efficiency
bylearningfromareplaybuffer. TheOff-PolicyActor-Criticalgorithm[Degrisetal.,2012]introduces
importance weighting to enable stable updates from off-policy data. ACER [Wang et al., 2016]
extends this with trust-region optimization and truncated importance sampling, enhancing by that
the learning efficiency in discrete action spaces. Mixing on-policy and off-policy methods aims to
leveragethestabilityofon-policyupdateswiththeefficiencyofoff-policylearning. P3O[Fakooretal.,
2020]providesaprincipledapproachthatinterleavespolicyupdatesfrombothon-andoff-policydata.
Off-Policy RLHF and other variants of GRPO. Noukhovitch et al. [2025] introduced within
the iterative DPO framework an asynchronous RLHF using off-policy data and that ensures faster
convergence to the optimal policy. New variants of GRPO have been proposed recently such as
DAPO [Yu et al., 2025] and DR-GRPO [Liu et al., 2025]. DAPO proposes the zero variance masking
without theoretical backing, our work roots this in the improvement lower bound. DR-GRPO
proposes to center only the reward without using the variance normalization.
## 5. Experiments
## 5.1. Ablation Studies on GSM8K.
Setup, Model, and Data. In our first set of experiments, we use GSM8K dataset from Cobbe et al.
[2021] (MIT license), and Qwen/Qwen2.5-0.5B-Instruct (Apache 2.0 license) by Yang et al. [2024].
We integrate our changes in Algorithm 1 to the GRPO implementation in TRL [von Werra et al.,
2020b], and train our models on the training split of GSM8K on a node with 8 GPUs (GPU for
0
the vLLM server and 7 other GPUs for distributed training). See Appendix B for the hardware
specification. We use a learning 5×10−6 for all experiments and the KL regularizer β = 0.1 in
Equation (7). We use the correctness of the LLM output as a reward. For GRPO training, the

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 9
hyperparameters are the following: group size G = 16 and per-device batch size 16 (meaning each
GPU processes a single prompt x with 16 responses). To increase the overall batchsize we use
gradient accumulation of 4, ending with an effective batch size of prompts of 28. The context length
used for this experiment is 200, and the sampling temperature is set to τ = 0.1.
Ablations and Results. We train our models with GRPO using Algorithm 1 with a verifiable
reward for answer correctness. We use for GRPO different configurations given in Table 1 and report
on the test split of GSM8K Pass@1 using 50 samples (i.e. frequency of success given 50 generations for
each question) using the same sampling configuration as in training. We report results in Figure 2:
Fig. 2a for on-policy GRPO (i = 1,v = 1) with the objective given in Equation (7) with S = 3 (i.e.
for 4 epochs with π swap at end of each epoch with latest model); Fig. 2b for on-policy GRPO
ref
(i = 1,v = 1) with masking zero variance samples i.e. using the objective given Equation (8) with
S = 3; Fig. 2c for our off-policy GRPO (v = 10,i = 1), with S = 3 and Fig. 2d for Shao et al.
[2024]’s off-policy GRPO i.e (v = 1,i = 10) for a single epoch. We see in Fig. 2a that while the
on-policyGRPOconvergestoamaximumPass@1of45%itisunstable. Themaskingofzerovariance
sampling in 2b stabilizes the on-policy GRPO and leads to an improvement of the performance to
50%. This is in line with our theoretical grounding through the improvement lower bound. Our
off-policy GRPO in Fig. 2c stabilizes the training also and leads to an improved Pass@1 of 50% on
the test set. In all three cases, we see that by resetting the π to the latest model, GRPO amplifies
ref
the success rate above the current π , this concurs with the theoretical findings in Mroueh [2025].
ref
Finally,theoff-policyvariantinShaoetal.[2024]inFig.2dshowsaslowerconvergenceoveranepoch.
## 5.2. Finetuning Qwen Distill R1 model (1.5 B) on Deepscaler Data. In this section we use
GRPOtofinetuneDeepSeek-R1-Distill-Qwen-1.5B[Guoetal.,2025]onDeepScaleR-Preview-Dataset
from Luo et al. [2025] consisting of roughly 40K math questions with known answers. We used
math-verify as the verifiable reward. We use a learning rate of 1×10−6 in the same distributed
setting as before (GPU for vLLM and 7 GPUs for distributed training). We use a context length
0
of 4096, a group size G = 16, a per-device batch size of 16, and the KL regularizer is β = 0.001.
The sampling temperature used is 0.7. We compared here the on-policy GRPO (v = 1,i = 1) to our
off-policy GRPO (v = 10,i = 1) and report the performance of the trained model on a single epoch
(around 24 hours on a single node). We report in Tables 3 and 2 Aime24 and Math500 performance
using Huggingface light-eval [Habib et al., 2023]. Aime24 is evaluated with Pass@1 using 32 samples,
and math500 with extractive matching as recommended in light-eval with a context length of 32K
(evaluation context length and all other sampling hyperparameters are set to the default in OpenR1
for this model). Plots of evaluation as function of iterations are given in Appendix D. We see that
both on-policy and off-policy GRPO improve the performance of DeepSeek-R1-Distill-Qwen-1.5B
that has an Aime24 of 29% to 32% at maximum (over iterations), and its math-500 from 83% to
87%. This result confirms our theoretical results that by going off-policy we don’t loose in term of
overall performance.
Model/Aime24 Min Max Median Mean
v1-i1-length-4096 0.2802 0.3229 0.3021 0.3022
v10-i1-length-4096 0.2781 0.3250 0.3047 0.3049
Table 2. Aime24 using lighteval with on & off-policy ( (v1-i1) and (v10-i1))
GRPO.

## 10 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
(a) On-Policy GRPO with π swap at end of each (b) On-Policy GRPO with masking of samples with
ref
epoch. (v =1, i=1, S =3) varianceσ =0,andwithπ swapatendofeach
πk,r ref
epoch. v =1, i=1, S =3)
(c) Off-Policy GRPO using v =10 (this amounts to (d) Off-Policy GRPO using fixed samples from π
k
fixingthemodelonthevLLMserverfor10iterations for 10 iterations. This will make 1 epoch 10× slower.
andgettingfreshsamplesfornewbatches), andwith v =1, i=10, S =1)
π swap.(v =10, i=1, S =3)
ref
Figure 2. We train different variants of GRPO on the train portion of GSM8K and
report the Pass@1 on GSM8 test set using 50 samples for each question in the test
set for various variant of on-policy and off-policy GRPO. We see that as predicted by
our theory, masking samples with zero variance stabilizes the training for on-policy
training and leads to better performance. For off-policy training we see that using
v = 10,i = 1 stabilizes also the training and leads also to better performance.
Model/Math500 Min Max Median Mean
v1-i1-length-4096 0.830 0.870 0.854 0.8519
v10-i1-length-4096 0.822 0.872 0.846 0.8474
Table 3. Math 500 extractive matching using light-eval [Habib et al., 2023] with on
and off-policy (v1-i1) and (v10-i1) GRPO.
## 6. Conclusion and Discussion
We revisited (on-policy) GRPO [Shao et al., 2024] and showed that its clipping objective can be
derived from first principles as a lower bound for reward improvement. We also gave theoretical
grounding to masking of zero variance samples suggested in DAPO [Yu et al., 2025]. We introduced
off-policy GRPO and layed conditions under which it leads to policy improvement. Our off-policy
GRPO has the advantage of reducing communication costs in serving the model for inference
within the GRPO loop at each iteration as done in the on-policy counter-part, while not sacrificing

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 11
performance. We showcased that off-policy GRPO stabilizes training and leads to either on par or
improved performance as the on-policy one.
The main takeaways of our paper to practitioners are: (1) Zero variance masking stabilizes
on-policy GRPO’s training (2) Off-policy GRPO attains its full potential in terms of maintaining
performance and lowering latencies and communication overhead in larger scale training where
models are served using tensor parallelism (see vLLM [2025]).
We hope our proof of concept for off-policy GRPO will help enabling stable and efficient reinforce-
ment learning at scale.
## References
Y. Bai, A. Jones, K. Ndousse, A. Askell, A. Chen, N. DasSarma, D. Drain, S. Fort, D. Ganguli,
T. Henighan, et al. Training a helpful and harmless assistant with reinforcement learning from
human feedback. arXiv preprint arXiv:2204.05862, 2022.
P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei. Deep reinforcement
learning from human preferences. In I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach, R. Fergus,
S. Vishwanathan, and R. Garnett, editors, Advances in Neural Information Processing Systems,
volume 30. Curran Associates, Inc., 2017. URL https://proceedings.neurips.cc/paper_files/
paper/2017/file/d5e2c0adad503c91f91df240d0cd4e49-Paper.pdf.
K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton,
R. Nakano, C. Hesse, and J. Schulman. Training verifiers to solve math word problems. arXiv
preprint arXiv:2110.14168, 2021.
T. Degris, M. White, and R. S. Sutton. Off-policy actor-critic. arXiv preprint arXiv:1205.4839, 2012.
R. Fakoor, P. Chaudhari, and A. J. Smola. P3o: Policy-on policy-off policy optimization. In
Proceedings of The 35th Uncertainty in Artificial Intelligence Conference, pages 1017–1027. PMLR,
2020.
Y. Gan, R. Yan, X. Tan, Z. Wu, and J. Xing. Transductive off-policy proximal policy optimization.
arXiv preprint arXiv:2406.03894, 2024.
D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint
arXiv:2501.12948, 2025.
N. Habib, C. Fourrier, H. Kydlíček, T. Wolf, and L. Tunstall. Lighteval: A lightweight framework
for llm evaluation, 2023. URL https://github.com/huggingface/lighteval.
HuggingFace. Open r1: A fully open reproduction of deepseek-r1, January 2025a. URL https:
//github.com/huggingface/open-r1.
HuggingFace. Open r1: Update #3, Mar. 2025b. URL https://huggingface.co/blog/open-r1/
update-3. Accessed: 2025-05-11.
W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica.
Efficientmemorymanagementforlargelanguagemodelservingwithpagedattention. InProceedings
of the ACM SIGOPS 29th Symposium on Operating Systems Principles, 2023.
N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu,
N. Dziri, S. Lyu, et al. Tülu 3: Pushing frontiers in open language model post-training. arXiv
preprint arXiv:2411.15124, 2024.
Z. Liu, C. Chen, W. Li, P. Qi, T. Pang, C. Du, W. S. Lee, and M. Lin. Understanding r1-zero-like
training: A critical perspective, 2025. URL https://arxiv.org/abs/2503.20783.
M. Luo, S. Tan, J. Wong, X. Shi, W. Y. Tang, M. Roongta, C. Cai, J. Luo, T. Zhang, L. E. Li,
R. A. Popa, and I. Stoica. Deepscaler: Surpassing o1-preview with a 1.5b model by scaling rl.
https://tinyurl.com/5e9rs33z, 2025. Notion Blog.
W. Meng, Q. Zheng, G. Pan, and Y. Yin. Off-policy proximal policy optimization. Proceedings of
the AAAI Conference on Artificial Intelligence, 37(8):9162–9170, 2023.

## 12 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
Y. Mroueh. Reinforcement learning with verifiable rewards: Grpo’s effective loss, dynamics, and
success amplification, 2025. URL https://arxiv.org/abs/2503.06639.
M.Noukhovitch, S.Huang, S.Xhonneux, A.Hosseini, R.Agarwal, andA.Courville. Faster, moreeffi-
cient RLHF through off-policy asynchronous learning. In The Thirteenth International Conference
on Learning Representations, 2025. URL https://openreview.net/forum?id=FhTAG591Ve.
L.Ouyang, J.Wu, X.Jiang, D.Almeida, C.Wainwright, P.Mishkin, C.Zhang, S.Agarwal, K.Slama,
A. Ray, et al. Training language models to follow instructions with human feedback. Advances in
Neural Information Processing Systems, 35:27730–27744, 2022.
A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein,
L. Antiga, A. Desmaison, A. Köpf, E. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy,
B. Steiner, L. Fang, J. Bai, and S. Chintala. PyTorch: An Imperative Style, High-Performance
Deep Learning Library, Dec. 2019.
J. Queeney, I. C. Paschalidis, and C. G. Cassandras. Generalized proximal policy optimization with
sample reuse. In Advances in Neural Information Processing Systems, volume 34, 2021.
J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz. Trust region policy optimization. In
International conference on machine learning, pages 1889–1897. PMLR, 2015.
J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal policy optimization
algorithms. arXiv preprint arXiv:1707.06347, 2017.
Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv
preprint arXiv:2402.03300, 2024.
N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss, A. Radford, D. Amodei, and P. F.
Christiano. Learning to summarize with human feedback. Advances in Neural Information
Processing Systems, 33:3008–3021, 2020.
P. vLLM. Pytorch ci hud: vllm benchmark dashboard. https://hud.pytorch.org/benchmark/
llms?repoName=vllm-project/vllm, 2025. Accessed: 2025-05-14.
M. Vojnovic and S.-Y. Yun. What is the alignment objective of grpo?, 2025. URL https://
arxiv.org/abs/2502.18548.
L. von Werra, Y. Belkada, L. Tunstall, E. Beeching, T. Thrush, N. Lambert, S. Huang, K. Rasul, and
Q. Gallouédec. Trl: Transformer reinforcement learning. https://github.com/huggingface/trl,
2020a.
L. von Werra, Y. Belkada, L. Tunstall, E. Beeching, T. Thrush, N. Lambert, S. Huang, K. Rasul, and
Q. Gallouédec. Trl: Transformer reinforcement learning. https://github.com/huggingface/trl,
2020b.
Z. Wang, V. Bapst, N. Heess, V. Mnih, R. Munos, K. Kavukcuoglu, and N. De Freitas. Sample
efficient actor-critic with experience replay. arXiv preprint arXiv:1611.01224, 2016.
T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi, P. Cistac, T. Rault, R. Louf,
M. Funtowicz, J. Davison, S. Shleifer, P. von Platen, C. Ma, Y. Jernite, J. Plu, C. Xu, T. L. Scao,
S. Gugger, M. Drame, Q. Lhoest, and A. M. Rush. HuggingFace’s Transformers: State-of-the-art
Natural Language Processing, July 2020.
A. Yang, B. Yang, B. Hui, B. Zheng, B. Yu, C. Zhou, C. Li, C. Li, D. Liu, F. Huang, G. Dong,
H. Wei, H. Lin, J. Tang, J. Wang, J. Yang, J. Tu, J. Zhang, J. Ma, J. Yang, J. Xu, J. Zhou, J. Bai,
J. He, J. Lin, K. Dang, K. Lu, K. Chen, K. Yang, M. Li, M. Xue, N. Ni, P. Zhang, P. Wang,
R. Peng, R. Men, R. Gao, R. Lin, S. Wang, S. Bai, S. Tan, T. Zhu, T. Li, T. Liu, W. Ge, X. Deng,
X. Zhou, X. Ren, X. Zhang, X. Wei, X. Ren, X. Liu, Y. Fan, Y. Yao, Y. Zhang, Y. Wan, Y. Chu,
Y. Liu, Z. Cui, Z. Zhang, Z. Guo, and Z. Fan. Qwen2 Technical Report, Sept. 2024.
Q. Yu, Z. Zhang, R. Zhu, Y. Yuan, X. Zuo, Y. Yue, T. Fan, G. Liu, L. Liu, X. Liu, H. Lin, Z. Lin,
B. Ma, G. Sheng, Y. Tong, C. Zhang, M. Zhang, W. Zhang, H. Zhu, J. Zhu, J. Chen, J. Chen,
C. Wang, H. Yu, W. Dai, Y. Song, X. Wei, H. Zhou, J. Liu, W.-Y. Ma, Y.-Q. Zhang, L. Yan,
M. Qiao, Y. Wu, and M. Wang. Dapo: An open-source llm reinforcement learning system at scale,

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 13
## 2025. URL https://arxiv.org/abs/2503.14476.

## 14 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
Appendix A. Broader Impact and Limitations
Our work analyzes the celebrated GRPO algorithm and develops an adaptation for the off-
policy setting motivated by recent efforts for PPO that demonstrated higher stability and efficiency.
Our primary contributions are theoretical, providing formal conditions under which advantage
optimization guarantees policy improvement for the on-policy and off-policy regimes. These insights
provide lower bounds on policy improvement and directly inform a practical clipped surrogate
optimization objective for large language model (LLM) policy training that inherits our theoretical
guarantees for both on policy and off policy regimes. In the on-policy regime our lower bound
shed the light and give theoretical backing to the benefits of masking samples with zero variance as
suggested in the DAPO paper [Yu et al., 2025]. Our formulation also clarifies theoretical relationships
between our newly introduced off-policy GRPO, PPO variants, and general off-policy optimization
frameworks – a linkage previously underexplored in the literature. Our derived off-policy GRPO
algorithm is validated experimentally demonstrating improved performance compared to standard
GRPO, while having the potential to reduce the communication overhead across devices in serving
large models for sampling that is needed in GRPO. The broader impacts that we anticipate from
our work (beside those directly inherited from GRPO and reinforcement fine-tuning of LLMs and
the risks associated to the dual use of the enabled reasoning models) are then generally positive, as
it enhances RL efficiency, reducing computational costs and improving stability.
The main limitation of our work is that the empirical validation remains constrained to smaller
datasets, smaller model architectures, and smaller context size (4096 tokens at maximum) that can
be trained on our hardware setup consisting of one compute node with 8 H100 NVIDIA gpus (1
used for the vLLM server and 7 for training the policy LLM). Our 1.5 B experimental setup, with
deepscaler data is at the limit of what can fit in the memory of a single node.
This limitation primarily reflects the common resource constraints associated with provisioning
large-scale distributed training environments, rather than any inherent restriction of the algorithm
itself. Note that for larger context, larger batch size and larger architectures than the ones used in
our paper, multi-node training is required.
While our main contribution here remains theoretical and backed with ablation studies on a
single node, we reserve to scale up our experiments to larger training runs in future work aimed at
showcasing the fact that the benefits of our off-policy algorithms in terms of efficient and reduced
communication are expected to become even more pronounced in the large-scale distributed regime
as it is already showed in multiple off policy RL works.
Appendix B. Assets
Hardware setup. All our experiments were run on one compute node with Dual 48-core Intel Xeon
8468, 2TB of RAM, 8 NVIDIA HGX H100 80GB SMX5, 8x 3.4TB Enterprise NVMe U.2 Gen4, and
10x NVIDIA Mellanox Infiniband Single port NDR adapters, running RedHat Enterprise Linux 9.5
Libraries. Our experiments rely on the open-source libraries pytorch [Paszke et al., 2019] (license:
BSD), HuggingFace Transformers [Wolf et al., 2020] (Apache 2.0 license), and HuggingFace TRL
[von Werra et al., 2020a] (Apache 2.0 license). We also relied on Open-R1 [HuggingFace, 2025a] as
well as light-eval [Habib et al., 2023] for the evaluation of Aime24 and Math500.
Code re-use. Our GRPO training code is based on the public Github repository https://
github.com/huggingface/open-r1 [HuggingFace, 2025a].
Data and Models. In our experiments, we use following publicly available datasets: (1) GSM8K
dataset from Cobbe et al. [2021] (MIT license), and (2) the DeepScaleR-Preview-Dataset from Luo
et al. [2025] (MIT license). The models that we used were Qwen/Qwen2.5-0.5B-Instruct (Apache

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 15
2.0 license) by Yang et al. [2024], and DeepSeek-R1-Distill-Qwen-1.5B (MIT license) by Guo et al.
[2025].
Appendix C. Reward Improvement Lower Bound
C.1. Proof of Theorem 1. We have :
J(π(·|x)) = E r(x,y)
y∼π(·|x)
Let π be the current policy and α(·|x) be another policy typically consider α(·|x) = π (·|x).
k k−i
Define mean and variances of the off-policy reward, i.e policy under α:
(cid:113)
µ (x) = E r(x,y) and σ (x) = E (r(x,y)−µ (x))2, and denote for 0 < ε < 1:
α y∼α(·|x) α y∼α(·|x) α
(cid:112)
σ (x) = σ2(x)+ε.
α,ε α
Note that we have a bounded reward 0 ≤ r(x,y) ≤ ∥r∥ which implies that σ2(x) ≤
∥r∥2
∞, and
∞ α 4
hence we have:
(cid:115)
∥r∥2
σ (x) ≤ ∞ +ε.
α,ε
4
(cid:113)
∥r∥2
We normalize the reward so that : σ (x) ≤ ∞ +ε ≤ 1.
α,ε 4
We denote GRPO advantage function as:
r(x,y)−µ (x)
α
A (x,y) =
α
σ (x)
α,ε
π(y|x)
L (π(·|x)) = E A (x,y)
α y∼α(·|x)α(y|x) α
If α = π , we obtain the online policy objective function of GRPO, where the advantage is
k
computed with the current policy π , i.e using A (x,y).
k π k
We have:
L (π(·|x)) =
1 (cid:0)E
r(x,y)−µ (x)
(cid:1)
α σ (x) y∼π(·|x) α
α,ε
1 1
= J(π(·|x))− J(α(·|x))
σ (x) σ (x)
α,ε α,ϵ
Our goal is to provide an upper bound on :
L (π(·|x))−(J(π(·|x))−J(π (·|x)))
α k
Hence we have:
(cid:18) (cid:19)
1 1
L (π(·|x))−(J(π(·|x))−J(π (·|x))) = −1 J(π(·|x))+J(π (·|x))− J(α(·|x))
α k k
σ (x) σ (x)
α,ε α,ε
(cid:18) (cid:19)
1 1
= −1 (J(π(·|x))−J(α(·|x))+J(α(·|x)))+J(π (·|x))− J(α(·|x))
k
σ (x) σ (x)
α,ε α,ε
1−σ (x) 1 1
α,ε
= (J(π(·|x))−J(α(·|x)))+(J(π (·|x))−J(α(·|x)))+ J(α(·|x))− J(α(·|x))
k
σ (x) σ (x) σ (x)
α,ε α,ε α,ε
1−σ (x)
α,ε
= (J(π(·|x))−J(α(·|x)))+(J(π (·|x))−J(α(·|x)))
k
σ (x)
α,ε
Lemma 1 (Kantorovich-Rubenstein duality of total variation distance, see ). The Kantorovich-
Rubenstein duality (variational representation) of the total variation distance is as follows:
1
TV(m ,m ) = sup {E [g(Z)]−E [g(Z)]}, (9)
1 2
2L
Z∼m1 Z∼m2
g∈GL

## 16 REVISITING GROUP RELATIVE POLICY OPTIMIZATION
where G = {g : Z → R,||g|| ≤ L}.
L ∞
On the other hand using Lemma 1 we have:
J(π(·|x))−J(α(·|x)) ≤ 2∥r∥ TV(π(·|x),α(·|x))
∞
and
J(π (·|x))−J(α(·|x)) ≤ 2∥r∥ TV(π (·|x),α(·|x))
k ∞ k
By our assumption on the reward we have :
1−σ (x)
α,ε
≥ 0
σ (x)
α,ε
so that we obtain the final bound as follows:
1−σ (x)
L (π(·|x))−(J(π(·|x))−J(π (·|x))) ≤ 2 α,ε ∥r∥ TV(π(·|x),α(·|x))+2∥r∥ TV(π (·|x),α(·|x))
α k σ (x) ∞ ∞ k
α,ε
We obtain finally our lower bound on policy improvement as follows:
1−σ (x)
J(π(·|x))−J(π (·|x)) ≥ L (π(·|x))−2 α,ε ∥r∥ TV(π(·|x),α(·|x))−2∥r∥ TV(π (·|x),α(·|x))
k α σ (x) ∞ ∞ k
α,ε
Integrating over x (the prompts) we have:
1−σ (x)
E J(π(·|x))−E J(π (·|x)) ≥ E L (π(·|x))−2∥r∥ E α,ε TV(π(·|x),α(·|x))
x∼ρX x∼ρX k x∼ρX α ∞ x∼ρX σ (x)
α,ε
−2∥r∥ E TV(π (·|x),α(·|x))
∞ x∼ρX k
(cid:115)
(1−σ (x))2(cid:113)
≥ E L (π(·|x))−2∥r∥ E α,ε E TV2(π(·|x),α(·|x))−2∥r∥ E TV(π (·|x),α(·|x))
x∼ρX α ∞ x∼ρX σ2 (x) x∼ρX ∞ x∼ρX k
α,ε
Appendix D. Experiments

REVISITING GROUP RELATIVE POLICY OPTIMIZATION 17
(a) Aime 24
(b) Math 500.
Figure 3. Aime 24/ Math 500

## My Notes

-
-
-
-
-