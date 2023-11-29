export function stressPercentLabelMap(percent: number) {
  if (percent > 75) return 'Stressful';
  if (percent > 50) return 'Tense';
  if (percent > 25) return 'Neutral';
  return 'Relaxed';
}
