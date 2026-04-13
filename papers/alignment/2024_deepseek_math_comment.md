# deepseekmath_comment

### 1) 结论
* **构建了 120B 高质量数学预训练语料**：通过一套精心设计的数据迭代筛选管道，从 Common Crawl 中成功提取了海量高质量的数学专属网页数据（DeepSeekMath Corpus）。
* **提出去 Critic 模型的 GRPO 算法**：引入了组相对策略优化（Group Relative Policy Optimization），摒弃了传统 PPO 中与策略模型同等大小的价值模型（Value/Critic Model），通过组内得分标准化来估计基线，大幅缩减了强化学习的显存开销。
* **刷新开源 7B 模型的数学极限**：基于纯代码模型（DeepSeek-Coder-v1.5）继续预训练，在无外部工具和多数投票的情况下，MATH 基准测试达到 51.7%，逼近 GPT-4 早期水平。

### 2) 依据
* **证据一**：明确说明了 120B token 数据集的收集管道与质量验证机制。 *(因无附加文件，暂标注外部版本)*
* **证据二**：指出 GRPO 的核心机制是摒弃价值网络（"foregoes the critic model, instead estimating the baseline from group scores"）。 *(因无附加文件，暂标注外部版本)*
* **证据三**：给出了 MATH 测评的 51.7% 与 60.9% (Self-consistency) 的确切数据对标。 *(因无附加文件，暂标注外部版本)*

### 3) 下一步阅读建议
* **阅读 1**：《DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning》
    * **理由**：这篇是 GRPO 算法真正"破圈"的后续核心工作，它证明了在仅使用强化学习和规则奖励（甚至不需要 SFT）的情况下，就能依靠 GRPO 激发出模型卓越的零样本逻辑思维能力。
* **阅读 2**：《REVISITING GROUP RELATIVE POLICY OPTIMIZATION: INSIGHTS INTO ON-POLICY AND OFF-POLICY TRAINING》
    * **理由**：这是前置探讨过的 IBM 论文，它为 GRPO 补全了严密的数学提升下界，并探讨了通过异策略（Off-policy）进一步降低大规模集群通信开销的系统级方案。

---

### 最易误解点
1. **GRPO 只能用于数学题**：容易误以为该算法深度绑定数学领域。实际上只要任务目标有清晰的可验证反馈（Verifiable Rewards，如代码编译状态、Json 格式校验），GRPO 就能作为一种通用的低显存 RL 框架。
2. **"学好数学只需多读数学书"**：容易忽略底座模型的特性。论文中强调了"在代码模型基础上继续训练数学"，证明了 Code 预训练是提升模型严格逻辑和后续工具使用能力（Tool-use）的关键先决条件。

### 可复现实验切入点
* **GRPO 的单节点显存与吞吐量验证**：基于 HuggingFace TRL（目前已原生集成 GRPO），使用小参数模型（如 Qwen2.5-0.5B）和 GSM8K 训练集，严格控制相同的 Batch Size，实测带有 Critic 的标准 PPO 与去 Critic 的 GRPO 在实际显存占用（VRAM Profile）和吞吐率（Tokens/sec）上的显著差异。
