"""Identidad de rentabilidad COP / USD / TRM y descomposición del valor."""

from __future__ import annotations


def fx_identity(r_usd: float, trm_actual: float, trm_ponderada: float) -> dict:
    """(1 + r_COP) = (1 + r_USD) * (TRM_actual / TRM_ponderada)."""
    r_fx = trm_actual / trm_ponderada - 1
    r_cop = (1 + r_usd) * (1 + r_fx) - 1
    return {
        "r_usd": r_usd,
        "r_fx": r_fx,
        "r_cop": r_cop,
        "check": (1 + r_usd) * (1 + r_fx) - 1 - r_cop,
    }


def decompose_cop(
    capital_usd: float,
    valor_usd: float,
    trm_ponderada: float,
    trm_actual: float,
) -> dict:
    """Parte el valor actual en COP en capital, FX sobre capital y ganancia a TRM de hoy."""
    capital_cop = capital_usd * trm_ponderada
    valor_cop = valor_usd * trm_actual
    fx_sobre_capital = capital_usd * trm_actual - capital_cop
    ganancia_usd = valor_usd - capital_usd
    ganancia_cop_hoy = ganancia_usd * trm_actual
    return {
        "capital_cop": capital_cop,
        "fx_sobre_capital_cop": fx_sobre_capital,
        "ganancia_cop_a_trm_hoy": ganancia_cop_hoy,
        "valor_cop": valor_cop,
        "cierra": capital_cop + fx_sobre_capital + ganancia_cop_hoy - valor_cop,
        "r_usd": ganancia_usd / capital_usd,
        "r_cop": valor_cop / capital_cop - 1,
    }


def fmt_pct(x: float) -> str:
    return f"{x*100:+.1f}%"


def fmt_cop(x: float) -> str:
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


def fmt_usd(x: float) -> str:
    return f"${x:,.0f}"
