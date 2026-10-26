"""Entrenamiento del clasificador ligero (protocolo, sección 6.4). Requiere `uv sync --group cnn`.

- Arquitectura "pequena": red convolucional de unos 25 mil parámetros, entrenada desde cero.
- Arquitectura "mobilenet": MobileNetV3-Small con pesos de ImageNet (transferencia de
  aprendizaje). Necesita torchvision y descargar los pesos una vez, con internet.

El modelo elegido se decide con el conjunto de validación, nunca con el de prueba.
Se exporta a ONNX para ejecutarlo en la Raspberry Pi con ONNX Runtime.
"""

import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .clasificador import LADO_RED, preparar


def _torch():
    try:
        import torch
        return torch
    except ImportError as e:  # pragma: no cover - depende del entorno
        raise SystemExit("Falta PyTorch. Instálelo con: uv sync --group cnn") from e


def construir(arquitectura: str, n_clases: int):
    torch = _torch()
    nn = torch.nn
    if arquitectura == "pequena":
        def bloque(a, b):
            return nn.Sequential(nn.Conv2d(a, b, 3, padding=1, bias=False), nn.BatchNorm2d(b), nn.ReLU(inplace=True),
                                 nn.Conv2d(b, b, 3, padding=1, bias=False), nn.BatchNorm2d(b), nn.ReLU(inplace=True),
                                 nn.MaxPool2d(2))
        return nn.Sequential(bloque(3, 16), bloque(16, 32), bloque(32, 48),
                             nn.AdaptiveAvgPool2d(1), nn.Flatten(), nn.Dropout(0.2), nn.Linear(48, n_clases))
    if arquitectura == "mobilenet":
        try:
            from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small
        except ImportError as e:
            raise SystemExit("La arquitectura mobilenet necesita torchvision: uv add --group cnn torchvision") from e
        red = mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.IMAGENET1K_V1)
        red.classifier[-1] = nn.Linear(red.classifier[-1].in_features, n_clases)
        return red
    raise ValueError(f"Arquitectura desconocida: {arquitectura}")


def _aumentar(x, gen):
    """Aumento de datos en el lote: volteos, brillo y desplazamiento de pocos píxeles."""
    torch = _torch()
    n = x.shape[0]
    volteo_h = torch.rand(n, generator=gen) < 0.5
    volteo_v = torch.rand(n, generator=gen) < 0.5
    x = torch.where(volteo_h[:, None, None, None], x.flip(3), x)
    x = torch.where(volteo_v[:, None, None, None], x.flip(2), x)
    factor = 1 + (torch.rand(n, 1, 1, 1, generator=gen) - 0.5) * 0.4
    x = (x * 0.25 + 0.5) * factor
    x = (x.clamp(0, 1) - 0.5) / 0.25
    dx, dy = (torch.randint(-4, 5, (2,), generator=gen)).tolist()
    return torch.roll(x, shifts=(dy, dx), dims=(2, 3))


def exactitud_balanceada(verdad: list[str], pred: list[str], clases: list[str]) -> float:
    sens = []
    for c in clases:
        n = sum(v == c for v in verdad)
        if n:
            sens.append(sum(v == c and p == c for v, p in zip(verdad, pred)) / n)
    return float(np.mean(sens)) if sens else float("nan")


@dataclass
class Resultado:
    semilla: int
    arquitectura: str
    clases: list[str]
    mejor_epoca: int
    val_exactitud_balanceada: float
    historial: list[dict] = field(default_factory=list)
    modelo: object = None


def entrenar(ent_recortes: list[np.ndarray], ent_clases: list[str],
             val_recortes: list[np.ndarray], val_clases: list[str],
             semilla: int = 1, arquitectura: str = "pequena", epocas: int = 40,
             lote: int = 64, lr: float = 2e-3, paciencia: int = 10) -> Resultado:
    torch = _torch()
    random.seed(semilla)
    np.random.seed(semilla)
    torch.manual_seed(semilla)
    torch.set_num_threads(max(1, torch.get_num_threads()))
    clases = sorted(set(ent_clases))
    idx = {c: i for i, c in enumerate(clases)}
    X = torch.from_numpy(preparar(ent_recortes, LADO_RED))
    y = torch.tensor([idx[c] for c in ent_clases])
    Xv = torch.from_numpy(preparar(val_recortes, LADO_RED)) if val_recortes else None
    conteo = torch.bincount(y, minlength=len(clases)).float()
    pesos = conteo.sum() / (len(clases) * conteo.clamp(min=1))
    red = construir(arquitectura, len(clases))
    opt = torch.optim.AdamW(red.parameters(), lr=lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epocas)
    perdida_f = torch.nn.CrossEntropyLoss(weight=pesos)
    gen = torch.Generator().manual_seed(semilla)
    mejor, mejor_estado, mejor_epoca, sin_mejora, historial = -1.0, None, 0, 0, []
    for ep in range(1, epocas + 1):
        red.train()
        orden = torch.randperm(len(X), generator=gen)
        total = 0.0
        for i in range(0, len(X), lote):
            b = orden[i:i + lote]
            opt.zero_grad()
            perdida = perdida_f(red(_aumentar(X[b], gen)), y[b])
            perdida.backward()
            opt.step()
            total += perdida.item() * len(b)
        sched.step()
        fila = {"epoca": ep, "perdida": total / len(X)}
        if Xv is not None:
            red.eval()
            with torch.no_grad():
                pred = [clases[i] for i in red(Xv).argmax(1).tolist()]
            fila["val_exactitud_balanceada"] = exactitud_balanceada(val_clases, pred, clases)
            if fila["val_exactitud_balanceada"] > mejor:
                mejor, mejor_epoca, sin_mejora = fila["val_exactitud_balanceada"], ep, 0
                mejor_estado = {k: v.detach().clone() for k, v in red.state_dict().items()}
            else:
                sin_mejora += 1
        historial.append(fila)
        if Xv is not None and sin_mejora >= paciencia:
            break
    if mejor_estado is not None:
        red.load_state_dict(mejor_estado)
    red.eval()
    return Resultado(semilla, arquitectura, clases, mejor_epoca or len(historial), mejor, historial, red)


def exportar(res: Resultado, ruta_onnx: Path, nota: str = "", n_entrenamiento: int = 0) -> Path:
    torch = _torch()
    ruta_onnx = Path(ruta_onnx)
    ruta_onnx.parent.mkdir(parents=True, exist_ok=True)
    ejemplo = torch.zeros(1, 3, LADO_RED, LADO_RED)
    torch.onnx.export(res.modelo, ejemplo, str(ruta_onnx), input_names=["recortes"], output_names=["logits"],
                      dynamic_axes={"recortes": {0: "n"}, "logits": {0: "n"}}, opset_version=17, dynamo=False)
    meta = {
        "tipo": "red_onnx",
        "arquitectura": res.arquitectura,
        "clases": res.clases,
        "lado": LADO_RED,
        "semilla": res.semilla,
        "mejor_epoca": res.mejor_epoca,
        "val_exactitud_balanceada": res.val_exactitud_balanceada,
        "n_entrenamiento": n_entrenamiento,
        "historial": res.historial,
        "creado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "nota": nota,
    }
    ruta_onnx.with_suffix(".json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta_onnx
