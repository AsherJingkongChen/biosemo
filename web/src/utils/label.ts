export function percentLabelMap(percent: number) {
  if (percent > 75) {
    return 'Stressful';
  } else if (percent > 25) {
    return 'Neutral';
  } else {
    return 'Relaxed';
  }
}
