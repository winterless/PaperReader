1) 结论

- 贡献1：论文提出了 Transformer，作为“完全基于 attention 的序列转导模型”，用 multi-head self-attention 替换了传统 encoder-decoder 里的 recurrence（以及卷积主干），核心目标是提升并行性并保留/提升效果。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `Abstract`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `1 Introduction`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `7 Conclusion`]
- 贡献2：论文给出了 Scaled Dot-Product Attention 与 Multi-Head Attention 的具体设计动机：通过 1/sqrt(d_k) 缩放缓解大维度下 softmax 梯度过小问题；通过多头并行投影提升不同子空间建模能力。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `3.2.1 Scaled Dot-Product Attention`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `3.2.2 Multi-Head Attention`]
- 贡献3：在 WMT14 英德/英法翻译任务上，文中报告 Transformer 达到当时 SOTA 级别结果，同时训练成本显著下降，支撑“质量+效率”双收益主张。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `Abstract`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `6.1 Machine Translation`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `5.2 Hardware and Schedule`]

2) 依据

- 对“架构创新”的直接证据：Abstract 与 Introduction 明确写到 Transformer “dispensing with recurrence and convolutions entirely / relying entirely on attention”，Conclusion 再次确认其为首个 entirely-attention 的序列转导模型。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `Abstract`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `1 Introduction`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `7 Conclusion`]
- 对“核心机制”的直接证据：3.2.1 说明缩放点积注意力的计算与缩放理由（避免 d_k 大时点积过大导致梯度问题）；3.2.2 说明多头并行投影、拼接再投影，以及 h=8、d_k=d_v=64 的实现选择与成本说明。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `3.2.1 Scaled Dot-Product Attention`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `3.2.2 Multi-Head Attention`]
- 对“顺序信息处理”的直接证据：3.5 指出由于无 recurrence/convolution，必须显式注入位置信息；采用 sinusoidal positional encoding，并报告 learned positional embedding 与其结果接近（Table 3(E)）。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `3.5 Positional Encoding`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `6.2 Model Variations`]
- 对“性能与效率”的直接证据：6.1 报告英德 28.4 BLEU、3.5 天/8×P100，且称超过既有模型（含 ensemble）；5.2 给出 base/big 的训练时长与步数；Table 2 给出与其他模型的 BLEU 与 FLOPs 对比。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `6.1 Machine Translation`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `5.2 Hardware and Schedule`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `5.4 Regularization`]

3) 下一步阅读建议

- 阅读顺序1：`Convolutional sequence to sequence learning`（文中 [9]）。理由：本文在 Table 2/Section 4 中与卷积序列模型做了直接效率与路径长度讨论，先读它有助于理解 Transformer 相比 ConvS2S 的关键差异。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `4 Why Self-Attention`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `6.1 Machine Translation`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `References`]
- 阅读顺序2：`Google's neural machine translation system: Bridging the gap between human and machine translation`（文中 [38]）。理由：本文在结果和解码设置中多次以 GNMT 系列为比较对象；读完 [9] 后读 [38]，更容易从“卷积/循环基线 -> 全 attention 架构”形成完整对照。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `6.1 Machine Translation`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `References`]
- 说明：若将“后续论文”严格限定为“2017 年后发表且由本文直接点名推荐”，本文未给出明确名单。I cannot verify this from current repository sources.

最易误解点（2个）

- 误解点1：“Transformer 不需要任何位置信息。”更准确地说：它不使用 recurrence/convolution，但明确需要并添加 positional encoding；否则无法表达 token 顺序。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `3.5 Positional Encoding`]
- 误解点2：“多头注意力只是参数堆叠，计算一定更贵。”文中给出的设置是每头降维（d_k=d_v=d_model/h），并声称总计算成本与全维单头相近，核心收益在于子空间并行建模。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `3.2.2 Multi-Head Attention`]

可复现实验切入点（1个）

- 建议做一个最小可复现 ablation：固定 base 配置（N=6, d_model=512, d_ff=2048, h=8, dropout=0.1, label smoothing=0.1, 100K steps），只改一个变量并复现实验趋势：  
  (a) 改 attention 头数 h（对照 Table 3 的 A 组）；或  
  (b) 把 sinusoidal positional encoding 换成 learned positional embedding（对照 Table 3 的 E 组）。  
  评价指标用 dev PPL/BLEU，训练策略按文中 Adam + warmup=4000 + inverse-sqrt decay 复现。[source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `6.2 Model Variations`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `5.3 Optimizer`][source: `inbox/md_converted/foundation__attention_is_all_you_need_2017.md` -> `5.4 Regularization`]
