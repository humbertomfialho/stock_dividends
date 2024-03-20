# XP Investment Portfolio Analysis
This repository contains code developed to analyze XP's automatic investment portfolio data, focusing on dividend returns.

## Data Collection

We collect data from two primary sources to conduct our analysis:
- **PDF Negotiation Notes**: Detailed transaction records.
- **Market Data**: Current stock prices and dividends.

We collect data from pdf negotiation notes and market data to analyse:
- The duration and initial amount of the investment;
- The number and cost of transactions;
- The segments and the sectors of stocks chosen;
- Variations in prices between buying and selling stock transactions;
- Monthly positions and financial values;
- Dividend yield;

## Prerequisites

Before running this code, you need to obtain API tokens from the following sources:
- [Dados de Mercado API](https://api.dadosdemercado.com.br/v1/)
- [BrAPI](https://brapi.dev/api/)

Enter your access tokens in the `./api/constants.py` file within the respective string variables.

## Storing PDF Trading Notes

Save your PDF trading notes in the `./pdf` folder. Ensure you follow the naming conventions as described in the `help.txt` file within that folder for proper organization.
