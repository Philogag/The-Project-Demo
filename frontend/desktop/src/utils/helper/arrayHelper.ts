

export function sum(arr: Array<number>) {
  return arr.reduce((total, current) => total + current, 0);
}


export function mean(arr: Array<number>) {
  return arr.length > 0 ? sum(arr) / arr.length : 0;
}