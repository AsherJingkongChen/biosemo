export function percentColorMap_G2R(percent: number): string {
  const MID = 50;
  const p_norm =
    1 - Math.min(1, Math.abs(percent / MID - 1));
  const p_norm_cmpl = 1 - p_norm;
  let r = p_norm * 255,
    g = p_norm * 236,
    b = p_norm * 132;
  if (percent < MID) {
    r += p_norm_cmpl * 99;
    g += p_norm_cmpl * 191;
    b += p_norm_cmpl * 124;
  } else {
    r += p_norm_cmpl * 249;
    g += p_norm_cmpl * 105;
    b += p_norm_cmpl * 108;
  }
  r = Math.floor(r);
  g = Math.floor(g);
  b = Math.floor(b);
  return `rgb(${r}, ${g}, ${b})`;
}
