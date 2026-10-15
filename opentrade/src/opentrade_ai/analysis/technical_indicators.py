import numpy as np
import pandas as pd

try:
    import pandas_ta as ta
except Exception:
    ta = None


def _calc_sma(series: pd.Series, length: int) -> pd.Series:
    if ta is not None:
        try:
            return ta.sma(series, length=length)
        except Exception:
            pass
    return series.rolling(length).mean()


def _calc_ema(series: pd.Series, length: int) -> pd.Series:
    if ta is not None:
        try:
            return ta.ema(series, length=length)
        except Exception:
            pass
    return series.ewm(span=length, adjust=False).mean()


def _calc_rsi(close: pd.Series, length: int = 14) -> pd.Series:
    if ta is not None:
        try:
            return ta.rsi(close, length=length)
        except Exception:
            pass
    diff = close.diff()
    gain = diff.clip(lower=0)
    loss = -diff.clip(upper=0)
    avg_gain = gain.ewm(com=length - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=length - 1, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def _calc_macd(close: pd.Series) -> pd.DataFrame:
    if ta is not None:
        try:
            res = ta.macd(close)
            if res is not None and not res.empty:
                return res
        except Exception:
            pass
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    hist = macd_line - signal_line
    return pd.DataFrame({"macd": macd_line, "signal": signal_line, "hist": hist}, index=close.index)


def _calc_bbands(close: pd.Series, length: int = 20) -> pd.DataFrame:
    if ta is not None:
        try:
            res = ta.bbands(close, length=length)
            if res is not None and not res.empty:
                return res
        except Exception:
            pass
    sma = close.rolling(length).mean()
    std = close.rolling(length).std()
    return pd.DataFrame({
        "upper": sma + 2 * std,
        "middle": sma,
        "lower": sma - 2 * std
    }, index=close.index)


def _calc_atr(high: pd.Series, low: pd.Series, close: pd.Series, length: int = 14) -> pd.Series:
    if ta is not None:
        try:
            return ta.atr(high, low, close, length=length)
        except Exception:
            pass
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.ewm(com=length - 1, adjust=False).mean()


def _calc_stoch(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.DataFrame:
    if ta is not None:
        try:
            res = ta.stoch(high, low, close)
            if res is not None and not res.empty:
                return res
        except Exception:
            pass
    low_min = low.rolling(14).min()
    high_max = high.rolling(14).max()
    denom = (high_max - low_min).replace(0, np.nan)
    stoch_k = 100 * (close - low_min) / denom
    stoch_d = stoch_k.rolling(3).mean()
    return pd.DataFrame({"stoch_k": stoch_k, "stoch_d": stoch_d}, index=close.index)


def _calc_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    if ta is not None:
        try:
            return ta.obv(close, volume)
        except Exception:
            pass
    direction = np.sign(close.diff()).fillna(0)
    return (direction * volume).cumsum()


class TechnicalAnalyzer:
    def compute_indicators(self, df: pd.DataFrame) -> dict:
        if df.empty or len(df) < 14:
            raise ValueError("Insufficient data for technical analysis (need at least 14 rows)")

        close = df["Close"]
        high = df["High"]
        low = df["Low"]
        volume = df["Volume"]

        indicators = {}

        indicators["sma_20"] = self._safe_last(_calc_sma(close, length=20))
        indicators["sma_50"] = self._safe_last(_calc_sma(close, length=50))
        indicators["ema_12"] = self._safe_last(_calc_ema(close, length=12))
        indicators["ema_26"] = self._safe_last(_calc_ema(close, length=26))

        rsi = _calc_rsi(close, length=14)
        indicators["rsi"] = self._safe_last(rsi)

        macd_result = _calc_macd(close)
        if macd_result is not None and not macd_result.empty:
            indicators["macd"] = self._safe_last(macd_result.iloc[:, 0])
            indicators["macd_signal"] = self._safe_last(macd_result.iloc[:, 1])
            indicators["macd_histogram"] = self._safe_last(macd_result.iloc[:, 2])

        bbands = _calc_bbands(close, length=20)
        if bbands is not None and not bbands.empty:
            indicators["bb_upper"] = self._safe_last(bbands.iloc[:, 0])
            indicators["bb_middle"] = self._safe_last(bbands.iloc[:, 1])
            indicators["bb_lower"] = self._safe_last(bbands.iloc[:, 2])

        atr = _calc_atr(high, low, close, length=14)
        indicators["atr"] = self._safe_last(atr)

        stoch = _calc_stoch(high, low, close)
        if stoch is not None and not stoch.empty:
            indicators["stoch_k"] = self._safe_last(stoch.iloc[:, 0])
            indicators["stoch_d"] = self._safe_last(stoch.iloc[:, 1])

        obv = _calc_obv(close, volume)
        indicators["obv"] = self._safe_last(obv)

        indicators["current_price"] = float(close.iloc[-1])
        indicators["price_change_pct"] = float(
            ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100
        )
        indicators["avg_volume"] = float(volume.mean())
        indicators["volume_trend"] = float(
            volume.iloc[-5:].mean() / volume.mean() if volume.mean() > 0 else 1.0
        )

        return indicators

    def get_signal_summary(self, indicators: dict) -> dict:
        signals = {}

        rsi = indicators.get("rsi")
        if rsi is not None:
            if rsi < 30:
                signals["rsi"] = "oversold (bullish)"
            elif rsi > 70:
                signals["rsi"] = "overbought (bearish)"
            else:
                signals["rsi"] = "neutral"

        macd = indicators.get("macd")
        macd_signal = indicators.get("macd_signal")
        if macd is not None and macd_signal is not None:
            if macd > macd_signal:
                signals["macd"] = "bullish crossover"
            else:
                signals["macd"] = "bearish crossover"

        price = indicators.get("current_price")
        sma_20 = indicators.get("sma_20")
        sma_50 = indicators.get("sma_50")
        if price is not None and sma_20 is not None:
            if price > sma_20:
                signals["sma_20"] = "price above SMA20 (bullish)"
            else:
                signals["sma_20"] = "price below SMA20 (bearish)"
        if price is not None and sma_50 is not None:
            if price > sma_50:
                signals["sma_50"] = "price above SMA50 (bullish)"
            else:
                signals["sma_50"] = "price below SMA50 (bearish)"

        bb_upper = indicators.get("bb_upper")
        bb_lower = indicators.get("bb_lower")
        if price is not None and bb_upper is not None and bb_lower is not None:
            if price >= bb_upper:
                signals["bollinger"] = "at upper band (potential reversal)"
            elif price <= bb_lower:
                signals["bollinger"] = "at lower band (potential bounce)"
            else:
                signals["bollinger"] = "within bands (normal)"

        volume_trend = indicators.get("volume_trend")
        if volume_trend is not None:
            if volume_trend > 1.5:
                signals["volume"] = "high volume surge"
            elif volume_trend < 0.5:
                signals["volume"] = "low volume"
            else:
                signals["volume"] = "normal volume"

        bullish_count = sum(1 for v in signals.values() if "bullish" in v or "bounce" in v)
        bearish_count = sum(1 for v in signals.values() if "bearish" in v or "reversal" in v)
        total = len(signals)

        if total > 0:
            if bullish_count > bearish_count:
                signals["overall"] = "bullish"
            elif bearish_count > bullish_count:
                signals["overall"] = "bearish"
            else:
                signals["overall"] = "neutral"
            signals["confidence"] = round(max(bullish_count, bearish_count) / total * 100, 1)
        else:
            signals["overall"] = "insufficient data"
            signals["confidence"] = 0.0

        return signals

    def _safe_last(self, series: pd.Series | None) -> float | None:
        if series is None or series.empty:
            return None
        val = series.iloc[-1]
        if pd.isna(val):
            return None
        return float(val)
