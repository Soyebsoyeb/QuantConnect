\section*{Financial Sector PE Ratio \& Performance Analysis}

\subsection*{Overview}
This research notebook analyzes Price-to-Earnings (PE) ratios and cumulative returns for major U.S. financial sector stocks (\texttt{JPM, BAC, MS, SCHW, GS, AXP, C}) over the period \textbf{January 2021 to January 2022}. It also explores the relationship between valuation (PE) and returns, and demonstrates BAC option chain and Bollinger Band technical analysis with regression forecasting.

\subsection*{Libraries Used}
\begin{itemize}
    \item \textbf{matplotlib}: For plotting graphs and visualizing data.
    \item \textbf{numpy}: For numerical operations and matrix calculations.
    \item \textbf{QuantConnect QuantBook}: For market data retrieval and indicator computation.
\end{itemize}

\subsection*{Data Sources}
\begin{itemize}
    \item \textbf{QuantConnect Dataset Market}: Financial fundamentals (PE ratios) and daily price data.
\end{itemize}

\subsection*{Key Features}
\begin{itemize}
    \item Retrieval and visualization of PE ratios for selected stocks.
    \item Calculation and plotting of cumulative returns.
    \item Correlation study between PE ratio and yearly returns.
    \item Options chain and Bollinger Band analysis for BAC.
    \item Linear regression forecasting using Bollinger Band middle line.
\end{itemize}

\subsection*{Installation \& Setup}
\begin{enumerate}
    \item Run in QuantConnect Research Environment (Jupyter notebook).
    \item Libraries are automatically available. No additional installation required.
\end{enumerate}

\subsection*{Usage}
\begin{itemize}
    \item Specify the time period and tickers as needed.
    \item Run all cells sequentially for complete analysis.
\end{itemize}

\subsection*{Example Output}
\begin{itemize}
    \item Graphs of PE ratios and cumulative returns.
    \item Scatter plot of return vs. PE ratio.
    \item Bollinger Band and linear regression plots.
\end{itemize}

\subsection*{Documentation References}
\begin{itemize}
    \item \href{https://www.quantconnect.com/docs/v2/cloud-platform/research/getting-started}{QuantConnect Research Docs}
    \item \href{https://github.com/QuantConnect/Tutorials}{QuantConnect Tutorials}
\end{itemize}
