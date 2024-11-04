export interface StockFundamentals {
    Symbol: string;
    AssetType: string;
    Name: string; // IMPORTANT
    Description: string;
    CIK: string;
    Exchange: string;
    Currency: string;
    Country: string;
    Sector: string; // IMPORTANT
    Industry: string; // IMPORTANT
    Address: string;
    OfficialSite: string;
    FiscalYearEnd: string;
    LatestQuarter: string;
    MarketCapitalization: string; // IMPORATANT
    EBITDA: string; //IMPORTANT
    PERatio: string; // IMPORTANT
    PEGRatio: string; // IMPORTANT
    BookValue: string; // IMPORTANT
    DividendPerShare: string;
    DividendYield: string; // IMPORTANT
    EPS: string; //IMPORTANT
    RevenuePerShareTTM: string;
    ProfitMargin: string;
    OperatingMarginTTM: string;
    ReturnOnAssetsTTM: string;
    ReturnOnEquityTTM: string;
    RevenueTTM: string;
    GrossProfitTTM: string;
    DilutedEPSTTM: string;
    QuarterlyEarningsGrowthYOY: string; // INTERESTING
    QuarterlyRevenueGrowthYOY: string; // INTERESTING
    AnalystTargetPrice: string;
    AnalystRatingStrongBuy: string;
    AnalystRatingBuy: string;
    AnalystRatingHold: string;
    AnalystRatingSell: string;
    AnalystRatingStrongSell: string;
    TrailingPE: string;
    ForwardPE: string; // IMPORTANT
    PriceToSalesRatioTTM: string; // IMPORTANT
    PriceToBookRatio: string; // IMPORTANT
    EVToRevenue: string;
    EVToEBITDA: string;
    Beta: string; // DEFAULT
    "52WeekHigh": string; // DEFAULT
    "52WeekLow": string; // DEFAULT
    "50DayMovingAverage": string;
    "200DayMovingAverage": string;
    SharesOutstanding: string;
    DividendDate: string;
    ExDividendDate: string;
}
