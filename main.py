import seaborn as sns
import yfinance as yf
from matplotlib import pyplot as plt
import statsmodels.tsa.stattools as ts
import numpy as np
import pandas as pd

class stock:
    def __init__(self, name):
        self.name = name
        self.data =yf.Ticker(self.name)
        self.price=self.data.history(period='1d', start='2020-4-1', end='2022-1-1')
        self.close=self.price['Close']
        self.pct_variation=self.close.pct_change().dropna()
        self.cumulative_return=(self.pct_variation+1).cumprod()
        self.standard_deviation = self.pct_variation.std()
        self.sharpe_ratio = (self.pct_variation.mean() * 252-0)/ (self.pct_variation.std() * np.sqrt(252))





def plot_data(label,what_to_show,Firms,stocks):
    for i in range(len(stocks)):
        plt.plot(getattr(Firms[i],what_to_show), label=Firms[i].name)
    plotting_backend(label)
    
def plotting_backend(label):
    plt.title(label)
    plt.legend(loc="upper left")
    plt.xticks(rotation=45)
    sns.despine(left=True)
    plt.show(block=False)
    plt.grid('off')
    plt.pause(50)
    plt.close()

def violin_plot(all_stocks):
    plt.style.use('seaborn-deep')
    plt.style.use('ggplot')
    plt.violinplot(all_stocks)
    plt.xlabel("Stocks")
    plt.title("Violin Plot Distribution of Daily % Variations")
    extra=plt.subplot(111)
    pos = [1, 2, 3]
    extra.set_xticks(pos)
    extra.set_xticklabels(all_stocks.columns)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.style.use('seaborn-poster')
    plt.style.use('ggplot')
    plt.show(block=False)
    plt.pause(5)
    plt.close()

def daily_variation_distribution(Firms):
    for i in range(len(Firms)):
        sns.distplot(Firms[i].pct_variation, hist = False, kde = True,kde_kws = {'shade': True, 'linewidth': 3},label =Firms[i].name)
    plt.xlabel(" Daily % Variation")
    plotting_backend("Daily % Variation Distribution")


def sharpe_ratio(Firms):
    plt.style.use('seaborn-deep')
    plt.style.use('seaborn-poster')
    plt.style.use('ggplot')
    Sharpe_ratios=[0,0,0,0]
    Names=["","","",""]
    what='sharpe_ratio'
    for i in range(len(Firms)):
         Sharpe_ratios[i]=getattr(Firms[i],what)
         Names[i]=getattr(Firms[i],"name")
    plt.bar(Names,Sharpe_ratios,color=['black'])
    sns.set_context("poster")
    plt.title("Sharpe Ratios")
    plt.show(block=False)
    plt.pause(5)
    plt.close()

def standard_deviation_analysis(Firms):
    for i in range(len(Firms)):
        getattr(Firms[i],"pct_variation").rolling(window=60).std().plot(title="60 Day Rolling Standard Deviation",label=Firms[i].name);
    plt.legend(loc="upper right")
    plt.show(block=False)
    plt.pause(5)
    plt.close()

def correlation_analysis(all_stocks,SP500,Firms):
    all_stocks=pd.concat([all_stocks,getattr(SP500,'pct_variation')],axis='columns', join='inner')
    all_stocks.columns = [getattr(Firms[0], "name"), getattr(Firms[1], "name"), getattr(Firms[2], "name"),getattr(SP500,"name")]
    corr=all_stocks.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    corr.style.background_gradient(cmap='coolwarm')
    sns.heatmap(corr, cmap='RdYlGn', vmax=1.0,mask=mask, vmin=-1.0, linewidths=2.5)
    plt.yticks(rotation=0)
    plt.title("Correlation Between Daily Stocks-Performance")
    plt.xticks(rotation=45)
    plt.show()

def cointegration(tesla,sp500):
    cointegration_result = ts.coint(getattr(tesla, "close"),getattr(sp500,"close"))
    print("------------------------------------------------")
    print("cointegration test results:")
    print(cointegration_result)

def main():
    stocks=['TSLA','BAC','BLK']
    Firms=['Tesla','Bank of America', 'BlackRock','S&P 500']


    for i in range(len(stocks)):
        Firms[i]=stock(stocks[i])

    all_stocks = pd.concat(
        [getattr(Firms[0], "pct_variation"), getattr(Firms[1], "pct_variation"), getattr(Firms[2], "pct_variation")],
        axis='columns', join='inner')
    all_stocks.columns = [getattr(Firms[0], "name"), getattr(Firms[1], "name"), getattr(Firms[2], "name")]

    plt.style.use('seaborn-poster')
    plt.style.use('ggplot')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plot_data("Daily % Variation of Stock","pct_variation",Firms,stocks)

    stocks=['TSLA','BAC','BLK','S&P500']
    SP500 = stock('^GSPC')
    Firms[3] = SP500

    plot_data("Cumulative Return over Period","cumulative_return",Firms,stocks)
    violin_plot(all_stocks)
    daily_variation_distribution(Firms)
    standard_deviation_analysis(Firms)
    sharpe_ratio(Firms)
    correlation_analysis(all_stocks,SP500,Firms)
    cointegration(Firms[0],Firms[3])

if __name__ == "__main__":
    main()