"""CPU light-transport microscope: spheres, BVH, diffuse paths and explicit MIS.
No GPU ray tracing, neural network or full ReSTIR implementation is claimed.
Images use a finite path-depth cutoff; this omits longer paths and is biased.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
import random
from pathlib import Path
from typing import Sequence

Vec = tuple[float, float, float]
def add(a: Vec, b: Vec) -> Vec: return tuple(x+y for x, y in zip(a, b))
def sub(a: Vec, b: Vec) -> Vec: return tuple(x-y for x, y in zip(a, b))
def mul(a: Vec, s: float) -> Vec: return tuple(x*s for x in a)
def dot(a: Vec, b: Vec) -> float: return sum(x*y for x, y in zip(a, b))
def cross(a: Vec, b: Vec) -> Vec:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def unit(a: Vec) -> Vec:
    length = math.sqrt(dot(a, a))
    if length == 0: raise ValueError("zero direction")
    return mul(a, 1/length)


def balance(p: float, q: float, np: int = 1, nq: int = 1) -> float:
    if min(p, q, np, nq) < 0:
        raise ValueError("negative density/count")
    total = np*p+nq*q
    return np*p/total if total else 0.0


def area_to_solid_angle(pdf_area: float, distance_squared: float, light_cosine: float) -> float:
    if pdf_area < 0 or distance_squared < 0:
        raise ValueError("negative density/distance")
    return pdf_area*distance_squared/abs(light_cosine) if light_cosine else math.inf


def integrate_mis(n: int, seed: int = 7) -> float:
    """Integral x^2 dx over [0,1], uniform and 2x proposals; n samples EACH."""
    if n <= 0: raise ValueError("positive sample count required")
    rng = random.Random(seed)
    total = 0.0
    for _ in range(n):
        x = rng.random()
        total += balance(1.0, 2*x)*x*x/n
        x = math.sqrt(rng.random())
        if x > 0:
            total += balance(2*x, 1.0)*x*x/(n*2*x)
    return total


@dataclass
class Reservoir:
    """Weighted stream selection only. Not a rendering reuse estimator."""
    total: float = 0.0
    count: int = 0
    selected: object = None

    def update(self, item: object, weight: float, rng: random.Random) -> None:
        if weight < 0 or not math.isfinite(weight):
            raise ValueError("nonnegative finite reservoir weight required")
        if not math.isfinite(self.total+weight):
            raise OverflowError("reservoir weight sum overflow")
        self.count += 1
        self.total += weight
        if weight and rng.random() < weight/self.total:
            self.selected = item


def temporal_filter(current: Sequence[float], history: Sequence[float],
                    valid: Sequence[bool], alpha: float = .2) -> list[float]:
    """Validity-gated exponential blend; assumes correspondence was already checked."""
    if len(current) != len(history) or len(current) != len(valid) or not 0 <= alpha <= 1:
        raise ValueError("invalid temporal-filter input")
    return [alpha*c+(1-alpha)*h if ok else c for c, h, ok in zip(current, history, valid)]


def inverse_albedo(cosines: Sequence[float], observations: Sequence[float],
                   irradiance: float = 1.0) -> dict:
    """Bounded least-squares scalar albedo, known lighting, no visibility changes.
    Model observations = albedo * irradiance * max(cosine,0) / pi.
    """
    if len(cosines) != len(observations) or not cosines or irradiance <= 0:
        raise ValueError("invalid observations")
    basis = [irradiance*max(c, 0)/math.pi for c in cosines]
    denom = sum(b*b for b in basis)
    if denom == 0:
        raise ValueError("albedo unidentifiable from all-dark observations")
    raw = sum(b*y for b, y in zip(basis, observations))/denom
    rho = max(0.0, min(1.0, raw))
    loss = .5*sum((rho*b-y)**2 for b, y in zip(basis, observations))
    return dict(albedo=rho, unconstrained=raw, loss=loss, curvature=denom)


@dataclass(frozen=True)
class Sphere:
    center: Vec
    radius: float
    albedo: float = .7
    emission: float = 0.0

    def __post_init__(self):
        if self.radius <= 0 or not 0 <= self.albedo <= 1 or self.emission < 0:
            raise ValueError("invalid sphere/material")

    def intersect(self, origin: Vec, direction: Vec, limit: float = math.inf):
        oc = sub(origin, self.center)
        a, b = dot(direction, direction), dot(oc, direction)
        disc = b*b-a*(dot(oc, oc)-self.radius*self.radius)
        if disc < 0 or a == 0: return None
        root = math.sqrt(disc)
        for t in ((-b-root)/a, (-b+root)/a):
            if 1e-6 < t < limit:
                p = add(origin, mul(direction, t))
                return t, p, unit(sub(p, self.center))
        return None

    def bounds(self):
        return tuple(c-self.radius for c in self.center), tuple(c+self.radius for c in self.center)


@dataclass
class BVH:
    lo: Vec
    hi: Vec
    ids: tuple[int, ...] = ()
    left: 'BVH | None' = None
    right: 'BVH | None' = None

    @classmethod
    def build(cls, spheres: Sequence[Sphere], ids=None):
        ids = list(range(len(spheres))) if ids is None else list(ids)
        if not ids: return None
        bounds = [spheres[i].bounds() for i in ids]
        lo = tuple(min(b[0][j] for b in bounds) for j in range(3))
        hi = tuple(max(b[1][j] for b in bounds) for j in range(3))
        if len(ids) <= 2: return cls(lo, hi, tuple(ids))
        axis = max(range(3), key=lambda j: hi[j]-lo[j])
        ids.sort(key=lambda i: spheres[i].center[axis])
        mid = len(ids)//2
        return cls(lo, hi, (), cls.build(spheres, ids[:mid]), cls.build(spheres, ids[mid:]))

    def refit(self, spheres: Sequence[Sphere]) -> None:
        if self.ids:
            bounds = [spheres[i].bounds() for i in self.ids]
        else:
            self.left.refit(spheres); self.right.refit(spheres)
            bounds = [(self.left.lo, self.left.hi), (self.right.lo, self.right.hi)]
        self.lo = tuple(min(b[0][j] for b in bounds) for j in range(3))
        self.hi = tuple(max(b[1][j] for b in bounds) for j in range(3))

    def box_hit(self, origin: Vec, direction: Vec, limit: float) -> bool:
        t0, t1 = 0.0, limit
        for j in range(3):
            if direction[j] == 0:
                if origin[j] < self.lo[j] or origin[j] > self.hi[j]: return False
            else:
                a, b = (self.lo[j]-origin[j])/direction[j], (self.hi[j]-origin[j])/direction[j]
                t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
                if t1 < t0: return False
        return True

    def hit(self, spheres, origin, direction, limit=math.inf):
        if not self.box_hit(origin, direction, limit): return None
        if self.ids:
            best = None
            for i in self.ids:
                hit = spheres[i].intersect(origin, direction, limit)
                if hit:
                    limit = hit[0]; best = (*hit, i)
            return best
        a = self.left.hit(spheres, origin, direction, limit)
        b = self.right.hit(spheres, origin, direction, a[0] if a else limit)
        return b if b else a


def cosine_sample(normal: Vec, rng: random.Random) -> Vec:
    r = math.sqrt(rng.random()); phi = 2*math.pi*rng.random()
    helper = (0., 1., 0.) if abs(normal[0]) > .9 else (1., 0., 0.)
    tangent = unit(cross(helper, normal)); bitangent = cross(normal, tangent)
    return unit(add(add(mul(tangent, r*math.cos(phi)), mul(bitangent, r*math.sin(phi))),
                    mul(normal, math.sqrt(max(0., 1-r*r)))))


def sample_sphere(sphere: Sphere, rng: random.Random):
    z = 1-2*rng.random(); phi = 2*math.pi*rng.random(); r = math.sqrt(max(0., 1-z*z))
    n = (r*math.cos(phi), z, r*math.sin(phi))
    return add(sphere.center, mul(n, sphere.radius)), n


def path_radiance(scene, tree, origin, direction, rng, *, mode="mis", max_depth=6):
    if mode not in ("bsdf", "nee", "mis") or max_depth < 1:
        raise ValueError("invalid path settings")
    lights = [i for i, s in enumerate(scene) if s.emission > 0]
    beta, radiance, prev_pdf, prev_point = 1.0, 0.0, 0.0, None
    # max_depth counts non-emitting scattering vertices. The final iteration
    # can still hit an emitter, so last-vertex NEE and BSDF sampling have
    # the same truncated path support and their MIS weights remain paired.
    for depth in range(max_depth + 1):
        hit = tree.hit(scene, origin, direction) if tree else None
        if hit is None: break  # Black environment is part of this scene contract.
        _, point, outward, index = hit
        obj = scene[index]
        if obj.emission > 0:
            if dot(outward, mul(direction, -1)) > 0:
                weight = 1.0
                if depth > 0 and mode == "nee": weight = 0.0
                if depth > 0 and mode == "mis":
                    delta = sub(point, prev_point)
                    pl = area_to_solid_angle(1/(len(lights)*4*math.pi*obj.radius**2),
                                              dot(delta, delta), dot(outward, mul(direction, -1)))
                    weight = balance(prev_pdf, pl)
                radiance += beta*obj.emission*weight
            break
        if depth == max_depth:
            break  # No additional scattering beyond the declared path budget.
        normal = outward if dot(outward, direction) < 0 else mul(outward, -1)
        if mode != "bsdf" and lights:
            li = lights[rng.randrange(len(lights))]; light = scene[li]
            target, ln = sample_sphere(light, rng)
            delta = sub(target, point); d2 = dot(delta, delta); wi = unit(delta)
            cos_i, cos_l = max(0., dot(normal, wi)), dot(ln, mul(wi, -1))
            if cos_i > 0 and cos_l > 0:
                pl = area_to_solid_angle(1/(len(lights)*4*math.pi*light.radius**2), d2, cos_l)
                shadow = tree.hit(scene, add(point, mul(normal, 1e-5)), wi)
                visible = shadow and shadow[3] == li and abs(shadow[0]-math.sqrt(d2)) < 1e-3
                if visible:
                    pb = cos_i/math.pi
                    weight = balance(pl, pb) if mode == "mis" else 1.0
                    radiance += beta*light.emission*obj.albedo*pb*weight/pl
        next_dir = cosine_sample(normal, rng)
        prev_pdf = max(0., dot(normal, next_dir))/math.pi
        prev_point = point
        beta *= obj.albedo
        # Roulette compensation preserves expectation for the remaining bounded path.
        if depth >= 2:
            survive = min(.95, max(.05, beta))
            if rng.random() >= survive: break
            beta /= survive
        origin, direction = add(point, mul(normal, 1e-5)), next_dir
    return radiance


def demo_scene():
    return [Sphere((0., -1001., 0.), 1000., .75), Sphere((-.8, 0., 0.), 1., .7),
            Sphere((1.1, -.35, -.7), .65, .35), Sphere((0., 3., -.5), .7, 0., 12.)]


def render(width=32, height=24, spp=8, seed=43, mode="mis") -> dict:
    if min(width, height, spp) < 1 or max(width, height) > 4096:
        raise ValueError("invalid image dimensions/spp")
    scene = demo_scene(); tree = BVH.build(scene); rng = random.Random(seed)
    pixels = []
    for y in range(height):
        for x in range(width):
            value = 0.0
            for _ in range(spp):
                dx = ((x+rng.random())/width-.5)*width/height
                dy = .5-(y+rng.random())/height
                direction = unit((dx, dy-.10, -1.35))
                value += path_radiance(scene, tree, (0., 1., 5.), direction, rng, mode=mode)
            pixels.append(value/spp)
    return dict(width=width, height=height, spp=spp, seed=seed, mode=mode,
                pixels=pixels, max_depth=6, depth_convention="maximum non-emitting scattering vertices",
                evidence="CPU measurement; finite-depth diffuse educational renderer")


def write_ppm(image: dict, path: str | Path) -> None:
    """Display preview only; numerical comparisons must use linear JSON pixels."""
    with open(path, "w", encoding="ascii") as f:
        f.write(f"P3\n{image['width']} {image['height']}\n255\n")
        for v in image['pixels']:
            c = int(255*max(0., min(1., v/(1+v)))**(1/2.2))
            f.write(f"{c} {c} {c}\n")
