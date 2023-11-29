export function stressPercentColorMap(
  percent: number,
  alpha?: number | string,
): string {
  const MID = 50;
  const p_norm =
    1 - Math.min(1, Math.abs(percent / MID - 1));
  const p_norm_cmpl = 1 - p_norm;
  // yellow
  let r = p_norm * 250,
    g = p_norm * 200,
    b = p_norm * 70;
  if (percent < MID) {
    // green
    r += p_norm_cmpl * 70;
    g += p_norm_cmpl * 200;
    b += p_norm_cmpl * 90;
  } else {
    // red
    r += p_norm_cmpl * 250;
    g += p_norm_cmpl * 70;
    b += p_norm_cmpl * 70;
  }
  r = Math.floor(r);
  g = Math.floor(g);
  b = Math.floor(b);
  if (alpha !== undefined) {
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  } else {
    return `rgb(${r}, ${g}, ${b})`;
  }
}
