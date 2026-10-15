import json
from dataclasses import dataclass, field
from enum import Enum

from opentrade_ai.llm.provider import LLMProvider


class AgentRole(Enum):
    FUNDAMENTAL_ANALYST = "fundamental_analyst"
    SENTIMENT_ANALYST = "sentiment_analyst"
    NEWS_ANALYST = "news_analyst"
    TECHNICAL_ANALYST = "technical_analyst"
    BULL_RESEARCHER = "bull_researcher"
    BEAR_RESEARCHER = "bear_researcher"
    TRADER = "trader"
    RISK_MANAGER = "risk_manager"
    VERIFIER = "verifier"


AGENT_ROLE_LABELS = {
    AgentRole.FUNDAMENTAL_ANALYST: "基本面分析師",
    AgentRole.SENTIMENT_ANALYST: "情緒分析師",
    AgentRole.NEWS_ANALYST: "新聞分析師",
    AgentRole.TECHNICAL_ANALYST: "技術分析師",
    AgentRole.BULL_RESEARCHER: "多方研究員",
    AgentRole.BEAR_RESEARCHER: "空方研究員",
    AgentRole.TRADER: "交易決策員",
    AgentRole.RISK_MANAGER: "風控經理",
    AgentRole.VERIFIER: "數據驗證員",
}


@dataclass
class AnalysisResult:
    agent_role: AgentRole
    ticker: str
    summary: str
    signal: str = "neutral"
    confidence: float = 0.0
    details: dict = field(default_factory=dict)


class BaseAgent:
    role: AgentRole
    system_prompt: str = ""

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def analyze(self, ticker: str, context: dict) -> AnalysisResult:
        raise NotImplementedError

    def _build_prompt(self, ticker: str, context: dict) -> str:
        raise NotImplementedError

    def _parse_response(self, ticker: str, response: str) -> AnalysisResult:
        parsed = None
        text = response.strip()

        if text.startswith("{") and text.endswith("}"):
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = None
        elif "```json" in text:
            try:
                block = text.split("```json", 1)[1].split("```", 1)[0].strip()
                parsed = json.loads(block)
            except (IndexError, json.JSONDecodeError):
                parsed = None

        if isinstance(parsed, dict):
            raw_signal = str(parsed.get("signal", "")).strip()
            raw_conf = parsed.get("confidence")
            summary = str(parsed.get("summary") or parsed.get("rationale") or response)

            signal = self._normalize_signal(raw_signal)
            confidence = self._normalize_confidence(raw_conf)

            if signal == "neutral":
                signal, confidence = self._heuristic_signal_from_text(summary)

            return AnalysisResult(
                agent_role=self.role,
                ticker=ticker,
                summary=summary,
                signal=signal,
                confidence=confidence,
            )

        signal, confidence = self._heuristic_signal_from_text(response)
        return AnalysisResult(
            agent_role=self.role,
            ticker=ticker,
            summary=response,
            signal=signal,
            confidence=confidence,
        )

    def _heuristic_signal_from_text(self, response: str) -> tuple[str, float]:
        signal = "neutral"
        confidence = 50.0
        lower = response.lower()

        if any(k in lower for k in ("strong buy", "strongly bullish", "強力買進", "強烈買進", "強力買入", "強烈買入")):
            signal = "strong_buy"
            confidence = 85.0
        elif any(k in lower for k in ("buy", "bullish", "買進", "買入", "做多", "偏多")):
            signal = "buy"
            confidence = 70.0
        elif any(k in lower for k in ("strong sell", "strongly bearish", "強力賣出", "強烈賣出")):
            signal = "strong_sell"
            confidence = 85.0
        elif any(k in lower for k in ("sell", "bearish", "賣出", "做空", "偏空")):
            signal = "sell"
            confidence = 70.0
        elif any(k in lower for k in ("hold", "持有", "觀望", "中立")):
            signal = "hold"
            confidence = 60.0

        return signal, confidence

    def _normalize_signal(self, raw_signal: str) -> str:
        lower = raw_signal.lower().strip()

        if ("strong" in lower and "buy" in lower) or any(k in lower for k in ("強力買進", "強烈買進", "強力買入", "強烈買入")):
            return "strong_buy"
        if lower == "buy" or "bull" in lower or "bullish" in lower or any(k in lower for k in ("買進", "買入", "做多", "偏多")):
            return "buy"
        if ("strong" in lower and "sell" in lower) or any(k in lower for k in ("強力賣出", "強烈賣出")):
            return "strong_sell"
        if lower == "sell" or "bear" in lower or "bearish" in lower or any(k in lower for k in ("賣出", "做空", "偏空")):
            return "sell"
        if lower == "hold" or "neutral" in lower or any(k in lower for k in ("持有", "觀望", "中立")):
            return "hold"
        return "neutral"

    def _normalize_confidence(self, raw_confidence) -> float:
        if raw_confidence is None:
            return 50.0
        if isinstance(raw_confidence, (int, float)):
            return float(raw_confidence)
        if isinstance(raw_confidence, str):
            cleaned = (
                raw_confidence.replace("%", "")
                .replace("confidence", "")
                .replace(":", "")
                .strip()
            )
            try:
                return float(cleaned)
            except ValueError:
                return 50.0
        return 50.0
