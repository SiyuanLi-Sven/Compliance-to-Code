# 📚 TOMORIN: A Legal Domain Benchmark for Evaluating LLMs on Translating Ordinances into Machine-operable Regulatory Inferences

<!-- [![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Last Updated](https://img.shields.io/badge/Last%20Updated-2025--04-green.svg)](https://github.com/SiyuanLi-Sven/TOMORIN) -->

> A Legal Domain Benchmark for Evaluating LLMs on Translating Ordinances into Machine-operable Regulatory Inferences

👤 Maintainer

**Siyuan LI**
* Email: lisiyuansven@foxmail.com


# 0. 📝 Abstract

略.

# 1. 🗂️ Project Structure

## Directory Tree
```tree
meu_graph_v2/                         # Root directory
├── MEU_to_code/
│   ├── MEU_code/
│   │   ├── GT/
│   │   └── raw_response/
│   └── MEU_selected_with_relation_GT/
├── converter/                  # 临时文件转换路径
├── data_simulation/
│   ├── data_generated/
│   └── data_labeled/
└── law_to_MEU/             # 法条拆解为MEU的任务
    ├── st_0_law_docx/  
    │   └── with_appendix/ 
    ├── st_1_law_csv/  
    ├── st_2_law_keywords_definitions/
    │   ├── GT/   # 人类标注的 Ground Truth, 下同
    │   └── raw_response/    # 模型原始回复, 下同
    ├── st_3_0_MEU/
    │   ├── GT/
    │   └── raw_response/
    ├── st_3_1_inner_relations/
    │   ├── GT/
    │   └── raw_response/
    ├── st_4_MEU_relations/
    │   ├── MEU_with_relation/  # 将MEU与relation一起保存的格式
    │   │   └── GT/  # 这是后续coding和评估会使用的GT
    │   └── raw_response/
    ├── st_5_MEU_Graph_HTML/
    │   └── GT/    # 用GT数据的MEU Graph可视化
    └── st_6_MEU_evaluate/    # 用LLM对MEU进行评分
        ├── GT/    # 人类的评分结果
        └── raw_response/
```

# 2. 代码说明

## 2.0 数据格式约定

使用csv格式文件时, encoding设置为utf-8-sig. 
 - 这是为了方便采用excel打开和检查. 
 - 但注意不要使用excel保存, 这可能丢失信息. 

llm的原始回复也即raw_response文件夹下面都是csv的. llm回复经过解析后的格式都是xlsx的. GT的MEU也都是xlsx的. 
 - 这样做主要是为了和我们的数据标注平台进行联动. 数据标注平台只支持xlsx格式. 
 - 在VS Code中安装Open插件即可用系统默认应用打开xlsx文件. 


完整的MEU Graph数据的columns:
`["MEU_id", "subjec", "condition", "constraint", "contextual_info", "relation", "target"]`
 - 有时候会有confirmed, comments和comments_relation



## 2.1 法条转化为MEU Graph的任务

`st_1_get_law_from_doc.ipynb`
将docx格式的法律法规文件转化为csv格式, 每行为一个法条. 


`st_2_get_keywords_and_definition.ipynb`
从整个法律中提取关键词和全局定义, 方便后续处理局部时调用. 


`st_3_0_get_MEU_from_law.ipynb`
将法条拆分为MEU, 每次输入一个法条, 输出该法条下属的若干MEU. 


`st_3_1_get_inner_relation.ipynb`
输入一个法条和该法条中的一个MEU, 找到MEU之间的关系(且, 或, 非等关系)


`st_4_get_relation_from_MEU.ipynb`
对于每个relation, 对于每个法律文件, 输入该法律法规文件下的所有MEU, 让LLM找到其中的所有该relation的情况. 


`st_5_draw_MEU_Graph.ipynb`
用pyechart绘制有relation的decision graph. 采用GT_MEU和生成的relation. 仅做可视化用. 


`st_5_draw_MEU_Graph_GT.ipynb`
用pyechart绘制有relation的decision graph. 采用GT_MEU和GT_relation. 仅做可视化用. 


`csv_xlsx_convert.ipynb`
将 csv 和 xlsx 相互转换, 适应数据标注工作的需要. 
将 MEU 和 relation 合并为 MEU_with_relation 格式. 这是我们 MEU Graph 的标准数据格式. 


## 2.2 MEU Graph 的 evaluate

`st_6_MEU_evaluate.ipynb`
读取生成的MEU和GT_MEU, 检查每个GT_MEU被回应的情况. 


## 2.3 Data Simulation

### 生成的数据


### 标注的数据


## 2.4 MEU Coding 任务

### 2.4.1 根据 MEU 生成代码

#### 生成的代码

#### 标注的GT代码


### 2.4 1 根据 Graph 执行代码






