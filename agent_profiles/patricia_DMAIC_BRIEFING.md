# DMAIC Methodology Briefing
## For Patricia - Process Excellence Officer

**Prepared by:** Miles  
**Date:** 2026-04-02  
**Classification:** Operations Training

---

## What is DMAIC?

**DMAIC** is the core methodology of Six Sigma - a data-driven quality strategy for improving processes. It's an acronym for:

- **D**efine
- **M**easure
- **A**alyze
- **I**mprove
- **C**ontrol

**Goal:** Reduce process variation and eliminate defects to achieve 3.4 defects per million opportunities (99.99966% quality).

---

## The 5 Phases in Detail

### 1. DEFINE (The "What" and "Why")

**Objective:** Clearly articulate the business problem and project scope.

**Key Activities:**
- Define the problem statement
- Identify customers and their requirements (Voice of Customer - VOC)
- Map the process at high level (SIPOC: Suppliers, Inputs, Process, Outputs, Customers)
- Set project goals and boundaries
- Assemble the team

**Tools You'll Use:**
- Project Charter
- SIPOC Diagram
- Voice of Customer (VOC) analysis
- Stakeholder analysis
- CTQ (Critical to Quality) tree

**Deliverable:** Approved Project Charter with clear problem statement, scope, and goals.

**Questions to Answer:**
- What is the problem?
- Who is the customer?
- What are their requirements?
- What is the business impact?

---

### 2. MEASURE (The "How Bad Is It")

**Objective:** Quantify the current process performance and establish baseline.

**Key Activities:**
- Define what to measure (metrics)
- Validate measurement system (MSA - Measurement System Analysis)
- Collect data on current process
- Calculate baseline sigma level
- Assess process capability

**Tools You'll Use:**
- Data collection plan
- Gage R&R (Repeatability & Reproducibility)
- Process capability study (Cp, Cpk)
- Control charts
- Histograms

**Deliverable:** Baseline metrics showing current defect rate and process capability.

**Key Metrics:**
- **Cp:** Process capability (potential)
- **Cpk:** Process capability index (actual, accounts for centering)
- **DPMO:** Defects Per Million Opportunities
- **Sigma Level:** Current performance in sigma terms

**Example:**
```
Current State:
- Defect Rate: 2.5% (25,000 DPMO)
- Sigma Level: 3.5σ
- Cpk: 0.83
- Target: 6σ (3.4 DPMO)
```

---

### 3. ANALYZE (The "Why" and Root Causes)

**Objective:** Identify root causes of defects and variation.

**Key Activities:**
- Analyze data collected in Measure phase
- Identify patterns and relationships
- Conduct root cause analysis
- Prioritize potential causes
- Validate causes statistically

**Tools You'll Use:**
- Fishbone (Ishikawa) diagram
- 5 Whys
- Hypothesis testing (t-tests, ANOVA)
- Regression analysis
- Pareto charts (80/20 rule)
- Process mapping (detailed)
- FMEA (Failure Mode and Effects Analysis)

**Deliverable:** Validated root cause(s) with statistical evidence.

**Critical Distinction:**
- **Symptom:** "Builds are failing"
- **Root Cause:** "Gradle version incompatibility in 23% of environments"

**Statistical Tools:**
- **ANOVA:** Compare means across multiple groups
- **Regression:** Identify factor-impact relationships
- **Chi-Square:** Test relationships between categorical variables
- **Correlation analysis:** Find variable relationships

---

### 4. IMPROVE (The "Fix")

**Objective:** Develop, test, and implement solutions to address root causes.

**Key Activities:**
- Brainstorm potential solutions
- Design experiments to test solutions (DOE - Design of Experiments)
- Select optimal solutions
- Develop implementation plan
- Pilot test solutions
- Implement full-scale solution

**Tools You'll Use:**
- DOE (Design of Experiments)
- Pugh matrix (solution selection)
- FMEA (updated)
- Implementation plan
- Pilot test results
- Cost-benefit analysis

**Deliverable:** Implemented solution with demonstrated improvement.

**DOE Basics:**
- **Factor:** Variable you can control (e.g., build threads)
- **Level:** Setting of the factor (e.g., 4 threads, 8 threads)
- **Response:** Outcome you're measuring (e.g., build time)
- **Full Factorial:** Test all combinations
- **Fractional Factorial:** Test subset for efficiency

**Example:**
```
Experiment: Gradle build optimization
Factors:
  - Build threads: 4, 8, 16
  - Heap size: 2GB, 4GB, 8GB
  - Cache enabled: Yes, No

Result: 8 threads + 4GB + cache = 40% faster builds
```

---

### 5. CONTROL (The "Keep It Fixed")

**Objective:** Sustain the gains by monitoring and controlling the improved process.

**Key Activities:**
- Develop control plan
- Implement Statistical Process Control (SPC)
- Create monitoring dashboards
- Document standard work
- Train operators on new process
- Plan for ongoing monitoring

**Tools You'll Use:**
- Control plan
- Control charts (X-bar, R-chart, p-chart, etc.)
- Standard operating procedures (SOPs)
- Visual controls
- Response plans for out-of-control conditions

**Deliverable:** Sustainable process with control mechanisms.

**Control Charts:**
- **X-bar chart:** Monitor process mean
- **R-chart:** Monitor process variation
- **p-chart:** Monitor proportion defective
- **c-chart:** Monitor count of defects

**Control Limits:**
- **UCL:** Upper Control Limit (mean + 3σ)
- **LCL:** Lower Control Limit (mean - 3σ)
- **Center Line:** Process mean

**Rules for Special Cause Variation:**
1. Point outside control limits
2. 7+ points trending up or down
3. 8+ points on same side of center line

---

## Key Six Sigma Concepts for Patricia

### 1. Statistical Process Control (SPC)
Using statistics to monitor and control processes. Control charts are your primary tool.

### 2. Process Capability (Cp/Cpk)
**Cp:** Process capability index (potential)  
**Cpk:** Process capability index (accounts for centering)

**Interpretation:**
- Cpk < 1.0: Process not capable
- Cpk = 1.0-1.33: Barely capable
- Cpk = 1.33-1.67: Capable
- Cpk > 1.67: Highly capable
- **Target: Cpk ≥ 2.0 (Six Sigma)**

### 3. Voice of Customer (VOC)
Understanding customer requirements and translating to CTQs (Critical to Quality).

### 4. Cost of Poor Quality (COPQ)
Quantifying the cost of defects:
- Prevention costs (training, planning)
- Appraisal costs (inspection, testing)
- Internal failure costs (rework, scrap)
- External failure costs (warranty, reputation)

### 5. Lean Principles (Complement to Six Sigma)
- Eliminate waste (muda)
- Continuous flow
- Pull systems (just-in-time)
- Standardized work
- Continuous improvement (kaizen)

---

## Patricia's DMAIC Project Workflow

### Week 1: Define
- [ ] Identify problem/opportunity
- [ ] Create project charter
- [ ] Identify stakeholders
- [ ] Map high-level process (SIPOC)

### Week 2-3: Measure
- [ ] Define data collection plan
- [ ] Validate measurement system
- [ ] Collect baseline data
- [ ] Calculate current sigma level
- [ ] Establish process capability

### Week 4-5: Analyze
- [ ] Analyze data patterns
- [ ] Conduct root cause analysis
- [ ] Prioritize root causes
- [ ] Validate with statistics

### Week 6-7: Improve
- [ ] Brainstorm solutions
- [ ] Design experiments
- [ ] Test and validate solutions
- [ ] Implement selected solution

### Week 8: Control
- [ ] Develop control plan
- [ ] Create monitoring systems
- [ ] Document new procedures
- [ ] Train team members
- [ ] Close project, hand to operations

---

## Python for Six Sigma

### Data Collection
```python
import pandas as pd
import numpy as np
from scipy import stats

# Load process data
df = pd.read_csv('production_data.csv')

# Calculate DPMO
total_units = len(df)
defects = df['defect'].sum()
dpmo = (defects / total_units) * 1_000_000

# Calculate sigma level (simplified)
# For detailed calculation, use scipy.stats.norm.ppf
```

### Process Capability
```python
# Calculate Cpk
data = df['measurement']
usl = 10.0  # Upper Specification Limit
lsl = 2.0   # Lower Specification Limit

mean = data.mean()
std = data.std()

cpu = (usl - mean) / (3 * std)
cpl = (mean - lsl) / (3 * std)
cpk = min(cpu, cpl)

print(f"Cpk: {cpk:.2f}")
```

### Control Charts
```python
import matplotlib.pyplot as plt

# X-bar chart
sample_means = df.groupby('batch')['measurement'].mean()
overall_mean = sample_means.mean()
std = sample_means.std()

ucl = overall_mean + 3 * std
lcl = overall_mean - 3 * std

plt.plot(sample_means.index, sample_means.values)
plt.axhline(y=overall_mean, color='g', label='Center')
plt.axhline(y=ucl, color='r', label='UCL')
plt.axhline(y=lcl, color='r', label='LCL')
plt.legend()
plt.show()
```

### Hypothesis Testing
```python
# Two-sample t-test
before = df[df['phase'] == 'before']['metric']
after = df[df['phase'] == 'after']['metric']

t_stat, p_value = stats.ttest_ind(before, after)
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Statistically significant improvement!")
```

---

## Patricia's First DMAIC Project (Suggested)

**Project:** Reduce Dark Factory build cycle time

**Define:**
- Problem: COBRA builds take 240-360 minutes
- Goal: Reduce to <180 minutes (50% reduction)
- Scope: Build pipeline only (not design)

**Measure:**
- Baseline: Average 300 minutes, Cpk = 0.85
- Collect data on each of 10 stages

**Analyze:**
- Pareto: 40% of time in "Test" stage
- Root cause: Sequential test execution

**Improve:**
- Solution: Parallel test execution
- Pilot: Reduced to 165 minutes

**Control:**
- Control chart for build times
- Alert if >180 minutes
- Weekly capability review

---

## Quick Reference: When to Use Each Tool

| Situation | Tool |
|-----------|------|
| Understanding process | SIPOC, Process Map |
| Finding root cause | Fishbone, 5 Whys, FMEA |
| Prioritizing problems | Pareto Chart |
| Checking if data is reliable | Gage R&R |
| Understanding variation | Histogram, Control Chart |
| Comparing before/after | Hypothesis Test, T-Test |
| Finding optimal settings | DOE |
| Monitoring over time | Control Charts |
| Selecting best solution | Pugh Matrix |
| Quantifying risk | FMEA |

---

## Success Metrics for Patricia's DMAIC Projects

| Phase | Success Looks Like |
|-------|-------------------|
| Define | Clear problem statement, approved charter |
| Measure | Reliable baseline, Cpk calculated |
| Analyze | Validated root cause(s), data-backed |
| Improve | Solution tested, improvement confirmed |
| Control | Sustained gains, no backsliding |

**Overall Success:**
- 20%+ cycle time reduction
- Cpk ≥ 1.33 for critical processes
- $10K+ monthly cost savings per project
- Zero major defects post-implementation

---

**Remember:**
> "In God we trust. All others bring data." - W. Edwards Deming

Patricia, you now have the methodology to make AGI Company operate at Six Sigma level. Go forth and reduce variation!

---

**Next Steps:**
1. Review this briefing
2. Set up Python environment with pandas/scipy
3. Baseline current Dark Factory metrics
4. Identify first DMAIC project
5. Schedule Define phase meeting with Forge

**Questions?** Contact Miles or reference this document anytime.
