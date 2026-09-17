"""Simulaciones educativas: caso de dos cuentas + DCA a 10 años bajo 3 senderos de TRM."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(__file__).resolve().parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from fx_identity import decompose_cop, fmt_cop, fmt_pct, fmt_usd, fx_identity

CASE = json.loads((ROOT / "data" / "generic_case.json").read_text())


def section(title: str) -> None:
    print("\n" + title)
    print("-" * len(title))


def caso_dos_cuentas() -> None:
    section("1. Caso genérico — dos cuentas, mismo portafolio, distinta edad")
    trm = CASE["trm_actual"]
    print(f"TRM actual: {trm:,.0f} COP/USD\n")
    print(f"{'Cuenta':<28} {'USD in':>10} {'USD hoy':>10} {'r USD':>8} {'r FX':>8} {'r COP':>8}")
    for key in ("A_larga", "B_nueva"):
        a = CASE["accounts"][key]
        d = decompose_cop(a["capital_usd"], a["valor_usd"], a["trm_ponderada"], trm)
        ident = fx_identity(d["r_usd"], trm, a["trm_ponderada"])
        print(
            f"{a['label']:<28} {fmt_usd(a['capital_usd']):>10} "
            f"{fmt_usd(a['valor_usd']):>10} {fmt_pct(d['r_usd']):>8} "
            f"{fmt_pct(ident['r_fx']):>8} {fmt_pct(d['r_cop']):>8}"
        )
        print(
            f"  Descomposición COP: capital {fmt_cop(d['capital_cop'])}  "
            f"FX capital {fmt_cop(d['fx_sobre_capital_cop'])}  "
            f"ganancia a TRM hoy {fmt_cop(d['ganancia_cop_a_trm_hoy'])}  "
            f"= valor {fmt_cop(d['valor_cop'])}"
        )


def mini_ejemplo() -> None:
    section("2. Mini ejemplo — por qué +USD puede ser −COP")
    pesos = 4_000_000
    trm_compra = 4_000
    usd = pesos / trm_compra
    r_usd = 0.185
    usd_hoy = usd * (1 + r_usd)
    trm_hoy = 3_123
    cop_hoy = usd_hoy * trm_hoy
    print(f"Aportas {fmt_cop(pesos)} cuando el dólar está a {trm_compra:,.0f} → {fmt_usd(usd)}")
    print(f"El portafolio sube {fmt_pct(r_usd)} → {fmt_usd(usd_hoy)}")
    print(f"Hoy el dólar está a {trm_hoy:,.0f} → {fmt_cop(cop_hoy)}")
    print(f"Resultado USD {fmt_pct(r_usd)} | Resultado COP {fmt_pct(cop_hoy / pesos - 1)}")
    print("El FX se aplica al saldo completo (capital + ganancia), no solo a la ganancia.")


def dca_10y() -> None:
    section("3. Simulación 10 años — DCA familiar fijo en COP")
    monthly = CASE["household_dca_cop_monthly"]
    years = CASE["horizon_years"]
    months = years * 12
    r_m = (1 + CASE["expected_usd_cagr"]) ** (1 / 12) - 1
    trm0 = CASE["trm_actual"]
    paths = {
        "Peso fuerte (USDCOP −3%/año)": -0.03,
        "TRM estable": 0.00,
        "Peso débil, patrón largo (USDCOP +4%/año)": 0.04,
    }
    print(
        f"Aporte: {fmt_cop(monthly)} / mes durante {years} años. "
        f"CAGR de mercado USD supuesto: {CASE['expected_usd_cagr']:.0%}."
    )
    print("El aporte es SIEMPRE la misma cantidad de pesos. Cambia cuántos dólares compra cada mes.\n")
    print(f"{'Sendero':<44} {'USD acumulado':>14} {'COP final':>16} {'r COP simple':>14}")
    for name, drift in paths.items():
        usd = 0.0
        cop_in = 0.0
        trm = trm0
        monthly_drift = (1 + drift) ** (1 / 12) - 1
        for _ in range(months):
            usd += monthly / trm
            usd *= 1 + r_m
            cop_in += monthly
            trm *= 1 + monthly_drift
        cop_out = usd * trm
        print(f"{name:<44} {fmt_usd(usd):>14} {fmt_cop(cop_out):>16} {fmt_pct(cop_out / cop_in - 1):>14}")
    print("\nLectura: el mismo DCA en pesos produce más o menos dólares según la TRM,")
    print("y el valor final en pesos depende de DÓNDE quede la TRM el día que midas (o gastes).")


def stock_vs_flujo() -> None:
    section("4. Stock vs flujo — por qué no hay que parar el DCA")
    print("Peso fuerte hoy:")
    print("  • Stock (lo ya invertido): vale menos en COP. Duele en el extracto.")
    print("  • Flujo (el aporte del mes): compra MÁS dólares por el mismo salario.")
    print("Peso débil mañana:")
    print("  • Stock: vale más en COP.")
    print("  • Flujo: compra MENOS dólares.")
    print("El DCA fijo en pesos promedia las dos patas. Parar cuando el dólar 'está barato'")
    print("es dejar de construir stock justo cuando el flujo es más productivo.")


if __name__ == "__main__":
    print("DCA + TRM  |  caso educativo genérico")
    print("No es asesoría. Cifras redondeadas a propósito.")
    caso_dos_cuentas()
    mini_ejemplo()
    dca_10y()
    stock_vs_flujo()
