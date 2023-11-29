export function stressPercentLabelMap(percent: number) {
  if (percent > 85) return 'Stressful';
  if (percent > 70) return 'Tense';
  if (percent > 25) return 'Neutral';
  return 'Relaxed';
}
