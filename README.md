# Enchanted Equities

## Introduction
**Enchanted Equities** is an advanced analytical platform that applies computational finance and data science techniques to decode the stock market's complex behaviors. This tool integrates the principles of Richard Wyckoff’s method with modern statistical and machine learning algorithms to provide predictive insights into market trends.

## Conceptual Framework

### Wyckoff Method
The Wyckoff Method involves a series of principles and strategies that traders can use to gauge the market's probable future direction based on its current structure. **Enchanted Equities** focuses on the following key aspects of the Wyckoff Method:
- **Accumulation and Distribution**: Identifying key phases where market makers accumulate and distribute shares.
- **Tests for Supply and Demand**: Evaluating the balance of supply and demand at key price points to confirm the likelihood of a phase transition.
- **Price and Volume Analysis**: Utilizing the interrelationship between price movements and volume to discern the strength of a price trend.

### Technical Indicators
The application computes several technical indicators to supplement the Wyckoff analysis, providing a multi-faceted view of the markets:
- **Moving Averages (SMA and EMA)**: Simple and Exponential Moving Averages that smooth out price data to identify trends.
- **MACD (Moving Average Convergence Divergence)**: A trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.
- **RSI (Relative Strength Index)**: A momentum oscillator that measures the speed and change of price movements.
- **OBV (On-Balance Volume)**: Uses volume flow to predict changes in stock price.

## System Architecture

### Data Acquisition
Data is sourced live from financial markets using the `yfinance` API, which provides comprehensive historical market data in real-time.

### Computational Modules
1. **Data Processing**: Raw data is cleansed, normalized, and structured into a format suitable for analysis.
2. **Indicator Calculation**: Technical indicators are calculated using both built-in and custom functions that leverage `pandas` and `numpy` for numerical operations.
3. **Phase Detection**: Implements algorithmic logic based on the Wyckoff method to detect accumulation and distribution phases.
4. **Visualization**: Leverages `Plotly` for dynamic and interactive charting that not only illustrates the data but also highlights significant market events.

## Usage

**Enchanted Equities** is designed to run directly in your web browser without the need for installation:
1. Open your browser and navigate to Web App.
2. Enter the stock symbol and select your desired time frame and parameters.
3. The system will process the data and display the analysis through interactive charts and indicators.

## Advanced Features

- **Interactive Dashboards**: Customize views and charts to focus on specific data aspects.
- **Real-Time Data Processing**: Analyze live data feeds as the market fluctuates.
- **Alert System**: Get notifications for significant market movements based on set thresholds.

## Contributing
We encourage contributions from the community, whether they are feature requests, improvements, or bug fixes. Please use the standard Git workflows for contributions.

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature/your_feature_name`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your_feature_name`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.

## Authors
- **Marco** - "Financial Mathematics"
- **Domenico** - "Data Scientist"

## Acknowledgements
- [Pandas](https://pandas.pydata.org/) and [NumPy](http://numpy.org/) for data manipulation
- [yfinance](https://pypi.org/project/yfinance/) for fetching financial data
- [Plotly](https://plotly.com/) for interactive visualizations

Thank you for visiting **Enchanted Equities**. We hope this tool empowers you with the insights needed to navigate the complexities of the financial markets.
