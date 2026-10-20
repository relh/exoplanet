"""Conditional PRF fits with a planar background; not host probabilities."""
import numpy as np
from scipy.optimize import least_squares, lsq_linear


def fit_templates(image, error, templates, nonnegative=False):
    image, error = np.asarray(image), np.asarray(error)
    yy, xx = np.indices(image.shape, dtype=float)
    columns = [np.asarray(t) for t in templates] + [np.ones_like(xx), xx-xx.mean(), yy-yy.mean()]
    valid = np.isfinite(image) & np.isfinite(error) & (error > 0)
    valid &= np.all(np.isfinite(columns), axis=0)
    design = np.stack([c[valid] / error[valid] for c in columns], axis=1)
    data = image[valid] / error[valid]
    if len(data) <= len(columns):
        raise ValueError('Insufficient valid pixels')
    if np.linalg.matrix_rank(design) < len(columns):
        raise ValueError('Rank deficient PRF design')
    if nonnegative:
        fit = lsq_linear(design, data, bounds=(np.r_[np.zeros(len(templates)), [-np.inf]*3], np.inf), tol=1e-10, method="bvls", max_iter=1000)
        if not fit.success:
            raise ValueError(fit.message)
        coefficients = fit.x
    else:
        coefficients = np.linalg.lstsq(design, data, rcond=None)[0]
    model = np.einsum('i,ijk->jk', coefficients, np.asarray(columns))
    residual = (image[valid] - model[valid]) / error[valid]
    return dict(coefficients=coefficients, model=model, residual=residual,
                chi2=float(residual @ residual), dof=len(data)-len(columns))


def fit_shift(image, error, positions, locate, bound=.6, nonnegative=True):
    """Common scene displacement, with per-source fluxes profiled out.

    Alignment uses only the provided image. Its uncertainty/model mismatch is
    not propagated into subsequent fixed-position fits.
    """
    positions = np.asarray(positions, dtype=float)
    def evaluate(shift):
        templates = [locate(*(p+shift), image.shape) for p in positions]
        return fit_templates(image, error, templates, nonnegative)
    fits = [least_squares(lambda shift: evaluate(shift)['residual'], start,
                          bounds=(-bound, bound), diff_step=1e-4, max_nfev=100)
            for start in ([0., 0.], [.2, -.2], [-.2, .2])]
    best = min(fits, key=lambda fit: np.sum(fit.fun**2))
    if not best.success:
        raise ValueError(best.message)
    result = evaluate(best.x)
    result.update(shift=best.x, boundary=bool(np.any(abs(best.x) > .99*bound)))
    return result
