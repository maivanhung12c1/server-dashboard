export function truncate(str: string, max = 60): string {
  return str.length <= max ? str : str.slice(0, max - 3) + "...";
}

export function formatNumber(n: number): string {
  return n.toLocaleString();
}
