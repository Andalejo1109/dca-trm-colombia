# DCA en dólares desde Colombia y el efecto de la TRM

Caso **educativo y genérico** para hogares que invierten en activos USD (ETFs) con aportes mensuales en pesos.

No es una cuenta real. No es asesoría. Las cifras están redondeadas a propósito.

**Repo:** https://github.com/Andalejo1109/dca-trm-colombia

---

## La pregunta

Un portafolio puede estar **arriba en dólares y abajo en pesos** al mismo tiempo.

¿Eso significa que la estrategia falló? ¿Hay que parar el DCA porque el dólar “está barato”? ¿Cómo se ve esto a 10 años si la familia sigue aportando todos los meses?

---

## La identidad que sí cierra

No se restan retornos. Se multiplican, porque el tipo de cambio se aplica al **valor de mercado completo** (capital + ganancia):

```text
(1 + r_COP) = (1 + r_USD) × (TRM_actual / TRM_ponderada_de_aportes)
```

Restar `r_USD − r_FX` sobreestima la rentabilidad en pesos: trata la ganancia como si viviera en la TRM vieja.

---

## Caso genérico: dos cuentas, mismo portafolio, distinta edad

TRM de valoración: **3.123 COP/USD**.

| Cuenta | Capital USD | Valor hoy USD | r USD | r FX | r COP |
|---|---:|---:|---:|---:|---:|
| A — historial largo (desde 2024) | 22.200 | 37.000 | +66.7% | −20.5% | **+32.5%** |
| B — historial corto, aportes recientes (desde 2025) | 17.300 | 20.505 | +18.5% | −16.8% | **−1.3%** |

Misma familia, mismos ETFs, misma TRM de hoy. Cambia **cuándo** entró el dinero.

### Dónde se come la ganancia (cuenta B)

1. Capital que salió del bolsillo: 17.300 × 3.752 ≈ **64.9 M COP**
2. Ese capital, a la TRM de hoy: 17.300 × 3.123 ≈ **54.0 M COP** → FX sobre el capital **−10.9 M**
3. Ganancia USD convertida *hoy*: 3.205 × 3.123 ≈ **+10.0 M COP**

Neto: 64.9 − 10.9 + 10.0 = **64.0 M COP**. En dólares hay +3.205. En pesos, casi plano o un poco abajo.

El +USD es real. No alcanza a tapar la revaluación del peso sobre el *stock*.

### Mini ejemplo

Aportas 4.000.000 COP con el dólar a 4.000 → 1.000 USD.  
El portafolio sube 18.5% → 1.185 USD.  
Hoy el dólar está a 3.123 → 3.70 M COP.

- Resultado USD: **+18.5%**
- Resultado COP: **−7.5%**

---

## Simulación a 10 años

Regla: la familia aporta **4.000.000 COP cada mes**, 10 años. El mercado USD rinde 8% anual (supuesto, no pronóstico). Cambia solo el sendero de la TRM.

| Sendero de TRM | USD acumulados | Valor final en COP | r COP simple |
|---|---:|---:|---:|
| Peso fuerte (USDCOP −3%/año) | 265.874 | 612 M | +27.6% |
| TRM estable | 232.191 | 725 M | +51.1% |
| Peso débil, patrón largo (USDCOP +4%/año) | 197.187 | 912 M | +89.9% |

Lectura incómoda y útil:

- Con peso *fuerte* compras **más** dólares con el mismo salario (265 k vs 197 k).
- El valor final en pesos igual puede ser el más bajo, porque el día de la foto el dólar “vale menos pesos”.
- Con peso *débil* compras menos dólares, pero el stock se revaloriza en COP.

El DCA fijo en pesos promedia las dos patas. Parar aportes cuando el dólar está barato es dejar de construir stock justo cuando el flujo es más productivo.

---

## Conclusión práctica

1. Reporta **dos números**: r USD (qué tan bien inviertes) y r COP (qué tanto crece el patrimonio en Colombia). No los restes.
2. A 1–3 años el FX puede dominar, sobre todo en cuentas jóvenes. A 8–15 años, para un hogar que gasta en Colombia, el USDCOP históricamente ha tendido a subir con el diferencial de inflación. El tramo 2023–2026 es un contraejemplo, no la media.
3. El instrumento anti-TRM de un inversionista de largo plazo **es el DCA en pesos**, no un forward.
4. No conviertas el saldo a pesos “para protegerlo” en medio de un dólar barato. Ese es el error simétrico a vender el S&P porque tuvo un buen año.
5. Cuando falten 3–5 años para vivir de la plata, ahí sí: un DCA de *venta* gradual a COP. No el día 1 del retiro.

---

## Cómo correr las simulaciones

```bash
git clone https://github.com/Andalejo1109/dca-trm-colombia.git
cd dca-trm-colombia
python3 src/simulate_dca.py
```

Solo usa la librería estándar. Edita `data/generic_case.json` para probar otros capitales, TRM o un CAGR distinto.

---

## Cómo leer este material

- `src/fx_identity.py` — identidad y descomposición.
- `src/simulate_dca.py` — caso de dos cuentas + mini ejemplo + 10 años.
- `data/generic_case.json` — supuestos editables.
- `posts/etoro_2026-09-22.md` — texto del post educativo.

Este contenido no es una recomendación de inversión. Rentabilidades pasadas y senderos de TRM no predicen el futuro.
