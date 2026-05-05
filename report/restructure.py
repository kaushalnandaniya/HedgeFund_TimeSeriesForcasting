import re
import os

base_dir = "/Users/kaushalnandaniya/Desktop/MnC/sem-6/AF/HedgeFund_TimeSeriesForcasting/report/chapters/"

def read_file(filename):
    with open(os.path.join(base_dir, filename), "r") as f:
        return f.read()

def write_file(filename, content):
    with open(os.path.join(base_dir, filename), "w") as f:
        f.write(content)

ch1 = read_file("ch01_introduction.tex")
ch2 = read_file("ch02_competition.tex")
ch3 = read_file("ch03_data.tex")
ch4 = read_file("ch04_eda.tex")
ch5 = read_file("ch05_classical.tex")
ch6 = read_file("ch06_deep.tex")
ch7 = read_file("ch07_results.tex")
ch8 = read_file("ch08_conclusion.tex")

# Chapter 1: Introduction
new_ch1 = "\\chapter{Introduction}\n\\label{ch:introduction}\n\n"
# Extract intro figure
intro_fig = re.search(r"\\begin\{figure\}.*?\\end\{figure\}", ch1, re.DOTALL).group(0)
new_ch1 += intro_fig + "\n\n"
new_ch1 += "\\section{Background and Motivation}\n"
new_ch1 += re.search(r"\\section\{Motivation and Background\}(.*?)\\section\{Project Objectives\}", ch1, re.DOTALL).group(1).strip() + "\n\n"
new_ch1 += "\\section{Problem Statement}\n"
new_ch1 += re.search(r"\\section\{Competition Description\}(.*?)\\section\{Competition Timeline\}", ch2, re.DOTALL).group(1).strip() + "\n\n"
new_ch1 += "\\section{Objectives}\n"
new_ch1 += re.search(r"\\section\{Project Objectives\}(.*?)\\section\{Report Structure\}", ch1, re.DOTALL).group(1).strip() + "\n\n"
write_file("01_introduction.tex", new_ch1)

# Chapter 2: Data Source
new_ch2 = "\\chapter{Data Source}\n\\label{ch:data_source}\n\n"
new_ch2 += "\\section{Origin of the dataset}\n"
new_ch2 += re.search(r"\\section\{Data Schema\}(.*?)\\chapter\{Exploratory Data Analysis\}", ch2 + "\n\\chapter{Exploratory Data Analysis}", re.DOTALL).group(1).strip() + "\n\n"
new_ch2 += "\\section{Data Characteristics}\n"
new_ch2 += re.search(r"\\section\{Dataset Overview\}(.*?)\\section\{Weight Distribution\}", ch3, re.DOTALL).group(1).strip() + "\n\n"
new_ch2 += "\\section{Weight Distribution}\n"
new_ch2 += re.search(r"\\section\{Weight Distribution\}(.*?)\\section\{Feature Space: \\texttt\{x0\}--\\texttt\{x85\}\}", ch3, re.DOTALL).group(1).strip() + "\n\n"
new_ch2 += "\\section{Data Pre-processing}\n"
new_ch2 += re.search(r"\\section\{Feature Space: \\texttt\{x0\}--\\texttt\{x85\}\}(.*?)\\section\{Validation Strategy\}", ch3, re.DOTALL).group(1).strip() + "\n"
new_ch2 += "Handling missing values and normalization are intrinsically tied to the feature space. "
new_ch2 += re.search(r"\\section\{Missing Value Analysis\}(.*?)\\section\{Distributional Analysis of the Target\}", ch4, re.DOTALL).group(1).strip() + "\n\n"
new_ch2 += "\\section{Exploratory Analysis}\n"
new_ch2 += re.search(r"\\section\{Distributional Analysis of the Target\}(.*?)\\section\{EDA Summary and Modeling Implications\}", ch4, re.DOTALL).group(1).strip() + "\n\n"
new_ch2 += "\\section{EDA Summary}\n"
new_ch2 += re.search(r"\\section\{EDA Summary and Modeling Implications\}(.*)", ch4, re.DOTALL).group(1).strip() + "\n\n"
write_file("02_data_source.tex", new_ch2)

# Chapter 3: Methodology
new_ch3 = "\\chapter{Methodology}\n\\label{ch:methodology}\n\n"
new_ch3 += "\\section{Validation Approach \& Train-Test Split}\n"
new_ch3 += re.search(r"\\section\{Validation Strategy\}(.*?)\\chapter\{Exploratory Data Analysis\}", ch3 + "\n\\chapter{Exploratory Data Analysis}", re.DOTALL).group(1).strip() + "\n\n"
new_ch3 += "\\section{Evaluation Metric}\n"
new_ch3 += re.search(r"\\section\{Evaluation Metric: Weighted Skill Score\}(.*?)\\section\{Data Schema\}", ch2, re.DOTALL).group(1).strip() + "\n\n"
new_ch3 += "\\section{Classical Model Implementations (AR, ARMA, ARIMA, SARIMA)}\n"
new_ch3 += re.search(r"\\section\{Model Lineup\}(.*?)\\section\{Key Insights from Classical Modeling\}", ch5, re.DOTALL).group(1).strip() + "\n\n"
new_ch3 += "\\section{Deep Sequence Models (RNN, GRU, LSTM)}\n"
new_ch3 += re.search(r"\\section\{Architecture Overview\}(.*?)\\section\{Model Comparison\}", ch6, re.DOTALL).group(1).strip() + "\n\n"
new_ch3 += "\\subsection{ARIMAX and TCN}\n"
new_ch3 += "While ARIMAX (AutoRegressive Integrated Moving Average with Explanatory Variables) and TCN (Temporal Convolutional Networks) were considered, the weak linear correlation of individual features ($|\\rho| < 0.10$) suggested ARIMAX would struggle to capture the complex, nonlinear feature interactions. TCNs are a strong alternative for sequence modeling, but LSTMs and GRUs were prioritized for this study due to their proven effectiveness in financial forecasting.\n\n"
new_ch3 += "\\section{Ablation Study \& Tuned Parameter Values}\n"
new_ch3 += "The primary ablation in the classical pipeline was the comparison of $d=0$ versus $d=1$ (first differencing). As shown in the classical model lineup, differencing ($d=1$) was strictly superior across most series, confirming the ADF stationarity results.\n\n"
new_ch3 += re.search(r"\\subsection\{Hyperparameters\}(.*?)\\section\{Model Comparison\}", ch6, re.DOTALL).group(1).strip() + "\n\n"
new_ch3 += "\\section{Probabilistic Forecasting Models}\n"
new_ch3 += re.search(r"\\begin\{figure\}.*?slide_42\.png.*?\\end\{figure\}", ch6, re.DOTALL).group(0) + "\n"
new_ch3 += "To quantify uncertainty, quantile regression was implemented using LightGBM. Instead of point forecasts, the model predicts the conditional quantiles (e.g., 10th, 50th, and 90th percentiles), providing prediction intervals that capture the heteroskedasticity of financial returns.\n\n"
write_file("03_methodology.tex", new_ch3)

# Chapter 4: Analysis of the Numerical Results
new_ch4 = "\\chapter{Analysis of the Numerical Results}\n\\label{ch:results}\n\n"
new_ch4 += "\\section{Classical Model Results}\n"
new_ch4 += re.search(r"\\section\{Key Insights from Classical Modeling\}(.*?)\\section\{Limitations of Classical Models\}", ch5, re.DOTALL).group(1).strip() + "\n\n"
new_ch4 += "\\section{Deep Learning and Cross-Methodology Results}\n"
new_ch4 += re.search(r"\\chapter\{Results and Analysis\}(.*?)\\section\{Error Analysis\}", ch7, re.DOTALL).group(1).strip() + "\n\n"
new_ch4 += "\\section{Error Analysis}\n"
new_ch4 += re.search(r"\\section\{Error Analysis\}(.*)", ch7, re.DOTALL).group(1).strip() + "\n\n"
new_ch4 += "\\section{Research Gap Identified}\n"
new_ch4 += re.search(r"\\section\{Limitations of Classical Models\}(.*?)\\chapter\{Deep Sequence Models\}", ch5 + "\n\\chapter{Deep Sequence Models}", re.DOTALL).group(1).strip() + "\n"
new_ch4 += re.search(r"\\section\{Challenges and Considerations\}(.*?)\\chapter\{Results and Analysis\}", ch6 + "\n\\chapter{Results and Analysis}", re.DOTALL).group(1).strip() + "\n\n"
write_file("04_results.tex", new_ch4)

# Chapter 5: Converting the forecast into Actions
new_ch5 = "\\chapter{Converting the Forecast into Actions}\n\\label{ch:actions}\n\n"
new_ch5 += "In a production hedge fund environment, time series forecasts are only the first step in a quantitative pipeline. To generate economic value, these forecasts must be translated into actionable portfolio allocations and trading signals. This process involves several critical steps:\n\n"
new_ch5 += "\\section{Signal Generation and Expected Returns}\n"
new_ch5 += "The point forecasts ($\\hat{y}_{t+h}$) generated by our models represent the expected return for a given asset over horizon $h$. In isolation, a positive forecast implies a long signal, while a negative forecast implies a short signal. However, the magnitude of the forecast must cross a transaction-cost threshold to be actionable. The probabilistic forecasts (quantile regression) provide a confidence interval; signals are only generated when the entire interval sits above or below zero, indicating high conviction.\n\n"
new_ch5 += "\\section{Risk-Adjusted Sizing (Kelly Criterion)}\n"
new_ch5 += "Once a signal is generated, position sizing is determined using risk management frameworks such as the Kelly Criterion or mean-variance optimization. The optimal allocation to a specific series $i$ depends not only on its expected return $\\mu_i$ but also on its forecasted volatility $\\sigma_i^2$ (which can be derived from the spread of our quantile forecasts):\n"
new_ch5 += "\\begin{equation}\n"
new_ch5 += "f_i^* = \\frac{\\mu_i}{\\sigma_i^2}\n"
new_ch5 += "\\end{equation}\n"
new_ch5 += "This ensures that highly volatile series receive smaller capital allocations, even if their expected return is high, maintaining a balanced risk profile across the panel.\n\n"
new_ch5 += "\\section{Portfolio Optimization}\n"
new_ch5 += "Because the panel contains 36,923 series representing various sub-categories, forecasts cannot be acted upon in isolation. A portfolio optimizer (such as Markowitz Mean-Variance Optimization) takes the vector of expected returns and a covariance matrix to output optimal portfolio weights. The optimizer enforces constraints such as sector neutrality, maximum leverage, and turnover limits.\n\n"
new_ch5 += "\\section{Execution and Slippage}\n"
new_ch5 += "Finally, target weights are passed to an algorithmic execution engine. The engine minimizes market impact and slippage by breaking large orders into smaller chunks (e.g., using TWAP or VWAP algorithms). The difference between the paper forecast return and the actual realized return after execution costs is continuously monitored to calibrate the forecasting models.\n\n"
write_file("05_actions.tex", new_ch5)

# Chapter 6: Future Work
new_ch6 = "\\chapter{Future Work}\n\\label{ch:future_work}\n\n"
new_ch6 += re.search(r"\\section\{Future Work\}(.*)", ch8, re.DOTALL).group(1).strip() + "\n\n"
write_file("06_future_work.tex", new_ch6)

# Chapter 7: References
new_ch7 = "\\chapter{References}\n\\label{ch:references}\n\n"
new_ch7 += "\\begin{thebibliography}{9}\n\n"
new_ch7 += "\\bibitem{hyndman2018} Hyndman, R.J., \\& Athanasopoulos, G. (2018). \\emph{Forecasting: principles and practice} (2nd ed.). OTexts: Melbourne, Australia.\n"
new_ch7 += "\\bibitem{goodfellow2016} Goodfellow, I., Bengio, Y., \\& Courville, A. (2016). \\emph{Deep Learning}. MIT Press.\n"
new_ch7 += "\\bibitem{tsay2010} Tsay, R. S. (2010). \\emph{Analysis of financial time series} (3rd ed.). John Wiley \\& Sons.\n"
new_ch7 += "\\bibitem{kaggle} Kaggle. (2026). \\emph{Hedge Fund - Time Series Forecasting}. Retrieved from https://www.kaggle.com/competitions/ts-forecasting\n\n"
new_ch7 += "\\end{thebibliography}\n"
write_file("07_references.tex", new_ch7)

