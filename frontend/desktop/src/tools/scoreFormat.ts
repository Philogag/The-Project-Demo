export function timeLengthToFloat(minutes?: number, seconds?: number, mSeconds?: number) {
  return (minutes || 0) * 60 + (seconds || 0) + (mSeconds || 0) * 0.01;
}

export function floatToTimeLength(result: number) {
  return {
    minutes: Math.floor(result / 60),
    seconds: Math.floor(result) % 60,
    mSeconds: Math.round((result - Math.floor(result)) * 100),
  };
}

const patterns = [
  /^(\s*\d+\s*)\'(\s*\d+\s*)(?:\'\'(\s*\d+\s*))$/i,
  /^(\s*\d+\s*)分(\s*\d+\s*)秒(\s*\d+\s*)$/i,
  /^(\s*\d+\s*):(\s*\d+\s*).(\s*\d+\s*)$/i,
];

export function scoreFloatFromString(value: string) {
  for (const pattern of patterns) {
    const result = value.match(pattern);
    if (result) {
      return timeLengthToFloat(parseInt(result[1]), parseInt(result[2]), parseInt(result[3]));
    }
  }
  return null;
}

export function scoreFloatToString(value: number, format = '${MM}分 ${SS}秒 ${MS}') {
  const data = floatToTimeLength(value);
  return format
    .replace('${MM}', data.minutes.toString())
    .replace('${SS}', data.seconds.toString().padStart(2, '0'))
    .replace('${MS}', data.mSeconds.toString().padStart(2, '0'));
}
