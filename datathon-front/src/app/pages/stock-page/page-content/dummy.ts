import { StockInfo } from '../../../interfaces/stock-info.interface';
export const dummy: any = {
  // Basic stock information
  stock: {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    dayChange: 10,
    closePrice: 10,
  },

  // Stock-specific news
  stockNews: [
    {
      summary: 'Apple announces new iPhone release date',
      url: 'https://example.com/apple-iphone-news',
      sentiment_score: 0.8,
    },
    {
      summary: "Apple's services revenue hits all-time high",
      url: 'https://example.com/apple-services-revenue',
      sentiment_score: 0.9,
    },
  ],

  // Sector-related news
  sectorNews: [
    {
      summary: 'Tech sector shows strong growth in Q2',
      url: 'https://example.com/tech-sector-q2',
      sentiment_score: 0.7,
    },
    {
      summary: 'Semiconductor shortage affecting tech industry',
      url: 'https://example.com/semiconductor-shortage',
      sentiment_score: -0.3,
    },
  ],

  // Technical analysis insight
  technicalInsight:
    'AAPL shows bullish momentum with strong support at $170. RSI indicates slightly overbought conditions.',

  // General insights about the stock
  generalInsights: [
    {
      text: 'Strong balance sheet with high cash reserves',
      source: 'aaa.com',
    },
    {
      text: 'Market saturation in smartphone segment',
      source: 'aaa.com',
    },
  ],

  // Historical price data
  priceHistory: {
    timeframe: '1Y',
    data: [
      { date: '2023-01-01', price: 150.23 },
      { date: '2023-06-01', price: 165.45 },
      { date: '2024-01-01', price: 173.45 },
    ],
  },

  // Fundamental data
  fundamentalData: {
    shortName: 'Apple Inc.',
    sector: 'Technology',
    industry: 'Consumer Electronics',
    marketCap: 2800000000000,
    volume: 55000000,
    trailingPE: 28.5,
    forwardPE: 25.3,
    dividendYield: 0.55,
    dividendRate: 0.96,
    exDividendDate: '2024-02-09',
    beta: 1.28,
    trailingEps: 6.08,
    fiftyTwoWeekHigh: 185.12,
    fiftyTwoWeekLow: 143.9,
    priceToBook: 35.2,
  },
};
